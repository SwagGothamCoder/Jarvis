def find_location(input_structure, user_input, phrase_structures, data_points):
    loc = 'place'
    for i in data_points:
        if input_structure[i] == 'NNP':
            loc = user_input[i]
    return 'Locating '+loc+'.'