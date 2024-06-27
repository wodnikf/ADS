class Stack:
    def __init__(self, max_size, data_type):
        self.max_size = max_size
        self.data_type = data_type
        self.top_in = -1
        self.stack = []

    def push(self, item):
        if len(self.stack) >= self.max_size:
            print("Stack is full")
        else:
            self.stack.append(self.data_type(item))
            self.top_in += 1

    def pop(self):
        if self.top_in == -1:
            return None
        else:
            item = self.stack[self.top_in]
            del self.stack[self.top_in]
            self.top_in -= 1
            return item
        
    def is_empty(self):
        if len(self.stack) == 0:
            return True
        return False

    def top(self):
        if self.top_in == -1:
            return None
        else:
            return self.stack[self.top_in]
        
    def print_stack(self):
        for item in self.stack:
            print(item, end=" ")
        print()

def priority(operator):
    if operator in ['+', '-']:
        return 2
    elif operator in ['*', '/']:
        return 1
    return 0

operators = ('+', '-', '*', '/', '(', ')')
operators_2 = ('+', '-','*', '/')

def are_next_to_each_other(string):
    numbers = string.split()

    for i in range(len(numbers) - 1):
        if numbers[i].lstrip('-').isdigit() and numbers[i + 1].lstrip('-').isdigit():
            return True
    return False

def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def get_equation(stack, input):
    global operators
    open_parenthesis = 0
    closed_parenthesis = 0
    is_last_space = True
    number_of_operators = 0
    number_of_digits = 0
    j = 0

    if are_next_to_each_other(input):
        return 'error'

    for i in range(len(input)):
        if input[i] != ' ':
            if input[i] == '(':
                open_parenthesis += 1
            if input[i] == ')':
                closed_parenthesis += 1
            if input[i] in operators or input[i].lstrip('-').isdigit() or input[i] == '.':
                if input[i] in operators_2:
                    number_of_operators += 1
                if input[i].lstrip('-').isdigit():
                    number_of_digits += 1
                if is_last_space:
                    if input[i] == '.':
                        return 'error'
                    stack.push(input[i])
                    is_last_space = False

                else:
                    if stack.top_in >= j:
                        stack.stack[j] += input[i]
                    else:
                        stack.push(input[i])
        else:
            is_last_space = True
            j += 1

    if open_parenthesis != closed_parenthesis:
        return 'error'

    if number_of_operators >= number_of_digits:
        return 'error'

def infix_to_postfix(stack, expression):
    global operators
    result = Stack(len(expression), str)
    o_temp = Stack(len(expression), str)
    o_temp.push('(')
    i = 0

    while i < len(stack.stack):
        x = stack.stack[i]

        if x.lstrip('-').isdigit() or is_float(x):
            result.push(x)

        elif x == '(':
            o_temp.push(x)
        elif x == ')':
            temp = o_temp.pop()
            while temp != '(':
                result.push(temp)
                temp = o_temp.pop()
        elif x in operators:
            if o_temp.top() != '(' and o_temp.top() != ')':
                if priority(x) <= priority(o_temp.top()):
                    result.push(o_temp.pop())
                    o_temp.push(x)
                    
                else:
                    o_temp.push(x)
            else:
                o_temp.push(x)
        i += 1
        

    x = o_temp.pop()
    while len(o_temp.stack) != 0 and x != '(':
        result.push(x)
        x = o_temp.pop()

    return result


def evaluation(stack, data_type):
    result = Stack(len(stack.stack), float)

    for i in range(len(stack.stack)):
        x = stack.stack[i]
        if x.lstrip('-').isdigit() or is_float(x):
            result.push(data_type(x))
        else:
                if stack.is_empty():
                    return 'error'
                a = result.pop()
                if stack.is_empty():
                    return 'error'
                b = result.pop()
                try:
                    match x:
                        case '+':
                            result.push(a + b)
                        case '-':
                            result.push(b - a)
                        case '*':
                            result.push(a * b)
                        case '/':
                            result.push(b / a)
                except:
                    return 'error'
    if result.top_in == 0:
        return result.top()
    else:
        return 'error'


input_equation = "( 3 * 6 + 2 ) + ( 14 / 3 + 4 )"

s = Stack(len(input_equation), str)
print("Input Equation:", input_equation)
is_error = get_equation(s, input_equation)

if not is_error:
    print("Infix Expression:", s.stack)

    s = infix_to_postfix(s, input_equation)
    

    print("Postfix Expression: ", end="")
    s.print_stack()
    value = evaluation(s, float)
    if value != 'error':
        print(f"The result: {value}")
    else:
        print("Error in postfix calculation.")

else:
    print("Wrong input")