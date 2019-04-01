from gpiozero import OutputDevice, Button, LED
from time import sleep

motor = OutputDevice(3)
button = Button(14)
led = LED(4)

button.wait_for_press()
led.on()
motor.on()
sleep(3)
led.off()
motor.off()
