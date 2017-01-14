import nltk
import os
from textblob import TextBlob

class Document_Reader(object):
    def __init__(self, document=''):
        self.answer_type = {'who': 'PERSON', 'where': 'GPE', 'what': 'NONE'}
        self.significant_points = {}
        self.document = document
        java_path = "C:/Program Files/Java/jdk1.8.0_71/bin/java.exe"
        os.environ['JAVAHOME'] = java_path
        path1 = ''
        path2 = ''
        self.st = nltk.tag.StanfordNERTagger(path1, path2)
    
    def add_to_kb(self, user_input):
        self.document += user_input+' '
    
    def query(self, user_input):
        user_input = nltk.word_tokenize(user_input)
        user_structure = nltk.pos_tag(user_input)
        user_structure = ''.join(tag[1]+' ' for tag in user_structure)[:-1]
        if user_structure not in self.significant_points:
            points = raw_input('Enter significant data points:')
            points = [int(point) for point in points.split()]
            self.significant_points[user_structure] = list(points)
            process = raw_input('Does this question require an external process? (Yes or No):')
            if process.lower() == 'yes':
                process = raw_input('What is the name of the required process?')
                self.significant_points[user_structure] = (list(points), process)
            else:
                self.significant_points[user_structure] = (list(points), '')
        data_points, process = self.significant_points[user_structure]
        if process:
            return '<PROCESS>', data_points, process
        qualifiers = [user_input[point] for point in data_points]
        qword = 'what'
        if 'who' in user_input:
            qword = 'who'
        elif 'where' in user_input:
            qword = 'where'
        return self.read(self.document, qword, qualifiers)
    
    def read(self, doc, qword, qualifiers):
        sents = nltk.sent_tokenize(doc)
        sents = [nltk.word_tokenize(sent) for sent in sents]
        
        potential_sents = []
        for sent in sents:
            if all([qualifier in sent for qualifier in qualifiers]):
                potential_sents.append(sent)
        answers = []
        answer_appended_last = False
        for sent in potential_sents:
            if qword == 'what':
                sent = TextBlob(''.join(word+' ' for word in sent)[:-1])
                for answer in sent.noun_phrases:
                    answers.append(answer)
            else:
                ner_chunked = self.st.tag(sent)
                for tag in ner_chunked:
                    if tag[1] == self.answer_type[qword]:
                        if answer_appended_last:
                            answers[-1] += ' '+tag[0]
                        else:
                            answers.append(tag[0])
                        answer_appended_last = True
                    else:
                        answer_appended_last = False
        return answers