#!/bin/bash

# =====================================================================
# JSBach Router - Programa d'Instal·lació Professional
# =====================================================================

# 1. Comprovació de privilegis (Root)
if [[ $EUID -ne 0 ]]; then
   echo "⚠️ Aquest script s'ha d'executar com a root (sudo)."
   exit 1
fi

echo "🚀 Iniciant la instal·lació de JSBach..."

# 2. Definició de rutes del projecte
PROJECT_DIR="/usr/local/JSBach"
SYSTEM_DIR="/etc/systemd/system"

# 3. Actualització i instal·lació de dependències
echo "📦 Instal·lant dependències del sistema..."
apt update
apt install -y apache2 curl net-tools expect iw ebtables iptables bridge-utils ncat sed grep dnsmasq hostapd

# 4. Configuració d'Apache (CGI)
echo "🌐 Configurant el servidor web Apache..."
a2enmod cgi
systemctl restart apache2

# 5. Desactivació de NetworkManager
echo "🔌 Desactivant NetworkManager per a configuració de xarxa manual..."
systemctl stop NetworkManager
systemctl disable NetworkManager
systemctl mask NetworkManager

# 6. Activació de l'IP Forwarding (Permanent)
echo "🛣️ Activant el reenviament de paquets IP (IPv4 Forwarding)..."
sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf
sysctl -p

# 7. Creació i instal·lació del servei srv_cli
echo "⚙️ Instal·lant el servei de sistema JSBach (srv_cli)..."
cat << EOF > "$SYSTEM_DIR/srv_cli.service"
[Unit]
Description=Serviço JSBach srv_cli
After=network-pre.target

[Service]
Type=simple
ExecStart=/usr/bin/bash $PROJECT_DIR/system/srv_cli
WorkingDirectory=$PROJECT_DIR/system/
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable srv_cli.service
systemctl start srv_cli.service

# 8. Configuració de DNSMasq
echo "🌐 Configurant DNSMasq..."
cat << EOF > /etc/dnsmasq.conf
########################################
# INTERFACES
########################################

interface=br0.1
interface=br0.2
interface=br0.3
interface=br0.4
interface=wlp5s0
bind-interfaces

########################################
# DNS (usando systemd-resolved)
########################################

no-resolv
server=127.0.0.53

local-service
expand-hosts

########################################
# DHCP - RED 10.0.1.0/24
########################################

dhcp-range=interface:br0.1,10.0.1.100,10.0.1.200,255.255.255.0,12h
dhcp-option=interface:br0.1,3,10.0.1.1
dhcp-option=interface:br0.1,6,10.0.1.1

########################################
# DHCP - RED 10.0.2.0/24
########################################

dhcp-range=interface:br0.2,10.0.2.100,10.0.2.200,255.255.255.0,12h
dhcp-option=interface:br0.2,3,10.0.2.1
dhcp-option=interface:br0.2,6,10.0.2.1

########################################
# DHCP - RED 10.0.3.0/24
########################################

dhcp-range=interface:br0.3,10.0.3.100,10.0.3.200,255.255.255.0,12h
dhcp-option=interface:br0.3,3,10.0.3.1
dhcp-option=interface:br0.3,6,10.0.3.1

########################################
# DHCP - RED 10.0.4.0/24
########################################

dhcp-range=interface:br0.4,10.0.4.100,10.0.4.200,255.255.255.0,12h
dhcp-option=interface:br0.4,3,10.0.4.1
dhcp-option=interface:br0.4,6,10.0.4.1

########################################
# WIFI
########################################

dhcp-range=interface:wlp5s0,10.0.100.100,10.0.100.200,255.255.255.0,12h
dhcp-option=interface:wlp5s0,3,10.0.100.1
dhcp-option=interface:wlp5s0,6,10.0.100.1

########################################
# OPCIONES GENERALES
########################################

log-dhcp
log-queries
EOF

systemctl enable dnsmasq
systemctl restart dnsmasq

# 9. Configuració de Hostapd
echo "📶 Configurant Hostapd..."
mkdir -p /etc/hostapd
cat << EOF > /etc/hostapd/hostapd.conf
########################################
# Interfície WiFi
########################################

interface=wlp5s0
driver=nl80211

########################################
# Configuració bàsica
########################################

ssid=JPeligroso
hw_mode=g
channel=1

########################################
# Control d’accés
########################################

auth_algs=1
wmm_enabled=1
ignore_broadcast_ssid=0

########################################
# WPA2
########################################

wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=admin123

country_code=ES
ieee80211d=1

#bridge = br0
EOF

# Configurar el fitxer per defecte de hostapd per apuntar al nou conf
sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

systemctl unmask hostapd
systemctl enable hostapd
systemctl restart hostapd

# 10. Configuració de permisos massiva
echo "🔑 Configurant permisos i propietats del projecte..."
chown -R www-data:www-data "$PROJECT_DIR"
# Permisos d'execució totals per a scripts i CGIs
chmod -R 777 "$PROJECT_DIR/cgi-bin"
chmod -R 777 "$PROJECT_DIR/scripts"
chmod -R 777 "$PROJECT_DIR/system"

# 11. Neteja de fitxers antics (si existeixen)
echo "🧹 Netejant brossa d'instal·lacions anteriors..."
rm -f "$PROJECT_DIR/install/install"
rm -f "$PROJECT_DIR/install/servicio_automatico"

echo "✅ Instal·lació completada amb èxit!"
echo "👉 Ja pots accedir a la consola d'administració a: http://127.0.0.1"
echo "👉 Recomanem reiniciar el sistema per aplicar tots els canvis de xarxa."
