from gpiozero import OutputDevice, Button, LED

motor = OutputDevice(3)
button = Button(14)
led = LED(4)

while True:
    button.wait_for_press()
    print("you pressed the button")
    motor.on()
    led.on()
    button.wait_for_release()
    print("you release the button")
    motor.off()
    led.off()
