import sys, termios, tty


class Editor():
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key

    def render(self, lines, cursor_row):
        sys.stdout.write("\033[H\033[J") #]]
        for i, line in enumerate(lines):
            if i == cursor_row:
                sys.stdout.write(f"> {line}\n")
            else:
                sys.stdout.write(f"  {line}\n")

    def main(self, lines):
        cursor_row = 0
        while True:
            self.render(lines, cursor_row)
            key = self.get_key()

            if key == "\r": # Enter
                cursor_row += 1
                lines.insert(cursor_row, "")

            elif key == "\x7f": # Backspace
                if lines[cursor_row]:
                    lines[cursor_row] = lines[cursor_row][:-1]
                elif cursor_row > 0:
                    lines.pop(cursor_row)
                    cursor_row -= 1

            elif key == "\033":  # Arrow keys
                next_key = self.get_key()
                if next_key == "[": #]
                    direction = self.get_key()
                    if direction == "A" and cursor_row > 0: # Up
                        cursor_row -= 1
                    elif direction == "B" and cursor_row < len(lines) - 1: # Down
                        cursor_row += 1

            elif key == "\x03": # ^C
                 break

            else:
                lines[cursor_row] += key

        return lines
