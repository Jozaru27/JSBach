#!/bin/bash

# ======================================================================
# JSBach - Script de Gestió de Switches
# ======================================================================

source /usr/local/JSBach/conf/variables.conf

# Valores por defecto
[ -z "$DIR" ] && DIR=/usr/local
[ -z "$PROJECTE" ] && PROJECTE=JSBach
[ -z "$DIR_CONF" ] && DIR_CONF=conf
[ -z "$CONF_SWITCHES" ] && CONF_SWITCHES=switches.conf
[ -z "$MACS_SWITCHES_CONF" ] && MACS_SWITCHES_CONF=mac_switches.conf

SW_CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$CONF_SWITCHES"
MAC_CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$MACS_SWITCHES_CONF"

# Asegurar archivos existen
[ ! -f "$SW_CONF_FILE" ] && touch "$SW_CONF_FILE" && chmod 666 "$SW_CONF_FILE"
[ ! -f "$MAC_CONF_FILE" ] && touch "$MAC_CONF_FILE" && chmod 666 "$MAC_CONF_FILE"

######################################################################
###  Funcions Auxiliars
######################################################################

mostrar_tabla_macs() {
    local IP="$1" USER="$2" PASS="$3" PROTO="$4"
    # Lógica de SSH vs Telnet
    if [ "$PROTO" == "telnet" ]; then
        # Telnet implementation simplified (expect needs adjustment for telnet)
        /usr/bin/expect <<EOF
            set timeout 10
            spawn telnet $IP
            expect "Username:" { send "$USER\r" }
            expect "Password:" { send "$PASS\r" }
            expect ">" { send "en\r" }
            expect "Password:" { send "$PASS\r" }
            expect "#" { send "show mac address-table\r" }
            expect "#" { send "exit\r" }
EOF
    else
        /usr/bin/expect <<EOF | awk '/MAC[[:space:]]+VLAN[[:space:]]+Port/ {show=1} /Address[[:space:]]+Vlan[[:space:]]+Type/ {show=1} show /Total MAC Addresses/ {exit}'
            set timeout 10
            log_user 0
            spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
            expect {
                "yes/no" { send "yes\r"; exp_continue }
                "[Pp]assword:" { send "$PASS\r" }
                timeout { exit 1 }
            }
            expect {
                ">" { send "en\r"; exp_continue }
                "[Pp]assword:" { send "$PASS\r"; exp_continue }
                "#" {}
            }
            expect "#"
            send "show mac address-table\r"
            expect "#"
            puts \$expect_out(buffer)
            send "exit\r"
            expect eof
EOF
    fi
}

eliminar_acls() {
    local IP="$1" USER="$2" PASS="$3"
    local INTF="gigabitEthernet 1/0/1-10"
    expect <<EOF
        set timeout 15
        spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect { "yes/no" { send "yes\r"; exp_continue } "[Pp]assword:" { send "$PASS\r" } }
        expect { ">" { send "en\r"; exp_continue } "[Pp]assword:" { send "$PASS\r"; exp_continue } "#" {} }
        expect "#"
        send "conf\r"
        expect "(config)#"
        send "no access-list bind 1 interface $INTF\r"
        expect "(config)#"
        send "no access-list create 1\r"
        expect "(config)#"
        send "exit\r"
        expect "#"
        send "exit\r"
        expect eof
EOF
}

crear_acls() {
    local IP="$1" USER="$2" PASS="$3"
    local INTF="gigabitEthernet 1/0/1-10"
    local MAC_LIST=$(grep -v "^#" "$MAC_CONF_FILE" | grep -v "^$" | tr '\n' ' ')
    expect <<EOF
        set timeout 20
        spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect { "yes/no" { send "yes\r"; exp_continue } "[Pp]assword:" { send "$PASS\r" } }
        expect { ">" { send "en\r"; exp_continue } "[Pp]assword:" { send "$PASS\r"; exp_continue } "#" {} }
        expect "#"
        send "conf\r"
        expect "(config)#"
        send "access-list create 1 name \"BLOQUEAR_MAC\"\r"
        expect "(config)#"
        set i 1
        foreach mac [list $MAC_LIST] {
            send "access-list mac 1 rule \$i deny logging disable smac \$mac smask ff:ff:ff:ff:ff:ff\r"
            expect "(config)#"
            incr i
        }
        send "access-list mac 1 rule \$i permit logging disable\r"
        expect "(config)#"
        send "access-list bind 1 interface $INTF\r"
        expect "(config)#"
        send "exit\r"
        expect "#"
        send "exit\r"
        expect eof
EOF
}

######################################################################
###  Configuració
######################################################################

fnc_configurar() {	
	local CMD=$1
	shift
	case "$CMD" in
		afegir_switch)
			local nom=$1 ip=$2 usr=$3 pwd=$4 proto=$5
            grep -v ";$ip;" "$SW_CONF_FILE" > "${SW_CONF_FILE}.tmp"
            echo "$nom;$ip;$usr;$pwd;$proto;" >> "${SW_CONF_FILE}.tmp"
            mv "${SW_CONF_FILE}.tmp" "$SW_CONF_FILE"
            chmod 666 "$SW_CONF_FILE"
			;;
		eliminar_switch)
			local ip=$1
            grep -v ";$ip;" "$SW_CONF_FILE" > "${SW_CONF_FILE}.tmp"
            mv "${SW_CONF_FILE}.tmp" "$SW_CONF_FILE"
            chmod 666 "$SW_CONF_FILE"
			;;
        afegir_mac)
            local mac=$1
            if ! grep -qix "^$mac$" "$MAC_CONF_FILE"; then
                echo "$mac" >> "$MAC_CONF_FILE"
            fi
            ;;
        eliminar_mac)
            local mac=$1
            grep -v "^$mac$" "$MAC_CONF_FILE" > "${MAC_CONF_FILE}.tmp"
            mv "${MAC_CONF_FILE}.tmp" "$MAC_CONF_FILE"
            chmod 666 "$MAC_CONF_FILE"
            ;;
        mostrar_tabla_macs)
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                local pr=$(echo $linea | cut -d ";" -f 5)
                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    echo "=================================================="
                    echo "SWITCH: $n ($i)"
                    echo "=================================================="
                    mostrar_tabla_macs "$i" "$u" "$p" "$pr"
                    echo ""
                fi
            done < "$SW_CONF_FILE"
            ;;
        crear_acls)
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    echo "Creant ACLs al switch $n ($i)..."
                    crear_acls "$i" "$u" "$p"
                fi
            done < "$SW_CONF_FILE"
            ;;
        eliminar_acls)
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    echo "Eliminant ACLs del switch $n ($i)..."
                    eliminar_acls "$i" "$u" "$p"
                fi
            done < "$SW_CONF_FILE"
            ;;
	esac
}

fnc_estat() {
	while IFS=';' read -r linea; do
        [[ $linea == \#* || -z "$linea" ]] && continue
		local nom=$(echo $linea | cut -d ";" -f 1)
		local ip=$(echo $linea | cut -d ";" -f 2)
		ping -c 1 -w 1 "$ip" > /dev/null 2>&1 && echo "$nom;$ip;Activo" || echo "$nom;$ip;No Encontrado"
	done < "$SW_CONF_FILE"
}

case "$1" in
  configurar) shift; fnc_configurar "$@" ;;
  estat) fnc_estat ;;
esac
