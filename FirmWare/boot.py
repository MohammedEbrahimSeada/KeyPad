# boot.py for Mohammed Seada KeyPad


import storage
import usb_cdc
import usb_hid

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,)
)


print("M.Seada KeyPad boot complete!")