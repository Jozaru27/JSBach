#!/bin/bash
IP="10.0.1.2"
USER="admin"
PASS="ciberseg"

/usr/bin/expect <<EOF
    set timeout 15
    spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
    expect {
        "yes/no" { send "yes\r"; exp_continue }
        -re ".*\[Pp\]assword: *$" { send "$PASS\r"; exp_continue }
        -re ".*> *$" { send "en\r"; exp_continue }
        -re ".*# *$" {}
        timeout { exit 1 }
        eof { exit 1 }
    }
    send "terminal length 0\r"
    expect -re ".*# *$"
    send "show mac address-table\r"
    expect -re ".*# *$"
    send "exit\r"
    expect eof
EOF
