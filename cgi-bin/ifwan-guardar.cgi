#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<html>
<head>
  <meta http-equiv="refresh" content="3;url=/cgi-bin/ifwan.cgi?comand=estat">
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 40px 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  text-align: center;
  backdrop-filter: blur(10px);
  animation: slideIn 0.4s ease-out;
}

.icon-success {
  font-size: 4rem;
  margin-bottom: 20px;
  color: #4ade80;
}

h2 {
  margin: 0 0 15px 0;
  color: #fff;
}

.message {
  color: #94a3b8;
  margin-bottom: 30px;
  line-height: 1.6;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  display: inline-block;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn {
  background: #3b82f6;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  display: inline-block;
  transition: all 0.2s;
}

.btn:hover { background: #2563eb; transform: translateY(-2px); }
</style>
</head>
<body>
  <div class="card">
    <div class="icon-success">✅</div>
    <h2>Configuració WAN Desada</h2>
    <div class="message">
      La configuració de la interfície WAN s'ha actualitzat correctament. Recordeu que pot ser necessari reiniciar la interfície per aplicar els canvis.
    </div>
    <div class="loader"></div>
    <p style="font-size: 0.9rem; color: #64748b;">Redirigint en 3 segons...</p>
    <br>
    <a href="/cgi-bin/ifwan.cgi?comand=estat" class="btn">Tornar ara</a>
  </div>
EOF

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

# Extreiem els valors i executem
mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

# Decode base parameters
mode=$(urldecode "$mode")
int=$(urldecode "$int")

if [[ "$mode" == "manual" ]]; then
	ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
	masc=$(echo "$QUERY_STRING" | sed -n 's/^.*masc=\([^&]*\).*$/\1/p')
	pe=$(echo "$QUERY_STRING" | sed -n 's/^.*pe=\([^&]*\).*$/\1/p')
	dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
    
    # Decode manual parameters
    ip=$(urldecode "$ip")
    masc=$(urldecode "$masc")
    pe=$(urldecode "$pe")
    dns=$(urldecode "$dns")
    
    ipmas=$ip/$masc
fi

$RUTA ifwan configurar $mode $int $ipmas $pe $dns > /dev/null 2>&1

cat << EOF
</body>
</html>
EOF
