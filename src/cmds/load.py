import test_config
import pyautogui
#loads a savestate

def load(components):
	response = 'There was a problem saving @' + components['sender'] + ". Either you aren't allowed to do that or you gave invalid arguments."
	slot = int(''.join(i for i in components['arguments'] if i.isdigit()))
	if slot not in  test_config.valid_savestates:
		print('not valid savestate')
	elif components['sender'].lower() in test_config.owner:
		print('gonna press shut to load now')
		pyautogui.press(str(slot))
		pyautogui.press(str(test_config.buttons['load']))
		pyautogui.press(str(test_config.default_savestate))
		response = 'loadd successfully in state ' +  str(slot)
	return response