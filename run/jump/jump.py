from readchar import readkey, key
import subprocess
import os


EXTENSIONS = {
    '.png':1,
    '.mp4':3,
}
COMMANDS = [
    'nvim',
    'feh',
    'mpv',
]


def print_lines(lines):
    for line in lines:
        try:
            print(line['name'])
        except:
            print('error')

def clear_line(): print("\033[A                                 \033[A") #]]
def gen_line(name, command, parent, isdir=False): return {'name':name, 'command':command, 'parent':parent, 'isdir':isdir, 'preview':False}
def generate_lines(path, show_hidden, parent):
    result = []
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
        result.append(new_line)
    return result

def get_parents(line, lines):
    parent = line['parent']
    parents = [line]
    while parent > 0:
        parents.append(lines[parent])
        parent = lines[parent]['parent']
    return parents

def get_path(line, lines):
    parents = get_parents(line, lines)
    path = ''
    for parent in parents:
        path = parent['name'] + path
    return path


class Lister:
    def __init__(self):
        self.chosen = 1
        self.printed = 0
        self.lines = [{}]
        self.show_hidden = False


    def clear(self):
        for _ in range(1, self.printed):
            clear_line()
        self.printed = 0


    def draw(self):
        for i in range(1, len(self.lines)):
            line = self.lines[i]
            margin = ''
            parents = get_parents(line, self.lines)
            for _ in parents:
                margin += '    '
            if i == self.chosen:
                print(f"{margin}=> {line['name']}")
            else:
                print(f"{margin}   {line['name']}")
        self.printed += len(self.lines)


    def move(self, go_up):
        if go_up and self.chosen > 1: self.chosen -= 1
        elif not go_up and self.chosen < len(self.lines)-1: self.chosen += 1
        self.clear()
        self.draw()


    def choose(self):
        self.clear()
        self.chosen = 1
        self.lines = [{}]
        self.lines.extend(generate_lines('.', self.show_hidden, 0))

        self.draw()
        try:
            while True:
                k = readkey()
                if   k == key.ENTER:              self.enter()     ; break
                elif k == key.BACKSPACE:          self.backspace() ; break
                elif k == 'h':                    self.hidden()    ; break
                elif k == 'k' or k == key.UP:     self.move(True)
                elif k == 'j' or k == key.DOWN:   self.move(False)
                elif k == 'l' or k == key.RIGHT:  self.right()
                elif k == 'h' or k == key.LEFT:   self.left()
        except KeyboardInterrupt: pass
        return os.getcwd()

    def enter(self):
        line = self.lines[self.chosen]
        if line['command'] == 0:
            os.chdir(get_path(line, self.lines))
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
            path = get_path(line, self.lines)
            self.lines[self.chosen+1:self.chosen+1] = generate_lines(path, self.show_hidden, self.chosen)
            self.lines[self.chosen]['preview'] = True
            self.clear()
            self.draw()

    def left(self):
        line = self.lines[self.chosen]
        if line['isdir'] and line['preview']:
            parents = get_parents(line, self.lines)
            parents_ids = []
            for parent in parents:
                parents_ids.append(parent['parent'])
            next = self.chosen + 1
            while True:
                if next == len(self.lines): break
                elif self.lines[next]['parent'] in parents_ids: break
                else:
                    del self.lines[next]
            self.lines[self.chosen]['preview'] = False
            self.clear()
            self.draw()

    def hidden(self):
        self.show_hidden = not self.show_hidden
        self.choose()




if __name__ == '__main__':
    lister = Lister()
    cd = lister.choose()
    lister.clear()
    print(cd)

























