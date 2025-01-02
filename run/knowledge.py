import os, argparse, json

PATH = os.path.dirname(os.path.abspath(__file__))


class Knowledge():
    def read_data(self):
        with open(f'{PATH}/data/knowledge.json', 'r') as file:
            return json.load(file)
    def write_data(self, data):
        with open(f'{PATH}/data/knowledge.json', 'w') as file:
            json.dump(data, file, indent=4)


    def write(self):
        title = input()
        command = input()

        data = self.read_data()
        data[title] = command
        self.write_data(data)


    def search(self, query_text):
        records = self.read_data().keys()
        query = query_text.split()
        answers = set(records)

        for r in records:
            for word in query:
                if word.lower() not in r.lower():
                    answers.remove(r)

        answers = list(answers)
        for i in range(len(answers)):
            print(f'{i}. {answers[i]}')


    def main(self, args):
        if args.query:
            self.search(args.query)
        else:
            self.write()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Knowledge Base system")
    parser.add_argument('query', nargs='?', help="search query to the knowledge base")
    args = parser.parse_args()

    knowledge = Knowledge()
    knowledge.main(args)
