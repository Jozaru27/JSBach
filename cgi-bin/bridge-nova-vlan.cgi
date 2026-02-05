#!/bin/bash

# JSBach Router Administration - Create New VLAN
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Crear VLAN - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-top: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 25px;
  margin: 20px 0;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

table {
  border-collapse: separate;
  border-spacing: 0;
  margin-bottom: 25px;
  width: 100%;
}

td, th {
  padding: 12px 16px;
  text-align: left;
}

th {
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
}

input[type=text] {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 10px 14px;
    border-radius: 8px;
    width: 100%;
    font-family: inherit;
    box-sizing: border-box;
    transition: all 0.2s;
}

input[type=text]:focus {
    outline: none;
    border-color: #3b82f6;
    background: rgba(15, 23, 42, 0.8);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(to right, #2563eb, #3b82f6);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-decoration: none;
  display: inline-block;
}

.btn:hover {
  background: linear-gradient(to right, #1d4ed8, #2563eb);
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
}

.btn-secondary {
    background: rgba(255,255,255,0.05);
    color: #cbd5e1;
    border: 1px solid rgba(255,255,255,0.1);
}

.btn-secondary:hover {
    background: rgba(255,255,255,0.1);
    color: #fff;
    box-shadow: none;
}
  </style>
</head>
<body>
<div class="container">
  <h1>✨ Crear Nova VLAN</h1>
  
  <div class="card">
    <form action='/cgi-bin/bridge-guardar.cgi' method='get'>
      <input type='hidden' name='accio' value='nova'>
      <table>
        <thead>
          <tr>
            <th>Nom</th>
            <th>VID</th>
            <th>IP/Subxarxa</th>
            <th>Gateway</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><input type='text' name='nom' placeholder='Ex: Xarxa Convidats' required pattern='^[a-zA-Z0-9 ]+$' title='Nom de VLAN (lletres i números)'></td>
            <td><input type='text' name='vid' placeholder='Ex: 50' style='width: 80px;' required pattern='^([1-9][0-9]{0,2}|[1-3][0-9]{3}|40[0-8][0-9]|409[0-4])$' title='VLAN ID (1-4094)'></td>
            <td><input type='text' name='ipmasc' placeholder='10.0.50.1/24' required pattern='^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/([0-9]|[12][0-9]|3[0-2])$' title='Format de subxarxa no vàlid (Ex: 10.0.50.1/24)'></td>
            <td><input type='text' name='ippe' placeholder='10.0.50.1' required pattern='^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$' title='Format d\u0027IP no vàlid'></td>
          </tr>
        </tbody>
      </table>
      
      <div style="display: flex; gap: 15px; margin-top: 20px;">
        <a href="/cgi-bin/bridge-configurar.cgi" class="btn btn-secondary">Cancel·lar</a>
        <button type='submit' class='btn'>Crear VLAN</button>
      </div>
    </form>
  </div>
</div>
</body>
</html>
EOF
