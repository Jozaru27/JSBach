#!/bin/bash

# JSBach Router Administration - Portal Captiu Management
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Function to URL decode
urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

CONF_PATH="$DIR/$PROJECTE/$DIR_CONF/$PORTAL_CAPTIU_CONF"

# Handle POST requests (Configuration / Save)
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r post_data
    usuario=$(echo "$post_data" | sed -n 's/^.*usuario=\([^&]*\).*$/\1/p')
    password=$(echo "$post_data" | sed -n 's/^.*password=\([^&]*\).*$/\1/p')
    
    # Decode strings
    user_dec=$(urldecode "$usuario")
    pass_dec=$(urldecode "$password")
    
    # Save to config via backend
    "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu "configurar" "$user_dec" "$pass_dec" > /dev/null
    
    echo "<html><head><script>window.location.href='/cgi-bin/portal_captiu.cgi?comand=configuracio';</script></head><body></body></html>"
    exit 0
fi

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Execute command for status/start/stop
if [ "$comand" != "configuracio" ] && [ -n "$comand" ]; then
    "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu "$comand" > /dev/null
fi

# Get State
ESTAT_GRAL=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu estat | head -n1)

# Header Config
ICON="🌐"
TITLE="Portal Captiu"
case "$comand" in
    iniciar)  TITLE="Iniciar Portal" ; ICON="🚀" ;;
    aturar)   TITLE="Aturar Portal"  ; ICON="🛑" ;;
    estat)    TITLE="Estat del Portal" ; ICON="📊" ;;
    configuracio) TITLE="Configuració Portal" ; ICON="⚙️" ;;
esac

get_badge() {
    if echo "$1" | grep -qiw "ACTIVAT"; then echo "<span class='badge badge-green'>ACTIU</span>"
    elif echo "$1" | grep -qiw "DESACTIVAT"; then echo "<span class='badge badge-red'>INACTIU</span>"
    else echo "<span class='badge badge-blue'>$1</span>"; fi
}

# Get current config
curr_user=$(cat "$CONF_PATH" | cut -d';' -f1)
curr_pass=$(cat "$CONF_PATH" | cut -d';' -f2)

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>$TITLE - JSBach</title>
  <style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code&display=swap');

body {
  font-family: 'Outfit', sans-serif;
  margin: 0; padding: 3rem;
  background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%);
  color: #f1f5f9; min-height: 100vh;
}

.container { max-width: 1100px; margin: 0 auto; }

.page-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 4rem;
}

h1 {
  background: rgba(255, 255, 255, 0.03); padding: 20px 30px;
  border-radius: 20px; border-left: 5px solid #3b82f6;
  font-weight: 800; display: flex; align-items: center;
  gap: 20px; margin: 0; backdrop-filter: blur(10px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

.card {
  background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px; padding: 40px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(15px); margin-bottom: 40px; transition: transform 0.3s ease;
}

.card:hover { transform: translateY(-5px); }

h3 { 
  margin: 0 0 30px 0; padding-bottom: 15px; border-bottom: 2px solid rgba(59, 130, 246, 0.3);
  font-size: 1.5rem; font-weight: 800; color: #60a5fa; letter-spacing: 0.5px;
}

.badge { display: inline-block; padding: 8px 18px; border-radius: 50px; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; }
.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); }

.btn-group { display: flex; gap: 15px; margin-top: 20px; }

.btn {
  padding: 15px 30px; border-radius: 12px; font-weight: 800; text-decoration: none;
  transition: all 0.3s ease; border: none; cursor: pointer; display: inline-flex;
  align-items: center; gap: 10px; font-size: 1rem;
}

.btn-green { background: #22c55e; color: white; box-shadow: 0 4px 10px rgba(34, 197, 94, 0.3); }
.btn-red { background: #ef4444; color: white; box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3); }
.btn-blue { background: #3b82f6; color: white; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3); }

.btn:hover { transform: translateY(-2px); filter: brightness(1.1); }

.form-group { margin-bottom: 30px; }
label { display: block; margin-bottom: 12px; font-weight: 700; color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }

input {
  width: 100%; padding: 16px 20px; background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px;
  color: #fff; font-size: 1rem; transition: all 0.3s ease; box-sizing: border-box;
}

input:focus { outline: none; border-color: #3b82f6; background: rgba(15, 23, 42, 0.8); box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2); }

.info-code {
  background: rgba(15, 23, 42, 0.8); color: #cbd5e1; padding: 25px;
  border-radius: 16px; font-family: 'Fira Code', monospace; font-size: 0.95rem;
  line-height: 1.7; border: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
</head>
<body>
  <div class="container">
    <div class="page-header">
        <h1><span style="font-size: 2.5rem;">$ICON</span> $TITLE</h1>
        $(get_badge "$ESTAT_GRAL")
    </div>

    <div class="card">
        <h3>Accions del Servei</h3>
        <p>Controla el funcionament del portal captiu per a les xarxes filtrades.</p>
        <div class="btn-group">
            <a href="?comand=iniciar" class="btn btn-green">🚀 Iniciar Portal</a>
            <a href="?comand=aturar" class="btn btn-red">🛑 Aturar Portal</a>
            <a href="?comand=estat" class="btn btn-blue">📊 Refrescar Estat</a>
        </div>
    </div>

    <div class="card">
        <h3>Configuració de Credencials</h3>
        <form method="POST">
            <div class="form-group">
                <label>Nom d'Usuari</label>
                <input type="text" name="usuario" value="$curr_user" required>
            </div>
            <div class="form-group">
                <label>Contrasenya d'accés</label>
                <input type="password" name="password" value="$curr_pass" required>
            </div>
            <button type="submit" class="btn btn-blue" style="width: 100%;">💾 Guardar i Aplicar</button>
        </form>
    </div>

    <div class="card">
        <h3>Estat de les Interfícies</h3>
        <div class="info-code">
$(ip addr show br0.3 2>/dev/null || echo "Interfície br0.3 (VLAN3) NO activa")
<br><br>
$(ip addr show wlp5s0 | grep -E "wlp5s0|inet " || echo "Interfície wlp5s0 (WiFi) NO configurada")
        </div>
    </div>

  </div>
</body>
</html>
EOF
