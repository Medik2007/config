from readchar import readkey, key
import subprocess
import os


def clear_line():
    print("\033[A                                 \033[A") #]]



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


class Lister:
    def __init__(self):
        self.chosen = 0
        self.printed = 0
        self.strings = []
        self.actions = [] # 0 - cd, 1 - nv, 2 - feh
        self.show_hidden = False
        self.preview_dirs = []


    def clear(self):
        for _ in range(self.printed):
            clear_line()
        self.printed = 0


    def draw(self):
        for i in range(len(self.strings)):
            line = self.strings[i]
            if i == self.chosen:
                print(f'=> {line}')
            else:
                print(f'   {line}')
            if os.path.isdir(line) and self.preview_dirs[i]:
                children = os.listdir(line)
                for j in children:
                    if os.path.isdir(line+j): print(f'       {j}/')
                    else:                     print(f'       {j}')
                    if not self.show_hidden and j.startswith('.'):
                        clear_line()
                    else:
                        self.printed += 1
                if len(children) == 0:
                    print('')
                    self.printed += 1
        self.printed += len(self.strings)


    def move(self, go_up):
        if go_up and self.chosen > 0:
            self.chosen -= 1;
        elif not go_up and self.chosen < len(self.strings)-1:
            self.chosen += 1;
        self.clear()
        self.draw()


    def choose(self):
        self.clear()
        self.strings = []
        self.preview_dirs = []
        all_strings = os.listdir()

        for s in all_strings:
            if not self.show_hidden and s.startswith('.'):
                continue
            _, ext = os.path.splitext(s)
            if ext == '':
                if os.path.isdir(s):
                    s += '/'
                    self.actions.append(0)
                else:
                    self.actions.append(1)
            else:
                if ext in EXTENSIONS:
                    self.actions.append(EXTENSIONS[ext])
                else:
                    self.actions.append(1)
            self.strings.append(s)
            self.preview_dirs.append(False)
        if self.chosen > len(self.strings):
            self.chosen = len(self.strings)-1

        self.draw()
        try:
            while True:
                k = readkey()
                if k == key.ENTER:
                    command = COMMANDS[self.actions[self.chosen]]
                    name = self.strings[self.chosen]
                    if command == 'cd':
                        os.chdir(name)
                    else:
                        subprocess.call([command, name])
                    self.choose()
                    break
                elif k == key.BACKSPACE:
                    os.chdir('..')
                    self.choose()
                    break
                elif k == 'k' or k == key.UP:
                    self.move(True)
                elif k == 'j' or k == key.DOWN:
                    self.move(False)
                elif k == 'l' or k == key.LEFT:
                    if os.path.isdir(self.strings[self.chosen]):
                        self.preview_dirs[self.chosen] = not self.preview_dirs[self.chosen]
                        self.clear()
                        self.draw()
                elif k == 'h':
                    self.show_hidden = not self.show_hidden
                    self.choose()
                    break
        except KeyboardInterrupt:
            pass
        return os.getcwd()




if __name__ == '__main__':
    lister = Lister()
    cd = lister.choose()
    lister.clear()
    print(cd)

























