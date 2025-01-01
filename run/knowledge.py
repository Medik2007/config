import os, argparse, json

PATH = os.path.dirname(os.path.abspath(__file__))


class Knowledge():

    def main(self):
        title = input()
        command = input()

        with open(f'{PATH}/data/jump.json', 'r') as file:
            data = json.load(file)

        data['commands'][title] = command

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Jumping program")
    parser.add_argument('file', nargs='?', default='default.txt', help="File to process (default: default.txt)")
    args = parser.parse_args()

    knowledge = Knowledge()
    knowledge.main()
