#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

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
    echo "<html><body style='background:#0f172a; color:white; font-family:sans-serif; padding:50px; text-align:center;'>"
    echo "<h2>Error</h2><p>No s'ha trobat cap VLAN amb VID = $VID</p>"
    echo "<a href='/cgi-bin/bridge-configurar.cgi' style='color:#3b82f6;'>Tornar</a></body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Esborrar VLAN - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 40px 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { margin: 0 auto; max-width: 600px; }

h1 {
  background: rgba(239, 68, 68, 0.1);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #ef4444;
  margin-bottom: 30px;
  color: #f87171;
  font-weight: 600;
  display: flex;
  align-items: center; gap: 15px;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.warning-text {
  color: #94a3b8;
  margin-bottom: 25px;
  font-size: 1rem;
  line-height: 1.6;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
  background: rgba(0,0,0,0.2);
  border-radius: 8px;
  overflow: hidden;
}

.data-table th, .data-table td { padding: 12px 15px; text-align: left; }
.data-table th { color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; }
.data-table td { color: #fff; font-weight: 600; border-top: 1px solid rgba(255,255,255,0.05); }

.actions { display: flex; gap: 12px; }

.btn {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
  border: none;
}

.btn-delete {
  background: #ef4444;
  color: white;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.3);
}

.btn-delete:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(239, 68, 68, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}
  </style>
</head>
<body>
  <div class="container">
    <h1>⚠️ Confirmar Eliminació</h1>
    
    <div class="card">
      <p class="warning-text">
        Esteu a punt d'eliminar la següent VLAN. Aquesta acció no es pot desfer i podria afectar la connectivitat del sistema.
      </p>
      
      <table class="data-table">
        <tr><th>Nom</th><td>$nom</td></tr>
        <tr><th>VID</th><td>$vid</td></tr>
        <tr><th>Subxarxa</th><td>$subnet</td></tr>
        <tr><th>Gateway</th><td>$gw</td></tr>
      </table>
      
      <form action='/cgi-bin/bridge-aplicar-esborrar.cgi' method='get'>
        <input type="hidden" name="vid" value="$vid">
        <div class="actions">
          <a href="/cgi-bin/bridge-configurar.cgi" class="btn btn-secondary">Cancel·lar</a>
          <button type="submit" class="btn btn-delete">Eliminar VLAN</button>
        </div>
      </form>
    </div>
  </div>
</body>
</html>
EOF
