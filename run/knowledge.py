import os, argparse, json, os, tempfile

PATH = os.path.dirname(os.path.abspath(__file__))



class Knowledge():
    def read_data(self):
        with open(f'{PATH}/data/knowledge.json', 'r') as file:
            return json.load(file)
    def write_data(self, data):
        with open(f'{PATH}/data/knowledge.json', 'w') as file:
            json.dump(data, file, indent=4)
    def input_int(self, text=''):
        response = ''
        print(text, end='')
        while True:
            try:
                response = int(input())
                break
            except ValueError:
                print('Input a number')
        return response


    def editor(self, lines):
        pass


    def open_record(self, record=None, lines=[''], is_new=True):
        data = self.read_data()
        if record:
            lines = data[record]
            is_new = False
        lines = self.editor(lines)

        if lines[0].replace(' ', '') == '':
            input("Enter the record's title as first line")
            self.open_record(lines=lines)
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
                if action.lower == 'e':
                    self.open_record(lines=lines, is_new=is_new)

        if lines[1].replace(' ', '') == '':
            lines[1] = 'Theme'
        #theme = lines[1]

        if lines[2].replace(' ', '') != '':
            lines.insert(2, '')


        data[title] = lines
        self.write_data(data)


    def search(self, query):
        data = self.read_data()
        answers = set(data.keys())

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
                id = self.input_int()
                if id > len(answers)-1:
                    print(f'Input a number between 0 and {len(answers)-1}')
                    continue
                break

        elif len(answers) == 0:
            print('No entries found')
            return

        border = "~"*len(answers[id])
        print(f'\n{border}\n{answers[id]}\n{border}\n')
        print(data[answers[id]])


    def main(self, args):
        if args.query:
            self.search(args.query)
        else:
            self.open_record()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Knowledge Base system")
    parser.add_argument('query', nargs='*', help="search query to the knowledge base")
    args = parser.parse_args()

    knowledge = Knowledge()
    try:
        knowledge.main(args)
    except KeyboardInterrupt:
        pass
