import pyautogui
import time

print (pyautogui.KEYBOARD_KEYS)
pyautogui.PAUSE = 3
pyautogui.press('win')
pyautogui.write('aplicativos: pycharm Community Edition 2022.2.1')
pyautogui.press('enter')
time.sleep(120)
pyautogui.hotkey('shift', 'f10')
time.sleep(10)
pyautogui.press('win')
pyautogui.write('c:\windows\syswow64\softparking.exe')
pyautogui.press('enter')



