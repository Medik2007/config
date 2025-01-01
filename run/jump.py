import argparse, os, json, sys

PATH = os.path.dirname(os.path.abspath(__file__))

try:
    with open(f'{PATH}/data/jump.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Data file not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Data file is corrupted.")
    sys.exit(1)

VENV      = os.path.expanduser(data['venv'])
JUMP_DIRS = data['jump_dirs']
SHORTCUTS = data['shortcuts']
FUNCTIONS = data['functions']



class Jump():

    def act_run(self, dest, command):
        return f'sh -c "source {VENV}{dest}/bin/activate && {command}; exec $SHELL"'

    def main(self, args):
        os.chdir(os.path.expanduser('~'))
        dest = args.destination

        if dest in SHORTCUTS:
            os.system(f'sh -c "cd {os.path.expanduser(SHORTCUTS[dest])}; exec $SHELL"')
            return

        if dest in FUNCTIONS:
            if dest == 'server':
                os.system(f'sh -c "sshpass -f {PATH}/data/pswd.txt ssh cz18090@185.114.247.170; exec $SHELL"')
            return
        
        for dir in JUMP_DIRS:
            if os.path.isdir(f'{dir}{dest}'):
                os.chdir(f'{dir}{dest}')
                if args.jump_only:
                    os.system(f'sh -c "cd ~/{dir}{dest}; exec $SHELL"')
                    break
                if os.path.isdir(VENV + dest):
                    # DJANGO
                    if os.path.isfile(f'manage.py'):
                        if args.server and args.code:
                            os.system(f'kitty @ launch --type tab --cwd current {self.act_run(dest, "nvim")}')
                            os.system(self.act_run(dest, 'python manage.py runserver 0.0.0.0:8000'))
                        elif args.code:
                            os.system(self.act_run(dest, 'nvim'))
                        elif args.server:
                            os.system(self.act_run(dest, 'python manage.py runserver 0.0.0.0:8000'))
                    # DEFAULT
                    elif args.code:
                        os.system(self.act_run(dest, 'nvim'))
                elif args.code:
                    os.system('nvim')
                os.system(f'sh -c "cd ~/{dir}{dest}; exec $SHELL"')
                break
        else:
            print('Jump destination not found')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Jumping program")

    parser.add_argument("destination", help="Jump destination")
    parser.add_argument('-s', '--server', action='store_false', help="don't start django server")
    parser.add_argument('-c', '--code',   action='store_false', help="don't open code")
    parser.add_argument('-j', '--jump-only', action='store_true', help="don't start any programs, only cd")

    args = parser.parse_args()

    jump = Jump()
    jump.main(args)
