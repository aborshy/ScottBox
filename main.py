from machine import I2C, Pin
from time import sleep, time
from apis.pico_i2c_lcd import I2cLcd
from timer import Timer

# vars and objects creation
power = Pin(7, Pin.OUT)
test_pin = Pin(25, Pin.OUT)
seconds = 0
button_held = 0

# create Timer objects
green = Timer(15, 16)
green.color = 'green'
red = Timer(14, 17)
red.color = 'red'
buttons = [green, red]
power_on_time = time()

# reset lights
for x in buttons:
    x.led.off()

# lcd api calls and object creation
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# startup actions
power.on()

lcd.clear()
lcd.putstr("JakeBox v.0.0.0")
sleep(1)

while True:
    # to execute every loop
    lcd.blink_cursor_on()
    test_pin.value(not test_pin.value())
    sleep(0.02)

    # check for button presses
    for x in buttons:
        if x.button.value() == 1:
            x.switch_running(time())
            if x.is_running == 1:
                x.led.on()
                sleep(0.33)
                break
            else:
                x.led.off()
                sleep(0.33)
                break

    # update running buttons
    for x in buttons:
        if x.is_running:
            x.update(time())

    # display
    for x in buttons:
        if x.is_running:
            if x.time != x.displayed_time:
                x.displayed_time = x.time
                lcd.clear()
                # lcd.putstr(f"{green.color} {str(green.time)} {x.is_running}")
                lcd.putstr(f"{green.color} {str(green.time)} {green.check_running()}\n")
                lcd.putstr(f"{red.color} {str(red.time)} {red.check_running()}")