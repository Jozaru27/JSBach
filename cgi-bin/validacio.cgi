#!/bin/bash

# JSBach Router Administration - Captive Portal Validation
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html"
echo ""

# Get credentials from config file
CONF_PATH="$DIR/$PROJECTE/$DIR_CONF/$PORTAL_CAPTIU_CONF"
VALID_USER=$(cat "$CONF_PATH" | cut -d';' -f1)
VALID_PASS=$(cat "$CONF_PATH" | cut -d';' -f2)

# Read POST data
if [ "$REQUEST_METHOD" = "POST" ]; then
    read -n $CONTENT_LENGTH query
    usuario=$(echo "$query" | sed -n 's/^.*usuario=\([^&]*\).*$/\1/p' | sed 's/+/ /g;s/%\(..\)/\\x\1/g;s/\\x/\\\\\x/g' | xargs -0 printf '%b')
    contrasena=$(echo "$query" | sed -n 's/^.*contrasena=\([^&]*\).*$/\1/p' | sed 's/+/ /g;s/%\(..\)/\\x\1/g;s/\\x/\\\\\x/g' | xargs -0 printf '%b')
fi

# Validation logic
if [ "$usuario" = "$VALID_USER" ] && [ "$contrasena" = "$VALID_PASS" ]; then
    # SUCCESS: Authenticate the IP
    # We use sudo because iptables requires it, and we assumed earlier the user will configure sudoers
    sudo /usr/local/JSBach/scripts/portal_captiu.sh autenticar "$REMOTE_ADDR"
    
    cat <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>JSBach | Acceso Concedido</title>
    <style>
        body {
            background: #0f2027;
            color: white;
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }
        .message {
            background: rgba(255,255,255,0.1);
            padding: 40px; border-radius: 20px;
            backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);
        }
        h1 { color: #2ecc71; }
        .spinner {
            border: 4px solid rgba(255,255,255,0.3); border-top: 4px solid #2ecc71;
            border-radius: 50%; width: 30px; height: 30px;
            animation: spin 1s linear infinite; margin: 20px auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    <meta http-equiv="refresh" content="3;url=http://www.google.com">
</head>
<body>
    <div class="message">
        <h1>Acceso Concedido</h1>
        <p>Tu IP ($REMOTE_ADDR) ha sido validada correctamente.</p>
        <p>Redirigiendo a internet...</p>
        <div class="spinner"></div>
    </div>
</body>
</html>
EOF
else
    # FAILURE: Redirect back to login
    cat <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>JSBach | Error de Acceso</title>
    <style>
        body {
            background: #0f2027; color: white;
            font-family: sans-serif; display: flex;
            justify-content: center; align-items: center;
            height: 100vh; margin: 0; text-align: center;
        }
        .message {
            background: rgba(255,255,255,0.1); padding: 40px;
            border-radius: 20px; backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        h1 { color: #e74c3c; }
    </style>
    <meta http-equiv="refresh" content="3;url=/validacio.html">
</head>
<body>
    <div class="message">
        <h1>Error de Autenticación</h1>
        <p>Usuario o contraseña incorrectos.</p>
        <p>Redirigiendo al login...</p>
    </div>
</body>
</html>
EOF
fi
