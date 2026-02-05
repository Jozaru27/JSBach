#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background: #0f172a;
  color: #e2e8f0;
  min-height: 100vh;
}

h2 {
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #475569;
  margin-bottom: 20px;
  padding-left: 10px;
}

a {
  display: block;
  text-decoration: none;
  padding: 12px 16px;
  margin-bottom: 8px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  color: #94a3b8;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

a:hover {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
  transform: translateX(4px);
  color: #60a5fa;
}

.icon { margin-right: 10px; }
</style>
</head>
<body>
  <h2>Mòdul WAN</h2>
  <a href="/cgi-bin/ifwan.cgi?comand=iniciar" target="body"><span class="icon">🚀</span> Iniciar WAN</a>
  <a href="/cgi-bin/ifwan.cgi?comand=aturar" target="body"><span class="icon">🛑</span> Aturar WAN</a>
  <a href="/cgi-bin/ifwan.cgi?comand=estat" target="body"><span class="icon">📊</span> Estat WAN</a>
  <a href="/cgi-bin/ifwan-configurar.cgi" target="body"><span class="icon">⚙️</span> Configuració</a>
  
  <div style="margin-top: 30px; padding: 10px; border-top: 1px solid rgba(255,255,255,0.05);">
    <a href="/cgi-bin/cos-admin.cgi" style="font-size: 0.8rem; opacity: 0.7;">⬅️ Tornar</a>
  </div>
</body>
</html>
EOF
