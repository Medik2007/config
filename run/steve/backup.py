import argparse, os


class Backup():

    def backup(self, repo):
        if not os.path.isdir('.git'):
            print('No git repo was found')
            os.system('git init')
            os.system(f'gh repo create {repo} --private || echo "Github repo already exists"')
            os.system(f'git remote add origin git@github.com:Medik2007/{repo}.git')
            print('Git repo created and remote added')
        print('Searching for changes...')
        os.system('git add -A')
        if os.system('git diff --quiet && git diff --cached --quiet'):
            print('Uploading changes...')
            os.system('git commit -m "Backup"')
            os.system('git push origin master')
        else:
            print('There are no changes')

    def main(self):
        print('\n===> System backup\n')
        os.chdir(os.path.expanduser('~'))
        self.backup('config')
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Backup program")

    backup = Backup()
    backup.main()
