import test_config
import pyautogui
#saves a savestate

def save(components):
	response = 'There was a problem saving @' + components['sender'] + ". Either you aren't allowed to do that or you gave invalid arguments."
	slot = int(''.join(i for i in components['arguments'] if i.isdigit()))
	if slot not in  test_config.valid_savestates:
		pass #todo(metro) fix this shit
	elif components['sender'].lower() in test_config.owner:
		print('gonna press shut to save now')
		pyautogui.press(str(slot))
		pyautogui.press(str(test_config.buttons['save']))
		pyautogui.press(str(test_config.default_savestate))
		response = 'saved successfully in state ' +  str(slot)
	return response