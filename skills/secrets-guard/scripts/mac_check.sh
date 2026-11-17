#!/bin/bash
# Read-only weekly security check of a Mac. Changes nothing. No sudo.
row() { printf '%-28s %s\n' "$1" "$2"; }
row "FileVault"            "$(fdesetup status 2>/dev/null | head -1)"
row "Firewall"             "$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null | sed 's/^Firewall is //')"
row "Stealth mode"         "$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode 2>/dev/null | sed 's/^Firewall stealth mode is //')"
row "System Integrity"     "$(csrutil status 2>/dev/null | sed 's/^System Integrity Protection status: //')"
row "Gatekeeper"           "$(spctl --status 2>/dev/null)"
for k in AutomaticCheckEnabled AutomaticDownload CriticalUpdateInstall ConfigDataInstall AutomaticallyInstallMacOSUpdates; do
  v=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate "$k" 2>/dev/null); row "Updates: $k" "${v:-not set (default)}"
done
row "Screen lock"          "$(sysadminctl -screenLock status 2>&1 | sed 's/.*screenLock delay is //;s/.*screenLock is //')"
row "Remote Login (SSH)"   "$(nc -z -G 1 127.0.0.1 22 >/dev/null 2>&1 && echo 'ON (port 22 answers)' || echo off)"
row "Screen Sharing (VNC)" "$(nc -z -G 1 127.0.0.1 5900 >/dev/null 2>&1 && echo 'ON (port 5900 answers)' || echo off)"
echo; echo "Launch agents / daemons (check for anything you don't recognise):"
for d in ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons; do
  [ -d "$d" ] && ls "$d" 2>/dev/null | sed "s|^|  $d/|"
done
