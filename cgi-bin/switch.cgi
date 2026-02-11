#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

get_switches() {
    [ -f "/usr/local/JSBach/conf/$CONF_SWITCHES" ] && grep -v "^#" "/usr/local/JSBach/conf/$CONF_SWITCHES" | grep -v "^$" | while IFS=';' read -r name ip user pass proto _; do
        [ -n "$ip" ] && echo "$name;$ip;$user;$pass;$proto"
    done
}

get_blocked_macs() {
    [ -f "/usr/local/JSBach/conf/$MACS_SWITCHES_CONF" ] && grep -v "^#" "/usr/local/JSBach/conf/$MACS_SWITCHES_CONF" | grep -v "^$"
}

if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH POST_DATA
    get_val() { echo "$POST_DATA" | grep -oP "(?<=&|^)$1=.*?(?=&|$)" | cut -d= -f2 | sed 's/+/ /g' | perl -pe 's/%([0-9a-f]{2})/chr(hex($1))/eig'; }
else
    get_val() { echo "$QUERY_STRING" | grep -oP "(?<=&|^)$1=.*?(?=&|$)" | cut -d= -f2 | sed 's/+/ /g' | perl -pe 's/%([0-9a-f]{2})/chr(hex($1))/eig'; }
fi

comand=$(get_val comand)

print_header() {
    echo "Content-type: text/html; charset=utf-8"
    echo ""
    cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="utf-8">
    <title>Gestió de Switches - JSBach</title>
    <style>
        :root { --bg: #0f172a; --card-bg: rgba(30, 41, 59, 0.7); --text: #e2e8f0; --primary: #3b82f6; --success: #10b981; --error: #ef4444; --border: rgba(255, 255, 255, 0.1); }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; margin: 0; }
        .container { max-width: 1000px; margin: 0 auto; }
        .card { background: var(--card-bg); backdrop-filter: blur(10px); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
        h1 { color: var(--primary); font-size: 1.5rem; }
        h2 { font-size: 1.1rem; color: #94a3b8; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; }
        .btn { padding: 0.5rem 1rem; border-radius: 6px; border: none; cursor: pointer; font-weight: 600; font-size: 0.85rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-success { background: var(--success); color: white; }
        .btn-error { background: var(--error); color: white; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th { text-align: left; color: #94a3b8; font-size: 0.8rem; padding: 0.5rem; border-bottom: 2px solid var(--border); }
        td { padding: 0.5rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        .status-badge { padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
        .status-active { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .status-down { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
        .form-group { display: flex; flex-direction: column; gap: 0.3rem; }
        label { font-size: 0.8rem; color: #94a3b8; }
        input, select { background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); border-radius: 4px; padding: 0.5rem; color: white; }
        pre { background: #000; color: #34d399; padding: 1rem; border-radius: 6px; font-size: 0.8rem; overflow-x: auto; }
        .mac-item { display: flex; justify-content: space-between; padding: 0.4rem; background: rgba(255,255,255,0.03); border-radius: 4px; margin-bottom: 0.3rem; }
    </style>
</head>
<body><div class="container">
EOF
}

print_footer() { echo "</div></body></html>"; }

case $comand in
    estat)
        print_header
        echo "<h1>📊 Estat Switch</h1><div class='card'><table><thead><tr><th>Nom</th><th>IP</th><th>Estat</th></tr></thead><tbody>"
        while IFS=';' read -r name ip user pass proto; do
            [ -z "$ip" ] && continue
            ID=$(echo "$ip" | sed 's/\./-/g')
            echo "<tr><td>$name</td><td><code>$ip</code></td><td><span id='s-$ID' class='status-badge'>🔄...</span></td></tr>"
            JS="$JS '$ip',"
        done < <(get_switches)
        echo "</tbody></table></div><script>
        [$JS].forEach(ip => {
            const el = document.getElementById('s-' + ip.replace(/\./g, '-'));
            fetch('/cgi-bin/switch.cgi?comand=p&ip=' + ip).then(r=>r.text()).then(d=>{
                el.textContent = d.trim()==='UP' ? '✅ Activo' : '❌ No Encontrado';
                el.className = 'status-badge ' + (d.trim()==='UP' ? 'status-active' : 'status-down');
            });
        });</script>"
        print_footer ;;
    p)
        echo "Content-type: text/plain"
        echo ""
        ping -c 1 -w 1 "$(get_val ip)" >/dev/null 2>&1 && echo "UP" || echo "DOWN"
        exit 0 ;;
    mostrar)
        print_header
        echo "<h1>📋 Taula MAC</h1>"
        while IFS=';' read -r n i u p pr; do
            [ -z "$i" ] && continue
            ping -c 1 -w 1 "$i" >/dev/null 2>&1 && echo "<div class='card'><h2>$n ($i)</h2><pre>$(/usr/local/JSBach/scripts/switch-scripts.sh configurar mostrar_tabla_macs "$i" "$u" "$p" "$pr" | sed '1,/SWITCH:/d')</pre></div>"
        done < <(get_switches)
        print_footer ;;
    gestion_mac)
        print_header
        echo "<h1>🛡️ Gestión de MAC</h1><div class='card'><h2>Acciones Globales</h2><a href='/cgi-bin/switch.cgi?comand=apply' class='btn btn-success'>🔒 Aplicar Bloqueos</a> <a href='/cgi-bin/switch.cgi?comand=clear' class='btn btn-error'>🔓 Borrar Bloqueos</a></div>"
        echo "<div class='card'><h2>Añadir MAC</h2><form action='/cgi-bin/switch.cgi' method='POST'><input type='hidden' name='comand' value='add_m'><div style='display:flex;gap:1rem;'><input type='text' name='mac' placeholder='XX:XX:XX:XX:XX:XX' required style='flex:1;'><button type='submit' class='btn btn-primary'>➕ Añadir</button></div></form></div>"
        echo "<div class='card'><h2>MACs Bloqueadas</h2>"
        for m in $(get_blocked_macs); do echo "<div class='mac-item'><code>$m</code><a href='/cgi-bin/switch.cgi?comand=del_m&mac=$m' class='btn btn-error btn-small' style='padding:0.2rem 0.5rem;'>🗑️</a></div>"; done
        echo "</div>"
        print_footer ;;
    add_m)
        /usr/local/JSBach/scripts/switch-scripts.sh configurar afegir_mac "$(get_val mac)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_mac"
        echo ""
        exit 0 ;;
    del_m)
        /usr/local/JSBach/scripts/switch-scripts.sh configurar eliminar_mac "$(get_val mac)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=gestion_mac"
        echo ""
        exit 0 ;;
    apply)
        print_header
        echo "<h1>🔒 Aplicando...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/switch-scripts.sh configurar crear_acls)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_mac' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    clear)
        print_header
        echo "<h1>🔓 Borrando...</h1><div class='card'><pre>$(/usr/local/JSBach/scripts/switch-scripts.sh configurar eliminar_acls)</pre></div><a href='/cgi-bin/switch.cgi?comand=gestion_mac' class='btn btn-primary'>Volver</a>"
        print_footer ;;
    configurar)
        print_header
        echo "<h1>⚙️ Configuració Switch</h1><div class='card'><h2>Añadir Switch</h2><form action='/cgi-bin/switch.cgi' method='POST'><input type='hidden' name='comand' value='save_s'><div class='form-grid'><input type='text' name='n' placeholder='Nombre' required><input type='text' name='i' placeholder='IP' required><input type='text' name='u' placeholder='Usuario' value='admin' required><input type='password' name='p' placeholder='Password' required><select name='pr'><option value='ssh'>SSH</option><option value='telnet'>Telnet</option></select></div><button type='submit' class='btn btn-success'>💾 Guardar</button></form></div>"
        echo "<div class='card'><h2>Configurados</h2><table><thead><tr><th>Nom</th><th>IP</th><th>Usuario</th><th>Protocolo</th><th>Accions</th></tr></thead><tbody>"
        while IFS=';' read -r n i u p pr; do
            [ -z "$i" ] && continue
            echo "<tr><td>$n</td><td><code>$i</code></td><td>$u</td><td>${pr^^}</td><td><a href='/cgi-bin/switch.cgi?comand=del_s&ip=$i' class='btn btn-error btn-small' onclick='return confirm(\"¿Seguro?\")'>🗑️</a></td></tr>"
        done < <(get_switches)
        echo "</tbody></table></div>"
        print_footer ;;
    save_s)
        /usr/local/JSBach/scripts/switch-scripts.sh configurar afegir_switch "$(get_val n)" "$(get_val i)" "$(get_val u)" "$(get_val p)" "$(get_val pr)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=configurar"
        echo ""
        exit 0 ;;
    del_s)
        /usr/local/JSBach/scripts/switch-scripts.sh configurar eliminar_switch "$(get_val ip)" >/dev/null 2>&1
        echo "Status: 302 Found"
        echo "Location: /cgi-bin/switch.cgi?comand=configurar"
        echo ""
        exit 0 ;;
    *)
        print_header
        echo "<h1>Switches</h1><p>Seleccione una opción.</p>"
        print_footer ;;
esac
