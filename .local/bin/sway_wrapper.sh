#!/usr/bin/env sh

cd ~ || exit

# XDG Specification
export XDG_CURRENT_DESKTOP=sway
export XDG_SESSION_TYPE=wayland
export XDG_SESSION_DESKTOP=sway
# QT Variables
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_QPA_PLATFORM="wayland;xcb"
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1
# Toolkit Backend Variables
export SDL_VIDEODRIVER=wayland
export _JAVA_AWT_WM_NONREPARENTING=1
export CLUTTER_BACKEND="wayland"
export GDK_BACKEND=wayland,x11
# Theming Related Variables
export MOZ_ENABLE_WAYLAND=1
export XCURSOR_SIZE=24

exec sway >>/dev/null
