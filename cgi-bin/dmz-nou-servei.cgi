#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Obrir Nou Servei DMZ - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { max-width: 700px; margin: 0 auto; }

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
  padding: 35px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

input[type="text"], select {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 12px 16px;
  color: #fff;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
  transition: all 0.2s;
}

input[type="text"]:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.actions {
  display: flex;
  gap: 15px;
  margin-top: 35px;
}

.btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #1d4ed8, #2563eb);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.tip {
  margin-top: 25px;
  background: rgba(59, 130, 246, 0.05);
  padding: 15px;
  border-radius: 10px;
  border-left: 3px solid #3b82f6;
  font-size: 0.9rem;
  color: #94a3b8;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.card { animation: slideUp 0.4s ease-out; }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔓 Obrir Nou Servei DMZ</h1>
    
    <div class="card">
      <form action="/cgi-bin/dmz-agregar.cgi" method="get">
        
        <div class="grid">
          <div class="form-group">
            <label>Port</label>
            <input type="text" name="port" placeholder="Ex: 80, 443, 22" required pattern="^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$" title="Vistiplau un port vàlid (1-65535)">
          </div>
          
          <div class="form-group">
            <label>Protocol</label>
            <select name="proto">
              <option value="tcp">TCP</option>
              <option value="udp">UDP</option>
              <option value="all">TOTS (ALL)</option>
            </select>
          </div>
        </div>
        
        <div class="form-group">
          <label>IP del Servidor Intern</label>
          <input type="text" name="ipdmz" placeholder="Ex: 192.168.1.100" required pattern="^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" title="Format d'IP no vàlid (0-255 en cada octet)">
        </div>
        
        <div class="tip">
          <strong>ℹ️ Informació:</strong> Aquesta acció redirigirà el tràfic extern del port seleccionat cap al servidor especificat en la zona DMZ.
        </div>
        
        <div class="actions">
          <a href="/cgi-bin/dmz-configurar.cgi" class="btn btn-secondary">Cancel·lar</a>
          <button type="submit" class="btn btn-primary">🚀 Obrir Servei</button>
        </div>
        
      </form>
    </div>
  </div>
</body>
</html>
EOF
