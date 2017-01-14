from doc_reader import Document_Reader
import response_architect
from actions import *

actions = {'find_location': find_location}

doc = ""
with open(path, 'rb') as f:
    doc = f.read()
doc = doc.replace('\n', ' ')
doc = doc.replace('\r', ' ')

def fill(answers, structure):
    tags_filled = 0
    tags = ['NNP', 'NN', 'NNS', 'JJ', 'RB']
    for idx, word in enumerate(structure):
        if word in tags:
            if tags_filled <= len(answers)-1:
                structure[idx] = answers[tags_filled]
            else:
                structure[idx] = answers[:-1]
            tags_filled += 1
    return structure

reader = Document_Reader(document=doc)
while True:
    user_input = raw_input('Input (EXIT to break):')
    if user_input == 'EXIT':
        break
    else:
        response = reader.query(user_input)
        if not response:
            print("I don't know.")
        else:
            if response[0] == '<PROCESS>':
                response = actions[response[2]](user_input, response[1])
            else:
                if len(response) == 1:
                    output_structure = response_architect.generate_output(user_input)
                    print('Output structure:', output_structure)
                    response = fill(response, output_structure)
            print('Output:', response)