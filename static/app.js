let map, mapFull, layer, data;

const color = level => {
  switch(level) {
    case 'HIGH': return '#dc2626';
    case 'MEDIUM': return '#f59e0b';
    case 'LOW': return '#16a34a';
    default: return '#6b7280';
  }
};

const getLevelClass = level => {
  switch(level) {
    case 'HIGH': return 'high';
    case 'MEDIUM': return 'medium';
    case 'LOW': return 'low';
    default: return '';
  }
};

// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const page = link.dataset.page;
    
    // Update active link
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    
    // Show page
    document.querySelectorAll('.page').forEach(p => {
      p.classList.remove('active');
      p.classList.add('hidden');
    });
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
      targetPage.classList.remove('hidden');
      targetPage.classList.add('active');
    }
    
    // Initialize map if switching to risk-map page
    if (page === 'risk-map' && data) {
      setTimeout(() => initFullMap(), 100);
    }
    
    // Initialize operations page if switching to operations
    if (page === 'operations') {
      setTimeout(() => initOperationsPage(), 100);
    }
  });
});

async function load() {
  try {
    data = await (await fetch('/api/data')).json();

    // Update stats
    document.querySelector('#total').textContent = data.total.toLocaleString();
    document.querySelector('#high').textContent = data.high;
    document.querySelector('#recurring').textContent = data.recurring;
    document.querySelector('#period').textContent = data.start + ' → ' + data.end;

    // Initialize overview map
    initOverviewMap();

    // Build priority list
    buildPriorityList();

    // Update backtest
    updateBacktest();

  } catch (error) {
    console.error('Error loading data:', error);
  }
}

function initOverviewMap() {
  if (!map) {
    map = L.map('map').setView([54.687, 25.28], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);
  }

  // Clear existing layer
  if (layer) {
    layer.clearLayers();
  } else {
    layer = L.layerGroup().addTo(map);
  }

  // Add hotspots to map
  data.hotspots.forEach((h, i) => {
    const radius = Math.max(8, Math.min(20, 8 + h.risk / 10));
    const marker = L.circleMarker([h.lat, h.lon], {
      radius: radius,
      color: color(h.level),
      fillColor: color(h.level),
      fillOpacity: 0.5,
      weight: 2
    }).addTo(layer);

    marker.bindPopup(`
      <div style="font-family: system-ui; min-width: 200px;">
        <b style="font-size: 14px;">Hotspot #${String(i + 1).padStart(2, '0')}</b><br>
        <div style="margin: 8px 0;">
          <span style="font-size: 24px; font-weight: 700; color: ${color(h.level)};">${h.risk}</span>
          <span style="color: #6b7280;">/100</span>
        </div>
        <div style="font-size: 12px; color: #4b5563; line-height: 1.6;">
          <strong>${h.incidents}</strong> incidents<br>
          <strong>${h.months}</strong> recurring months<br>
          Last: ${h.last}
        </div>
      </div>
    `);

    marker.on('click', () => why(h, i));
  });
}

function initFullMap() {
  if (!mapFull) {
    mapFull = L.map('map-full').setView([54.687, 25.28], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(mapFull);
  }

  const layerFull = L.layerGroup().addTo(mapFull);
  
  data.hotspots.forEach((h, i) => {
    const radius = Math.max(8, Math.min(20, 8 + h.risk / 10));
    L.circleMarker([h.lat, h.lon], {
      radius: radius,
      color: color(h.level),
      fillColor: color(h.level),
      fillOpacity: 0.5,
      weight: 2
    }).addTo(layerFull).bindPopup(`Hotspot #${i + 1} - Risk: ${h.risk}/100`);
  });
}

function buildPriorityList() {
  const list = document.querySelector('#list');
  list.innerHTML = '';

  data.hotspots.slice(0, 30).forEach((h, i) => {
    const el = document.createElement('div');
    el.className = 'hot';
    el.innerHTML = `
      <div class="row">
        <span>Hotspot #${String(i + 1).padStart(2, '0')}</span>
        <span class="risk ${getLevelClass(h.level)}">${h.risk}</span>
      </div>
      <div class="meta">${h.incidents} incidents · ${h.months} recurring months · ${h.level}</div>
    `;
    el.onclick = () => {
      map.setView([h.lat, h.lon], 14);
      why(h, i);
    };
    list.appendChild(el);
  });
}

function updateBacktest() {
  const b = data.backtest;
  const backtestEl = document.querySelector('#backtest');

  if (b.available) {
    const scoreClass = b.capture >= 70 ? 'high' : b.capture >= 50 ? 'medium' : 'low';
    backtestEl.innerHTML = `
      <div class="backtest-score ${scoreClass}">${b.capture}%</div>
      <div class="backtest-details">of future incidents fell inside the model's top-risk cells.</div>
      <div class="backtest-meta">
        Training: ${b.train} incidents · Future: ${b.test} incidents · Split: ${b.split}<br>
        Top-risk cells: ${b.high_risk_cells} of ${b.total_cells} total cells · Captured: ${b.hits} incidents
      </div>
    `;
  } else {
    backtestEl.innerHTML = `<p style="color: #6b7280;">${b.reason}</p>`;
  }
}

function why(h, index) {
  const frequency = Math.min(100, h.incidents * 12);
  const recurrence = Math.min(100, h.months * 20);
  const daysSince = (new Date(data.end) - new Date(h.last)) / 86400000;
  const recency = Math.max(0, Math.round(100 * Math.exp(-daysSince / 180)));

  const freqContribution = Math.round(frequency * 0.35);
  const recContribution = Math.round(recurrence * 0.30);
  const recencyContribution = Math.round(recency * 0.20);
  const densityContribution = Math.round(h.density * 0.15);

  const whyEl = document.querySelector('#why');
  whyEl.innerHTML = `
    <div class="whygrid">
      <div>
        <b>${frequency}</b>
        <span>Frequency</span>
        <small>${h.incidents} incidents</small>
      </div>
      <div>
        <b>${recurrence}</b>
        <span>Recurrence</span>
        <small>${h.months} months</small>
      </div>
      <div>
        <b>${recency}</b>
        <span>Recency</span>
        <small>${Math.round(daysSince)} days ago</small>
      </div>
      <div>
        <b>${h.risk}</b>
        <span>Overall Risk</span>
        <small>/100</small>
      </div>
    </div>
    <div style="margin-top: 20px;">
      <div style="font-size: 12px; font-weight: 600; color: #6b7280; margin-bottom: 8px;">RISK BREAKDOWN</div>
      <div class="risk-bar">
        <div class="risk-bar-segment" style="width: 35%; background: #3b82f6;" title="Frequency: 35%">
          <span>Freq</span>
        </div>
        <div class="risk-bar-segment" style="width: 30%; background: #8b5cf6;" title="Recurrence: 30%">
          <span>Rec</span>
        </div>
        <div class="risk-bar-segment" style="width: 20%; background: #f59e0b;" title="Recency: 20%">
          <span>Recency</span>
        </div>
        <div class="risk-bar-segment" style="width: 15%; background: #10b981;" title="Density: 15%">
          <span>Dens</span>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 12px; font-size: 11px; color: #6b7280;">
        <div style="text-align: center;">
          <span style="color: #3b82f6; font-weight: 600;">+${freqContribution}</span><br>
          from frequency
        </div>
        <div style="text-align: center;">
          <span style="color: #8b5cf6; font-weight: 600;">+${recContribution}</span><br>
          from recurrence
        </div>
        <div style="text-align: center;">
          <span style="color: #f59e0b; font-weight: 600;">+${recencyContribution}</span><br>
          from recency
        </div>
        <div style="text-align: center;">
          <span style="color: #10b981; font-weight: 600;">+${densityContribution}</span><br>
          from density
        </div>
      </div>
    </div>
    <div class="action-box">
      <b>Recommended action:</b>
      <p>Prioritize preventive inspection and operational review. The system does not identify an individual responsible party.</p>
    </div>
  `;
}

// Collection Planner functions
function addCollectionPoint() {
  alert('Collection point management - this would open a form to add a new collection point location. For demo purposes, this feature shows the UI flow.');
}

// Waste-to-Fuel Calculator
function calculateFuel() {
  const volume = parseFloat(document.getElementById('calc-volume').value) || 0;
  const recoverable = parseFloat(document.getElementById('calc-recoverable').value) || 0;
  const yieldFactor = parseFloat(document.getElementById('calc-yield').value) || 0;

  const feedstock = volume * (recoverable / 100);
  const fuel = feedstock * yieldFactor;

  document.getElementById('result-feedstock').textContent = feedstock.toFixed(2) + ' liters';
  document.getElementById('result-fuel').textContent = fuel.toFixed(2) + ' liters';
  document.getElementById('result-assumptions').textContent = 
    `Volume: ${volume}L × Recoverable: ${recoverable}% × Yield: ${yieldFactor} L/L`;
}

// Operations Dashboard
function initOperationsPage() {
  // Update operations metrics with demo data
  const opsData = {
    totalPoints: 12,
    activeRoutes: 5,
    collectedToday: 850,
    efficiency: 92
  };
  
  document.getElementById('ops-total-points').textContent = opsData.totalPoints;
  document.getElementById('ops-active-routes').textContent = opsData.activeRoutes;
  document.getElementById('ops-collected-today').textContent = opsData.collectedToday + ' L';
  document.getElementById('ops-efficiency').textContent = opsData.efficiency + '%';
}

function applyRecommendation() {
  alert('Recommendation applied: Vehicle VH-104 reassigned to Route E. Fleet optimization updated.');
}

// File upload handler
document.querySelector('#file').onchange = async e => {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/import', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();

    if (!result.ok) {
      alert('Import failed: ' + result.error);
      return;
    }

    alert('Successfully imported ' + result.rows + ' valid rows.');
    load();
  } catch (error) {
    alert('Import failed: ' + error.message);
  }
};

// Initial load
load();
