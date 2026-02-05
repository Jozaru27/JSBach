#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Modificar VLAN</title>"
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

input[type=text] {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    margin: 4px 0;
    width: 95%;
}
input[type=text]:focus {
    outline: none;
    border-color: #3b82f6;
    background: rgba(0, 0, 0, 0.3);
}
input.ip { width: 250px; }
</style>"
echo "</head><body>"
echo "<div style='max-width: 1200px; margin: 0 auto;'>"

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$vid" == "$VID" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap VLAN amb VID = $VID</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "<h2>Modificar VLAN</h2>"
echo "<form action='/cgi-bin/bridge-guardar.cgi' method='get'>"
echo "<input type='hidden' name='accio' value='modificar'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample

if [ "$vid" -lt "3" ]; then
     	echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;' readonly></td>"   
else
	echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;'></td>"
fi


# VID només lectura
echo "<td><input type='text' name='vid' value='$vid' readonly></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value='$subnet' required pattern='^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/([0-9]|[12][0-9]|3[0-2])$' title='Format de subxarxa no vàlid (Ex: 192.168.1.0/24)'></td>"
echo "<td><input type='text' class='ip' name='ippe' value='$gw' required pattern='^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$' title='Format de porta d\u0027enlla\u00e7 no vàlid'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Desar</button>"
echo "</form>"

echo "</body></html>"
