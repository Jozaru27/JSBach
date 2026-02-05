#!/bin/bash

# JSBach Router Administration - Modify Tag/Untag Configuration
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Extract parameters
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

# Fetch current data
VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
[ -z "$VLAN_UNTAG" ] && VLAN_UNTAG=0
VLAN_TAG=$(echo "$linia_int" | cut -d';' -f3)
[ -z "$VLAN_TAG" ] && VLAN_TAG=0

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>Modificar Tag-Untag - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 40px 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container {
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 20px 25px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  font-weight: 600;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 15px;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  animation: fadeIn 0.4s ease-out;
}

.form-group {
  margin-bottom: 20px;
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

input[type="text"] {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
  transition: all 0.2s;
}

input[type="text"]:focus {
  outline: none;
  border-color: #3b82f6;
  background: rgba(15, 23, 42, 0.8);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

input[readonly] {
  background: rgba(255, 255, 255, 0.03);
  color: #64748b;
  cursor: not-allowed;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(to right, #2563eb, #3b82f6);
  color: white;
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(to right, #1d4ed8, #2563eb);
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.tip {
  margin-top: 20px;
  font-size: 0.85rem;
  color: #64748b;
  display: flex;
  gap: 10px;
  background: rgba(59, 130, 246, 0.05);
  padding: 12px;
  border-radius: 8px;
}
  </style>
</head>
<body>
  <div class="container">
    <h1><span style="font-size: 1.2em;">⚙️</span> Modificar VLAN Tag-Untag</h1>
    
    <div class="card">
      <form action="/cgi-bin/bridge-guardar-taguntag.cgi" method="get">
        
        <div class="form-group">
          <label>Interfície</label>
          <input type="text" name="int" value="$int" readonly>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
          <div class="form-group">
            <label>VLAN Untagged (PVID)</label>
            <input type="text" name="untag" value="$VLAN_UNTAG" placeholder="Ex: 10">
          </div>
          
          <div class="form-group">
            <label>VLANs Tagged</label>
            <input type="text" name="tag" value="$VLAN_TAG" placeholder="Ex: 20,30,40">
          </div>
        </div>
        
        <div class="tip">
          <span style="font-size: 1.2em;">ℹ️</span>
          <div>
            Especifiqueu la VLAN <strong>Untagged</strong> (principal) i les VLANs <strong>Tagged</strong> separades per comes.
          </div>
        </div>
        
        <div class="actions">
          <a href="/cgi-bin/bridge-configurar-taguntag.cgi" class="btn btn-secondary">Cancel·lar</a>
          <button type="submit" class="btn btn-primary">Desar Canvis</button>
        </div>
        
      </form>
    </div>
  </div>
</body>
</html>
EOF
