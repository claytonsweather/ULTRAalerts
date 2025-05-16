const CONFIG_URL = 'https://gist.githubusercontent.com/claytonsweather/cc77ca8c82ed2627b2ea5d57e4743efa/raw/config.json';
const ALERTS_URL = 'https://gist.githubusercontent.com/claytonsweather/cc77ca8c82ed2627b2ea5d57e4743efa/raw/sent_alerts.json';

async function fetchConfig() {
  const res = await fetch(CONFIG_URL);
  return res.json();
}

async function fetchAlerts() {
  const res = await fetch(ALERTS_URL);
  return res.json();
}

function updateUI(config, alerts) {
  document.getElementById('status').innerText = config.system_on ? 'ON' : 'OFF';
  document.getElementById('zones').value = config.zones.join('\n');
  document.getElementById('recent-alerts').innerText = alerts.join('\n');
}

async function load() {
  try {
    const config = await fetchConfig();
    const alerts = await fetchAlerts();
    updateUI(config, alerts);
  } catch (e) {
    document.getElementById('recent-alerts').innerText = 'Error loading alert log.';
  }
}

document.getElementById('toggle').addEventListener('click', async () => {
  const config = await fetchConfig();
  config.system_on = !config.system_on;
  await saveConfig(config);
  load();
});

document.getElementById('save-zones').addEventListener('click', async () => {
  const zones = document.getElementById('zones').value.split('\n').map(z => z.trim()).filter(z => z);
  const config = await fetchConfig();
  config.zones = zones;
  await saveConfig(config);
  load();
});

document.getElementById('send-alert').addEventListener('click', () => {
  fetch('https://maker.ifttt.com/trigger/send_alert/with/key/YOUR_IFTTT_KEY'); // or GitHub Action webhook if custom
});

document.getElementById('send-test').addEventListener('click', () => {
  fetch('https://maker.ifttt.com/trigger/send_test/with/key/YOUR_IFTTT_KEY');
});

load();
