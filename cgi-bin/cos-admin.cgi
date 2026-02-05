#!/bin/bash

# JSBach Router Administration - Sidebar Stats (Catalan Premium)
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Obtenir informació del sistema
HOSTNAME=$(hostname)
UPTIME=$(uptime -p | sed 's/up //')
KERNEL=$(uname -r)
DATA=$(date "+%d/%m/%Y %H:%M")

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 1.5rem;
  background: #0f172a;
  color: #e2e8f0;
  min-height: 100vh;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.logo-section {
  text-align: center;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  margin-bottom: 0.5rem;
}

.logo-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  display: block;
}

.logo-text {
  font-size: 1.1rem;
  font-weight: 800;
  letter-spacing: 2px;
  color: #60a5fa;
  text-transform: uppercase;
}

.panel-title {
    font-size: 0.7rem;
    font-weight: 800;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
    padding-left: 5px;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  background: rgba(255, 255, 255, 0.03);
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.info-label {
  display: block;
  font-size: 0.65rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.info-value {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #cbd5e1;
  word-break: break-all;
}

.hint-box {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(59, 130, 246, 0.05);
  border: 1px dashed rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  font-size: 0.8rem;
  color: #93c5fd;
  line-height: 1.4;
}

.footer {
  margin-top: auto;
  padding-top: 2rem;
  text-align: center;
  font-size: 0.65rem;
  color: #475569;
}
</style>
</head>
<body>

<div class="sidebar-content">
  <div class="logo-section">
    <span class="logo-icon">🎹</span>
    <span class="logo-text">JSBACH</span>
    <div style="font-size: 0.6rem; color: #475569; margin-top: 4px;">ROUTER OS</div>
  </div>

  <div class="panel-title">Estat del Sistema</div>

  <div class="info-group">
    <div class="info-item">
      <span class="info-label">SISTEMA</span>
      <span class="info-value">$HOSTNAME</span>
    </div>

    <div class="info-item">
      <span class="info-label">TEMPS EN LÍNIA</span>
      <span class="info-value">$UPTIME</span>
    </div>

    <div class="info-item">
      <span class="info-label">KERNEL</span>
      <span class="info-value">$KERNEL</span>
    </div>

    <div class="info-item">
      <span class="info-label">DATA I HORA</span>
      <span class="info-value">$DATA</span>
    </div>
  </div>

  <div class="hint-box">
    Seleccioneu un mòdul al menú superior per a gestionar les opcions de xarxa.
  </div>

  <div class="footer">
    v2.1.0-stable<br>
    © 2026 Jozaru
  </div>
</div>

</body>
</html>
EOF
