#!/bin/bash

# JSBach Router - Portal Captiu Logic
source /usr/local/JSBach/conf/variables.conf

CONF_PATH="$DIR/$PROJECTE/$DIR_CONF/$PORTAL_CAPTIU_CONF"

fnc_comprovar_interficies() {
    echo "Comprovant interfícies..."
    
    # Comprovar br0.3 (VLAN3)
    if ! ip link show br0.3 &>/dev/null; then
        echo "Creant br0.3..."
        sudo ip link add link br0 name br0.3 type vlan id 3
        sudo ip link set br0.3 up
        sudo ip addr add 10.0.3.1/24 dev br0.3
    fi

    # Comprovar wlp5s0 (WiFi)
    if ! ip addr show wlp5s0 | grep -q "10.0.100.1"; then
        echo "Configurant wlp5s0..."
        sudo ip link set wlp5s0 up
        sudo ip addr flush dev wlp5s0
        sudo ip addr add 10.0.100.1/24 dev wlp5s0
    fi
}

fnc_iniciar() {
    echo "Iniciant Portal Captiu (Bloqueig Estricte)..."
    
    # 1. Comprovar i crear interfícies
    fnc_comprovar_interficies
    
    # 2. Reiniciar regles
    fnc_aturar > /dev/null 2>&1
    
    # === TAULA NAT (Redirecció HTTP) ===
    iptables -t nat -N PORTAL_CAPTIU_HTTP
    iptables -t nat -A PREROUTING -i wlp5s0 -p tcp --dport 80 -j PORTAL_CAPTIU_HTTP
    iptables -t nat -A PREROUTING -i br0.3 -p tcp --dport 80 -j PORTAL_CAPTIU_HTTP
    
    # Bypass per al propi router (pàgina de login)
    iptables -t nat -A PORTAL_CAPTIU_HTTP -d 10.0.100.1 -j RETURN
    iptables -t nat -A PORTAL_CAPTIU_HTTP -d 10.0.3.1 -j RETURN
    
    # Redirigir la resta a la IP del portal
    iptables -t nat -A PORTAL_CAPTIU_HTTP -p tcp --dport 80 -j DNAT --to-destination 10.0.100.1:80

    # === TAULA FILTER (Bloqueig de la resta de trànsit) ===
    iptables -N PORTAL_AUTH
    iptables -I FORWARD -i wlp5s0 -j PORTAL_AUTH
    iptables -I FORWARD -i br0.3 -j PORTAL_AUTH
    
    # Regles per defecte dins de PORTAL_AUTH:
    iptables -A PORTAL_AUTH -p udp --dport 53 -j ACCEPT
    iptables -A PORTAL_AUTH -p tcp --dport 53 -j ACCEPT
    iptables -A PORTAL_AUTH -p udp --dport 67:68 --sport 67:68 -j ACCEPT
    iptables -A PORTAL_AUTH -j DROP
    
    # Update state in config
    if [ -f "$CONF_PATH" ]; then
        USUARI=$(cat "$CONF_PATH" | cut -d';' -f1)
        PASS=$(cat "$CONF_PATH" | cut -d';' -f2)
        echo "$USUARI;$PASS;$ACTIVAT;" > "$CONF_PATH"
    fi
}

fnc_aturar() {
    echo "Aturant Portal Captiu..."
    
    # Neteja NAT
    iptables -t nat -D PREROUTING -i wlp5s0 -p tcp --dport 80 -j PORTAL_CAPTIU_HTTP 2>/dev/null
    iptables -t nat -D PREROUTING -i br0.3 -p tcp --dport 80 -j PORTAL_CAPTIU_HTTP 2>/dev/null
    iptables -t nat -F PORTAL_CAPTIU_HTTP 2>/dev/null
    iptables -t nat -X PORTAL_CAPTIU_HTTP 2>/dev/null
    
    # Neteja FILTER
    iptables -D FORWARD -i wlp5s0 -j PORTAL_AUTH 2>/dev/null
    iptables -D FORWARD -i br0.3 -j PORTAL_AUTH 2>/dev/null
    iptables -F PORTAL_AUTH 2>/dev/null
    iptables -X PORTAL_AUTH 2>/dev/null
    
    # Update state in config
    if [ -f "$CONF_PATH" ]; then
        USUARI=$(cat "$CONF_PATH" | cut -d';' -f1)
        PASS=$(cat "$CONF_PATH" | cut -d';' -f2)
        echo "$USUARI;$PASS;$DESACTIVAT;" > "$CONF_PATH"
    fi
}

fnc_autenticar() {
    IP=$1
    if [ -n "$IP" ]; then
        echo "Autenticant IP: $IP"
        # 1. Bypass al NAT
        if ! iptables -t nat -C PORTAL_CAPTIU_HTTP -s "$IP" -j RETURN 2>/dev/null; then
            iptables -t nat -I PORTAL_CAPTIU_HTTP -s "$IP" -j RETURN
        fi
        # 2. Permetre el trànsit al FORWARD
        if ! iptables -C PORTAL_AUTH -s "$IP" -j ACCEPT 2>/dev/null; then
            iptables -I PORTAL_AUTH -s "$IP" -j ACCEPT
        fi
    fi
}

fnc_configurar() {
    USUARI=$1
    PASS=$2
    if [ -n "$USUARI" ] && [ -n "$PASS" ]; then
        ESTAT=$(cat "$CONF_PATH" | cut -d';' -f3)
        echo "$USUARI;$PASS;$ESTAT;" > "$CONF_PATH"
        echo "Configuració del portal actualitzada."
    fi
}

fnc_estat() {
    if iptables -t nat -L PORTAL_CAPTIU_HTTP -n >/dev/null 2>&1; then
        echo "$ACTIVAT"
    else
        echo "$DESACTIVAT"
    fi
}

case "$1" in
    iniciar) fnc_iniciar ;;
    aturar) fnc_aturar ;;
    autenticar) fnc_autenticar "$2" ;;
    configurar) fnc_configurar "$2" "$3" ;;
    estat) fnc_estat ;;
    *) echo "Usage: $0 {iniciar|aturar|autenticar IP|configurar USER PASS|estat}" ; exit 1 ;;
esac
