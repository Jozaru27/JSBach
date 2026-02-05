#!/bin/bash

# JSBach Router Administration - Firewall IP Whitelist Actions (Catalan Premium)
source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

echo "Content-type: text/html; charset=utf-8"
echo ""

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

# Extract parameters
accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')

# Decode parameters
accio=$(urldecode "$accio")
vid=$(urldecode "$vid")
ip=$(urldecode "$ip")
mac=$(urldecode "$mac")

# Execute backend action
$RUTA tallafocs configurar "$accio" "$vid" "$ip" "$mac" > /dev/null 2>&1

# Determine display name
case "$accio" in
    afegir_ip_wls)    DISPLAY_ACT="IP Afegida"   ; ICON="➕" ; COLOR="#4ade80" ;;
    eliminar_ip_wls)  DISPLAY_ACT="IP Eliminada" ; ICON="🗑️" ; COLOR="#f87171" ;;
    *)                DISPLAY_ACT="Acció Completada" ; ICON="✅" ; COLOR="#fff"    ;;
esac

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="2;url=/cgi-bin/tallafocs-configuracio.cgi">
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 40px 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 40px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  text-align: center;
  backdrop-filter: blur(15px);
  animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.icon-box {
  font-size: 3.5rem;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.05);
  width: 90px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-left: auto;
  margin-right: auto;
  border: 2px solid $COLOR;
  color: $COLOR;
}

h2 { margin: 0 0 10px 0; color: #fff; font-size: 1.6rem; }
.message { color: #94a3b8; margin-bottom: 25px; line-height: 1.5; font-size: 1rem; }

.loader {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: $COLOR;
  border-radius: 50%;
  display: inline-block;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>
  <div class="card">
    <div class="icon-box">$ICON</div>
    <h2>$DISPLAY_ACT</h2>
    <div class="message">
      S'ha configurat correctament l'adreça IP <strong style="color:#fff;">$ip</strong> (VLAN $vid) a la llista d'accés no restringit.
    </div>
    <div class="loader"></div>
  </div>
</body>
</html>
EOF
