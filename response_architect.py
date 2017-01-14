import nltk
import pattern.en as pattern

phrase_structures = {}

def conjugate_verb(verb, user_input):
    '''Returns a verb that has been conjugated to match the changed perspective from the user's input to the computer's output.'''
    if verb == pattern.conjugate(verb, person=1):
        return pattern.conjugate(verb, person=2)
    elif verb == pattern.conjugate(verb, person=2) and (user_input[user_input.index(verb)-1].lower() == 'you' or user_input[user_input.index(verb)+1].lower() == 'you'):
        return pattern.conjugate(verb, person=1)
    else:
        return verb

def get_word_to_compare(user_structure, user_input, tag_counts, part_of_speech):
    '''Returns the nth word of a specific part of speech in the user's input, where n is the number of times the computer has iterated over a word of the same part of speech in the output structure.'''
    word_to_compare = ''
    count = 0
    for i, tag in enumerate(user_structure):
        if tag == part_of_speech:
            count += 1
            if count == tag_counts[part_of_speech]:
                word_to_compare = str(user_input[i])
    return word_to_compare

def generate_output(user_input):
    '''Returns a list that has replaced some of the output structure list elements with words that could be determined by the context of the user's input.'''
    user_input = nltk.word_tokenize(user_input)
    user_structure = nltk.pos_tag(user_input)
    user_structure = [tag[1] for tag in user_structure]
    user_structure_string = ''.join(tag+' ' for tag in user_structure)[:-1]
    if user_structure_string not in phrase_structures:
        print("How do I respond?")
        response = raw_input('Prefered response:')
        phrase_structures[user_structure_string] = [tag[1] for tag in nltk.pos_tag(nltk.word_tokenize(response))]
    structure = phrase_structures[user_structure_string]
    structure = list(structure)
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