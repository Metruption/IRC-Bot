import pyautogui
import test_config
def autosave(fuck): #for some reason it doesn't work if there are no arguments, just gonna give it this one and see what happens
	pyautogui.press(str(test_config.buttons['save']))
	return None