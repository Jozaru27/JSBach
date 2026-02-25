#!/bin/bash

# JSBach Router Administration - DHCP Actions and Status
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Handle config saving if POST
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -r post_data
    
    # Simple extraction logic for multiple ranges
    echo "$post_data" | sed 's/&/\n/g' | while read -r line; do
        key=$(echo "$line" | cut -d'=' -f1)
        val=$(echo "$line" | cut -d'=' -f2)
        
        if [[ $key == range_* ]]; then
            interface=$(echo "$key" | cut -d'_' -f2)
            type=$(echo "$key" | cut -d'_' -f3) # start or end
            
            # Store values temporarily to send them in one go per interface
            # Since we iterate lines, we'll store them in a temp file or associative array (if bash 4+)
            # For simplicity in this shell environment, we send them to backend one by one if they are both there
            # BUT we prefer sending the whole set. 
            # Let's just collect all and call a backend command that handles it.
            if [ "$type" == "start" ]; then
                # Get the matching end value from the same post_data
                end_val=$(echo "$post_data" | sed -n "s/^.*range_${interface}_end=\([^&]*\).*$/\1/p")
                
                # Send to backend
                "$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp "save_config_range" "$interface" "$val" "$end_val" > /dev/null
            fi
        fi
    done
    
    echo "<html><head><script>alert('Configuració DHCP guardada i servei reiniciat'); window.location.href='/cgi-bin/dhcp.cgi?comand=configuracio';</script></head><body></body></html>"
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
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

input[type="text"] {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #fff;
  padding: 5px;
  width: 120px;
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
  margin-top: 20px;
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
    cat << EOF
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
    </div>
    <div class="card">
      <h3>Configuració de Rangs DHCP</h3>
      <form method="POST">
        <table>
          <thead>
            <tr>
              <th>Interfície</th>
              <th>Inici</th>
              <th>Final</th>
              <th>Mascara</th>
              <th>Temps</th>
            </tr>
          </thead>
          <tbody>
EOF
    # Dynamic parsing of dnsmasq.conf ranges
    grep "dhcp-range=interface:" /etc/dnsmasq.conf | while read -r line; do
        ifname=$(echo "$line" | cut -d':' -f2 | cut -d',' -f1)
        start=$(echo "$line" | cut -d',' -f2)
        end=$(echo "$line" | cut -d',' -f3)
        mask=$(echo "$line" | cut -d',' -f4)
        lease=$(echo "$line" | cut -d',' -f5)
        
        echo "<tr>"
        echo "<td><b>$ifname</b></td>"
        echo "<td><input type='text' name='range_${ifname}_start' value='$start'></td>"
        echo "<td><input type='text' name='range_${ifname}_end' value='$end'></td>"
        echo "<td>$mask</td>"
        echo "<td>$lease</td>"
        echo "</tr>"
    done
    cat << EOF
          </tbody>
        </table>
        <button type="submit" class="btn-save">💾 Guardar Configuració</button>
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
