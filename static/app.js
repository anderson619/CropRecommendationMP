/**
 * Crop Recommendation – Frontend Logic
 */

// ── Crop → Emoji map ──────────────────────────────────────────────
const cropEmojis = {
  rice: '🌾', wheat: '🌾', maize: '🌽', corn: '🌽',
  chickpea: '🫘', kidneybeans: '🫘', pigeonpeas: '🫘',
  mothbeans: '🫘', mungbean: '🫘', blackgram: '🫘', lentil: '🫘',
  pomegranate: '🍎', banana: '🍌', mango: '🥭', grapes: '🍇',
  watermelon: '🍉', muskmelon: '🍈', apple: '🍎', orange: '🍊',
  papaya: '🥭', coconut: '🥥', cotton: '🧶', jute: '🧵',
  coffee: '☕',
};

// ── DOM References ────────────────────────────────────────────────
const form = document.getElementById('cropForm');
const btn = document.getElementById('btnPredict');
const resultBox = document.getElementById('resultBox');

// ── Submit handler ────────────────────────────────────────────────
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Collect input values
  const payload = {
    N: parseInt(document.getElementById('inputN').value, 10),
    P: parseInt(document.getElementById('inputP').value, 10),
    K: parseInt(document.getElementById('inputK').value, 10),
    temperature: parseFloat(document.getElementById('inputTemp').value),
    humidity: parseFloat(document.getElementById('inputHum').value),
    ph: parseFloat(document.getElementById('inputPh').value),
    rainfall: parseFloat(document.getElementById('inputRain').value),
  };

  const model = document.getElementById('modelSelect').value;
  const endpoint = `/predict/${model}`;

  // UI – loading state
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Prediciendo…';
  resultBox.classList.remove('show', 'success', 'error');

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || 'Error desconocido');

    // ── Success ───────────────────────────────────────────────────
    const crop = data.prediction.toLowerCase();
    document.getElementById('resultIcon').textContent = cropEmojis[crop] || '🌿';
    document.getElementById('resultCrop').textContent = data.prediction;
    document.getElementById('resultModel').textContent = `Modelo: ${data.model_used}`;
    document.getElementById('resultError').textContent = '';
    resultBox.classList.add('show', 'success');

  } catch (err) {
    // ── Error ─────────────────────────────────────────────────────
    document.getElementById('resultIcon').textContent = '⚠️';
    document.getElementById('resultCrop').textContent = '';
    document.getElementById('resultModel').textContent = '';
    document.getElementById('resultError').textContent = err.message;
    resultBox.classList.add('show', 'error');

  } finally {
    btn.disabled = false;
    btn.innerHTML = '🔍  Predecir Cultivo';
  }
});
