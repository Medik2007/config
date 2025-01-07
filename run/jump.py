import argparse, os, json, sys

PATH = os.path.dirname(os.path.abspath(__file__))

try:
    with open(f'{PATH}/config/jump.json', 'r') as file:
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
                os.system(f'sh -c "sshpass -f {PATH}/config/pswd.txt ssh cz18090@185.114.247.170; exec $SHELL"')
            return
        
        for dir in JUMP_DIRS:
            if os.path.isdir(f'{dir}{dest}'):
                os.chdir(f'{dir}{dest}')
                if args.jump:
                    pass
                elif os.path.isdir(VENV + dest):
                    # DJANGO
                    if os.path.isfile(f'manage.py'):
                        if not args.server and not args.code:
                            os.system(f'kitty @ launch --type tab --cwd current {self.act_run(dest, "nvim")}')
                            os.system(self.act_run(dest, 'python manage.py runserver 0.0.0.0:8000'))
                        elif args.code:
                            os.system(self.act_run(dest, 'nvim'))
                        elif args.server:
                            os.system(self.act_run(dest, 'python manage.py runserver 0.0.0.0:8000'))
                    # DEFAULT
                    elif not args.server:
                        os.system(self.act_run(dest, 'nvim'))
                elif not args.server:
                    os.system('nvim')
                os.system(f'sh -c "cd ~/{dir}{dest}; exec $SHELL"')
                break
            elif os.path.isfile(f'{dir}{dest}'):
                # FILE
                if not args.server:
                    os.system(f'nvim {dir}{dest}')
                os.system(f'sh -c "cd ~/{dir}; exec $SHELL"')
                break
        else:
            print('Jump destination not found')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Jumping program")

    parser.add_argument("destination", help="Jump destination")
    parser.add_argument('-c', '--code',   action='store_true', help="only open code")
    parser.add_argument('-s', '--server', action='store_true', help="only start django server")
    parser.add_argument('-j', '--jump', action='store_true', help="only jump, don't open any programs")

    args = parser.parse_args()

    jump = Jump()
    jump.main(args)
