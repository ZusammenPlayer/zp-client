#!/usr/bin/env sh
xset -dpms
xset s off
xset s noblank

sleep 5
/usr/bin/python3 /home/pi/MAC2ID.py
sleep 5

/usr/bin/python3 /opt/zp-client/backend/src/app.py /opt/zp-client/backend/settings.toml &
sleep 10

#/usr/bin/python3 /home/pi/gpio_socket_client.py &

unclutter & chromium-browser http://localhost:8090/ \
  --window-size=1920,1080 \
  --window-position=0,0 \
  --start-fullscreen \
#  --kiosk \
  --incognito \
  --noerrdialogs \
  --disable-translate \
  --no-first-run \
  --fast \
  --fast-start \
  --remote-debugging-port=9222 \
  --autoplay-policy=no-user-gesture-required \
  --disable-infobars \
  --disable-features=UseSkiaRenderer,TranslateUI,Translate \
  --disk-cache-dir=/dev/null \
  --overscroll-history-navigation=0 \
  --disable-pinch \
  --no-user-gesture-required

