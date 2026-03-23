# Mohammed Seada KeyPad

import board

import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import rotaryio
import digitalio


from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler


keyboard = KMKKeyboard()


# Intiation the variables and functions
macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)


\
displayio.release_displays()
i2c = busio.I2C(scl=board.GP5, sda=board.GP4) 

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


splash = displayio.Group()
display.show(splash)



text = "KMK Macropad"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=10, y=15)
splash.append(text_area)

status_text = label.Label(terminalio.FONT, text="Ready", color=0xFFFFFF, x=10, y=35)
splash.append(status_text)



encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3)
encoder_button = digitalio.DigitalInOut(board.GP1)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP


#define pins
SWITCH_PINS = [board.GP26, board.GP27, board.GP28, board.GP29]


keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
)



# Encoder
keyboard.encoder_handler.pins = ((board.GP2, board.GP3, board.GP1, False),)



# Define macros
COPY = KC.MACRO(Press(KC.LCTRL, KC.C), Release(KC.LCTRL, KC.C))
PASTE = KC.MACRO(Press(KC.LCTRL, KC.V), Release(KC.LCTRL, KC.V))
SCREENSHOT = KC.MACRO(Press(KC.LGUI, KC.LSHIFT, KC.S), Release(KC.LGUI, KC.LSHIFT, KC.S))
TASK_MANAGER = KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.ESC), Release(KC.LCTRL, KC.LSHIFT, KC.ESC))



# Keymap for the  switches  and   encoder


# the layout [SW1, SW2, SW3, SW4, ENCODER_CCW, ENCODER_CW, ENCODER_PRESS]

keyboard.keymap = [
    [
        COPY,              
        PASTE,            
        SCREENSHOT,        
        TASK_MANAGER,      
        KC.AUDIO_VOL_DOWN, 
        KC.AUDIO_VOL_UP,   
        KC.AUDIO_MUTE,     
    ]
]


# update display
def update_display(action):
    status_text.text = action
    display.show(splash)


#display updates

class CustomKeyboard(KMKKeyboard):

    def __init__(self):
        super().__init__()

        self.last_encoder_value = 0
        


    def during_bootup(self):
        super().during_bootup()
        self.last_encoder_value = encoder.position
        


    def before_matrix_scan(self):
        super().before_matrix_scan()
        


        # Check encoder postion
        current_encoder_value = encoder.position

        if current_encoder_value != self.last_encoder_value:


            if current_encoder_value > self.last_encoder_value:
                update_display("Vol Up")
            else:
                update_display("Vol Down")

            self.last_encoder_value = current_encoder_value
        

        
        # encoder button
        if not encoder_button.value:  
            update_display("Mute")
            


    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)


        if hasattr(sandbox, 'active_keys') and sandbox.active_keys:

            key = sandbox.active_keys[-1]
            if key == COPY:
                update_display("Copy")

            elif key == PASTE:
                update_display("Paste")

            elif key == SCREENSHOT:

                update_display("Screenshot")

            elif key == TASK_MANAGER:
                update_display("Task Mgr")



keyboard = CustomKeyboard()


#if custom keyboard
macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)



keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
)

keyboard.encoder_handler.pins = ((board.GP2, board.GP3, board.GP1, False),)

# Start
if __name__ == '__main__':
    keyboard.go()