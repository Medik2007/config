from readchar import readkey, key
import subprocess
import os
import sys


EXTENSIONS = {
    '.png':1,
    '.mp4':3,
}
COMMANDS = [
    'nvim',
    'feh',
    'mpv',
]
counter = 0


def print_lines(lines):
    print('-----')
    for line in lines:
        try:
            print(line['name'])
        except:
            print('error')
    print('-----')

def send_output(text):
    subprocess.call(['/home/medik/.config/hypr/scripts/notifications/notif.sh', 'normal', 'volume', text], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def signal():
    print('bruuuuuuuuuuuuuuuh\na\na\na\na\na\na\na\na')


def clear_line():
    #print('') ; return
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    #]]

def gen_line(name, command, parent, isdir=False): return {'name':name, 'command':command, 'parent':parent, 'isdir':isdir, 'preview':False}
def generate_lines(path, show_hidden, parent):
    result = {}
    global counter
    for name in os.listdir(path):
        current_path = path + '/' + name
        if not show_hidden and name.startswith('.'):
            continue
        _, ext = os.path.splitext(current_path)
        if ext == '':
            if os.path.isdir(current_path):
                name += '/'
                new_line = gen_line(name, 0, parent, True)
            else:
                new_line = gen_line(name, 1, parent)
        else:
            if ext in EXTENSIONS:
                new_line = gen_line(name, EXTENSIONS[ext], parent)
            else:
                new_line = gen_line(name, 1, parent)
        result[counter] = new_line
        counter += 1
    return result


def get_parents(id, lines):
    parents = [id]
    parent = lines[id]['parent']
    while parent != 0:
        parents.append(parent)
        parent = lines[parent]['parent']
    return parents

def get_path(id, lines):
    parents = get_parents(id, lines)
    path = ''
    for parent in parents:
        path = lines[parent]['name'] + path
    return path

def get_children(id, lines):
    source_ids = get_parents(id, lines)
    source_ids.reverse()
    source_ids.insert(0, 0)
    source_ids.pop()
    children = []
    while True:
        id += 1
        children.append(id)
        if id > len(lines)-1 or lines[id]['parent'] in source_ids:
            children.pop()
            break 
    return children


class Lister:
    def __init__(self):
        self.chosen = 1
        self.printed = 0
        self.lines = {}
        self.show_hidden = False


    def clear(self):
        for _ in range(1, self.printed):
            clear_line()
        self.printed = 0


    def draw(self):
        for i in range(1, len(self.lines)):
            line = self.lines[i]
            margin = ''
            parents = get_parents(i, self.lines)
            for _ in parents:
                margin += '    '
            if i == self.chosen:
                print(f"{margin}=> {line['name']} : {line['parent']}")
            else:
                print(f"{margin}   {line['name']} : {line['parent']}")
        self.printed += len(self.lines)


    def move(self, go_up):
        if go_up and self.chosen > 1: self.chosen -= 1
        elif not go_up and self.chosen < len(self.lines)-1: self.chosen += 1
        self.clear()
        self.draw()


    def choose(self):
        global counter
        counter = 0
        self.clear()
        self.chosen = 1
        self.lines = {}
        self.lines.update(generate_lines('.', self.show_hidden, 0))

        self.draw()
        try:
            while True:
                k = readkey()
                if   k == key.ENTER:              self.enter()     ; break
                elif k == key.BACKSPACE:          self.backspace() ; break
                elif k == 'd':                    self.hidden()    ; break
                elif k == 'k' or k == key.UP:     self.move(True)
                elif k == 'j' or k == key.DOWN:   self.move(False)
                elif k == 'l' or k == key.RIGHT:  self.right()
                elif k == 'h' or k == key.LEFT:   self.left()
        except KeyboardInterrupt: pass
        lister.clear()


    def enter(self):
        line = self.lines[self.chosen]
        if line['command'] == 0:
            os.chdir(get_path(self.chosen, self.lines))
        else:
            command = COMMANDS[line['command']]
            name = line['name']
            subprocess.call([command, name])
        self.choose()

    def backspace(self):
        os.chdir('..')
        self.choose()

    def right(self):
        line = self.lines[self.chosen]
        if line['isdir'] and not line['preview']:
            path = get_path(self.chosen, self.lines)
            self.lines.update(generate_lines(path, self.show_hidden, self.chosen))
            self.lines[self.chosen]['preview'] = True
            self.clear()
            self.draw()

    def left(self):
        line = self.lines[self.chosen]
        if line['isdir'] and line['preview']:
            children = get_children(self.chosen, self.lines)
            for _ in children:
                del self.lines[self.chosen+1]
            self.lines[self.chosen]['preview'] = False
            self.clear()
            self.draw()

    def hidden(self):
        self.show_hidden = not self.show_hidden
        self.choose()




if __name__ == '__main__':
    lister = Lister()
    lister.choose()

























