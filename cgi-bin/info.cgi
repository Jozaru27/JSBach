#!/bin/bash

# Carregar variables de configuració
source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
echo ""

# Funció per obtenir estat breu (Actiu/Inactiu)
get_status() {
    local modul="$1"
    # Capturar tot l'estat
    local estat=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli "$modul" estat 2>/dev/null)
    
    # Prioritat negativa: si conté paraules clau de parat, és INACTIU
    if echo "$estat" | grep -qiw "DESACTIVAT" || echo "$estat" | grep -qiw "DESCONNECTADA" || echo "$estat" | grep -qiw "ATURAT"; then
        echo "<span class='status-badge badge-inactive'>INACTIU</span>"
    # Si no és parat, busquem si conté paraules clau d'actiu
    elif echo "$estat" | grep -qiw "ACTIVAT" || echo "$estat" | grep -qiw "UP" || echo "$estat" | grep -qiw "ACTIU" || echo "$estat" | grep -qiw "CONNECTADA"; then
        echo "<span class='status-badge badge-active'>ACTIU</span>"
    else
        echo "<span class='status-badge badge-inactive'>INACTIU</span>"
    fi
}

get_wifi_status() {
    local estat=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi estat 2>/dev/null | head -n 1)
    if echo "$estat" | grep -qiw "ACTIVAT" || echo "$estat" | grep -qiw "UP"; then
        echo "<span class='status-badge badge-active'>ACTIU</span>"
    else
        echo "<span class='status-badge badge-inactive'>INACTIU</span>"
    fi
}

get_dhcp_details() {
    local estat=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp estat 2>/dev/null | head -n 1)
    if echo "$estat" | grep -qiw "ACTIVAT" || echo "$estat" | grep -qiw "UP"; then
        local leases=0
        if [ -f "/var/lib/misc/dnsmasq.leases" ]; then
            leases=$(wc -l < /var/lib/misc/dnsmasq.leases)
        fi
        echo "<span class='status-badge badge-active'>ACTIU ($leases lloguers)</span>"
    else
        echo "<span class='status-badge badge-inactive'>INACTIU</span>"
    fi
}

get_switch_status() {
    local sw_conf="/usr/local/JSBach/conf/switches.conf"
    [ ! -f "$sw_conf" ] && echo "<span class='status-badge badge-inactive'>SENSE CONFIGURAR</span>" && return
    
    local total=0
    local ips=()
    while IFS=';' read -r linea; do
        [[ $linea == \#* || -z "$linea" ]] && continue
        local ip=$(echo "$linea" | cut -d ";" -f 2)
        [ -n "$ip" ] && ips+=("$ip") && ((total++))
    done < "$sw_conf"
    
    if [ $total -eq 0 ]; then
        echo "<span class='status-badge badge-inactive'>SENSE CONFIGURAR</span>"
        return
    fi
    
    local active=0
    local pids=()
    local results_file=$(mktemp)
    
    for ip in "${ips[@]}"; do
        (
            if ping -c 1 -W 0.5 "$ip" > /dev/null 2>&1; then
                echo "1" >> "$results_file"
            fi
        ) &
        pids+=($!)
    done
    
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null
    done
    
    active=$(wc -l < "$results_file")
    rm -f "$results_file"
    
    if [ "$active" -gt 0 ]; then
        echo "<span class='status-badge badge-active'>ACTIU $active/$total</span>"
    else
        echo "<span class='status-badge badge-inactive'>INACTIU 0/$total</span>"
    fi
}


cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<style>
body {
  font-family: 'Outfit', 'Segoe UI', Roboto, sans-serif;
  margin: 0;
  padding: 3rem;
  background: radial-gradient(circle at top left, #1e293b 0%, #0f172a 100%);
  color: #f1f5f9;
  min-height: 100vh;
}

.dashboard {
  max-width: 1100px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 3.5rem;
  text-align: center;
}

.main-title {
  font-size: 3rem;
  font-weight: 900;
  margin-bottom: 0.8rem;
  background: linear-gradient(to right, #60a5fa, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}

.subtitle {
  color: #94a3b8;
  font-size: 1.2rem;
  max-width: 600px;
  margin: 0 auto;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 25px;
}

.module-card {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 30px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 18px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.module-card:hover {
  background: rgba(30, 41, 59, 0.6);
  border-color: rgba(96, 165, 250, 0.4);
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.4), 0 0 20px rgba(59, 130, 246, 0.1);
}

.module-card:hover::before { opacity: 1; }

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
}

.module-name {
  font-size: 1.5rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 15px;
  color: #fff;
}

.module-desc {
  color: #cbd5e1;
  font-size: 1rem;
  line-height: 1.6;
  position: relative;
  z-index: 1;
}

.status-badge {
  font-size: 0.8rem;
  font-weight: 800;
  padding: 6px 16px;
  border-radius: 50px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.badge-active {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

.badge-inactive {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

.action-hint {
  margin-top: auto;
  font-size: 0.9rem;
  color: #60a5fa;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
  position: relative;
  z-index: 1;
}

.module-card:hover .action-hint { opacity: 1; }

</style>
<script>
    function gotoModule(menuCgi, bodyCgi, id) {
        if(parent.frames['menu-general'] && parent.frames['menu-general'].loadModule) {
            parent.frames['menu-general'].loadModule(menuCgi, bodyCgi, id);
        } else {
            // Fallback
            parent.frames['menu'].location.href = menuCgi;
            window.location.href = bodyCgi;
        }
    }
</script>
</head>
<body>

<div class="dashboard">
  <div class="header-section">
    <h1 class="main-title">Estat del Sistema</h1>
    <p class="subtitle">Utilitseu els botons del menú superior per a navegar per l'administració.</p>
  </div>

  <div class="module-grid">
    <!-- WAN -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/ifwan-menu.cgi', '/cgi-bin/ifwan.cgi?comand=estat', 'btn-wan')">
      <div class="module-header">
        <div class="module-name">🌐 WAN</div>
        $(get_status "ifwan")
      </div>
      <p class="module-desc">Configuració de la interfície de xarxa externa, DHCP i IP manual.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- ENRUTAR -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/enrutar-menu.cgi', '/cgi-bin/enrutar.cgi?comand=estat', 'btn-enrutar')">
      <div class="module-header">
        <div class="module-name">🔀 Enrutar</div>
        $(get_status "enrutar")
      </div>
      <p class="module-desc">Gestió del forwarding d'IP, rutes estàtiques i taules d'enrutament.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- BRIDGE -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/bridge-menu.cgi', '/cgi-bin/bridge.cgi?comand=estat', 'btn-bridge')">
      <div class="module-header">
        <div class="module-name">Bridge</div>
        $(get_status "bridge")
      </div>
      <p class="module-desc">Administració de VLANs, ponts de xarxa i aïllament de ports.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- TALLAFOCS -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/tallafocs-menu.cgi', '/cgi-bin/tallafocs-configuracio.cgi', 'btn-tallafocs')">
      <div class="module-header">
        <div class="module-name">🛡️ Tallafocs</div>
        $(get_status "tallafocs")
      </div>
      <p class="module-desc">Regles del tallafocs, protecció de xarxa i gestió de tràfic.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- DMZ -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/dmz-menu.cgi', '/cgi-bin/dmz-configurar.cgi', 'btn-dmz')">
      <div class="module-header">
        <div class="module-name">🔓 DMZ</div>
        $(get_status "dmz")
      </div>
      <p class="module-desc">Configuració de zones desmilitaritzades i obertura de ports a servidors.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- Switches -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/switch-menu.cgi', '/cgi-bin/switch.cgi?comand=estat', 'btn-switch')">
      <div class="module-header">
        <div class="module-name">🔌 Switch</div>
        $(get_switch_status)
      </div>
      <p class="module-desc">Gestió de commutadors, puncis d'accés, polítiques de MAC i VLANs.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- WiFi -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/wifi-menu.cgi', '/cgi-bin/wifi.cgi?comand=estat', 'btn-wifi')">
      <div class="module-header">
        <div class="module-name">📡 WiFi</div>
        $(get_wifi_status)
      </div>
      <p class="module-desc">Configuració del Punt d'Accés per a xarxes sense fils.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>

    <!-- DHCP -->
    <div class="module-card" onclick="gotoModule('/cgi-bin/dhcp-menu.cgi', '/cgi-bin/dhcp.cgi?comand=estat', 'btn-dhcp')">
      <div class="module-header">
        <div class="module-name">🔌 DHCP</div>
        $(get_dhcp_details)
      </div>
      <p class="module-desc">Gestió d'assignació d'IPs dinàmiques i rangs de xarxa.</p>
      <div class="action-hint">Gestionar mòdul ➜</div>
    </div>
  </div>
</div>



</body>
</html>
EOF
