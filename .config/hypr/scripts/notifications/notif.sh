#!/bin/bash

notif_id="$HOME/.config/hypr/scripts/notifications/notifs/$2"
cat $notif_id || echo "0" > $notif_id
echo $(notify-send -p -u $1 -r $(cat $notif_id) "$3") > $notif_id
