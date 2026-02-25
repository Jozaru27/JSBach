#!/bin/bash

# JSBach Router Administration - WIFI Actions and Status
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Function to URL decode
urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

# Handle config saving if POST
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r post_data
    ssid=$(echo "$post_data" | sed -n 's/^.*ssid=\([^&]*\).*$/\1/p')
    passphrase=$(echo "$post_data" | sed -n 's/^.*passphrase=\([^&]*\).*$/\1/p')
    channel=$(echo "$post_data" | sed -n 's/^.*channel=\([^&]*\).*$/\1/p')
    
    # Decode
    ssid_dec=$(urldecode "$ssid")
    pass_dec=$(urldecode "$passphrase")
    
    # Send to backend via client_srv_cli
    # Use quotes for arguments with spaces
    "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi "save_config" "$ssid_dec" "$pass_dec" "$channel" > /dev/null
    
    echo "<html><head><script>alert('Configuració guardada i servei reiniciat'); window.location.href='/cgi-bin/wifi.cgi?comand=configuracio';</script></head><body></body></html>"
    exit 0
fi

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Execute command for status/start/stop
if [ "$comand" != "configuracio" ]; then
    RAW_OUTPUT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi "$comand")
    ESTAT_GRAL=$(echo "$RAW_OUTPUT" | head -n1)
    HTML_CONTENT=$(echo "$RAW_OUTPUT" | sed '1d')
fi

# Header Config
ICON="📶"
TITLE="WiFi"
case "$comand" in
    iniciar)  TITLE="Iniciar WiFi" ; ICON="🚀" ;;
    aturar)   TITLE="Aturar WiFi"  ; ICON="🛑" ;;
    estat)    TITLE="Estat del WiFi" ; ICON="📊" ;;
    configuracio) TITLE="Configuració WiFi" ; ICON="⚙️" ;;
esac

get_badge() {
    if echo "$1" | grep -qiw "ACTIVAT"; then echo "<span class='badge badge-green'>ACTIU</span>"
    elif echo "$1" | grep -qiw "DESACTIVAT"; then echo "<span class='badge badge-red'>INACTIU</span>"
    else echo "<span class='badge badge-blue'>$1</span>"; fi
}

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>$TITLE - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { max-width: 1100px; margin: 0 auto; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 18px 24px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(15px);
  margin-bottom: 35px;
}

h3 { 
  margin: 0 0 25px 0;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 1.3rem;
  font-weight: 700;
  color: #60a5fa;
  letter-spacing: 0.5px;
}

.badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }

.form-group { margin-bottom: 20px; }
label { display: block; margin-bottom: 8px; font-weight: 600; color: #94a3b8; }
input[type="text"], input[type="password"], select {
  width: 100%;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
}
.btn-save {
  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-save:hover { background: #1d4ed8; }

[style*="font-family: monospace"] {
  background: #020617;
  color: #94a3b8;
  padding: 20px;
  border-radius: 10px;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
</head>
<body>
  <div class="container">
EOF

if [ "$comand" = "configuracio" ]; then
    # Load current values
    curr_ssid=$(grep "^ssid=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_pass=$(grep "^wpa_passphrase=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_chan=$(grep "^channel=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
    </div>
    <div class="card">
      <h3>Configuració del Punt d'Accés</h3>
      <form method="POST">
        <div class="form-group">
          <label>SSID (Nom de la xarxa)</label>
          <input type="text" name="ssid" value="$curr_ssid" required>
        </div>
        <div class="form-group">
          <label>Contrasenya (WPA2)</label>
          <input type="password" name="passphrase" value="$curr_pass" required>
        </div>
        <div class="form-group">
          <label>Canal</label>
          <select name="channel">
            $(for i in {1..11}; do 
                echo -n "<option value='$i' "
                [ "$i" = "$curr_chan" ] && echo -n "selected"
                echo ">Canal $i</option>"
            done)
          </select>
        </div>
        <button type="submit" class="btn-save">💾 Guardar Canvis</button>
      </form>
    </div>
EOF
else
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
        $(get_badge "$ESTAT_GRAL")
    </div>
EOF
    echo "$HTML_CONTENT" | awk '
    BEGIN { first=1 }
    /<h3>/ {
        if (!first) print "</div>"
        print "<div class=\"card\">"
        first=0
    }
    { print $0 }
    END { if (!first) print "</div>" }
    '
fi

cat << EOF
  </div>
</body>
</html>
EOF
