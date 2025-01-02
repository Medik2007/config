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
        data['commands'][title] = command
        self.write_data(data)


    def search(self, query_text):
        data = self.read_data()
        query = query_text.split()
        result = {}

        for q in range(len(query)):
            records = list(data['commands'].keys())
            for r in range(len(records)):
                if query[q].lower() in records[r].lower():
                    offset = abs(q-r)/10
                    if records[r] in result.keys():
                        result[records[r]] += 1 + offset
                    else:
                        result[records[r]] = 1 + offset

        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        for i in result.keys():
            print(i, result[i])


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
