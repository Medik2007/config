#!/bin/bash

game() {
    timeout 1h "./run.sh" & sleep 3000; bash $HOME/.config/hypr/scripts/notifications/notif.sh normal reminder "Game will close in 10 minutes"
}
