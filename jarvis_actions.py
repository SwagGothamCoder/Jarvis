import webbrowser

session_data = {'current_loc': ''}

def find_location(input_structure, user_input, phrase_structures, data_points):
    '''Opens google maps showing the location of the queried place and then returns a string containing Jarvis' verbal response.'''
    loc = ''
    if data_points:
        loc = ''.join(user_input[point]+' ' for point in data_points)
        loc = loc[:-1]
    if not loc:
        loc = 'The United States'
    if 'near' in user_input or 'nearest' in user_input:
        if not session_data['current_loc']:
            current_loc = raw_input('Where are you?')
            session_data['current_loc'] = current_loc
        url = "https://www.google.com/maps/search/"+loc.replace(' ', '+')+"/@"+session_data['current_loc']
    else:
        url = "https://www.google.com/maps/place/"+loc.replace(' ', '+')
    webbrowser.open(url)
    return 'Locating '+loc+'.'

def nav(input_structure, user_input, phrase_structures, data_points):
    '''Opens google maps with the directions asked for and then returns a string containing Jarvis' verbal response.'''
    current_loc = session_data['current_loc']
    if not session_data['current_loc']:
        current_loc = raw_input('Where are you?')
        session_data['current_loc'] = current_loc
    destination = ''
    if data_points:
        destination = ''.join(user_input[point]+' ' for point in data_points)
        destination = destination[:-1]
    if not destination:
        return "I couldn't understand where you wanted to go. Please try again."
    url = "https://www.google.com/maps/dir/"+current_loc.replace(' ', '+')+"/"+destination.replace(' ', '+')
    webbrowser.open(url)
    return 'Here are your directions to '+destination+'.'