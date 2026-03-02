#!/bin/bash
IP="10.0.1.2"
USER="admin"
PASS="ciberseg"

/usr/bin/expect <<EOF
    exp_internal 1
    set timeout 10
    spawn ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $USER@$IP
    expect -re ".*\[Pp\]assword: *$" { send "$PASS\r" }
    expect -re ".*\[^ \r\n\]+> *$" { send "en\r" }
    expect -re ".*\[^ \r\n\]+# *$" { send "conf\r" }
    expect -re ".*\[^ \r\n\]+# *$"
    send "exit\r"
    expect -re ".*\[^ \r\n\]+# *$"
    send "exit\r"
    expect eof
EOF
