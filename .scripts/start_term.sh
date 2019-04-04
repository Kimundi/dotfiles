#!/bin/sh

exec fish -c "set -x i3wm_fish_term_parent_window_id (printf '%d\n' (xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print \$NF}')); exec urxvt -e fish"
