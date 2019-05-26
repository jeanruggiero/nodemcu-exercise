# nodemcu-exercise

This repository contains the code for an iot device built on an ESP8266MOD microcontroller. Check out the video for a preview of its coolest feature, party mode!

Party mode flashes a series of different color LEDs to create an effect that makes you want to dance. If you turn down the lights, it dims the LEDs to avoid blinding you. The hardest part of setting this up, was to get the correct relationship between room brightness and LED brightness. The first iteration of dimming used a linear relationship (LED_brightness = room_brightness), but it didn't get the LEDs dim enough to mid-to-low ambient lighting conditions. A quadratic relationship ($y = 1024x^2 - 1$) also wasn't cutting on it. I finally settled on an exponential relationship ($y = 1.00679x$), which has resulted in the best user experience.
