from gpiozero import OutputDevice, Button, LED
from time import sleep

motor = OutputDevice(4)
button = Button(14)
led = LED(3)

while True:
    button.wait_for_press()
    motor.on()
    led.on()
    sleep(3)
    led.off()
    motor.off()
