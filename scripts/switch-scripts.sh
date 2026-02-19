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
[ -z "$MACS_APPLIED_CONF" ] && MACS_APPLIED_CONF=mac_switches_applied.conf
[ -z "$MAC_ADMIN_CONF" ] && MAC_ADMIN_CONF=mac_admin.conf
[ -z "$MAC_ADMIN_APPLIED_CONF" ] && MAC_ADMIN_APPLIED_CONF=mac_admin_applied.conf

SW_CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$CONF_SWITCHES"
MAC_CONF_FILE="$DIR/$PROJECTE/$DIR_CONF/$MACS_SWITCHES_CONF"
MAC_APPLIED_FILE="$DIR/$PROJECTE/$DIR_CONF/$MACS_APPLIED_CONF"
MAC_ADMIN_FILE="$DIR/$PROJECTE/$DIR_CONF/$MAC_ADMIN_CONF"
MAC_ADMIN_APPLIED_FILE="$DIR/$PROJECTE/$DIR_CONF/$MAC_ADMIN_APPLIED_CONF"

# Asegurar archivos existen y tienen permisos de escritura para el CGI
for f in "$SW_CONF_FILE" "$MAC_CONF_FILE" "$MAC_ADMIN_FILE" "$MAC_APPLIED_FILE" "$MAC_ADMIN_APPLIED_FILE"; do
    [ -n "$f" ] && [ ! -f "$f" ] && touch "$f"
    [ -n "$f" ] && chmod 666 "$f"
done




######################################################################
###  Funcions Auxiliars
######################################################################

get_br0_mac() {
    # Dynamically get MAC address of br0 interface
    ip link show br0 | grep "link/ether" | awk '{print $2}'
}

validar_mac() {
    local mac=$1
    [[ $mac =~ ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$ ]]
}

validar_ip() {
    local ip=$1
    [[ $ip =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]
}


mostrar_tabla_macs() {
    local IP="$1" USER="$2" PASS="$3" PROTO="$4"
    if [ "$PROTO" == "telnet" ]; then
        /usr/bin/expect <<EOF
            set timeout 10
            spawn telnet $IP
            expect "Username:" { send "$USER\r" }
            expect "Password:" { send "$PASS\r" }
            expect -re ".+> *$" { send "en\r" }
            expect {
                -re ".*Password: *$" { send "$PASS\r"; exp_continue }
                -re ".+# *$" {}
            }
            send "terminal length 0\r"
            expect -re ".+# *$"
            send "show mac address-table\r"
            expect -re ".+# *$"
            send "exit\r"
            expect eof
EOF
    else
        /usr/bin/expect <<EOF | awk '/---/ {show=1; next} /Total MAC/ {show=0} show || /Gi/ || /dynamic/'
            set timeout 10
            spawn ssh -o ConnectTimeout=5 -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
            expect {
                "yes/no" { send "yes\r"; exp_continue }
                -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
                -re ".+> *$" { send "en\r"; exp_continue }
                -re ".+# *$" {}
                timeout { exit 1 }
                eof { exit 1 }
            }
            send "terminal length 0\r"
            expect -re ".\[>#\] *$"
            send "show mac address-table\r"
            expect -re ".\[>#\] *$"
            send "exit\r"
EOF
    fi
}


eliminar_acls() {
    local IP="$1" USER="$2" PASS="$3"
    
    /usr/bin/expect <<EOF
        set timeout 15
        spawn ssh -o ConnectTimeout=5 -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect {
            "yes/no" { send "yes\r"; exp_continue }
            -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
            -re ".+> *$" { send "en\r"; exp_continue }
            -re ".+# *$" {}
            timeout { exit 1 }
            eof { exit 1 }
        }
        send "conf\r"
        expect -re ".+# *"
        
        # Unbind from VLANs 1-4
        for {set v 1} {\$v <= 4} {incr v} {
            send "no access-list bind 1 interface vlan \$v\r"
            expect -re ".+# *"
        }

        send "no access-list create 1\r"
        expect -re ".+# *"
        send "exit\r"
        expect -re ".+# *$"
        send "copy running-config startup-config\r"
        expect -re ".*OK!.*# *"
EOF
}


crear_acls() {
    local IP="$1" USER="$2" PASS="$3" MODE="$4" NEW_MACS="$5"
    local ROUTER_MAC=$(get_br0_mac)
    
    [ -z "$ROUTER_MAC" ] && ROUTER_MAC="12:2b:a0:cf:77:58" # Fallback if dynamic fails
    
    [ ! -f "$MAC_APPLIED_FILE" ] && touch "$MAC_APPLIED_FILE"
    
    IP="$IP" USER="$USER" PASS="$PASS" MODE="$MODE" NEW_MACS="$NEW_MACS" \
    CFG="$MAC_CONF_FILE" APPLIED="$MAC_APPLIED_FILE" ROUTER_MAC="$ROUTER_MAC" \
    /usr/bin/expect <<'EOF'
        set timeout 60
        set IP $env(IP)
        set USER $env(USER)
        set PASS $env(PASS)
        set MODE $env(MODE)
        set NEW_MACS $env(NEW_MACS)
        set CFG $env(CFG)
        set APPLIED $env(APPLIED)
        set ROUTER_MAC $env(ROUTER_MAC)

        spawn ssh -o ConnectTimeout=60 -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect {
            "yes/no" { send "yes\r"; exp_continue }
            -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
            -re ".+> *$" { send "en\r"; exp_continue }
            -re ".+# *$" {}
            timeout { exit 1 }
        }
        
        send "terminal length 0\r"
        expect -re ".+# *$"

        set mode_actual $MODE
        send "show access-list 1\r"
        expect -re ".+# *$"
        if { [string match "*not defined*" $expect_out(buffer)] || [string match "*No access list*" $expect_out(buffer)] } {
            set mode_actual "rebuild"
        }

        send "conf\r"
        expect -re ".+# *"
        
        # Desvincular de todas las VLANs posibles para limpiar
        for {set v 1} {$v <= 4} {incr v} {
            send "no access-list bind 1 interface vlan $v\r"
            expect -re ".+# *"
        }

        if { $mode_actual == "rebuild" } {
            send "no access-list create 1\r"
            expect -re ".+# *"
            send "access-list create 1 name \"BLOQUEAR_MAC\"\r"
            expect -re ".+# *"
            
            set list ""
            catch { set list [exec grep -v "^#" $CFG | grep -v "^$" | tr "\n" " "] }
            set i 1
            foreach entry [split $list] {
                if { $entry == "" } continue
                set parts [split $entry ";"]
                set mac [lindex $parts 0]
                set mac [string tolower $mac]
                send "access-list mac 1 rule $i deny logging disable smac $mac smask ff:ff:ff:ff:ff:ff\r"
                expect -re ".+# *"
                # sleep 0.1
                incr i
            }
            send "access-list mac 1 rule 120 permit logging disable\r"
            expect -re ".+# *"
        } else {
            set idx 0
            catch { set idx [exec grep -v "^#" $APPLIED | grep -v "^$" | wc -l] }
            set i [expr $idx + 1]
            foreach entry [split $NEW_MACS] {
                if { $entry == "" } continue
                set parts [split $entry ";"]
                set mac [lindex $parts 0]
                set mac [string tolower $mac]
                send "access-list mac 1 rule $i deny logging disable smac $mac smask ff:ff:ff:ff:ff:ff\r"
                expect -re ".+# *"
                # sleep 0.1
                incr i
            }
        }
        
        # Vincular a VLANs únicas encontradas en la configuración
        set vlans_used [list]
        set list ""
        catch { set list [exec grep -v "^#" $CFG | grep -v "^$" | tr "\n" " "] }
        foreach entry [split $list] {
            if { $entry == "" } continue
            set parts [split $entry ";"]
            if { [llength $parts] > 1 } {
                set vlan [lindex $parts 1]
                if { [lsearch $vlans_used $vlan] == -1 } {
                    lappend vlans_used $vlan
                }
            }
        }
        
        # Si no hay VLANs especificadas, no vinculamos nada
        foreach vlan $vlans_used {
            send "access-list bind 1 interface vlan $vlan\r"
            expect -re ".+# *"
            # sleep 0.1
        }
        
        send "exit\r"
        expect -re ".+# *$"
        send "copy running-config startup-config\r"
        expect -re ".*OK!.*# *"
        send "exit\r"
EOF
}


eliminar_acls_admin() {
    local IP="$1" USER="$2" PASS="$3"
    IP="$IP" USER="$USER" PASS="$PASS" \
    /usr/bin/expect <<'EOF'
        set timeout 15
        set IP $env(IP)
        set USER $env(USER)
        set PASS $env(PASS)
        spawn ssh -o ConnectTimeout=5 -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect {
            -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
            -re ".+> *$" { send "en\r"; exp_continue }
            -re ".+# *$" {}
        }
        send "conf\r"
        expect -re ".+# *"
        send "no access-list bind 2 interface vlan 1\r"
        expect -re ".+# *"
        send "no access-list create 2\r"
        expect -re ".+# *"
        send "exit\r"
        expect -re ".+# *$"
        send "copy running-config startup-config\r"
        expect -re ".*OK!.*# *"
EOF
}


crear_acls_admin() {
    local IP="$1" USER="$2" PASS="$3" MODE="$4" NEW_MACS="$5"
    local ROUTER_MAC=$(get_br0_mac)
    [ -z "$ROUTER_MAC" ] && ROUTER_MAC="12:2b:a0:cf:77:58"
    
    [ ! -f "$MAC_ADMIN_APPLIED_FILE" ] && touch "$MAC_ADMIN_APPLIED_FILE"

    IP="$IP" USER="$USER" PASS="$PASS" MODE="$MODE" NEW_MACS="$NEW_MACS" \
    CFG="$MAC_ADMIN_FILE" APPLIED="$MAC_ADMIN_APPLIED_FILE" ROUTER_MAC="$ROUTER_MAC" \
    /usr/bin/expect <<'EOF'
        set timeout 60
        set IP $env(IP)
        set USER $env(USER)
        set PASS $env(PASS)
        set MODE $env(MODE)
        set NEW_MACS $env(NEW_MACS)
        set CFG $env(CFG)
        set APPLIED $env(APPLIED)
        set ROUTER_MAC $env(ROUTER_MAC)

        spawn ssh -o ConnectTimeout=60 -o GSSAPIAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect {
            "yes/no" { send "yes\r"; exp_continue }
            -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
            -re ".+> *$" { send "en\r"; exp_continue }
            -re ".+# *$" {}
            timeout { exit 1 }
        }
        
        send "terminal length 0\r"
        expect -re ".+# *$"

        send "conf\r"
        expect -re ".+# *"
        
        # Siempre eliminar y recrear la ACL de Admin para asegurar consistencia
        send "no access-list bind 2 interface vlan 1\r"
        expect -re ".+# *"
        # sleep 0.2
        send "no access-list create 2\r"
        expect -re ".+# *"
        # sleep 0.2
        
        send "access-list create 2 name \"PERMITIR_MAC_ADMIN\"\r"
        expect -re ".+# *"
        # sleep 0.2
        
        # Añadir todas las MACs de la lista (empezando desde regla 1)
        set list ""
        catch { set list [exec grep -v "^#" $CFG | grep -v "^$" | tr "\n" " "] }
        set i 1
        foreach m [split $list] {
            if { $m == "" || $m == $ROUTER_MAC } continue
            set m [string tolower $m]
            send "access-list mac 2 rule $i permit logging disable smac $m smask ff:ff:ff:ff:ff:ff\r"
            expect -re ".+# *"
            # sleep 0.1
            incr i
        }
        
        # Siempre permitir el Router (regla 125)
        send "access-list mac 2 rule 125 permit logging disable smac $ROUTER_MAC smask ff:ff:ff:ff:ff:ff\r"
        expect -re ".+# *"
        # sleep 0.2
        
        # Denegar todo lo demás (regla 130)
        send "access-list mac 2 rule 130 deny logging disable\r"
        expect -re ".+# *"
        # sleep 0.2
        
        # Vincular a VLAN 1 (Admin)
        send "access-list bind 2 interface vlan 1\r"
        expect -re ".+# *"
        # sleep 0.2
        
        send "exit\r"
        expect -re ".+# *$"
        send "copy running-config startup-config\r"
        expect -re ".*OK!.*# *"
        send "exit\r"
EOF
}


comprobar_acls() {
    local IP="$1" USER="$2" PASS="$3" ACL_ID="$4"
    [ -z "$ACL_ID" ] && ACL_ID=1
    /usr/bin/expect <<EOF | grep -q "access-list mac $ACL_ID" && echo "OK" || echo "FAIL"
        set timeout 10
        log_user 0
        spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
        expect {
            "yes/no" { send "yes\r"; exp_continue }
            -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
            -re ".+> *$" { send "en\r"; exp_continue }
            -re ".+# *$" {}
        }
        send "show access-list $ACL_ID\r"
        expect -re ".+# *"
        puts \$expect_out(buffer)
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
            local vlan=$2
            if ! validar_mac "$mac"; then echo "❌ ERROR: MAC invàlida"; exit 1; fi
            
            local entry="$mac;$vlan"
            if ! grep -qF "$mac" "$MAC_CONF_FILE"; then
                # Asegurar newline antes de añadir si el fichero no termina en newline
                [ -s "$MAC_CONF_FILE" ] && [ -n "$(tail -c1 "$MAC_CONF_FILE")" ] && echo "" >> "$MAC_CONF_FILE"
                echo "$entry" >> "$MAC_CONF_FILE"
                echo "✅ MAC afegida"
            else
                echo "⚠️ MAC ja existeix"
            fi
            ;;

        eliminar_mac)
            local mac=$1
            # Escapar caracteres especiales para grep
            local safe_mac=$(echo "$mac" | sed 's/;/\\;/g')
            # Borrar líneas que empiecen con la MAC (ignorando si tienen ;VLAN o no)
            # Primero intentamos match exacto de línea, si no, match de inicio
            grep -v "^$safe_mac" "$MAC_CONF_FILE" > "${MAC_CONF_FILE}.tmp"
            mv "${MAC_CONF_FILE}.tmp" "$MAC_CONF_FILE"
            chmod 666 "$MAC_CONF_FILE"
            ;;
        obtener_reglas_activas)
            local IP="$2"
            local USER="$3"
            local PASS="$4"
            /usr/bin/expect <<EOF > "/tmp/acl_status.tmp"
                set timeout 10
                spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
                expect {
                    -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
                    -re ".+> *$" { send "en\r"; exp_continue }
                    -re ".+# *$" {}
                }
                send "terminal length 0\r"
                expect -re ".+# *$"
                send "show access-list 1\r"
                expect -re ".+# *$"
                send "show access-list 2\r"
                expect -re ".+# *$"
                send "exit\r"
                expect eof
EOF
            chmod 666 "/tmp/acl_status.tmp"
            ;;
        afegir_mac_admin)
            local mac=$1
            if ! validar_mac "$mac"; then echo "❌ ERROR: MAC invàlida"; exit 1; fi
            if ! grep -qix "^$mac$" "$MAC_ADMIN_FILE"; then
                echo "$mac" >> "$MAC_ADMIN_FILE"
                echo "✅ MAC Admin afegida"
            else
                echo "⚠️ MAC Admin ja existeix"
            fi
            ;;

        eliminar_mac_admin)
            local mac=$1
            grep -v "^$mac$" "$MAC_ADMIN_FILE" > "${MAC_ADMIN_FILE}.tmp"
            mv "${MAC_ADMIN_FILE}.tmp" "$MAC_ADMIN_FILE"
            chmod 666 "$MAC_ADMIN_FILE"
            ;;
        mostrar_tabla_macs)
            local target_ip=$1
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                local pr=$(echo $linea | cut -d ";" -f 5)
                
                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" -c 1 -W 0.5 > /dev/null 2>&1; then
                    echo "=================================================="
                    echo "SWITCH: $n ($i)"
                    echo "=================================================="
                    mostrar_tabla_macs "$i" "$u" "$p" "$pr"
                    echo ""
                fi
            done < "$SW_CONF_FILE"
            ;;
        crear_acls)
            local target_ip=$1
            local MACS_ACTUALS=$(grep -v "^#" "$MAC_CONF_FILE" | grep -v "^$" | sort)
            local MACS_APLICADES=$(grep -v "^#" "$MAC_APPLIED_FILE" 2>/dev/null | grep -v "^$" | sort)
            
            local DELETED=$(comm -23 <(echo "$MACS_APLICADES") <(echo "$MACS_ACTUALS"))
            local NEW_MACS=$(comm -13 <(echo "$MACS_APLICADES") <(echo "$MACS_ACTUALS") | tr '\n' ' ')

            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                
                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" -c 1 -W 0.5 > /dev/null 2>&1; then
                    echo "--- Aplicando cambios al switch $n ($i) ---"
                    local S_MODE="append"
                    if [ -n "$DELETED" ]; then S_MODE="rebuild"; fi
                    
                    crear_acls "$i" "$u" "$p" "$S_MODE" "$NEW_MACS"
                    echo "  - ¡Hecho!"
                    sleep 2
                fi
            done < "$SW_CONF_FILE"
            
            cp "$MAC_CONF_FILE" "$MAC_APPLIED_FILE"
            chmod 666 "$MAC_APPLIED_FILE"
            ;;
        eliminar_acls)
            local target_ip=$1
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)

                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    echo "--- Eliminando ACLs del switch $n ($i) ---"
                    eliminar_acls "$i" "$u" "$p"
                    echo "  - ¡Hecho!"
                    sleep 0.5
                fi
            done < "$SW_CONF_FILE"
            rm -f "$MAC_APPLIED_FILE"
            ;;

        crear_acls_admin)
            local target_ip=$1
            local MACS_ACTUALS=$(grep -v "^#" "$MAC_ADMIN_FILE" | grep -v "^$" | sort)
            local MACS_APLICADES=$(grep -v "^#" "$MAC_ADMIN_APPLIED_FILE" 2>/dev/null | grep -v "^$" | sort)
            
            local DELETED=$(comm -23 <(echo "$MACS_APLICADES") <(echo "$MACS_ACTUALS"))
            local NEW_MACS=$(comm -13 <(echo "$MACS_APLICADES") <(echo "$MACS_ACTUALS") | tr '\n' ' ')

            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)
                
                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" -c 1 -W 0.5 > /dev/null 2>&1; then
                    echo "--- Aplicando cambios ADMIN al switch $n ($i) ---"
                    local S_MODE="append"
                    if [ -n "$DELETED" ]; then S_MODE="rebuild"; fi
                    
                    crear_acls_admin "$i" "$u" "$p" "$S_MODE" "$NEW_MACS"
                    echo "  - ¡Hecho!"
                    sleep 2
                fi
            done < "$SW_CONF_FILE"
            
            cp "$MAC_ADMIN_FILE" "$MAC_ADMIN_APPLIED_FILE"
            chmod 666 "$MAC_ADMIN_APPLIED_FILE"
            ;;
        eliminar_acls_admin)
            local target_ip=$1
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)

                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    echo "--- Eliminando ACLs ADMIN del switch $n ($i) ---"
                    eliminar_acls_admin "$i" "$u" "$p"
                    echo "  - ¡Hecho!"
                    sleep 0.5
                fi
            done < "$SW_CONF_FILE"
            rm -f "$MAC_ADMIN_APPLIED_FILE"
            ;;

        comprobar_acls)
            local target_ip=$1
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)

                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    comprobar_acls "$i" "$u" "$p" 1
                fi
            done < "$SW_CONF_FILE"
            ;;
        comprobar_acls_admin)
            local target_ip=$1
            while IFS=';' read -r linea; do
                [[ $linea =~ ^# || -z "$linea" ]] && continue
                local n=$(echo $linea | cut -d ";" -f 1)
                local i=$(echo $linea | cut -d ";" -f 2)
                local u=$(echo $linea | cut -d ";" -f 3)
                local p=$(echo $linea | cut -d ";" -f 4)

                if [ -n "$target_ip" ] && [ "$target_ip" != "$i" ]; then continue; fi

                if ping -c 1 -w 1 "$i" > /dev/null 2>&1; then
                    comprobar_acls "$i" "$u" "$p" 2
                fi
            done < "$SW_CONF_FILE"
            ;;
	esac
}

fnc_estat() {
    local pids=()
    local results_file=$(mktemp)
    while IFS=';' read -r linea; do
        [[ $linea == \#* || -z "$linea" ]] && continue
        local nom=$(echo $linea | cut -d ";" -f 1)
        local ip=$(echo $linea | cut -d ";" -f 2)
        (
            if ping -c 1 -W 0.5 "$ip" > /dev/null 2>&1; then
                echo "$nom;$ip;ACTIVAT" >> "$results_file"
            else
                echo "$nom;$ip;DESACTIVAT" >> "$results_file"
            fi
        ) &
        pids+=($!)
    done < "$SW_CONF_FILE"
    
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null
    done
    
    # Ordenamos un poco para que sea consistente
    sort "$results_file"
    rm -f "$results_file"
}


case "$1" in
  configurar) shift; fnc_configurar "$@" ;;
  estat) fnc_estat ;;
esac
