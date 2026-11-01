import ctypes
import win32gui
import win32api
import win32ui


# 1. test w/o arguments
# win32gui.MessageBox()


# 2. Yes or No
result = win32gui.MessageBox(
    None,
    "Harel, Gilad, No Attia and no Amrany",
    "my name",
    4
)

print("result, yes or no:", result)


# 3. Yes, No or Help
result = win32gui.MessageBox(
    None,
    "Noam Peled",
    "Favorite singer",
    4 | 16384
)

print("result, yes/no/help:", result)


# 4. Check the answer
if result == 6:
    print("Peled's Plan")
elif result == 7:
    print("you selected no")
else:
    print("a different button was selected:", result)


# 5. Test win32api
result = win32api.MessageBox(
    None,
    "test win32api",
    "API32",
    0
)

print("win32api result:", result)


# 6. win32api and win32gui use different wrapers

 
# 7. test win32ui
result = win32ui.MessageBox(
    "testing win32ui",
    "UI32"
)

print("win32ui result:", result)


# 8. load user32.dll
user32 = ctypes.WinDLL("user32.dll")


# 9.use the unicode version
# MessageBoxW = Unicode
MessageBoxW = user32.MessageBoxW


# 10. call MessageBoxW
result = MessageBoxW(
    None,
    "ctypes",
    "WinAPI",
    0
)

print("MessageBoxW result:", result)