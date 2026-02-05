#!/bin/bash

# JSBach Router Administration - Bridge Actions and Status (Premium Organized Fix)
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

# Execute command
RAW_OUTPUT=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge "$comand")

# Extract the first line (status) and the HTML content
ESTAT_GRAL=$(echo "$RAW_OUTPUT" | head -n1)
HTML_CONTENT=$(echo "$RAW_OUTPUT" | sed '1d')

# Header Config
ICON="🌉"
TITLE="Bridge"
case "$comand" in
    iniciar)  TITLE="Iniciar Bridge" ; ICON="🚀" ;;
    aturar)   TITLE="Aturar Bridge"  ; ICON="🛑" ;;
    estat)    TITLE="Estat del Bridge" ; ICON="📊" ;;
esac

get_badge() {
    if echo "$1" | grep -qiw "ACTIVAT"; then echo "<span class='badge badge-green'>ACTIU</span>"
    elif echo "$1" | grep -qiw "DESACTIVAT"; then echo "<span class='badge badge-red'>INACTIU</span>"
    else echo "<span class='badge badge-blue'>$1</span>"; fi
}

cat << EOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="utf-8">
  <title>$TITLE - JSBach</title>
  <style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 2.5rem;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  min-height: 100vh;
}

.container { max-width: 1100px; margin: 0 auto; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

h1 {
  background: rgba(255, 255, 255, 0.05);
  padding: 18px 24px;
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 15px;
  margin: 0;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(15px);
  margin-bottom: 35px;
  animation: slideIn 0.4s ease-out;
}

/* Section titles inside cards */
h3 { 
  margin: 0 0 25px 0;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 1.3rem;
  font-weight: 700;
  color: #60a5fa;
  letter-spacing: 0.5px;
}

h2 { display: none; } /* Hide backend title */

.badge { display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
.badge-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.badge-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-blue { background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: rgba(15, 23, 42, 0.4);
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

th, td { padding: 16px 20px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
th { background: rgba(59, 130, 246, 0.12); color: #fff; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.03); }

/* Fix code/monospace sections from backend */
[style*="font-family: monospace"] {
  background: #020617 !important;
  color: #94a3b8 !important;
  padding: 25px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.05) !important;
  white-space: pre !important;
  font-size: 0.95rem !important;
  line-height: 1.7 !important;
  margin-top: 15px !important;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

[style*="margin-bottom: 20px; font-size: 1.1em;"] { display: none; }
</style>
</head>
<body>
  <div class="container">
    <div class="page-header">
        <h1><span style="font-size: 2rem;">$ICON</span> $TITLE</h1>
        $(get_badge "$ESTAT_GRAL")
    </div>

EOF

# Correct Parsing: 
# 1. First, we identify sections by <h3>.
# 2. We skip anything before the first <h3> (likely headers we already replaced).
# 3. We split by <h3> and wrap each slice in a card.

# Use AWK for cleaner sectioning
echo "$HTML_CONTENT" | awk '
BEGIN { first=1 }
/<h3>/ {
    if (!first) print "</div>"
    print "<div class=\"card\">"
    first=0
}
{ print $0 }
END { if (!first) print "</div>" }
'

cat << EOF
  </div>
</body>
</html>
EOF
