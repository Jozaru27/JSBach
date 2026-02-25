#!/bin/bash

# JSBach Router Administration - DHCP Actions and Status
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
    
    action=$(echo "$post_data" | sed -n 's/^.*action=\([^&]*\).*$/\1/p')
    
    if [ "$action" == "toggle" ]; then
        interface=$(echo "$post_data" | sed -n 's/^.*interface=\([^&]*\).*$/\1/p')
        if_dec=$(urldecode "$interface")
        "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "toggle_range" "$if_dec" > /dev/null
        "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "restart_if_active" > /dev/null
        MSG="Estat del rang DHCP canviat"
    else
        # Collect all and apply
        echo "$post_data" | sed 's/&/\n/g' | grep "_start=" | while read -r line; do
            key=$(echo "$line" | cut -d'=' -f1)
            val=$(echo "$line" | cut -d'=' -f2)
            ifname=$(echo "$key" | cut -d'_' -f2)
            ifname_dec=$(urldecode "$ifname")
            
            end_val=$(echo "$post_data" | sed -n "s/^.*range_${ifname}_end=\([^&]*\).*$/\1/p")
            val_dec=$(urldecode "$val")
            end_dec=$(urldecode "$end_val")
            
            "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "save_config_range" "$ifname_dec" "$val_dec" "$end_dec" > /dev/null
        done
        # Restart once at the end if it was active
        "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "restart_if_active" > /dev/null
        MSG="Configuració DHCP guardada i servei actualitzat"
    fi
    
    echo "<html><head><script>window.location.href='/cgi-bin/dhcp.cgi?comand=configuracio';</script></head><body></body></html>"
    exit 0
fi

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Execute command for status/start/stop
if [ "$comand" != "configuracio" ]; then
    RAW_OUTPUT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "$comand")
    ESTAT_GRAL=$(echo "$RAW_OUTPUT" | head -n1)
    HTML_CONTENT=$(echo "$RAW_OUTPUT" | sed '1d')
fi

# Header Config
ICON="🔌"
TITLE="DHCP"
case "$comand" in
    iniciar)  TITLE="Iniciar DHCP" ; ICON="🚀" ;;
    aturar)   TITLE="Aturar DHCP"  ; ICON="🛑" ;;
    estat)    TITLE="Estat del DHCP" ; ICON="📊" ;;
    configuracio) TITLE="Configuració DHCP" ; ICON="⚙️" ;;
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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Fira+Code&display=swap');

body {
  font-family: 'Outfit', sans-serif;
  margin: 0;
  padding: 3rem;
  background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%);
  color: #f1f5f9;
  min-height: 100vh;
}

.container { max-width: 1100px; margin: 0 auto; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4rem;
}

h1 {
  background: rgba(255, 255, 255, 0.03);
  padding: 20px 30px;
  border-radius: 20px;
  border-left: 5px solid #3b82f6;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 20px;
  margin: 0;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
}

.card {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(15px);
  margin-bottom: 40px;
  transition: transform 0.3s ease;
}

.card:hover { transform: translateY(-5px); }

h3 { 
  margin: 0 0 30px 0;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(59, 130, 246, 0.3);
  font-size: 1.5rem;
  font-weight: 800;
  color: #60a5fa;
  letter-spacing: 0.5px;
}

.badge { display: inline-block; padding: 8px 18px; border-radius: 50px; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; }
.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.4); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4); }
.badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.4); }

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 12px;
  margin-top: 10px;
}

th {
  text-align: left;
  padding: 12px 20px;
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

td {
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.3s ease;
}

tr:hover td { background: rgba(255, 255, 255, 0.06); }

td:first-child { border-left: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px 0 0 16px; font-weight: 700; color: #fff; }
td:last-child { border-right: 1px solid rgba(255, 255, 255, 0.05); border-radius: 0 16px 16px 0; }

input[type="text"] {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  padding: 12px 15px;
  width: 100%;
  max-width: 180px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input[type="text"]:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

.btn-save {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 20px 40px;
  border-radius: 16px;
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
}

.btn-save:hover { 
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.4);
  filter: brightness(1.1);
}

[style*="font-family: monospace"] {
  background: rgba(15, 23, 42, 0.8);
  color: #cbd5e1;
  padding: 25px;
  border-radius: 16px;
  white-space: pre-wrap;
  word-break: break-all;
  border: 1px solid rgba(255, 255, 255, 0.05);
  font-family: 'Fira Code', monospace !important;
  font-size: 0.95rem;
  line-height: 1.7;
  box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
}

/* Overlay de reinici */
#overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(20px);
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}
.spinner {
  width: 70px;
  height: 70px;
  border: 4px solid rgba(59, 130, 246, 0.1);
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  margin-bottom: 30px;
  box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
}
@keyframes spin { to { transform: rotate(360deg); } }
.overlay-text { font-size: 1.8rem; font-weight: 800; color: #fff; letter-spacing: -0.02em; }
</style>
<script>
function showLoading(text) {
    if (text) document.querySelector('.overlay-text').innerText = text;
    document.getElementById('overlay').style.display = 'flex';
    document.querySelector('.container').style.filter = 'blur(8px)';
    document.querySelector('.container').style.transition = 'filter 0.5s ease';
}

function ip2int(ip) {
    return ip.split('.').reduce((res, item) => (res << 8) + parseInt(item), 0) >>> 0;
}

function isSameSubnet(ip1, ip2, maskStr) {
    const int1 = ip2int(ip1);
    const int2 = ip2int(ip2);
    let mask = 24;
    if (maskStr.includes('.')) {
        if (maskStr === '255.255.255.0') mask = 24;
        else if (maskStr === '255.255.255.128') mask = 25;
        else if (maskStr === '255.255.0.0') mask = 16;
        else if (maskStr === '255.0.0.0') mask = 8;
    } else {
        mask = parseInt(maskStr);
    }
    const shift = 32 - mask;
    return (int1 >>> shift) === (int2 >>> shift);
}

function validateAndSubmit() {
    const rows = document.querySelectorAll('tbody tr');
    for (let row of rows) {
        const start = row.querySelector('input[name*="_start"]').value;
        const end = row.querySelector('input[name*="_end"]').value;
        const mask = row.cells[4].innerText.trim();
        const iface = row.cells[0].innerText.trim();
        
        if (!isSameSubnet(start, end, mask)) {
            alert('Error a la interfície ' + iface + ': Els rangs han d\'estar a la mateixa subxarxa (' + mask + ')');
            return false;
        }
    }
    showLoading();
    return true;
}
</script>
</head>
<body>
  <div id="overlay">
    <div class="spinner"></div>
    <div class="overlay-text">Reiniciant servei DHCP...</div>
  </div>
  <div class="container">
EOF

if [ "$comand" = "configuracio" ]; then
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2.5rem;">$ICON</span> $TITLE</h1>
    </div>
    <div class="card">
      <h3>Configuració de Rangs DHCP</h3>
      <form method="POST" id="dhcpForm" onsubmit="return validateAndSubmit()">
        <input type="hidden" name="action" value="save" id="formAction">
        <input type="hidden" name="interface" value="" id="formInterface">
        <table>
          <thead>
            <tr>
              <th>Interfície</th>
              <th>Estat</th>
              <th>Rang d'Inici</th>
              <th>Rang Final</th>
              <th>Mascara</th>
              <th>Lloguer</th>
              <th style="text-align: right;">Accions</th>
            </tr>
          </thead>
          <tbody>
EOF
    # Dynamic parsing of dnsmasq.conf ranges (including commented ones)
    grep -E "^#?dhcp-range=interface:" /etc/dnsmasq.conf | while read -r line; do
        is_commented=0
        echo "$line" | grep -q "^#" && is_commented=1
        clean_line=$(echo "$line" | sed 's/^#//')
        ifname=$(echo "$clean_line" | cut -d':' -f2 | cut -d',' -f1)
        start=$(echo "$clean_line" | cut -d',' -f2)
        end=$(echo "$clean_line" | cut -d',' -f3)
        mask=$(echo "$clean_line" | cut -d',' -f4)
        lease=$(echo "$clean_line" | cut -d',' -f5)
        
        if [ $is_commented -eq 1 ]; then
            status_badge="<span class='badge badge-red'>INACTIU</span>"
            toggle_text="<span class='icon'>✅</span> Activar"
            row_style="opacity: 0.6;"
        else
            status_badge="<span class='badge badge-green'>ACTIU</span>"
            toggle_text="<span class='icon'>🚫</span> Desactivar"
            row_style=""
        fi

        echo "<tr style='$row_style'>"
        echo "<td>$ifname</td>"
        echo "<td>$status_badge</td>"
        echo "<td><input type='text' name='range_${ifname}_start' value='$start'></td>"
        echo "<td><input type='text' name='range_${ifname}_end' value='$end'></td>"
        echo "<td>$mask</td>"
        echo "<td>$lease</td>"
        echo "<td style='text-align: right;'>"
        echo "  <button type='button' class='badge badge-blue' style='cursor:pointer; border:1px solid rgba(59,130,246,0.5); font-family: inherit;' onclick=\"toggleRange('$ifname')\">$toggle_text</button>"
        echo "</td>"
        echo "</tr>"
    done
    cat << EOF
          </tbody>
        </table>
        <div style="margin-top: 30px; display: flex; justify-content: flex-end;">
            <button type="submit" class="btn-save">💾 Guardar Totes les Config d'Interfície</button>
        </div>
      </form>
    </div>
    
    <script>
    function toggleRange(iface) {
        showLoading("Canviant estat del rang...");
        document.getElementById('formAction').value = 'toggle';
        document.getElementById('formInterface').value = iface;
        document.getElementById('dhcpForm').submit();
    }
    </script>
EOF
else
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2.5rem;">$ICON</span> $TITLE</h1>
        $(get_badge "$ESTAT_GRAL")
    </div>
EOF
    echo "$HTML_CONTENT" | awk '
    BEGIN { first=1; card_opened=0 }
    /<h3>/ {
        if (card_opened) print "</div>"
        print "<div class=\"card\">"
        card_opened=1
        first=0
    }
    { 
        if (first && !card_opened) {
            print "<div class=\"card\">"
            card_opened=1
            first=0
        }
        print $0 
    }
    END { if (card_opened) print "</div>" }
    '
fi

cat << EOF
  </div>
</body>
</html>
EOF
