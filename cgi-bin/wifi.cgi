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
    hw_mode=$(echo "$post_data" | sed -n 's/^.*hw_mode=\([^&]*\).*$/\1/p')
    ieee=$(echo "$post_data" | sed -n 's/^.*ieee=\([^&]*\).*$/\1/p')
    wmm=$(echo "$post_data" | sed -n 's/^.*wmm=\([^&]*\).*$/\1/p')
    interface=$(echo "$post_data" | sed -n 's/^.*interface=\([^&]*\).*$/\1/p')
    auth_algs=$(echo "$post_data" | sed -n 's/^.*auth_algs=\([^&]*\).*$/\1/p')
    wpa_ver=$(echo "$post_data" | sed -n 's/^.*wpa_ver=\([^&]*\).*$/\1/p')
    key_mgmt=$(echo "$post_data" | sed -n 's/^.*key_mgmt=\([^&]*\).*$/\1/p')
    rsn_pairwise=$(echo "$post_data" | sed -n 's/^.*rsn_pairwise=\([^&]*\).*$/\1/p')
    
    # Decode strings
    ssid_dec=$(urldecode "$ssid")
    pass_dec=$(urldecode "$passphrase")
    if_dec=$(urldecode "$interface")
    kmgmt_dec=$(urldecode "$key_mgmt")
    rsn_dec=$(urldecode "$rsn_pairwise")
    
    # Send to backend via client_srv_cli
    "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi "save_config" \
        "$ssid_dec" "$pass_dec" "$channel" "$hw_mode" "$ieee" "$wmm" \
        "$if_dec" "$auth_algs" "$wpa_ver" "$kmgmt_dec" "$rsn_dec" > /dev/null
    
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

.form-group { margin-bottom: 25px; }
label { display: block; margin-bottom: 10px; font-weight: 600; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }

input[type="text"], 
input[type="password"], 
input[type="number"],
select {
  width: 100%;
  padding: 14px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

input:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Millora específica per a inputs numèrics */
input[type="number"] {
  -moz-appearance: textfield;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.btn-save {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
  width: 100%;
}

.btn-save:hover { 
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
  filter: brightness(1.1);
}

.btn-save:active {
  transform: translateY(0);
}

.grid-config {
  display: grid; 
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
  gap: 25px;
}

[style*="font-family: monospace"] {
  background: #020617;
  color: #94a3b8;
  padding: 24px;
  border-radius: 14px;
  white-space: pre-wrap;
  word-break: break-all;
  border: 1px solid rgba(255, 255, 255, 0.05);
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
    curr_hw=$(grep "^hw_mode=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_ieee=$(grep "^ieee80211n=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_wmm=$(grep "^wmm_enabled=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_if=$(grep "^interface=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_auth=$(grep "^auth_algs=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_wpa=$(grep "^wpa=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_kmgmt=$(grep "^wpa_key_mgmt=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    curr_rsn=$(grep "^rsn_pairwise=" /etc/hostapd/hostapd.conf | cut -d'=' -f2)
    
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
    </div>
    <div class="card">
      <h3>Configuració del Punt d'Accés</h3>
      <form method="POST">
        <div class="grid-config">
            <div class="form-group">
                <label>Nom de la interfície (interface)</label>
                <input type="text" name="interface" value="$curr_if" required>
            </div>
            <div class="form-group">
                <label>SSID (Nom de la xarxa)</label>
                <input type="text" name="ssid" value="$curr_ssid" required>
            </div>
            <div class="form-group">
                <label>Mode Hardware (hw_mode)</label>
                <select name="hw_mode">
                    <option value="g" $( [ "$curr_hw" = "g" ] && echo "selected" )>802.11g (2.4 GHz)</option>
                    <option value="a" $( [ "$curr_hw" = "a" ] && echo "selected" )>802.11a (5 GHz)</option>
                    <option value="b" $( [ "$curr_hw" = "b" ] && echo "selected" )>802.11b (Legacy)</option>
                </select>
            </div>
            <div class="form-group">
                <label>IEEE 802.11n</label>
                <select name="ieee">
                    <option value="1" $( [ "$curr_ieee" = "1" ] && echo "selected" )>Activat</option>
                    <option value="0" $( [ "$curr_ieee" = "0" ] && echo "selected" )>Desactivat</option>
                </select>
            </div>
            <div class="form-group">
                <label>WMM (Wireless Multimedia)</label>
                <select name="wmm">
                    <option value="1" $( [ "$curr_wmm" = "1" ] && echo "selected" )>Activat</option>
                    <option value="0" $( [ "$curr_wmm" = "0" ] && echo "selected" )>Desactivat</option>
                </select>
            </div>
            <div class="form-group">
                <label>Canal</label>
                <input type="number" name="channel" value="$curr_chan" min="1" max="165" required>
            </div>
            <div class="form-group">
                <label>Auth Algs</label>
                <input type="number" name="auth_algs" value="$curr_auth" min="1" max="3" required>
            </div>
            <div class="form-group">
                <label>WPA Version</label>
                <input type="number" name="wpa_ver" value="$curr_wpa" min="1" max="3" required>
            </div>
            <div class="form-group">
                <label>Key Management (wpa_key_mgmt)</label>
                <input type="text" name="key_mgmt" value="$curr_kmgmt" required>
            </div>
            <div class="form-group">
                <label>RSN Pairwise (Cifratge)</label>
                <input type="text" name="rsn_pairwise" value="$curr_rsn" required>
            </div>
            <div class="form-group" style="grid-column: 1 / -1;">
                <label>Contrasenya (WPA2)</label>
                <input type="password" name="passphrase" value="$curr_pass" required>
            </div>
        </div>
        <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
            <button type="submit" class="btn-save">💾 Guardar Canvis i Reiniciar Servei</button>
        </div>
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
