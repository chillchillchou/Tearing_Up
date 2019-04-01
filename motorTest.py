from gpiozero import OutputDevice
motor = OutputDevice(3)
button = OutputDevice(14)

button.wait_for_press()
print("you pressed the button")
motor.on()
