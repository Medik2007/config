def input_int(text=''):
    response = ''
    print(text, end='')
    while True:
        try:
            response = int(input())
            break
        except ValueError:
            print('Input a number')
    return response


def input_y_n(text, preference=''):
    y = 'y'
    n = 'n'
    if preference == 'y': y = 'Y'
    elif preference == 'n': n = 'N'
    action = input(f'{text} ({y}/{n}) ').lower()
    if action == 'y' or action == 'yes':
        return True
    elif action == 'n' or action == 'no':
        return False
    elif action == '':
        if preference == 'y': return True
        elif preference == 'n': return False
    else: input_y_n(text, preference)
