import argparse, os

PATH = os.path.dirname(os.path.abspath(__file__))


class Backup():

    def publish(self, repo):
        server_cmd = f"cd {repo}/public_html && git pull origin master" # && python manage.py collectstatic --noinput
        local_cmd = f'sshpass -f {PATH}/config/pswd.txt ssh -t cz18090@185.114.247.170 "{server_cmd}"' 
        os.system(local_cmd)

    def backup(self, repo):
        if not os.path.isdir('.git'):
            print('No git repo was found')
            os.system('git init')
            os.system('git branch backup')
            os.system(f'gh repo create {repo} --private || echo "Github repo already exists"')
            os.system(f'git remote add origin git@github.com:Medik2007/{repo}.git')
            print('Git repo created and remote added')
        print('Searching for changes...')
        os.system('git switch -q backup')
        os.system('git add -A')
        if os.system('git diff --quiet && git diff --cached --quiet'):
            print('Uploading changes...')
            os.system('git commit -m "Backup"')
            os.system('git push origin backup')
        else:
            print('There are no changes')
        os.system('git switch -q master')

    def main(self, args):
        os.chdir(os.path.expanduser('~'))
        if not args.repo:
            print('\n===> System backup\n')
            self.backup('config')

            if os.path.isdir('nts'):
                os.chdir('nts')
                print('\n===> Notes backup\n')
                self.backup('notes')
                os.chdir(os.path.expanduser('~'))

            if os.path.isdir('.password-store'):
                os.chdir('.password-store')
                print('\n===> Passwords backup\n')
                self.backup('pass')
                os.chdir(os.path.expanduser('~'))
            
            print('\n===> Projects backup')
            if os.path.isdir('prj'):
                os.chdir('prj')
                for dir in os.listdir('.'):
                    if dir[0] == '.':
                        continue
                    elif os.path.isdir(dir):
                        print(f'\n=> {dir}')
                        os.chdir(dir)
                        self.backup(dir)
                        os.chdir('..')
        else:
            if args.repo == 'config':
                os.chdir(os.path.expanduser('~'))
            else:
                os.chdir('prj/' + args.repo)
            print(f'\n=> {args.repo}')
            self.backup(args.repo)


        if args.publish:
            print(f'\nPublishing {args.publish}')
            self.publish(args.publish)
        if args.poweroff:
            os.system('poweroff')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Backup program")

    parser.add_argument("-r", "--repo", type=str, help="backup only one repo", default=None)
    parser.add_argument("-p", "--publish", type=str, help="publish repo to server", default=None)
    parser.add_argument("-pr", "--publish-repo", type=str, help="backup only one repo and publish it", default=None)
    parser.add_argument('-o', '--poweroff', action='store_true', help="poweroff after backup")

    args = parser.parse_args()

    if args.publish_repo:
        args.repo = args.publish_repo
        args.publish = args.publish_repo

    backup = Backup()
    backup.main(args)
