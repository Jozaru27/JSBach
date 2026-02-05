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
apt install -y apache2 curl net-tools expect iw ebtables iptables bridge-utils ncat sed grep

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

# 8. Configuració de permisos massiva
echo "🔑 Configurant permisos i propietats del projecte..."
chown -R www-data:www-data "$PROJECT_DIR"
# Permisos d'execució totals per a scripts i CGIs
chmod -R 777 "$PROJECT_DIR/cgi-bin"
chmod -R 777 "$PROJECT_DIR/scripts"
chmod -R 777 "$PROJECT_DIR/system"

# 9. Neteja de fitxers antics (si existeixen)
echo "🧹 Netejant brossa d'instal·lacions anteriors..."
rm -f "$PROJECT_DIR/install/install"
rm -f "$PROJECT_DIR/install/servicio_automatico"

echo "✅ Instal·lació completada amb èxit!"
echo "👉 Ja pots accedir a la consola d'administració a: http://127.0.0.1"
echo "👉 Recomanem reiniciar el sistema per aplicar tots els canvis de xarxa."
