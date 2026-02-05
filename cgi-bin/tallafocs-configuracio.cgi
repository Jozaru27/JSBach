#!/bin/bash

# JSBach Router Administration - Firewall Configuration (Catalan Premium Expanded + Logic)
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Tallafocs - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { max-width: 1200px; margin: 0 auto; }

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

table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

th, td { padding: 14px 20px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
th { background: rgba(59, 130, 246, 0.1); color: #fff; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.1em; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

.actions-cell {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: white;
}

.btn-primary { background: linear-gradient(135deg, #2563eb, #3b82f6); box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3); }

.btn-danger { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.btn-danger:hover { background: rgba(239, 68, 68, 0.25); border-color: #ef4444; }

.btn-connect { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.btn-connect:hover { background: rgba(34, 197, 94, 0.3); transform: translateY(-1px); }

.btn-disconnect { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.btn-disconnect:hover { background: rgba(239, 68, 68, 0.3); transform: translateY(-1px); }

.btn-wls { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.btn-wls:hover { background: rgba(59, 130, 246, 0.3); transform: translateY(-1px); }

.btn-isolate { background: rgba(96, 165, 250, 0.15); color: #93c5fd; border: 1px solid rgba(96,165,250,0.3); }
.btn-isolate:hover { background: rgba(96, 165, 250, 0.3); transform: translateY(-1px); }

.btn-restore { background: rgba(251, 146, 60, 0.15); color: #fdba74; border: 1px solid rgba(251,146,60,0.3); }
.btn-restore:hover { background: rgba(251, 146, 60, 0.3); transform: translateY(-1px); }

.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); }
.badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
.badge-orange { background: rgba(251, 146, 60, 0.2); color: #fdba74; border: 1px solid rgba(251,146,60,0.4); }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>
  <div class="container">
    <h1>🛡️ Gestió del Tallafocs</h1>
    
    <!-- SECCIÓ 1: ESTAT DE LES VLANS -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Monitoratge de VLANs</h3>
      </div>
      <table>
        <thead>
          <tr>
            <th>Interfície</th>
            <th>VLAN</th>
            <th>Estat</th>
            <th>Accions de Xarxa</th>
            <th>Estat DMZ</th>
          </tr>
        </thead>
        <tbody>
EOF

# Llegir configuració i mostrar estat
grep -v '^#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" | while IFS=';' read -r NOM VID IP GW RESTO; do
    ESTAT=$("$DIR/$PROJECTE/$DIR_SCRIPTS"/client_srv_cli tallafocs estat "$VID" | head -n1)
    
    BADGE_CLASS="badge-red"
    if [[ "$ESTAT" == "CONNECTADA" ]]; then
        BADGE_CLASS="badge-green"
    elif [[ "$ESTAT" == "CONNECTADA PORT WLS" ]]; then
        BADGE_CLASS="badge-blue"
    elif [[ "$ESTAT" == "AÏLLADA" ]]; then
        BADGE_CLASS="badge-orange"
    fi

    echo "<tr>"
    echo "<td><span style='font-weight:600;'>$NOM</span></td>"
    echo "<td><span style='font-family:monospace;'>$VID</span></td>"
    echo "<td><span class='badge $BADGE_CLASS'>$ESTAT</span></td>"
    
    # Columna 1: Connexió/Desconnexió
    echo "<td><div class='actions-cell'>"
    if [[ "$ESTAT" == "DESCONNECTADA" ]]; then
        echo "<a href='/cgi-bin/tallafocs-conndeconn.cgi?vid=$VID&accio=connectar' class='btn btn-connect'>🔗 Connectar</a>"
        echo "<a href='/cgi-bin/tallafocs-conndeconn.cgi?vid=$VID&accio=connectar_port_wls' class='btn btn-wls'>📶 WLS</a>"
    else
        echo "<a href='/cgi-bin/tallafocs-conndeconn.cgi?vid=$VID&accio=desconnectar' class='btn btn-disconnect'>🔌 Desconnectar</a>"
    fi
    echo "</div></td>"

    # Columna 2: Gestió DMZ (Aïllament)
    echo "<td><div class='actions-cell'>"
    if [[ "$ESTAT" == "AÏLLADA" ]]; then
        echo "<a href='/cgi-bin/tallafocs-conndeconn.cgi?vid=$VID&accio=desaillar_dmz' class='btn btn-restore'>🔥 Desaïllar</a>"
    else
        # Només permetem aïllar si no està desconnectada (opcional, però té més sentit)
        if [[ "$ESTAT" != "DESCONNECTADA" ]]; then
            echo "<a href='/cgi-bin/tallafocs-conndeconn.cgi?vid=$VID&accio=aillar_dmz' class='btn btn-isolate'>🧊 Aïllar</a>"
        else
            echo "<span style='color:#64748b; font-size:0.7rem; font-style:italic;'>Requereix connexió</span>"
        fi
    fi
    echo "</div></td>"

    echo "</tr>"
done

cat << EOF
        </tbody>
      </table>
    </div>

    <!-- SECCIÓ 2: PORTS EN LLISTA BLANCA -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Ports en Llista Blanca (WLS)</h3>
        <a href="/cgi-bin/tallafocs-nou-port-wls.cgi" class="btn btn-primary">➕ Afegir Port</a>
      </div>
      <table>
        <thead>
          <tr>
            <th>Protocol</th>
            <th>Número de Port</th>
            <th style="width:120px;">Acció</th>
          </tr>
        </thead>
        <tbody>
EOF

# Llegir ports WLS
grep -v '^#' "/usr/local/JSBach/conf/ports_wls.conf" | while IFS=';' read -r PROTO PORT RESTO; do
    if [ ! -z "$PROTO" ] && [ ! -z "$PORT" ]; then
        cat << EOF
        <tr>
          <td><span class="badge badge-blue">$PROTO</span></td>
          <td><span style="font-family:monospace; font-weight:700;">$PORT</span></td>
          <td>
            <a href="/cgi-bin/tallafocs-ports-wls.cgi?accio=eliminar_port_wls&protocol=$PROTO&port=$PORT" class="btn btn-danger">🗑️ Eliminar</a>
          </td>
        </tr>
EOF
    fi
done

cat << EOF
        </tbody>
      </table>
    </div>

    <!-- SECCIÓ 3: IPS AMB ACCÉS NO RESTRINGIT -->
    <div class="card">
      <div class="card-header">
        <h3 class="card-title">IPs amb Accés no Restringit</h3>
        <a href="/cgi-bin/tallafocs-nova-ip-wls.cgi" class="btn btn-primary">➕ Afegir IP</a>
      </div>
      <table>
        <thead>
          <tr>
            <th>VLAN</th>
            <th>Adreça IP</th>
            <th>Adreça MAC</th>
            <th style="width:120px;">Acció</th>
          </tr>
        </thead>
        <tbody>
EOF

# Llegir IPs WLS
grep -v '^#' "/usr/local/JSBach/conf/ip_wls.conf" | while IFS=';' read -r VID IP MAC RESTO; do
    if [ ! -z "$VID" ] && [ ! -z "$IP" ]; then
        cat << EOF
        <tr>
          <td><span style="font-weight:600;">VLAN $VID</span></td>
          <td><span style="font-family:monospace; color:#60a5fa;">$IP</span></td>
          <td><span style="font-family:monospace; font-size:0.85rem; opacity:0.8;">$MAC</span></td>
          <td>
            <a href="/cgi-bin/tallafocs-ips-wls.cgi?accio=eliminar_ip_wls&vid=$VID&ip=$IP&mac=$MAC" class="btn btn-danger">🗑️ Eliminar</a>
          </td>
        </tr>
EOF
    fi
done

cat << EOF
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
EOF
