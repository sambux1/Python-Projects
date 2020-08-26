'''
This program uses input from a USB game controller to move and click the mouse
'''

import pyautogui
import pygame

# turns off the delay for smoother movement
pyautogui.PAUSE = 0

# set the starting position with no movement
mouse_position = [200, 200]
velocity = [0, 0]

pygame.init()

# set up the controller
joystick = pygame.joystick.Joystick(0)
joystick.init()

# set the movement speed for the mouse
mouse_speed = 15

clock = pygame.time.Clock()

# loop condition
quit = False

# main loop
while not quit:
	left_click = False
	right_click = False
	
	# process each event
	for event in pygame.event.get():
		# get left joystick x and y component values
		velocity[0] = joystick.get_axis(0)
		velocity[1] = joystick.get_axis(1)
		
		# bottom button for left click (X on PS4)
		if joystick.get_button(0):
			left_click = True
		
		# top button for right click (triangle on PS4)
		if joystick.get_button(2):
			right_click = True
		
		# exit the program if the Start button is pressed
		if joystick.get_button(9):
			quit = True
		
		for i in range(10):
			if joystick.get_button(i):
				print(i)
			
	# perform clicks
	if left_click:
		pyautogui.click()
	if right_click:
		pyautogui.rightClick()
		
	# move mouse
	mouse_position[0] += velocity[0] * mouse_speed
	mouse_position[1] += velocity[1] * mouse_speed
	pyautogui.moveTo(int(mouse_position[0]), int(mouse_position[1]))
	# set fps at 50
	clock.tick(50)

pygame.quit()



