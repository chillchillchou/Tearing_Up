from gpiozero import PWMDevice, Button, LED
from time import sleep
motor = PWMOputDevice(23)
button = Button(4)
led = LED(3)


while True:
    button.wait_for_press()
    motor.value(0.8)
    print("turn on motor")
    led.on()
    sleep(20)
    led.off()
    motor.off()
    print("turn off motor")
