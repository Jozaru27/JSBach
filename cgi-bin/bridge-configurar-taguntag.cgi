#!/bin/bash

# JSBach Router Administration - Bridge Tag/Untag Configuration List
source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]] && [[ "$iface" != "$IFW_IFWAN" ]] && [[ $iface != br0* ]]; then
            if ! iw dev 2>/dev/null | grep -qw "$iface"; then
                echo "$iface"
            fi
        fi
    done
}

echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Configuració Tag-Untag - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-top: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.icon { font-size: 1.5em; }

table {
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  background: rgba(30, 41, 59, 0.7);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

th, td { padding: 16px 20px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
th { background: rgba(59, 130, 246, 0.15); color: #fff; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.05em; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.03); }

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: rgba(59, 130, 246, 0.15);
  color: #93c5fd;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
  border: 1px solid rgba(59,130,246,0.3);
}

.btn:hover {
  background: rgba(59, 130, 246, 0.3);
  color: #fff;
  transform: translateY(-1px);
}

.badge-vlan {
  background: rgba(15, 23, 42, 0.5);
  padding: 4px 10px;
  border-radius: 6px;
  font-family: monospace;
  color: #60a5fa;
  border: 1px solid rgba(255,255,255,0.05);
}

.iface-name { font-weight: 700; color: #fff; }
  </style>
</head>
<body>
  <div class="container">
    <h1><span class="icon">🌉</span> Configuració de VLANs Tag-Untag</h1>

    <table>
      <thead>
        <tr>
          <th>Interfície</th>
          <th>Untagged (PVID)</th>
          <th>Tagged (Extra)</th>
          <th>Accions</th>
        </tr>
      </thead>
      <tbody>
EOF

for iface in $(Interfaces_Ethernet); do
    linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
    VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
    [ -z "$VLAN_UNTAG" ] && VLAN_UNTAG="0"
    
    VLAN_TAG=$(echo "$linia_int" | cut -d';' -f3)
    [ -z "$VLAN_TAG" ] && VLAN_TAG="0"
    
    cat << EOF
        <tr>
          <td><span class="iface-name">$iface</span></td>
          <td><span class="badge-vlan">$VLAN_UNTAG</span></td>
          <td><span class="badge-vlan">$VLAN_TAG</span></td>
          <td>
            <a href="/cgi-bin/bridge-modificar-taguntag.cgi?int=$iface" class="btn">✏️ Modificar</a>
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
