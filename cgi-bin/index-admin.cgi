#!/bin/bash

# JSBach Router Administration - Header (Catalan Premium)
source /usr/local/JSBach/conf/variables.conf
HOSTNAME=$(hostname)

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      padding: 0;
      background: linear-gradient(to bottom, #1e293b, #0f172a);
      color: #e2e8f0;
      font-family: 'Segoe UI', system-ui, sans-serif;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border-bottom: 2px solid #3b82f6;
      box-sizing: border-box;
      overflow: hidden;
    }

    .header-container {
      width: 100%;
      max-width: 1300px;
      padding: 0 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo-container {
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .logo-icon {
      font-size: 2.8rem;
      filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.4));
    }

    .logo-text h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: 2px;
      color: #fff;
      text-transform: uppercase;
    }

    .nav-buttons {
      display: flex;
      gap: 10px;
    }

    .nav-btn {
      padding: 10px 18px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      color: #94a3b8;
      text-decoration: none;
      font-weight: 700;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }

    .nav-btn:hover {
      background: rgba(59, 130, 246, 0.15);
      color: #fff;
      border-color: #3b82f6;
      transform: translateY(-2px);
    }

    .nav-btn.active {
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      color: #fff;
      border: none;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    .nav-btn-home {
      border-color: rgba(34, 197, 94, 0.3);
      color: #4ade80;
    }
    
    .nav-btn-home:hover {
      background: rgba(34, 197, 94, 0.1);
      border-color: rgba(34, 197, 94, 0.5);
      color: #86efac;
    }

    .system-label {
        font-size: 0.7rem;
        color: #475569;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 5px;
        text-align: right;
    }
  </style>
  <script>
    function loadModule(menuCgi, bodyCgi, targetId) {
      if(menuCgi) parent.frames['menu'].location.href = menuCgi;
      if(bodyCgi) parent.frames['body'].location.href = bodyCgi;
      
      const buttons = document.querySelectorAll('.nav-btn');
      buttons.forEach(b => b.classList.remove('active'));
      
      if(targetId) {
          const btn = document.getElementById(targetId);
          if(btn) btn.classList.add('active');
      }
    }
  </script>
</head>
<body>
  <div class="header-container">
    <div class="logo-container">
      <span class="logo-icon">🎹</span>
      <div class="logo-text">
        <h1>JSBACH Admin</h1>
      </div>
    </div>

    <div>
      <div class="system-label">Host: $HOSTNAME</div>
      <div class="nav-buttons">
        <div id="btn-home" onclick="loadModule('/cgi-bin/cos-admin.cgi', '/cgi-bin/info.cgi', 'btn-home')" class="nav-btn nav-btn-home active">🏠 Inici</div>
        <div id="btn-wan" onclick="loadModule('/cgi-bin/ifwan-menu.cgi', '/cgi-bin/ifwan.cgi?comand=estat', 'btn-wan')" class="nav-btn">🌐 Wan</div>
        <div id="btn-enrutar" onclick="loadModule('/cgi-bin/enrutar-menu.cgi', '/cgi-bin/enrutar.cgi?comand=estat', 'btn-enrutar')" class="nav-btn">🔀 Enrutar</div>
        <div id="btn-bridge" onclick="loadModule('/cgi-bin/bridge-menu.cgi', '/cgi-bin/bridge.cgi?comand=estat', 'btn-bridge')" class="nav-btn">🌉 Bridge</div>
        <div id="btn-tallafocs" onclick="loadModule('/cgi-bin/tallafocs-menu.cgi', '/cgi-bin/tallafocs-configuracio.cgi', 'btn-tallafocs')" class="nav-btn">🛡️ Tallafocs</div>
        <div id="btn-dmz" onclick="loadModule('/cgi-bin/dmz-menu.cgi', '/cgi-bin/dmz-configurar.cgi', 'btn-dmz')" class="nav-btn">🔓 DMZ</div>
      </div>
    </div>
  </div>
</body>
</html>
EOF
