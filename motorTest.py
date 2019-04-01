from gpiozero import OutputDevice
from gpiozero import Button
motor = OutputDevice(3)
button = OutputDevice(14)

button.wait_for_press()
print("you pressed the button")
motor.on()
