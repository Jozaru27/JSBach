#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Executar comanda
OUTPUT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli enrutar $comand)

# Obtenir estat actual
ESTAT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli enrutar estat)

# Determinar títol i icona
case "$comand" in
    iniciar)
        TITLE="Iniciar Enrutament"
        ICON="🚀"
        ;;
    aturar)
        TITLE="Aturar Enrutament"
        ICON="🛑"
        ;;
    estat)
        TITLE="Estat de l'Encaminament"
        ICON="📊"
        ;;
    *)
        TITLE="Enrutar"
        ICON="🔀"
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.container { animation: fadeIn 0.4s ease-out; }
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
      <div class="card-title">Sistema d'Encaminament</div>
      <div class="terminal-output">
$ESTAT
      </div>
    </div>
EOF

cat << EOF
  </div>
</body>
</html>
EOF
