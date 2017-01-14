import webbrowser
import nltk

session_data = {'current_loc': ''}

def find_location(user_input, data_points):
    '''Opens google maps showing the location of the queried place and then returns a string containing Jarvis' verbal response.'''
    user_input = nltk.word_tokenize(user_input)
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