from gpiozero import OutputDevice, Button, LED
from time import sleep

motor = OutputDevice(3)
button = Button(14)
led = LED(4)

# button.wait_for_press()
while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
# motor.on()
# sleep(3)
# led.off()
# motor.off()
