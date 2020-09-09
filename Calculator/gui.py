import pygame
import pygame_gui
from calculator import Calculator

pygame.init()

# the size of the GUI, vertical rectangle
screen_dimensions = (600, 900)

# the size of each button
button_dimensions = (100, 100)
# the labels of each button, from top left to bottom right
button_texts = ['Clear', '(', ')', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', '.', '(-)', '=']

pygame.display.set_caption('Calculator')
window = pygame.display.set_mode(screen_dimensions)

# the background surface, gray
background = pygame.Surface(screen_dimensions)
background.fill(pygame.Color('#888888'))

# the surface that holds the button panel, light gray, located at the bottom of the screen
button_panel = pygame.Surface((500, 600))
button_panel.fill(pygame.Color('#aaaaaa'))

# the gui manager, needed for buttons and output label to display and update
manager = pygame_gui.UIManager(screen_dimensions)

# the expression displayed at the top of the screen
output_text = ''
# the label to contain the output text
output_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 100), (500, 100)), text=output_text, manager=manager)

# the current expression text box
output_text_box = pygame.font.SysFont('tlwgtypo', 25)
output_text_box_surface = output_text_box.render(output_text, True, (255, 255, 255))
output_text_rect = output_text_box_surface.get_rect()
output_text_rect.midright = (500, 150)

# the last expression displayed in the left corner of the output box
alternate_output_text = ''
alternate_output_text_box = pygame.font.SysFont('tlwgtypo', 15)
alternate_output_text_surface = alternate_output_text_box.render(alternate_output_text, True, (200, 200, 200))
alternate_output_text_rect = alternate_output_text_surface.get_rect()
alternate_output_text_rect.midleft = (75, 125)

buttons = []
# create the buttons and assign them their location (4 x 5 grid)
for i in range(0, len(button_texts)):
    # the x position should start at 100 and increase by 100, repeating every fourth button
    x = ((i % 4) + 1) * 100
    # the y position should start at 300 and increase by 100 every fourth button
    y = 300 + (int(i / 4) * 100)
    buttons.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x, y), button_dimensions), 
    				text=str(button_texts[i]), manager=manager))

quit = False
clock = pygame.time.Clock()

calculator = Calculator()

while not quit:
    # set the frame rate to 20 fps
    time_delta = clock.tick(20)

    # go through the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        # check for button clicks and iterate through each button until
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # find which button was clicked and pass the event to the calculator
                button = event.ui_element
                calculator.process_button_click(button)

                if (button.text == 'Clear'):
                    output_text = ''
                else:
                    output_text, alternate_output_text = calculator.get_output_text()
				
				# update the expression shown
                output_text_box_surface = output_text_box.render(output_text, True, (255, 255, 255))
                output_text_rect = output_text_box_surface.get_rect()
                output_text_rect.midright = (500, 150)

				# update the past expression shown if necessary
                alternate_output_text_surface = alternate_output_text_box.render(alternate_output_text, True, (200, 200, 200))
                alternate_output_text_rect = alternate_output_text_surface.get_rect()
                alternate_output_text_rect.midleft = (75, 125)

        manager.process_events(event)

    manager.update(time_delta)

	# update the screen
    window.blit(background, (0, 0))
    window.blit(button_panel, (50, 250))
    
    manager.draw_ui(window)

    window.blit(output_text_box_surface, output_text_rect)
    window.blit(alternate_output_text_surface, alternate_output_text_rect)

    pygame.display.update()

pygame.quit()

