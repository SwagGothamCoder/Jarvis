import webbrowser

def find_location(input_structure, user_input, phrase_structures, data_points):
    loc = ''
    if data_points:
        loc = ''.join(user_input[point]+' ' for point in data_points)
        loc = loc[:-1]
    print('loc', loc)
    if not loc:
        loc = 'The United States'
    url = "https://www.google.com/maps/place/"+loc.replace(' ', '+')
    webbrowser.open(url)
    return 'Locating '+loc+'.'