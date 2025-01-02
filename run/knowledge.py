import os, argparse, json, sys, tty, termios

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
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # Set terminal to raw mode
            key = sys.stdin.read(1)  # Read a single character
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Restore settings
        return key
    def render_text(self, lines, cursor_row):
        sys.stdout.write("\033[H\033[J")  # Clear the terminal]]
        for i, line in enumerate(lines):
            # Highlight the line with the cursor
            if i == cursor_row:
                sys.stdout.write(f"> {line}\n")
            else:
                sys.stdout.write(f"  {line}\n")


    def write(self):
        #title = input()
        #print('~'*len(title) + '\n')
        lines = [""]
        cursor_row = 0
        try:
            while True:
                self.render_text(lines, cursor_row)
                key = self.get_key()

                if key == "\r":  # Enter key
                    cursor_row += 1
                    lines.insert(cursor_row, "")
                elif key == "\x7f":  # Backspace key
                    if lines[cursor_row]:
                        # Delete the last character in the current line
                        lines[cursor_row] = lines[cursor_row][:-1]
                    elif cursor_row > 0:
                        # If the line is empty, delete the line and move the cursor up
                        lines.pop(cursor_row)
                        cursor_row -= 1
                elif key == "\033":  # Arrow keys (start with ESC)
                    next_key = self.get_key()
                    if next_key == "[":#]
                        direction = self.get_key()
                        if direction == "A" and cursor_row > 0:  # Up arrow
                            cursor_row -= 1
                        elif direction == "B" and cursor_row < len(lines) - 1:  # Down arrow
                            cursor_row += 1
                elif key == "\x03":
                     break
                else:
                    # Append the typed character to the current line
                    lines[cursor_row] += key
        except KeyboardInterrupt:
            pass

        #data = self.read_data()
        #data[title] = text
        #self.write_data(data)


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
            self.write()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Knowledge Base system")
    parser.add_argument('query', nargs='*', help="search query to the knowledge base")
    args = parser.parse_args()

    knowledge = Knowledge()
    try:
        knowledge.main(args)
    except KeyboardInterrupt:
        pass
