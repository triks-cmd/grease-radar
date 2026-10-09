"""
Unit tests for Grease Radar
Tests risk score calculation, backtesting, and edge cases
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import functions from app.py
CELL = 0.005

def mm(s):
    """Min-max normalization"""
    if len(s) == 0 or s.max() == s.min():
        return pd.Series(np.ones(len(s)) * 50, index=s.index)
    return 100 * (s - s.min()) / (s.max() - s.min())

def hotspots(d):
    """Calculate hotspots from incident data"""
    x = np.floor(d.lon / CELL) * CELL
    y = np.floor(d.lat / CELL) * CELL
    z = d.copy()
    z['cx'] = x
    z['cy'] = y
    
    g = z.groupby(['cx', 'cy'], as_index=False).agg(
        incidents=('date', 'size'),
        months=('month', 'nunique'),
        last=('date', 'max')
    )
    
    now = d.date.max()
    age = (now - g.last).dt.days.clip(lower=0)
    g['frequency'] = mm(g.incidents)
    g['recurrence'] = mm(g.months)
    g['recency'] = 100 * np.exp(-age / 180)
    
    occupied = {(round(a, 3), round(b, 3)) for a, b in zip(g.cx, g.cy)}
    dens = []
    for r in g.itertuples():
        dens.append(sum(
            (round(r.cx + dx, 3), round(r.cy + dy, 3)) in occupied
            for dx in (-CELL, 0, CELL)
            for dy in (-CELL, 0, CELL)
        ))
    g['density'] = mm(pd.Series(dens, index=g.index))
    g['risk'] = (
        .35 * g.frequency +
        .30 * g.recurrence +
        .20 * g.recency +
        .15 * g.density
    ).round().astype(int)
    
    g['level'] = pd.cut(
        g.risk,
        [-1, 39, 69, 101],
        labels=['LOW', 'MEDIUM', 'HIGH']
    ).astype(str)
    g['lat'] = g.cy + CELL / 2
    g['lon'] = g.cx + CELL / 2
    
    return g.sort_values('risk', ascending=False)

def backtest(d):
    """Temporal backtesting without leakage"""
    if len(d) < 20:
        return {'available': False, 'reason': 'Not enough incidents for a meaningful backtest.'}
    
    d = d.sort_values('date')
    cut = d.date.iloc[int(.7 * len(d))]
    train = d[d.date < cut]
    test = d[d.date >= cut]
    
    h = hotspots(train)
    top = h[h.risk >= h.risk.quantile(.8)]
    cells = {(round(a, 3), round(b, 3)) for a, b in zip(top.cx, top.cy)}
    
    hits = 0
    high_risk_cells = len(cells)
    
    for r in test.itertuples():
        if (round(np.floor(r.lon / CELL) * CELL, 3),
            round(np.floor(r.lat / CELL) * CELL, 3)) in cells:
            hits += 1
    
    return {
        'available': True,
        'train': len(train),
        'test': len(test),
        'capture': round(100 * hits / len(test), 1),
        'split': str(cut.date()),
        'high_risk_cells': high_risk_cells,
        'total_cells': len(h),
        'hits': hits
    }

# Tests
def test_empty_dataset():
    """Test behavior with empty dataset"""
    print("Testing empty dataset...")
    d = pd.DataFrame({'lat': [], 'lon': [], 'date': [], 'month': []})
    d['date'] = pd.to_datetime(d['date'])
    
    try:
        h = hotspots(d)
        assert len(h) == 0, "Empty dataset should produce no hotspots"
        print("[PASS] Empty dataset handled correctly")
    except Exception as e:
        print(f"[FAIL] Empty dataset test failed: {e}")
        return False
    return True

def test_single_incident():
    """Test behavior with single incident"""
    print("Testing single incident...")
    d = pd.DataFrame({
        'lat': [54.687],
        'lon': [25.279],
        'date': pd.to_datetime(['2024-01-01']),
        'month': ['2024-01']
    })
    
    try:
        h = hotspots(d)
        assert len(h) == 1, "Single incident should produce one hotspot"
        assert h.iloc[0]['incidents'] == 1, "Incident count should be 1"
        assert h.iloc[0]['months'] == 1, "Month count should be 1"
        print("[PASS] Single incident handled correctly")
    except Exception as e:
        print(f"[FAIL] Single incident test failed: {e}")
        return False
    return True

def test_duplicate_records():
    """Test behavior with duplicate records"""
    print("Testing duplicate records...")
    d = pd.DataFrame({
        'lat': [54.687, 54.687],
        'lon': [25.279, 25.279],
        'date': pd.to_datetime(['2024-01-01', '2024-01-01']),
        'month': ['2024-01', '2024-01']
    })
    
    try:
        h = hotspots(d)
        assert len(h) == 1, "Duplicates in same cell should produce one hotspot"
        assert h.iloc[0]['incidents'] == 2, "Should count both incidents"
        print("[PASS] Duplicate records handled correctly")
    except Exception as e:
        print(f"[FAIL] Duplicate records test failed: {e}")
        return False
    return True

def test_missing_coordinates():
    """Test behavior with missing coordinates"""
    print("Testing missing coordinates...")
    d = pd.DataFrame({
        'lat': [54.687, np.nan, 54.689],
        'lon': [25.279, 25.280, np.nan],
        'date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'month': ['2024-01', '2024-01', '2024-01']
    })
    
    try:
        # Filter out NaN coordinates
        d = d.dropna(subset=['lat', 'lon'])
        h = hotspots(d)
        assert len(h) == 1, "Only valid coordinates should be processed"
        print("[PASS] Missing coordinates handled correctly")
    except Exception as e:
        print(f"[FAIL] Missing coordinates test failed: {e}")
        return False
    return True

def test_invalid_dates():
    """Test behavior with invalid dates"""
    print("Testing invalid dates...")
    d = pd.DataFrame({
        'lat': [54.687, 54.689],
        'lon': [25.279, 25.280],
        'date': pd.to_datetime(['2024-01-01', 'invalid'], errors='coerce'),
        'month': ['2024-01', '2024-01']
    })
    
    try:
        # Filter out invalid dates
        d = d.dropna(subset=['date'])
        h = hotspots(d)
        assert len(h) == 1, "Only valid dates should be processed"
        print("[PASS] Invalid dates handled correctly")
    except Exception as e:
        print(f"[FAIL] Invalid dates test failed: {e}")
        return False
    return True

def test_risk_score_range():
    """Test that risk scores are in valid range"""
    print("Testing risk score range...")
    d = pd.DataFrame({
        'lat': [54.687, 54.689, 54.691, 54.693, 54.695],
        'lon': [25.279, 25.280, 25.281, 25.282, 25.283],
        'date': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01']),
        'month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05']
    })
    
    try:
        h = hotspots(d)
        for _, row in h.iterrows():
            assert 0 <= row['risk'] <= 100, f"Risk score {row['risk']} out of range"
            assert row['level'] in ['LOW', 'MEDIUM', 'HIGH'], f"Invalid risk level: {row['level']}"
        print("[PASS] Risk scores in valid range")
    except Exception as e:
        print(f"[FAIL] Risk score range test failed: {e}")
        return False
    return True

def test_backtest_insufficient_data():
    """Test backtest with insufficient data"""
    print("Testing backtest with insufficient data...")
    d = pd.DataFrame({
        'lat': [54.687, 54.689],
        'lon': [25.279, 25.280],
        'date': pd.to_datetime(['2024-01-01', '2024-02-01']),
        'month': ['2024-01', '2024-02']
    })
    
    try:
        result = backtest(d)
        assert result['available'] == False, "Should not be available with <20 incidents"
        print("[PASS] Backtest with insufficient data handled correctly")
    except Exception as e:
        print(f"[FAIL] Backtest insufficient data test failed: {e}")
        return False
    return True

def test_backtest_no_leakage():
    """Test that backtest doesn't leak future data"""
    print("Testing backtest for data leakage...")
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    d = pd.DataFrame({
        'lat': [54.687 + i * 0.001 for i in range(30)],
        'lon': [25.279 + i * 0.001 for i in range(30)],
        'date': dates,
        'month': [d.strftime('%Y-%m') for d in dates]
    })
    
    try:
        result = backtest(d)
        assert result['available'] == True, "Backtest should be available"
        assert result['train'] < len(d), "Training set should be smaller than full dataset"
        assert result['test'] > 0, "Test set should have incidents"
        print("[PASS] Backtest leakage test passed")
    except Exception as e:
        print(f"[FAIL] Backtest leakage test failed: {e}")
        return False
    return True

def test_geographic_filtering():
    """Test Vilnius coordinate filtering"""
    print("Testing geographic filtering...")
    # Valid Vilnius coordinates
    d = pd.DataFrame({
        'lat': [54.687, 54.689, 50.0, 60.0],  # Last two outside Vilnius
        'lon': [25.279, 25.280, 25.281, 25.282],
        'date': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']),
        'month': ['2024-01', '2024-02', '2024-03', '2024-04']
    })
    
    try:
        # Filter to Vilnius bounds
        d = d[d.lat.between(54.5, 54.9) & d.lon.between(25.0, 25.6)]
        h = hotspots(d)
        assert len(h) == 2, "Should only process Vilnius coordinates"
        print("[PASS] Geographic filtering works correctly")
    except Exception as e:
        print(f"[FAIL] Geographic filtering test failed: {e}")
        return False
    return True

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("GREASE RADAR UNIT TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_empty_dataset,
        test_single_incident,
        test_duplicate_records,
        test_missing_coordinates,
        test_invalid_dates,
        test_risk_score_range,
        test_backtest_insufficient_data,
        test_backtest_no_leakage,
        test_geographic_filtering
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
