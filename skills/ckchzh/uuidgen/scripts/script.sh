#!/bin/bash
cmd_v4() { python3 -c "import uuid; print(uuid.uuid4())"; }
cmd_batch() { local n="${1:-5}"; python3 -c "
import uuid
for i in range(int('$n')): print(uuid.uuid4())
"; }
cmd_short() { local length="${1:-8}"; python3 -c "
import random,string
chars=string.ascii_lowercase+string.digits
print(''.join(random.choice(chars) for _ in range(int('$length'))))
"; }
cmd_validate() { local id="$1"; [ -z "$id" ] && { echo "Usage: uuidgen validate <uuid>"; return 1; }
    python3 -c "
import uuid
try: uuid.UUID('$id'); print('✅ Valid UUID')
except: print('❌ Invalid UUID')
"; }
cmd_parse() { local id="$1"; [ -z "$id" ] && { echo "Usage: uuidgen parse <uuid>"; return 1; }
    python3 -c "
import uuid
try:
 u=uuid.UUID('$id')
 print('UUID: {}'.format(u))
 print('  Version: {}'.format(u.version))
 print('  Variant: {}'.format(u.variant))
 print('  Hex: {}'.format(u.hex))
 print('  Int: {}'.format(u.int))
except: print('❌ Invalid UUID')
"; }
cmd_help() { echo "UUIDGen - Unique ID Generator"; echo "Commands: v4 | batch [n] | short [length] | validate <uuid> | parse <uuid> | help"; }
cmd_info() { echo "UUIDGen v1.0.0 | Powered by BytesAgain"; }
case "$1" in v4) cmd_v4;; batch) shift; cmd_batch "$@";; short) shift; cmd_short "$@";; validate) shift; cmd_validate "$@";; parse) shift; cmd_parse "$@";; info) cmd_info;; help|"") cmd_help;; *) cmd_help; exit 1;; esac
