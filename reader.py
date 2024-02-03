import sys
import json
import csv
# python reader.py in.csv out.json 1,1,cat 0,1,dog 2,1,bread


class InputArguments:
    def __int__(self, args):
        self.input_file = args[0]
        self.output_file = args[1]
        self.changes = args[2:] if len(args) > 2 else []

        self.changes = [
            (
                int(a.split(',')[0]),
                int(a.split(',')[1]),
                a.split(',')[2]
            )
            for a in self.changes
        ]

    def __str__(self):
        return f"Read from: {self.input_file}\n Save to: {self.output_file}"


class BaseFileHandler:
    def __int__(self, file_name):
        self.file_name = file_name


class JSONFileHandler(BaseFileHandler):
    def read(self):
        with open(self.file_name, "rb") as f:
            content = json.load(f)
        return content

    def write(self, content):
        with open(self.file_name, "wb") as f:
            json.dump(content, f)


class CSVFilehandler:
    def __int__(self, file_name):
        self.file_name = file_name

    def load(self):
        with open(self.file_name) as f:
            content = f.read()
        rows = content.split("___")
        values = [r.split('---') for r in rows]
        return values

    def write(self, content):
        rows = ["---".join(r) for r in content]
        output_content = "---".join(rows)
        with open("output.csv", "w") as f:
            f.write(output_content)


def change_content(content, changes):
    for (x, y, v) in changes:
        content[y][x] = v
    return content


if len(sys.argv) < 3:
    print("Error: Too few arguments.")
    sys.exit()

if len(sys.argv) < 4:
    print("Warning: No changes were made. ")

arguments = InputArguments(sys.argv[0:])

# selects the right input files
if arguments.input_file.endswith(".csv"):
    input_file_handler = CSVFilehandler
elif arguments.input_file.endswith(".json"):
    input_file_handler = JSONFileHandler
else:
    raise NotImplementedError("Program handles only csv and json.")

# selects the right output files
if arguments.output_file.endswith(".csv"):
    output_file_handler = CSVFilehandler
elif arguments.output_file.endswith(".json"):
    output_file_handler = JSONFileHandler
else:
    raise NotImplementedError("Program handles only csv and json.")

input_file_handler = input_file_handler(arguments.input_file)
output_file_handler = output_file_handler(arguments.output_file)
content = input_file_handler.read()

print(content)
content = change_content(content, arguments.changes)
print(content)

output_file_handler.write(content)