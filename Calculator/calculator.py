import pygame
import pygame_gui

# processes button clicks and convert them into a calculation
class Calculator:

    # the list of all possible operators
    possible_operators = ['+', '-', '*', '/']
    # maps operators with their precedence
    operator_precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    # the queue to hold tokens before the expression is evaluated
    input = []
    # the position
    index = 0
    # used for keeping successive numbers as a single token
    current_token = ''
    # the list used for creating the final postfix expression
    output_list = []
    # the output to be displayed to the screen
    output_text = ''
    # the previous expression to be displayed to the screen
    alternate_output_text = ''

    def __init__(self):
        pass

	# handle a button click
    def process_button_click(self, button):
        previous = self.current_token
        
        # if the button is a number or decimal point, add it to the current token, or create a token if necessary
        if button.text.isdigit() or button.text == '.':
            self.current_token += button.text
            if previous == '':
                self.input.append(self.current_token)
            else:
                self.input[len(self.input) - 1] = self.current_token
        
        # if the button is the negative sign, add '-' to the beginning of the next token
        elif button.text == '(-)':
            self.current_token += '-'
            self.input.append(self.current_token)
        
        # clear the expression and prepare for the next
        elif button.text == 'Clear':
            self.output_text = ''
            self.current_token = ''
            self.input = []
        
        # calculate the result
        elif button.text == '=':
            self.alternate_output_text = self.output_text
            self.create_expression()
            self.current_token = ''
            self.input = []
        
        else:   # operator or parenthesis
            self.current_token = ''
            self.input.append(button.text)

	# generate a postfix expression from the input data
    def create_expression(self):
        try:
            self.output_list = []
            operator_stack = []
            
            i = 0
            for token in self.input:
            	# if the token is a number, add it to the output stack
                if self.is_number(token):
                    self.output_list.append(float(token))
                
                # if the token is a left parenthesis, add it to the operator stack
                elif token == '(':
                    operator_stack.append(token)
                
                # if the token is a right parenthesis, add all operators in the operator stack to
                #	the output list until a left parenthesis is found
                elif token == ')':
                    # go backwards through the list until a left parenthesis is found
                    while True:
                        # if the list is empty, there are mismatching parentheses
                        if len(operator_stack) == 0:
                            print('Parentheses do not match')
                            return
                        # pop the last item off the stack
                        last_operator = operator_stack.pop(-1)
                        if last_operator == '(':
                            break
                        else:
                            # if the popped item is an operator, add it to the output stack
                            self.output_list.append(last_operator)
                else:   # token is an operator
                    # while there is an operator on the top of the stack with a greater precedence than the token,
                    # pop operators from the operator stack onto the output stack
                    while True:
                        if len(operator_stack) == 0:
                            break
                        # get the top element from the operator stack
                        last_operator = operator_stack[-1]
                        if not self.is_operator(last_operator):
                            break
                        # if it gets here, there is an operator at the top of the stack
                        # compare the precedences of the operators
                        if self.operator_precedence[last_operator] >= self.operator_precedence[token]:
                            operator_stack.pop(-1)
                            self.output_list.append(last_operator)
                        else:
                            break

                    # add the token to the operator stack
                    operator_stack.append(token)

                i += 1

            # pop all remaining operators from the operator stack to the output stack
            while len(operator_stack) != 0:
                self.output_list.append(operator_stack.pop(-1))

            self.evaluate_postfix()

        except Exception:
            self.output_text = 'Error'

	# evaluate the expression created
    def evaluate_postfix(self):
        try:
            # stack used to hold tokens as the output list is traversed
            temp_stack = []

            # go through the output list
            for token in self.output_list:
            	# if the token is a number, add it to the stack
                if self.is_number(token):
                    temp_stack.append(token)
                else:   # operator
                    a = temp_stack.pop(-2)
                    b = temp_stack.pop(-1)
                    c = None    # the new number calculated from a and b

					# apply the correct operator to the next two items on the stack
                    if token == '+':
                        c = a + b
                    elif token == '-':
                        c = a - b
                    elif token == '*':
                        c = a * b
                    elif token == '/':
                        c = a / b

					# add the result of the operation to the stack
                    temp_stack.append(c)

            self.output_text = str(temp_stack[0])

        except Exception:
            self.output_text = 'Error'

    def get_output_text(self):
        if len(self.input) > 0:
            self.output_text = ''
            for token in self.input:
                self.output_text += token + ' '
            # eliminate extra space at the end
            self.output_text = self.output_text[:-1]

        return self.output_text, self.alternate_output_text

	# check if a token is a number
    @staticmethod
    def is_number(token):
        try:
            float(token)
            return True
        except:
            return False

	# check if a token is an operator
    def is_operator(self, token):
        if token in self.possible_operators:
            return True
        return False


