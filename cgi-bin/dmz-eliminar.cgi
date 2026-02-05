#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

echo "Content-type: text/html; charset=utf-8"
echo ""

# Extract parameters
PORT=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
PROTO=$(echo "$QUERY_STRING" | sed -n 's/^.*proto=\([^&]*\).*$/\1/p')
IP_DMZ=$(echo "$QUERY_STRING" | sed -n 's/^.*ipdmz=\([^&]*\).*$/\1/p')

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="3;url=/cgi-bin/dmz-configurar.cgi">
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
  border-radius: 20px;
  padding: 45px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  text-align: center;
  backdrop-filter: blur(15px);
  animation: slideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.icon-box {
  font-size: 4rem;
  margin-bottom: 25px;
  background: rgba(239, 68, 68, 0.1);
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-left: auto;
  margin-right: auto;
  border: 2px solid rgba(239, 68, 68, 0.2);
}

h2 {
  margin: 0 0 15px 0;
  color: #fff;
  font-size: 1.8rem;
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
  border-top-color: #ef4444;
  border-radius: 50%;
  display: inline-block;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes slideIn {
  from { opacity: 0; transform: translateY(30px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.btn {
  background: linear-gradient(135deg, #374151, #1f2937);
  color: white;
  padding: 12px 28px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 700;
  display: inline-block;
  transition: all 0.2s;
  border: 1px solid rgba(255,255,255,0.1);
}

.btn:hover { background: #111827; transform: translateY(-2px); border-color: #ef4444; }
</style>
</head>
<body>
  <div class="card">
    <div class="icon-box">🗑️</div>
    <h2>Servei Eliminat</h2>
    <div class="message">
      El servei al port <strong style="color:#fca5a5;">$PORT</strong> ($PROTO) ha estat eliminat correctament de la configuració DMZ.
    </div>
    <div class="loader"></div>
    <p style="font-size: 0.9rem; color: #64748b;">Redirigint a la llista en 3 segons...</p>
    <br>
    <a href="/cgi-bin/dmz-configurar.cgi" class="btn">Tornar ara</a>
  </div>
EOF

# Execute the action in background
$RUTA dmz configurar eliminar $PORT $PROTO $IP_DMZ > /dev/null 2>&1

cat << EOF
</body>
</html>
EOF
