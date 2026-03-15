#!/bin/bash
cmd_now() { python3 -c "import time; t=time.time(); print(int(t))"; }
cmd_date() { local ts="$1"; [ -z "$ts" ] && { echo "Usage: unixtime date <timestamp>"; return 1; }
    python3 -c "import datetime; ts=float('$ts'); ts=ts/1000 if ts>1e12 else ts; print(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))"; }
cmd_stamp() { local dt="$*"; [ -z "$dt" ] && { echo "Usage: unixtime stamp <date>"; return 1; }
    python3 -c "
import datetime
for fmt in ['%Y-%m-%d %H:%M:%S','%Y-%m-%d','%Y/%m/%d']:
 try: print(int(datetime.datetime.strptime('$dt',fmt).timestamp())); break
 except: continue
else: print('Cannot parse')
"; }
cmd_ago() { local ts="$1"; [ -z "$ts" ] && { echo "Usage: unixtime ago <timestamp>"; return 1; }
    python3 -c "
import time
diff=time.time()-float('$ts')
if diff<60: print('{:.0f} seconds ago'.format(diff))
elif diff<3600: print('{:.0f} minutes ago'.format(diff/60))
elif diff<86400: print('{:.1f} hours ago'.format(diff/3600))
elif diff<2592000: print('{:.1f} days ago'.format(diff/86400))
else: print('{:.1f} months ago'.format(diff/2592000))
"; }
cmd_ms() { python3 -c "import time; print(int(time.time()*1000))"; }
cmd_help() { echo "UnixTime - Quick Timestamp Utility"; echo "Commands: now | date <ts> | stamp <date> | ago <ts> | ms | help"; }
cmd_info() { echo "UnixTime v1.0.0 | Powered by BytesAgain"; }
case "$1" in now) cmd_now;; date) shift; cmd_date "$@";; stamp) shift; cmd_stamp "$@";; ago) shift; cmd_ago "$@";; ms) cmd_ms;; info) cmd_info;; help|"") cmd_help;; *) cmd_help; exit 1;; esac
