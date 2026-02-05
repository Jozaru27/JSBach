#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Executar comanda
OUTPUT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan $comand)

# Obtenir estat actual
ESTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat)

# Determinar títol i icona
case "$comand" in
    iniciar)
        TITLE="Iniciar WAN"
        ICON="🚀"
        ;;
    aturar)
        TITLE="Aturar WAN"
        ICON="🛑"
        ;;
    estat)
        TITLE="Estat de la WAN"
        ICON="📊"
        ;;
    *)
        TITLE="WAN"
        ICON="🌐"
        ;;
esac

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

.container { max-width: 900px; margin: 0 auto; }

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 15px;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  margin-bottom: 30px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #60a5fa;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.terminal-output {
  background: #020617;
  color: #cbd5e1;
  padding: 24px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-wrap;
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
}

.status-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
}
.badge-blue { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.badge-green { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.container { animation: fadeIn 0.4s ease-out; }

table { width: 100%; border-collapse: collapse; }
td { padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
tr:last-child td { border-bottom: none; }
.label { color: #94a3b8; width: 40%; font-weight: 600; }
.value { color: #fff; font-family: monospace; }
</style>
</head>
<body>
  <div class="container">
    <h1><span style="font-size: 1.8rem;">$ICON</span> $TITLE</h1>

EOF

# Resultat de l'operació (si no és només estat)
if [[ "$comand" != "estat" ]]; then
    cat << EOF
    <div class="card">
      <div class="card-title">Resultat de l'operació</div>
      <div class="terminal-output">
$OUTPUT
      </div>
    </div>
EOF
fi

# Estat Actual
cat << EOF
    <div class="card">
      <div class="card-title">Estat Actual del Sistema</div>
      <div class="terminal-output">
$ESTAT
      </div>
    </div>
EOF

# Configuració detallada si és estat
if [ "$comand" == "estat" ]; then
    CONFIGURACIO=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan configurar mostrar)
    conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f1)
    conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f2)

    cat << EOF
    <div class="card">
      <div class="card-title">Configuració de la interfície</div>
      <table>
        <tr>
          <td class="label">Mode de connexió</td>
          <td>
EOF
    if [ "$conf_mode" == "dhcp" ]; then
        echo "<span class='status-badge badge-blue'>DHCP</span>"
    else
        echo "<span class='status-badge badge-green'>ESTÀTICA (MANUAL)</span>"
    fi
    echo "</td></tr>"
    echo "<tr><td class='label'>Interfície física</td><td class='value'>$conf_int</td></tr>"

    if [ "$conf_mode" == "manual" ]; then
        conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f3)
        conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f4)
        conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f5)
        conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6)
        cat << EOF
        <tr><td class='label'>Adreça IP</td><td class='value'>$conf_ip</td></tr>
        <tr><td class='label'>Màscara</td><td class='value'>$conf_masc</td></tr>
        <tr><td class='label'>Porta d'enllaç</td><td class='value'>$conf_pe</td></tr>
        <tr><td class='label'>DNS mestre</td><td class='value'>$conf_dns</td></tr>
EOF
    fi

    echo "</table>"
    echo "</div>"
fi

cat << EOF
  </div>
</body>
</html>
EOF
