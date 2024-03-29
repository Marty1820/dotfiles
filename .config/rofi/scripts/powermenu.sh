#!/usr/bin/env sh

# Commands
lock_cmd="swaylock"
#lock_cmd="i3lock -i ~/wallpapers/lockscreen.png"
rofi_conf="rofi -theme $HOME/.config/rofi/apps/powermenu.rasi"
uptime=$(uptime -p | sed -e 's/up //g')

# Icons
shutdown="󰐥"
reboot="󰑐"
lock="󰌾"
if [ "$(cat /sys/class/power_supply/BAT1/status)" = Discharging ]; then
  suspend="󰤁"
else
  suspend="󰒲"
fi
logout="󰗽"

chosen=$(printf '%s;%s;%s;%s;%s\n' "$shutdown" "$reboot" "$lock" "$suspend" "$logout" |
  $rofi_conf \
    -p "  󱎫  $uptime" \
    -dmenu \
    -sep ';' \
    -selected-row 2)

case "$chosen" in
"$shutdown")
  systemctl poweroff
  ;;
"$reboot")
  systemctl reboot
  ;;
"$lock")
  $lock_cmd
  ;;
"$suspend")
  if [ "$(cat /sys/class/power_supply/BAT1/status)" = Discharging ]; then
    systemctl hibernate
  else
    $lock_cmd
    systemctl suspend
  fi
  ;;
"$logout")
  session=$(loginctl session-status | head -n 1 | awk '{print $1}')
  loginctl terminate-session "$session"
  ;;
esac
