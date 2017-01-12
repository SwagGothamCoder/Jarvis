class Jarvis_Memory(object):
    def __init__(self):
        self.knowledge = {}
        self.statement_data_points = {}
        self.question_data_points = {}
    
    def add_to_knowledge(self, user_structure, user_input):
        if '?' in user_input:
            data_points = raw_input('Give the question data points:')
            data_points = [int(c) for c in data_points.split()]
            self.question_data_points[user_structure] = [list(data_points), 'False']
            
            special = raw_input('Does the question require a special process to find an answer? (True or False):')
            if special == 'True':
                process_name = raw_input('What is the name of this process? ')
                self.question_data_points[user_structure][1] = process_name
        else:
            if user_structure in self.statement_data_points:
                phrase_data_points = [[]]
                current_index = 0
                for point in self.statement_data_points[user_structure]:
                    if user_input[point] == 'and' or user_input[point] == 'or':
                        phrase_data_points.append([])
                        current_index += 1
                    else:
                        phrase_data_points[current_index].append(point)
                for data_points in phrase_data_points:
                    if len(data_points) == 2:
                        if user_input[data_points[0]] not in self.knowledge:
                            self.knowledge[user_input[data_points[0]]] = [[], {}]
                        self.knowledge[user_input[data_points[0]]][0] += [str(user_input[data_points[1]])]
                    else:
                        if user_input[data_points[0]] in self.knowledge:
                            self.knowledge[user_input[data_points[0]]][1][user_input[data_points[1]]] = str(user_input[data_points[2]])
                        else:
                            self.knowledge[user_input[data_points[0]]] = [[], {}]
                            self.knowledge[user_input[data_points[0]]][1][user_input[data_points[1]]] = str(user_input[data_points[2]])
                    print('Added:', [user_input[point] for point in data_points])
            else:
                data_points = raw_input('Give the statement data points:')
                data_points = [int(c) for c in data_points.split()]
                self.statement_data_points[user_structure] = list(data_points)
        print('Knowledge', self.knowledge)
    
    def retrieve_from_knowledge(self, user_structure, user_input):
        if user_structure not in self.question_data_points:
            print('ERROR: not in question_data_points.')
        else:
            if self.question_data_points[user_structure][1] != 'False':
                return [('PROCESS: '+self.question_data_points[user_structure][1], self.question_data_points[user_structure][0])]
            else:
                output = []
                phrase_data_points = [[]]
                current_index = 0
                for point in self.question_data_points[user_structure][0]:
                    if user_input[point] == 'and' or user_input[point] == 'or':
                        phrase_data_points.append([])
                        current_index += 1
                    else:
                        phrase_data_points[current_index].append(point)
                for data_points in phrase_data_points:
                    if user_input[data_points[0]] in self.knowledge:
                        if user_input[data_points[1]] in self.knowledge[user_input[data_points[0]]][1]:
                            output.append((self.knowledge[user_input[data_points[0]]][1][user_input[data_points[1]]], self.question_data_points[user_structure][0]))
                        else:
                            print('missing attribute in knowledge')
                    else:
                        print('missing hierarchical parent in knowledge')
                return output