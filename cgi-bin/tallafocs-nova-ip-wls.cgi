#!/bin/bash

# JSBach Router Administration - Add Unrestricted IP Form (Catalan Premium)
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Afegir IP sese Restricció - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
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
  padding: 40px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(15px);
  animation: slideIn 0.4s ease-out;
}

h2 {
  margin: 0 0 25px 0;
  color: #fff;
  font-size: 1.6rem;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 15px;
}

.form-group { margin-bottom: 20px; }

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #94a3b8;
  font-size: 0.9rem;
}

select, input[type="text"] {
  width: 100%;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  color: #fff;
  font-size: 1rem;
  box-sizing: border-box;
  transition: all 0.2s;
}

select:focus, input:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(0, 0, 0, 0.5);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.btn-row {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  text-decoration: none;
}

.btn-save {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: white;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
}

.btn-save:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); }

.btn-cancel {
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-cancel:hover { background: rgba(255, 255, 255, 0.1); color: #fff; }

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
</head>
<body>
  <div class="card">
    <h2>➕ Nova IP sese Restricció</h2>
    <form action="/cgi-bin/tallafocs-ips-wls.cgi" method="GET">
      <input type="hidden" name="accio" value="afegir_ip_wls">
      
      <div class="form-group">
        <label for="vid">Selecciona VLAN</label>
        <select name="vid" id="vid">
EOF

# Llistar VLANs del fitxer de configuració
grep -v '^#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" | while IFS=';' read -r NOM VID RESTO; do
    if [ ! -z "$VID" ]; then
        echo "<option value='$VID'>$NOM (VLAN $VID)</option>"
    fi
done

cat << EOF
        </select>
      </div>

      <div class="form-group">
        <label for="ip">Adreça IP</label>
        <input type="text" name="ip" id="ip" placeholder="Ex: 10.0.1.50" required pattern="^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" title="Format d'IP no vàlid (0-255 en cada octet)">
      </div>

      <div class="form-group">
        <label for="mac">Adreça MAC</label>
        <input type="text" name="mac" id="mac" placeholder="Ex: AA:BB:CC:11:22:33" required pattern="^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$" title="Format de MAC no vàlid (XX:XX:XX:XX:XX:XX)">
      </div>

      <div class="btn-row">
        <a href="/cgi-bin/tallafocs-configuracio.cgi" class="btn btn-cancel">Cancel·lar</a>
        <button type="submit" class="btn btn-save">Desar IP</button>
      </div>
    </form>
  </div>
</body>
</html>
EOF
