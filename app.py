from flask import Flask, render_template, request, jsonify
import pandas as pd, numpy as np
from pathlib import Path
from datetime import datetime

app=Flask(__name__)
DATA=Path('data'); DATA.mkdir(exist_ok=True)
OFFICIAL=DATA/'incidents.csv'
DEMO=DATA/'demo_incidents.csv'
COLLECTION=DATA/'collection_points.csv'
CELL=.005

def load_df():
    p=OFFICIAL if OFFICIAL.exists() else DEMO
    raw=pd.read_csv(p)
    m={c.lower().strip():c for c in raw.columns}
    def pick(names):
        for n in names:
            if n in m:return m[n]
    lat,lon,date=pick(['lat','latitude','y']),pick(['lon','lng','longitude','x']),pick(['date','datetime','incident_date','data'])
    if not all([lat,lon,date]): raise ValueError('CSV needs latitude, longitude and date columns.')
    d=pd.DataFrame({'lat':pd.to_numeric(raw[lat],errors='coerce'),'lon':pd.to_numeric(raw[lon],errors='coerce'),'date':pd.to_datetime(raw[date],errors='coerce')}).dropna()
    d=d[d.lat.between(54.5,54.9)&d.lon.between(25.0,25.6)].copy(); d['month']=d.date.dt.to_period('M').astype(str)
    return d

def mm(s):
    if len(s)==0 or s.max()==s.min(): return pd.Series(np.ones(len(s))*50,index=s.index)
    return 100*(s-s.min())/(s.max()-s.min())

def hotspots(d):
    x=np.floor(d.lon/CELL)*CELL; y=np.floor(d.lat/CELL)*CELL; z=d.copy(); z['cx']=x;z['cy']=y
    g=z.groupby(['cx','cy'],as_index=False).agg(incidents=('date','size'),months=('month','nunique'),last=('date','max'))
    now=d.date.max(); age=(now-g.last).dt.days.clip(lower=0); g['frequency']=mm(g.incidents);g['recurrence']=mm(g.months);g['recency']=100*np.exp(-age/180)
    occupied={(round(a,3),round(b,3)) for a,b in zip(g.cx,g.cy)}; dens=[]
    for r in g.itertuples():
        dens.append(sum((round(r.cx+dx,3),round(r.cy+dy,3)) in occupied for dx in (-CELL,0,CELL) for dy in (-CELL,0,CELL)))
    g['density']=mm(pd.Series(dens,index=g.index));g['risk']=(.35*g.frequency+.30*g.recurrence+.20*g.recency+.15*g.density).round().astype(int)
    g['level']=pd.cut(g.risk,[-1,39,69,101],labels=['LOW','MEDIUM','HIGH']).astype(str);g['lat']=g.cy+CELL/2;g['lon']=g.cx+CELL/2
    return g.sort_values('risk',ascending=False)

def backtest(d):
    if len(d)<20:return {'available':False,'reason':'Not enough incidents for a meaningful backtest.'}
    d=d.sort_values('date');cut=d.date.iloc[int(.7*len(d))];train=d[d.date<cut];test=d[d.date>=cut]
    h=hotspots(train); top=h[h.risk>=h.risk.quantile(.8)]; cells={(round(a,3),round(b,3)) for a,b in zip(top.cx,top.cy)}
    hits=0; high_risk_cells=len(cells)
    for r in test.itertuples():
        if (round(np.floor(r.lon/CELL)*CELL,3),round(np.floor(r.lat/CELL)*CELL,3)) in cells:hits+=1
    return {
        'available':True,
        'train':len(train),
        'test':len(test),
        'capture':round(100*hits/len(test),1),
        'split':str(cut.date()),
        'high_risk_cells':high_risk_cells,
        'total_cells':len(h),
        'hits':hits
    }

@app.route('/')
def home():return render_template('index.html')
@app.route('/api/data')
def api():
    d=load_df();h=hotspots(d)
    return jsonify({
        'demo':not OFFICIAL.exists(),
        'total':len(d),
        'start':str(d.date.min().date()),
        'end':str(d.date.max().date()),
        'high':int((h.level=='HIGH').sum()),
        'recurring':int((h.months>=2).sum()),
        'points':[{'lat':float(r.lat),'lon':float(r.lon),'date':r.date.strftime('%Y-%m-%d')} for r in d.itertuples()],
        'hotspots':[{
            'lat':float(r.lat),
            'lon':float(r.lon),
            'incidents':int(r.incidents),
            'months':int(r.months),
            'last':r.last.strftime('%Y-%m-%d'),
            'risk':int(r.risk),
            'level':r.level,
            'frequency':int(r.frequency),
            'recurrence':int(r.recurrence),
            'recency':int(r.recency),
            'density':int(r.density)
        } for r in h.itertuples()],
        'backtest':backtest(d)
    })
@app.route('/api/import',methods=['POST'])
def imp():
    f=request.files.get('file')
    if not f:return jsonify(error='Choose a CSV file.'),400
    OFFICIAL.write_bytes(f.read())
    try:n=len(load_df());return jsonify(ok=True,rows=n)
    except Exception as e:OFFICIAL.unlink(missing_ok=True);return jsonify(ok=False,error=str(e)),400

@app.route('/api/hotspot/<int:index>')
def hotspot_detail(index):
    d=load_df();h=hotspots(d)
    if index < 0 or index >= len(h):return jsonify(error='Hotspot not found'),404
    row=h.iloc[index]
    return jsonify({
        'index':index,
        'lat':float(row.lat),
        'lon':float(row.lon),
        'incidents':int(row.incidents),
        'months':int(row.months),
        'last':row.last.strftime('%Y-%m-%d'),
        'risk':int(row.risk),
        'level':row.level,
        'frequency':int(row.frequency),
        'recurrence':int(row.recurrence),
        'recency':int(row.recency),
        'density':int(row.density)
    })

@app.route('/api/collection', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        if not COLLECTION.exists():
            return jsonify({'points': [], 'total': 0})
        try:
            df = pd.read_csv(COLLECTION)
            points = []
            for _, row in df.iterrows():
                points.append({
                    'id': row.get('id', ''),
                    'name': row.get('name', ''),
                    'lat': float(row.get('lat', 0)),
                    'lon': float(row.get('lon', 0)),
                    'type': row.get('type', 'unknown'),
                    'volume': row.get('volume', 0),
                    'date': row.get('date', '')
                })
            return jsonify({'points': points, 'total': len(points)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    if request.method == 'POST':
        data = request.json
        if not COLLECTION.exists():
            df = pd.DataFrame(columns=['id', 'name', 'lat', 'lon', 'type', 'volume', 'date'])
        else:
            df = pd.read_csv(COLLECTION)
        
        new_point = pd.DataFrame([{
            'id': data.get('id', f'CP-{len(df)+1}'),
            'name': data.get('name', ''),
            'lat': data.get('lat', 0),
            'lon': data.get('lon', 0),
            'type': data.get('type', 'restaurant'),
            'volume': data.get('volume', 0),
            'date': datetime.now().strftime('%Y-%m-%d')
        }])
        
        df = pd.concat([df, new_point], ignore_index=True)
        df.to_csv(COLLECTION, index=False)
        return jsonify({'ok': True, 'id': new_point.iloc[0]['id']})

@app.route('/api/fuel-calculate', methods=['POST'])
def fuel_calculate():
    data = request.json
    volume = float(data.get('volume', 0))
    recoverable = float(data.get('recoverable', 85)) / 100
    yield_factor = float(data.get('yield', 0.9))
    
    feedstock = volume * recoverable
    fuel_output = feedstock * yield_factor
    
    return jsonify({
        'feedstock': round(feedstock, 2),
        'fuel_output': round(fuel_output, 2),
        'assumptions': {
            'volume': volume,
            'recoverable_percent': recoverable * 100,
            'yield_factor': yield_factor
        }
    })

if __name__=='__main__':app.run(host='0.0.0.0',port=5000)
