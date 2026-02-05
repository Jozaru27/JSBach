#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Configuració DMZ - JSBach</title>
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

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 35px;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0;
}

.btn-add {
  background: linear-gradient(135deg, #34d399, #10b981);
  color: white;
  padding: 14px 24px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 700;
  box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
  transition: all 0.25s;
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.4);
}

table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  background: rgba(30, 41, 59, 0.7);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

th, td { padding: 18px 25px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
th { background: rgba(59, 130, 246, 0.1); color: #fff; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.1em; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

.port-badge {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  padding: 4px 12px;
  border-radius: 8px;
  font-family: inherit;
  font-weight: 700;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.ip-text { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #fff; }

.btn-delete {
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s;
  border: 1px solid rgba(239, 68, 68, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-delete:hover {
  background: rgba(239, 68, 68, 0.3);
  color: #fff;
  border-color: #ef4444;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.container { animation: fadeIn 0.4s ease-out; }

</style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🔐 Configuració DMZ</h1>
      <a href="/cgi-bin/dmz-nou-servei.cgi" class="btn-add">➕ Obrir Nou Servei</a>
    </header>

    <table>
      <thead>
        <tr>
          <th>Port</th>
          <th>Protocol</th>
          <th>IP Servidor Intern</th>
          <th>Accions</th>
        </tr>
      </thead>
      <tbody>
EOF

for iface in $("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar mostrar); do
	PORT=$(echo "$iface"|cut -d';' -f1)
	PROTO=$(echo "$iface"|cut -d';' -f2)
	IP_DMZ=$(echo "$iface"|cut -d';' -f3)
	
	cat << EOF
        <tr>
          <td><span class="port-badge">$PORT</span></td>
          <td><span style="font-weight:600; text-transform:uppercase;">$PROTO</span></td>
          <td><span class="ip-text">$IP_DMZ</span></td>
          <td>
            <a href="/cgi-bin/dmz-eliminar.cgi?port=$PORT&proto=$PROTO&ipdmz=$IP_DMZ" class="btn-delete">🗑️ Eliminar</a>
          </td>
        </tr>
EOF
done

cat << EOF
      </tbody>
    </table>
  </div>
</body>
</html>
EOF
