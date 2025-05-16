// Simple front-end control UI interacting with GitHub repo config via GitHub API
// NOTE: For demo purposes, it uses localStorage for config because GitHub API calls require OAuth tokens not included here.
// You will need to implement GitHub API calls with authentication for real repo config management.

const configKey = "weather_alert_config";

function loadConfig() {
  let config = localStorage.getItem(configKey);
  if (!config) {
    config = JSON.stringify({
      system_on: true,
      locations: [
        {name: "Houston", zone_code: "TXZ213"},
        {name: "New Braunfels", zone_code: "TXZ234"}
      ],
      sent_alerts: []
    });
    localStorage.setItem(configKey, config);
  }
  return JSON.parse(config);
}

function saveConfig(config) {
  localStorage.setItem(configKey, JSON.stringify(config));
}

function render() {
  const config = loadConfig();
  document.getElementById("status").innerText = "System is " + (config.system_on ? "ON" : "OFF");
  const list = document.getElementById("location-list");
  list.innerHTML = "";
  config.locations.forEach((loc, i) => {
    const li = document.createElement("li");
    li.innerText = loc.name + " (" + loc.zone_code + ") ";
    const delBtn = document.createElement("button");
    delBtn.textContent = "Remove";
    delBtn.onclick = () => {
      config.locations.splice(i, 1);
      saveConfig(config);
      render();
    };
    li.appendChild(delBtn);
    list.appendChild(li);
  });
}

document.getElementById("toggle-btn").onclick = () => {
  const config = loadConfig();
  config.system_on = !config.system_on;
  saveConfig(config);
  render();
};

document.getElementById("add-loc-btn").onclick = () => {
  const name = document.getElementById("loc-name").value.trim();
  const zone = document.getElementById("loc-zone").value.trim();
  if (!name || !zone) {
    alert("Please enter both location name and zone code.");
    return;
  }
  const config = loadConfig();
  config.locations.push({name, zone_code: zone});
  saveConfig(config);
  document.getElementById("loc-name").value = "";
  document.getElementById("loc-zone").value = "";
  render();
};

document.getElementById("send-manual-btn").onclick = () => {
  const msg = document.getElementById("manual-msg").value.trim();
  if (!msg) {
    alert("Please enter a message.");
    return;
  }
  alert("Manual alert sending is not implemented in this demo.
Implement GitHub API backend to trigger manual emails.");
  document.getElementById("manual-msg").value = "";
};

render();