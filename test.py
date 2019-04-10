from gpiozero import OutputDevice, Button, LED
from time import sleep
motor = OutputDevice(23)
button = Button(4)
led = LED(3)


while True:
    button.wait_for_press()
    motor.on()
    print("turn on motor")
    led.on()
    sleep(20)
    led.off()
    motor.off()
    print("turn off motor")
