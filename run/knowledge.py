import os, argparse, json, os, tempfile
from tools import input_int, input_y_n

PATH = os.path.dirname(os.path.abspath(__file__))
EDITOR = 'nvim'



class Knowledge():
    def read_data(self):
        with open(f'{PATH}/knowledge/knowledge.json', 'r') as file:
            return json.load(file)
    def write_data(self, data):
        with open(f'{PATH}/knowledge/knowledge.json', 'w') as file:
            json.dump(data, file)


    def editor(self, text='', path=None):
        if path:
            os.system(f'{EDITOR} {path}')
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as file:
                file.write(text.encode('utf-8'))
                temp = file.name
            try:
                os.system(f'nvim {temp}')
                with open(temp, 'r') as file:
                    text = file.read()
            finally:
                os.remove(temp)
        return text 


    def edit(self, record=None, text='', is_new=True):
        data = self.read_data()
        old_title = None
        if record:
            text = data[record]
            is_new = False
            old_title = text.split('\n')[0]
        text = self.editor(text)
        lines = text.split('\n')

        if text.rstrip() == '':
            print('Input is empty')
            return

        if lines[0].replace(' ', '') == '':
            input("Enter the record's title as first line")
            self.edit(text=text)
            return

        title = lines[0]

        if title in data and is_new:
            while True:
                print('There is already a record with such title')
                print('O - Overwrite existing record with new input')
                print('E - Edit new input')
                action = input()
                if action.lower() == 'o':
                    print('Are you sure you want to overwrite existing record? (Y/n)')
                    action = input()
                    if action.lower() == 'y' or action.lower() == 'yes' or action == '':
                        break
                    else:
                        print()
                        continue
                elif action.lower() == 'e':
                    self.edit(text=text, is_new=is_new)
                    return

        if len(lines) == 1 or lines[1].replace(' ', '') == '':
            input("\nERR: You should write the record's theme as the second line of file")
            self.edit(text=text, is_new=is_new)
            return
        elif len(lines[1].split()) > 1:
            input("\nERR: Record's theme should be a single word")
            self.edit(text=text, is_new=is_new)
            return
        #theme = lines[1].lower()

        if len(lines) > 2:
            if lines[2].replace(' ', '') != '':
                lines.insert(2, '')
                text = '\n'.join(lines)

        if old_title and old_title != title:
            del data[old_title]

        data[title] = text
        self.write_data(data)


    def search(self, query, all, delete):
        data = self.read_data()
        answers = set(data.keys())

        if not all:
            for record in data.keys():
                for word in query:
                    if word.lower() not in record.lower():
                        try: answers.remove(record)
                        except KeyError: continue
        answers = list(answers)
        id = 0

        if len(answers) > 1:
            for n, a in enumerate(answers):
                print(f'{n}. {a}')
            print()
            while True:
                id = input_int()
                if id > len(answers)-1:
                    print(f'Input a number between 0 and {len(answers)-1}')
                    continue
                break

        elif len(answers) == 0:
            print('No entries found')
            return

        if delete:
            if input_y_n(f'\nAre you sure you want to delete record {answers[id]}?', 'n'):
                del data[answers[id]]
                self.write_data(data)
                print('Record deleted')
            else:
                print('Aborting')
            return
        self.edit(record=answers[id])


    def main(self, args):
        if args.query or args.all:
            self.search(args.query, args.all, args.delete)
        elif args.delete:
            print('Specify which record to delete')
        else:
            self.edit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Knowledge Base system")
    parser.add_argument('-a', '--all', action='store_true', help="display all records")
    parser.add_argument('-d', '--delete', action='store_true', help="delete chosen record")
    parser.add_argument('query', nargs='*', help="search query to the knowledge base")
    args = parser.parse_args()

    knowledge = Knowledge()
    try:
        knowledge.main(args)
    except KeyboardInterrupt:
        pass
