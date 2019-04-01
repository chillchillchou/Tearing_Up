from gpiozero import OutputDevice, Button, LED

motor = OutputDevice(3)
button = Button(14)
led = LED(4)

button.wait_for_press()
print("you pressed the button")
motor.on()
led.on()
button.wati_for_release()
motor.off()
led.off()
