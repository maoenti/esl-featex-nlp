from src.utils.file_handling import set_training_data

class DataPreprocess():
    def __init__(self, data, nlp, filename, question_type):
        self.data = data
        self.nlp = nlp
        self.filename = filename
        self.question_type = question_type

    def pos_tag(self, text):
        doc = self.nlp(text)
        counter = 0
        pos_tag = []
        for token in doc:
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            #         token.shape_, token.is_alpha, token.is_stop)
            pos_tag.append([counter, token.text, token.tag_])
            counter += 1
        return pos_tag
    
    def get_underlines(self, data):
        pos_tag = data['pos_tag']
        options = ['A', 'B', 'C', 'D']
        index = 0

        for opt in options:
            temp_underline, index = self.option_underline(pos_tag, data[opt], index)
            for i in range(len(data[opt])):
                data[opt][i][0] = temp_underline[i]

        return True

    def option_underline(self, question, option, index):
        underline = []
        check = 0
        while check != len(option):
            for word in option:
                while index != len(question):
                    if word[1] == question[index][1]:
                        underline.append(index)
                        check += 1
                        break
                    index += 1

        return underline, index
    
    def fill_sentence(self, question, key_answer_text):
        filled_question = question.replace("...", key_answer_text)
        print(filled_question)
        return filled_question

    def start(self):
        options = ['A', 'B', 'C', 'D']
        counter = 0
        for data in self.data:
            data['id'] = counter
            if self.question_type == 'snc':
                data['question_text'] = self.fill_sentence(data['question_text'], data[data['key_answer']])
            data['pos_tag'] = self.pos_tag(data['question_text'])
            for opt in options:
                data[opt] = self.pos_tag(data[opt])
            if self.question_type == 'err':
                self.get_underlines(data)
            counter += 1
        set_training_data(f'{self.filename}_preprocessed', self.data)
        return self.data
