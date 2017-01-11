import nltk
import pattern.en as pattern
import jarvis_actions

from jarvis_memory import Jarvis_Memory

#nltk.help.upenn_tagset()
jm = Jarvis_Memory()
phrase_structures = {}
actions = {'find_location': jarvis_actions.find_location, 'nav': jarvis_actions.nav}

def conjugate_verb(verb, user_input):
    if verb == pattern.conjugate(verb, person=1):
        return pattern.conjugate(verb, person=2)
    elif verb == pattern.conjugate(verb, person=2) and (user_input[user_input.index(verb)-1].lower() == 'you' or user_input[user_input.index(verb)+1].lower() == 'you'):
        return pattern.conjugate(verb, person=1)
    else:
        return verb

def get_word_to_compare(user_structure, user_input, tag_counts, part_of_speech):
    word_to_compare = ''
    count = 0
    for i, tag in enumerate(user_structure):
        if tag == part_of_speech:
            count += 1
            if count == tag_counts[part_of_speech]:
                word_to_compare = str(user_input[i])
    return word_to_compare

def generate_output(user_input, structure):
    structure = list(structure)
    user_structure = nltk.pos_tag(user_input)
    user_structure = [tag[1] for tag in user_structure]
    tag_counts = {'PRP$': 0, 'VBZ': 0, 'VBP': 0, 'NN': 0, 'NNS': 0, 'PRP': 0, 'JJ': 0, 'CC': 0}
    for idx, tag in enumerate(structure):
        if tag == 'PRP$':
            tag_counts[tag] += 1
            word_to_compare = get_word_to_compare(user_structure, user_input, tag_counts, 'PRP$')
            if not not word_to_compare:
                if 'my' == word_to_compare:
                    structure[idx] = 'your'
                elif 'your' == word_to_compare:
                    structure[idx] = 'my'
        elif tag in ['VBZ', 'VBP']:
            tag_counts[tag] += 1
            if tag in user_structure:
                verb = get_word_to_compare(user_structure, user_input, tag_counts, tag)
                structure[idx] = conjugate_verb(verb, user_input)
        elif tag in ['NN', 'NNS', 'JJ']:
            tag_counts[tag] += 1
            if tag in user_structure:
                structure[idx] = get_word_to_compare(user_structure, user_input, tag_counts, tag)
        elif tag == 'PRP':
            tag_counts[tag] += 1
            if 'PRP' in user_structure:
                pronoun = get_word_to_compare(user_structure, user_input, tag_counts, tag)
                if pronoun == 'I':
                    structure[idx] = 'you'
                elif pronoun == 'you':
                    structure[idx] = 'I'
                else:
                    structure[idx] = pronoun
        elif tag == 'CC':
            tag_counts[tag] += 1
            if 'CC' in user_structure:
                conjunction = get_word_to_compare(user_structure, user_input, tag_counts, tag)
                structure[idx] = conjunction
    return structure

while True:
    user_input = nltk.word_tokenize(raw_input('Input (EXIT to break):'))
    if user_input == ['EXIT']:
        break
    else:
        input_structure = []
        for tag in nltk.pos_tag(user_input):
            input_structure += [tag[1]]
        input_structure = ''.join(word+' ' for word in input_structure)
        input_structure = input_structure[:-1]
        print('Input structure:', input_structure)
        if input_structure in phrase_structures:
            print(phrase_structures[input_structure])
            print('Response:', generate_output(user_input, phrase_structures[input_structure]))
            if '?' in user_input:
                knowledge_base_response, data_points = jm.retrieve_from_knowledge(input_structure, user_input)
                if knowledge_base_response.startswith('PROCESS:'):
                    answer = actions[knowledge_base_response[knowledge_base_response.index(':')+2:]](nltk.word_tokenize(input_structure), user_input, phrase_structures, data_points)
                else:
                    answer = knowledge_base_response
                print('Answer:', answer)
            else:
                jm.add_to_knowledge(input_structure, user_input)
        else:
            print("How do I respond?")
            response = raw_input('Prefered response:')
            phrase_structures[input_structure] = [tag[1] for tag in nltk.pos_tag(nltk.word_tokenize(response))]
            jm.add_to_knowledge(input_structure, user_input)