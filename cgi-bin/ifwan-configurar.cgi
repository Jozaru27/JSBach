#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

#Vull una pagina cgi amb bash per apache2 per linux que... primera seccio dos radius option, la #primera opcio "dhcp" i la segona "manual" cas de polsar algun dels dos, que per metode get es pase #mode=[dhcp o manual] Segona secció "Interfaç" Amb la funció: Interfaces_Ethernet() { for iface in #$(ip -o link show | awk -F': ' '{print $2}'); do if [[ "$iface" != "lo" ]]; then if ! iw dev 2>/#dev/null | grep -q "$iface"; then echo "$iface" fi fi done } amb la llista que me torne, crea una #llista de radius option i la que siga seleccionada torne per GET int="el nome de la targeta" I #tercera seccio: Estarà oculta i cas de seleccionar mode manual en la primera seccio, mostrar #quatre inptus de text, el primer de no ip i torna per metode get ip="la ip introduida", el segon #de nom mascara tornarà per get masc="la mascara introduida", el tercer de nom porta d'enllaç i #torna per GET pe="la ip introduida" i el darrer de nom dns i torna per get dns=" la ip introduida" #Acabarem amb un boto guardar que al polsar enllace amb la paguina guardar-ifwan.cgi

echo "Content-type: text/html"
echo ""

# --- Funció per obtenir interfícies Ethernet (sense lo ni wifi ni bridge) ---
Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        # Filtrar: no loopback, no wifi, no bridge (br0*)
        if [[ "$iface" != "lo" ]] && [[ "$iface" != br0* ]]; then
            if ! iw dev 2>/dev/null | grep -qw "$iface"; then
                echo "$iface"
            fi
        fi
    done
}

CONFIGURACIO=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan configurar mostrar)
conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f1 )
conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f2 )
if [[ "$conf_mode" == "manual" ]] then
	conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f3 )
	conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f4 )
	conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f5 )
	conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6 )
fi

# --- Inici HTML ---
cat <<'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Configuració de la WAN</title>

<style>
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

button, input[type=submit], input[type=text], select {
  padding: 10px 15px;
  margin: 5px;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
}

input[type=text] {
  background: rgba(0,0,0,0.2);
  color: white;
}
input[type=text]:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(0,0,0,0.3);
}

button, input[type=submit] {
  background: linear-gradient(to right, #2563eb, #3b82f6);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
  border: none;
}

button:hover, input[type=submit]:hover {
  background: linear-gradient(to right, #1d4ed8, #2563eb);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
}

fieldset {
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.1);
  padding: 20px;
  margin-bottom: 25px;
  background: rgba(30, 41, 59, 0.5);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

legend {
  font-weight: bold;
  font-size: 1.1em;
  padding: 0 10px;
  color: #60a5fa;
}

label {
  margin-left: 5px;
  color: #cbd5e1;
}

.hidden {
  display: none;
}

</style>
<script>
function toggleManual() {
  const modeManual = document.getElementById("manual").checked;
  const manualSection = document.getElementById("manual-section");
  manualSection.style.display = modeManual ? "block" : "none";
}

  // Quan la pàgina es carrega, comprova l'estat i actualitza la visibilitat
  window.addEventListener("DOMContentLoaded", toggleManual);
  
</script>
</head>
<body>
<h2>Configuració de la interfície WAN</h2>

<form action="/cgi-bin/ifwan-guardar.cgi" method="get">
EOF

# --- SECCIÓ 1: MODE (DHCP o MANUAL) ---
cat <<'EOF'
<fieldset>
  <legend>Mode de configuració</legend>
EOF
	dhcp_check=""
	manual_check=""
	if [[ "$conf_mode" == "dhcp" ]] then
  		dhcp_check="checked"
	else
		manual_check="checked"
	fi
	
  echo '<input type="radio" id="dhcp" name="mode" value="dhcp" onclick="toggleManual()" '$dhcp_check'>'
cat <<'EOF' 
  <label for="dhcp">DHCP</label><br>
EOF
   echo '<input type="radio" id="manual" name="mode" value="manual" onclick="toggleManual()" '$manual_check'>'
cat <<'EOF'

  <label for="manual">Manual</label>
</fieldset>
EOF

# --- SECCIÓ 2: INTERFÍCIES ---
echo '<fieldset>'
echo '  <legend>Interfície</legend>'

for iface in $(Interfaces_Ethernet); do
    if [[ "$iface" == "$conf_int" ]] then 
    	echo "  <input type='radio' name='int' id='$iface' value='$iface' checked>"
    else
    	echo "  <input type='radio' name='int' id='$iface' value='$iface' >"
    fi
    echo "  <label for='$iface'>$iface</label><br>"
done


echo '</fieldset>'

# --- SECCIÓ 3: CONFIGURACIÓ MANUAL (OCULTA PER DEFECTE) ---
cat <<'EOF'
<fieldset id="manual-section" class="hidden">
  <legend>Configuració manual</legend>
  <label>IP:</label><br>
EOF
  echo "<input type=\"text\" name=\"ip\" value=\"$conf_ip\" placeholder=\"Ex: 192.168.1.10\" required pattern=\"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$\" title=\"Format d'IP no vàlid (0-255 en cada octet)\"><br><br>"
cat <<'EOF'

  <label>Màscara:</label><br>
EOF
  echo " <input type=\"text\" name=\"masc\" value=\"$conf_masc\" placeholder=\"Ex: 255.255.255.0\" required pattern=\"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$\" title=\"Format de màscara no vàlid (0-255 en cada octet)\"><br><br>"
cat <<'EOF'

  <label>Porta d'enllaç:</label><br>
EOF
  echo " <input type=\"text\" name=\"pe\" value=\"$conf_pe\" placeholder=\"Ex: 192.168.1.1\" required pattern=\"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$\" title=\"Format de porta d'enllaç no vàlid (0-255 en cada octet)\"><br><br>"
cat <<'EOF'

  <label>DNS:</label><br>
EOF
  echo " <input type=\"text\" name=\"dns\" value=\"$conf_dns\" placeholder=\"Ex: 8.8.8.8\" required pattern=\"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$\" title=\"Format de DNS no vàlid (0-255 en cada octet)\"><br><br>"
cat <<'EOF'

</fieldset>

<br><br>
<input type="submit" value="Desar">
</form>
</body>
</html>
EOF

