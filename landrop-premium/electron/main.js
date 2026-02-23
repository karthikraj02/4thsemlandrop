const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");

function createWindow() {

  const win = new BrowserWindow({
    width: 1100,
    height: 750,

    webPreferences: {
      nodeIntegration: true,      // ⭐ REQUIRED
      contextIsolation: false     // ⭐ REQUIRED
    }
  });

  win.loadFile("ui/index.html");

  // Start Python services
  spawn("python", ["engine/receiver.py"]);
  spawn("python", ["engine/discovery_server.py"]);
}

app.whenReady().then(createWindow);