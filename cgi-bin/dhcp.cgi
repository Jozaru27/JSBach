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
        MSG="Configuració DHCP guardada i servei reiniciat"
    fi
    
    echo "<html><head><script>alert('$MSG'); window.location.href='/cgi-bin/dhcp.cgi?comand=configuracio';</script></head><body></body></html>"
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

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
  margin-top: 10px;
}

th {
  text-align: left;
  padding: 12px 15px;
  color: #94a3b8;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

td {
  padding: 15px;
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

td:first-child { border-left: 1px solid rgba(255, 255, 255, 0.03); border-radius: 12px 0 0 12px; }
td:last-child { border-right: 1px solid rgba(255, 255, 255, 0.03); border-radius: 0 12px 12px 0; }

input[type="text"] {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  padding: 10px 12px;
  width: 100%;
  max-width: 160px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

input[type="text"]:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
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
}

.btn-save:hover { 
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
  filter: brightness(1.1);
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
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
    </div>
    <div class="card">
      <h3>Configuració de Rangs DHCP</h3>
      <form method="POST" id="dhcpForm">
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
              <th>Temps de lloguer</th>
              <th style="text-align: right;">Accions</th>
            </tr>
          </thead>
          <tbody>
EOF
    # Dynamic parsing of dnsmasq.conf ranges (including commented ones)
    grep -E "^#?dhcp-range=interface:" /etc/dnsmasq.conf | while read -r line; do
        is_commented=0
        echo "$line" | grep -q "^#" && is_commented=1
        
        # Clean line for parsing
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
        echo "<td><b>$ifname</b></td>"
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
    function toggleRange(ifname) {
        document.getElementById('formAction').value = 'toggle';
        document.getElementById('formInterface').value = ifname;
        document.getElementById('dhcpForm').submit();
    }
    </script>
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
