#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VLANs</title>"
echo "<meta charset='utf-8'>"
echo "<style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

h2 {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px 20px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-top: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  letter-spacing: 0.5px;
}

h3 {
  color: #94a3b8;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 8px;
  margin-top: 25px;
  font-size: 1.2rem;
}

table {
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 25px;
  width: 100%;
  background: rgba(30, 41, 59, 0.7);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

td, th {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

th {
  background: rgba(59, 130, 246, 0.15);
  color: #fff;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

button, input[type=submit], .btn {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(to right, #2563eb, #3b82f6);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
  text-decoration: none;
  display: inline-block;
  font-size: 0.9rem;
}

button:hover, input[type=submit]:hover, .btn:hover {
  background: linear-gradient(to right, #1d4ed8, #2563eb);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
}

a {
  color: #60a5fa;
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: #93c5fd;
  text-decoration: underline;
}
</style>"
echo "</head><body>"
echo "<div style='max-width: 1200px; margin: 0 auto;'>"

# -------------------------------------------------------------------
# Aquí posem la comanda o fitxer que genera les VLANs
# -------------------------------------------------------------------
VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"


# Llegim totes les línies en un array
mapfile -t VLANS <<< "$VLAN_DATA"

# Comprovem que tinguem almenys dues línies
if [ "${#VLANS[@]}" -lt 2 ]; then
    echo "<p><b>Error:</b> no hi ha prou VLANs definides.</p>"
    echo "</body></html>"
    exit 0
fi

# -------------------------------------------------------------------
# VLAN ADMINISTRACIÓ (primera línia)
# -------------------------------------------------------------------
echo "<h2>VLAN ADMINISTRACIÓ</h2>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[0]}"
echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid'\">Modificar</button></td></tr>"
echo "</table>"

# -------------------------------------------------------------------
# VLAN DMZ (segona línia)
# -------------------------------------------------------------------
echo "<h2>VLAN DMZ</h2>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[1]}"
echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid'\">Modificar</button></td></tr>"
echo "</table>"

# -------------------------------------------------------------------
# Altres VLANS (de la tercera en avant)
# -------------------------------------------------------------------
echo "<h2>VLANS</h2>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"

for ((i=2; i<${#VLANS[@]}; i++)); do
    line="${VLANS[$i]}"
    [ -z "$line" ] && continue
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
    echo "<td>"
    echo "<button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid'\">Modificar</button>"
    echo "<button onclick=\"location.href='/cgi-bin/bridge-esborrar.cgi?vid=$vid'\">Esborrar</button>"
    echo "</td></tr>"
done

echo "</table>"

# -------------------------------------------------------------------
# Botó final
# -------------------------------------------------------------------
echo "<button onclick=\"location.href='/cgi-bin/bridge-nova-vlan.cgi'\">Crear nova VLAN</button>"

echo "</body></html>"
