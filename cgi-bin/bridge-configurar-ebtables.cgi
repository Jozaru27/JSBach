#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

# -------------------------------------------------------------------
# Processar accions (GET/POST)
# -------------------------------------------------------------------
if [ "$RM" = "POST" ]; then
    read -r QUERY_STRING_POST
    # Parsejar POST si cal
fi

QUERY_STRING="$QUERY_STRING"

# Funció per parsejar query string
saveIFS=$IFS
IFS='&'
for KEY_VAL in $QUERY_STRING; do
    KEY=$(echo $KEY_VAL | cut -d '=' -f 1)
    VAL=$(echo $KEY_VAL | cut -d '=' -f 2)
    export "$KEY"="$VAL"
done
IFS=$saveIFS

MENSAJE_ACCION=""

if [ -n "$vid" ]; then
    if [ "$accion" == "aislar" ]; then
        OUTPUT=$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" bridge Aplicar_Ebtables "$vid" 2>&1)
        MENSAJE_ACCION="<p style='color: lightgreen'>S'ha aplicat l'aïllament a la VLAN $vid.</p>"
    fi

    if [ "$accion" == "no_aislar" ]; then
        OUTPUT=$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" bridge Esborrar_Ebtables "$vid" 2>&1)
        MENSAJE_ACCION="<p style='color: orange'>S'ha eliminat l'aïllament de la VLAN $vid.</p>"
    fi
fi

# -------------------------------------------------------------------
# Generar HTML
# -------------------------------------------------------------------
echo "Content-type: text/html; charset=utf-8"
echo ""

cat << HTML_HEADER
<!DOCTYPE html>
<html lang="ca">
<head>
<title>Configuració Ebtables</title>
<meta charset='utf-8'>
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

.btn {
  padding: 8px 16px;
  text-decoration: none;
  display: inline-block;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9em;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.btn-red {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.5);
}
.btn-red:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(239, 68, 68, 0.2);
}

.btn-green {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.5);
}
.btn-green:hover {
  background: rgba(34, 197, 94, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(34, 197, 94, 0.2);
}

.status-badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85em;
    display: inline-block;
}
.status-aislado {
    background-color: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #fca5a5;
}
.status-no-aislado {
    background-color: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.4);
    color: #86efac;
}

.vlan-container {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.vlan-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.vlan-title {
    font-size: 1.3em;
    font-weight: 700;
    color: #f1f5f9;
    display: flex;
    align-items: center;
    gap: 10px;
}

</style>
</head>
<body>

<h2>Gestió d'Aïllament per VLAN</h2>

$MENSAJE_ACCION

HTML_HEADER

BRIDGE_CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF"
BRIDGE_IF_FILE="$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_IF"

if [ ! -f "$BRIDGE_CONF_FILE" ]; then
    echo "<p>Error: No s'ha trobat el fitxer de configuració de VLANs ($BRIDGE_CONF_FILE)</p>"
    echo "</body></html>"
    exit 0
fi

# Llegir BRIDGE.CONF línia a línia (excepte comentaris)
grep -v '^#' "$BRIDGE_CONF_FILE" | while IFS=';' read -r NOM VID IP GW RESTO; do
    
    # Obtenir Estat per aquesta VLAN
    ESTAT_VLAN=$("$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli" bridge Estat_Ebtables "$VID")
    
    # Determinar botó i badge
    if [ "$ESTAT_VLAN" == "AISLADO" ]; then
        BADGE="<span class='status-badge status-aislado'>AÏLLAT</span>"
        ACCION_BTN="<a href='?accion=no_aislar&vid=$VID' class='btn btn-green'>Deixar d'Aïllar</a>"
    else
        BADGE="<span class='status-badge status-no-aislado'>NO AÏLLAT</span>"
        ACCION_BTN="<a href='?accion=aislar&vid=$VID' class='btn btn-red'>Aïllar Interfícies</a>"
    fi

    echo "<div class='vlan-container'>"
    echo "  <div class='vlan-header'>"
    echo "    <div class='vlan-title'>$NOM (VLAN $VID) $BADGE</div>"
    echo "    <div>$ACCION_BTN</div>"
    echo "  </div>"
    
    echo "  <table>"
    echo "    <tr><th>Interfície</th><th>VLAN Untag</th><th>VLAN Tag</th></tr>"
    
    # Filtrar i mostrar interfícies d'aquesta VLAN
    if [ -f "$BRIDGE_IF_FILE" ]; then
        grep -v '^#' "$BRIDGE_IF_FILE" | while IFS=';' read -r IFACE UNTAG TAG RESTOO; do
            IS_RELATED=0
            if [ "$UNTAG" == "$VID" ]; then
                IS_RELATED=1
            else
                for t in ${TAG//,/ }; do
                    if [ "$t" == "$VID" ]; then
                        IS_RELATED=1
                        break
                    fi
                done
            fi

            if [ "$IS_RELATED" -eq 1 ]; then
                echo "    <tr>"
                echo "      <td>$IFACE</td>"
                echo "      <td>$UNTAG</td>"
                echo "      <td>$TAG</td>"
                echo "    </tr>"
            fi
        done
    fi
    
    echo "  </table>"
    echo "</div>"

done

cat << HTML_FOOTER
</body>
</html>
HTML_FOOTER
