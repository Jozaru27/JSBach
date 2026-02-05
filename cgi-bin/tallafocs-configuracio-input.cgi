#!/bin/bash

# JSBach Router Administration - Firewall Input Configuration (Catalan Premium)
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Configuració Input - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { max-width: 1000px; margin: 0 auto; }

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 15px;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  margin-bottom: 35px;
  animation: fadeIn 0.4s ease-out;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #60a5fa;
  margin: 0;
}

.vlan-box {
  background: rgba(15, 23, 42, 0.3);
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s;
}

.vlan-box:hover { background: rgba(255, 255, 255, 0.02); }

.vlan-info { display: flex; flex-direction: column; gap: 4px; }
.vlan-name { font-weight: 700; color: #fff; }
.vlan-details { font-family: monospace; font-size: 0.85rem; color: #94a3b8; }

.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
  margin-right: 15px;
}

.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); }

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.btn-connect { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.btn-connect:hover { background: rgba(34, 197, 94, 0.3); transform: translateY(-1px); }

.btn-disconnect { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.btn-disconnect:hover { background: rgba(239, 68, 68, 0.3); transform: translateY(-1px); }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>
  <div class="container">
    <h1>📥 Configuració Input (Router)</h1>

    <!-- SECCIÓ WAN -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Internet Input (WAN)</h3>
      </div>
EOF

# Get WAN status using absolute path and quoting
ESTAT_WAN=$("/usr/local/JSBach/scripts/client_srv_cli" tallafocs estat_wan 0 | head -n1)

cat << EOF
      <div class="vlan-box">
        <div class="vlan-info">
          <span class="vlan-name">Canal d'Internet</span>
          <span class="vlan-details">Interfície externa (enp6s0)</span>
        </div>
        <div>
EOF

if [ "$ESTAT_WAN" == "BLOCKED" ]; then
    echo "<span class='badge badge-red'>ACCÉS BLOQUEJAT</span>"
    echo "<a href='/cgi-bin/tallafocs-input-action.cgi?accio=desbloquejar_internet&vid=0' class='btn btn-connect'>🔓 Desbloquejar</a>"
else
    echo "<span class='badge badge-green'>ACCÉS OBERT</span>"
    echo "<a href='/cgi-bin/tallafocs-input-action.cgi?accio=bloquejar_internet&vid=0' class='btn btn-disconnect'>🔒 Bloquejar + No Ping</a>"
fi

cat << EOF
        </div>
      </div>
    </div>

    <!-- SECCIÓ VLANS -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Accés Local al Router (VLANs)</h3>
      </div>
EOF

# Loop through VLANs - using absolute path for bridge.conf
grep -v '^#' "/usr/local/JSBach/conf/bridge.conf" | while IFS=';' read -r NOM VID IP GW RESTO; do
    if [ ! -z "$VID" ]; then
        ESTAT_INPUT=$("/usr/local/JSBach/scripts/client_srv_cli" tallafocs estat_input "$VID" | head -n1)
        
        cat << EOF
      <div class="vlan-box">
        <div class="vlan-info">
          <span class="vlan-name">$NOM</span>
          <span class="vlan-details">VLAN $VID • $IP</span>
        </div>
        <div>
EOF

        if [ "$ESTAT_INPUT" == "CONNECTADA" ]; then
            echo "<span class='badge badge-green'>ESCOLTANT</span>"
            echo "<a href='/cgi-bin/tallafocs-input-action.cgi?vid=$VID&accio=input_desconnectar' class='btn btn-disconnect'>🔌 Tallar Accés</a>"
        else
            echo "<span class='badge badge-red'>IGNORANT</span>"
            echo "<a href='/cgi-bin/tallafocs-input-action.cgi?vid=$VID&accio=input_connectar' class='btn btn-connect'>🔗 Obrir Accés</a>"
        fi

cat << EOF
        </div>
      </div>
EOF
    fi
done

cat << EOF
    </div>
  </div>
</body>
</html>
EOF
