from readchar import readkey, key
import subprocess
import os
import sys


def clear_line(): sys.stdout.write('\x1b[1A') ; sys.stdout.write('\x1b[2K') #]]

EXTENSIONS = {
    '.png':1,
    '.mp4':3,
}
COMMANDS = [
    'nvim',
    'feh',
    'mpv',
]


class Lister:
    def __init__(self):
        self.counter = 0
        self.chosen = 0
        self.lines = {}
        self.positions = []
        self.show_hidden = False


    ##########
    ## MAIN ##
    ##########


    def main(self):
        self.clear()
        self.counter = 1
        self.lines = {0:self.gen_line(0, '', 0, 0)}
        self.generate_lines('.', 0)
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

    def gen_line(self, id, name, command, parent, isdir=False):
        return {'id':id, 'name':name, 'command':command, 'parent':parent, 'isdir':isdir, 'children':[]}

    def generate_lines(self, path, parent):
        result = {}
        ids = []
        for name in os.listdir(path):
            current_path = path + '/' + name
            if not self.show_hidden and name.startswith('.'):
                continue
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

        if parent != 0:
            for id in ids:
                self.positions.insert(self.chosen, id)
        else:
            self.positions = ids

        self.lines.update(result)
        return ids


    ##########
    ## GETS ##
    ##########


    def get_chosen(self):
        return self.lines[self.positions[self.chosen]]

    def get_parents(self, id):
        parents = [id]
        parent = self.lines[id]['parent']
        while parent != 0:
            parents.append(parent)
            parent = self.lines[parent]['parent']
        return parents

    def get_path(self):
        parents = self.get_parents(self.get_chosen())
        path = ''
        for parent in parents:
            path = self.lines[parent]['name'] + path
        return path


    #############
    ## DRAWING ##
    #############


    def draw_line(self, line):
        info = line['id'], line['parent']
        return f"{line['name']} --- {info}"

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
        chosen = self.get_chosen()
        for i in range(1, len(self.lines)):
            line = self.lines[i]
            if line['parent'] != 0:
                continue
            if i == chosen:
                print(f"=> {self.draw_line(line)}")
            else:
                print(f"   {self.draw_line(line)}")
            if line['children']:
                self.draw_children(line['children'], chosen, 1)

    def clear(self):
        for _ in range(len(self.lines)):
            clear_line()


    #################
    ## KEY PRESSES ##
    #################


    def enter(self):
        line = self.lines[self.get_chosen()]
        if line['command'] == 0:
            os.chdir(self.get_path())
        else:
            command = COMMANDS[line['command']]
            name = line['name']
            subprocess.call([command, name])
        self.main()

    def backspace(self):
        os.chdir('..')
        self.main()

    def right(self):
        line = self.lines[self.get_chosen()]
        if line['isdir'] and not line['children']:
            path = self.get_path()
            new_ids = self.generate_lines(path, self.get_chosen())
            self.lines[self.get_chosen()]['children'] = new_ids
            self.clear()
            self.draw()

    def delete_children(self, children):
        for child in children:
            if self.lines[child]['children']:
                self.delete_children(self.lines[child]['children'])
            del self.lines[child]['children']
    def left(self):
        line = self.lines[self.get_chosen()]
        if line['isdir'] and line['children']:
            self.delete_children(line['children'])
            self.lines[self.get_chosen()]['children'] = []
            self.clear()
            self.draw()

    def hidden(self):
        self.show_hidden = not self.show_hidden
        self.main()

    def move(self, go_up):
        if go_up and self.chosen > 0: self.chosen -= 1
        elif not go_up and self.chosen < len(self.lines)-2: self.chosen += 1
        self.clear()
        self.draw()



if __name__ == '__main__':
    lister = Lister()
    lister.main()

























