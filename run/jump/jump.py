from readchar import readkey, key
import subprocess
import os
import sys


def clear_line(): sys.stdout.write('\x1b[1A') ; sys.stdout.write('\x1b[2K') #]]

# Lister

EXTENSIONS = {
    '.png':2,
    '.mp4':3,
}
COMMANDS = [
    'cd',
    'nvim',
    'feh',
    'mpv',
]

# Jumper

JUMP_DIRS = [
    '.config/',
    'prj/',
    'run/',
    'stf/books/',
    'stf/iso/',
    'stf/',
]



class Jumper:
    def __init__(self, dest):
        self.main(dest)

    def check_env(self, path, dir):
        if os.path.isfile('pyvenv.cfg'):
            if os.path.isfile(f'{dir}/manage.py'):
                os.system(f'kitty @ launch --type tab --cwd current sh -c "source bin/activate && cd {dir} && nvim; exec $SHELL"')
                os.system(f'sh -c "source {path}/bin/activate && cd {dir} && python manage.py runserver"')
            else:
                os.system(f'sh -c "source {path}/bin/activate && cd {path}/{dir} && nvim"')

    def main(self, dest):
        end = False
        old_path = os.getcwd()
        os.chdir(os.path.expanduser('~'))
        for dir in JUMP_DIRS:
            if end: break
            if os.path.isdir(f'{dir}{dest}'):
                os.chdir(f'{dir}{dest}')
                children = os.listdir('.')
                for child in children:
                    if child.startswith(dest):
                        end = True
                        if os.path.isdir(child):
                            self.check_env(os.getcwd(), child)
                        else:
                            subprocess.run(['nvim', child])
                    elif child.startswith('main'):
                        end = True
                        subprocess.run(['nvim', child])
                    if end:
                        break
                if not end:
                    end = True
                    subprocess.run(['nvim'])
        if not end:
            os.chdir(old_path)
            lister = Lister(dest)
            lister.main(True)



class Lister:
    def __init__(self, dir=''):
        self.counter = 0
        self.chosen = 0
        self.lines = {}
        self.show_hidden = False
        self.input_mode = False
        self.input_text = ''
        if dir:
            if os.path.isdir(dir):
                os.chdir(dir)
            else:
                self.input_text = dir
                self.input_mode = True


    ##########
    ## MAIN ##
    ##########


    def main(self, first_time=False):
        if not first_time: self.clear()
        self.counter = 1
        self.chosen = 0
        self.lines = {0:self.gen_line(0, '', 0, 0)}
        self.generate_lines('.', 0)
        self.draw()

        try:
            while True:
                k = readkey()
                if   k == key.RIGHT:  self.right()
                elif k == key.LEFT:   self.left()
                elif k == key.UP:     self.move(True)
                elif k == key.DOWN:   self.move(False)
                elif k == key.TAB:    self.set_input(False)
                elif k == key.CTRL_L: os.system('clear') ; self.draw()
                elif k == key.CTRL_H: self.hidden() ; break
                elif not self.input_mode:
                    if   k == key.ENTER:  self.right(True)
                    elif k in ['=', '+']: self.enter() ; break
                    elif k == '-': self.back()         ; break
                    elif k == 'k': self.move(True)
                    elif k == 'j': self.move(False)
                    elif k == 'l': self.right()
                    elif k == 'h': self.left()
                    elif k == ':': self.set_input(True)
                else:
                    if   k == key.BACKSPACE: self.edit_input(backspace=True)
                    elif k == key.SPACE:     self.input_space()
                    elif k != key.ENTER:     self.edit_input(text=k)
        except KeyboardInterrupt: self.clear() ; exit(0)

    def gen_line(self, id, name, command, parent, isdir=False):
        return {'id':id, 'name':name, 'command':command, 'parent':parent, 'isdir':isdir, 'children':[]}

    def generate_lines(self, path, parent):
        listdir = os.listdir(path)
        input_text = self.input_text.split('_')[-1]
        result = {}
        ids = []
        for name in listdir:
            if not name.startswith(input_text):
                continue
            if not self.show_hidden and name.startswith('.'):
                if len(input_text) == 0 or input_text[0] != '.':
                    continue
            current_path = path + '/' + name
            _, ext = os.path.splitext(current_path)
            if ext == '':
                if os.path.isdir(current_path):
                    name += '/'
                    new_line = self.gen_line(self.counter, name, 0, parent, True)
                else:
                    new_line = self.gen_line(self.counter, name, 1, parent)
            else:
                if ext in EXTENSIONS:
                    new_line = self.gen_line(self.counter, name, EXTENSIONS[ext], parent)
                else:
                    new_line = self.gen_line(self.counter, name, 1, parent)
            result[self.counter] = new_line
            ids.append(self.counter)
            self.counter += 1

        key = list(self.lines.keys()).index(parent)
        lines = list(self.lines.items())
        if parent != 0: lines[key+1:key+1] = result.items()
        else:
            lines[0:] = result.items()

        self.lines = dict(lines)
        return ids


    ###########
    ## INPUT ##
    ###########


    def set_input(self, var):
        self.input_mode = var
        if not var: self.input_text = ''
        self.clear()
        self.draw()

    def edit_input(self, text='', backspace=False):
        if backspace:
            if len(self.input_text) > 0:
                if self.input_text[-1] == '_':
                    self.input_text = self.input_text[:-1]
                    self.back()
                else:
                    self.input_text = self.input_text[:-1]
        else:
            self.input_text += text
        self.main()

    def input_space(self):
        if len(self.input_text) > 0 and len(self.lines) > 0 and self.input_text[-1] != '_':
            self.input_text += '_'
            self.enter(True)


    ##########
    ## GETS ##
    ##########


    def get_chosen(self):
        return list(self.lines.keys())[self.chosen]

    def get_parents(self, id):
        parents = [id]
        parent = self.lines[id]['parent']
        while parent != 0:
            parents.append(parent)
            parent = self.lines[parent]['parent']
        return parents

    def get_path(self, id):
        parents = self.get_parents(id)
        path = ''
        for parent in parents:
            path = self.lines[parent]['name'] + path
        return path


    #############
    ## DRAWING ##
    #############


    def draw_line(self, line):
        info = f'' # For debugging
        return f"{line['name']}{info}"

    def draw_children(self, children, chosen, margin):
        text_margin = ''
        for _ in range(margin):
            text_margin += '    '
        for child in children:
            if child == chosen:
                print(f"{text_margin}=> {self.draw_line(self.lines[child])}")
            else:
                print(f"{text_margin}   {self.draw_line(self.lines[child])}")
            if self.lines[child]['children']:
                self.draw_children(self.lines[child]['children'], chosen, margin+1)

    def draw(self):
        path = os.getcwd()
        user_path = os.path.expanduser('~')
        if path.startswith(user_path):
            path = f'~{path[len(user_path):]}'
            if path == '~': path = '~/'
        print(f'{path}\n')
        if len(self.lines) > 0:
            chosen = self.get_chosen()
            for i in self.lines.keys():
                if i == 0: continue
                line = self.lines[i]
                if line['parent'] != 0:
                    continue
                if i == chosen:
                    print(f"=> {self.draw_line(line)}")
                else:
                    print(f"   {self.draw_line(line)}")
                if line['children']:
                    self.draw_children(line['children'], chosen, 1)
        if self.input_mode:
            print(f'\n  :{self.input_text}')
        else:
            print(f'\n   {self.input_text}')

    def clear(self):
        for _ in range(len(self.lines) + 4):
            clear_line()


    #################
    ## KEY PRESSES ##
    #################


    def enter(self, text=False):
        line = self.lines[self.get_chosen()]
        if line['command'] != 0:
            if text and self.input_text[-1] == '_':
                self.input_text = self.input_text[:-1]
                while self.input_text[-1] != '_':
                    self.input_text = self.input_text[:-1]
            name = line['name']
            command = COMMANDS[line['command']]
            subprocess.run([command, name])
        else:
            if line['parent'] != 0: line = self.lines[line['parent']]
            path = self.get_path(line['id'])
            if os.listdir(path): os.chdir(path)
        self.main()

    def back(self):
        os.chdir('..')
        self.main()

    def right(self, reverse=False):
        line = self.lines[self.get_chosen()]
        if line['command'] != 0:
            path = os.getcwd()
            if line['parent'] != 0:
                os.chdir(self.get_path(self.lines[line['parent']]['id']))
            name = line['name']
            command = COMMANDS[line['command']]
            subprocess.run([command, name])
            os.chdir(path)
        elif line['isdir'] and not line['children']:
            self.clear()
            path = self.get_path(line['id'])
            new_ids = self.generate_lines(path, self.get_chosen())
            self.lines[self.get_chosen()]['children'] = new_ids
            self.draw()
        elif reverse and line['children']:
            self.left()


    def delete_children(self, children):
        for child in children:
            if self.lines[child]['children']:
                self.delete_children(self.lines[child]['children'])
            del self.lines[child]
    def left(self):
        line = self.lines[self.get_chosen()]
        if line['isdir'] and line['children']:
            self.clear()
            self.delete_children(line['children'])
            self.lines[self.get_chosen()]['children'] = []
            self.draw()

    def hidden(self):
        self.show_hidden = not self.show_hidden
        self.main()

    def move(self, go_up):
        if go_up and self.chosen > 0: self.chosen -= 1
        elif not go_up and self.chosen < len(self.lines)-1: self.chosen += 1
        self.clear()
        self.draw()



if __name__ == '__main__':
    argv = sys.argv
    l = len(argv)
    if l == 1:
        lister = Lister()
        lister.main(True)
    elif l == 2:
        Jumper(argv[1])
    else:
        print('Jump takes one or no arguments')

