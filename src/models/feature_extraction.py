from src.utils.file_handling import set_training_data

class FeatureExtraction:
    def __init__(self, data, nlp):
        self.data = data
        self.nlp = nlp

    def start(self):
        indicators = []

        for item in self.data:
            temp_dict = {}
            indicator = FeatureExtraction(item, self.nlp)
            temp_dict['id'] = item['id']
            temp_dict['question_text'] = item['question_text']
            temp_dict['relative_pronoun'] = indicator.relative_pronoun()
            temp_dict['subjunctive'] = indicator.subjunctive()
            options_based_indicators = indicator.check_opt_tag()
            temp_dict['participle'] = options_based_indicators['participle']
            temp_dict['singular_plural'] = options_based_indicators['singular_plural']
            temp_dict['articles'] = options_based_indicators['articles']
            temp_dict['demonstratives'] = options_based_indicators['demonstratives']
            temp_dict['gerund'] = options_based_indicators['gerund']
            temp_dict['infinitive'] = options_based_indicators['infinitive']
            temp_dict['irregular_verb'] = options_based_indicators['irregular_verb']
            temp_dict['passive'] = indicator.is_passive()
            # temp_dict['subject_verb_agreement'], temp_dict['auxiliary_verb'] = indicator.check_sva_aux_opt()
            indicator.is_passive()
            indicators.append(temp_dict)
        set_training_data('feature_extraction', indicators)
        return indicators

    def infinitives(self, index):
        doc = self.nlp(self.data['question_text'])
        i = 0
        for token in doc:
            if i == index+1 and token.pos_ == 'VERB':
                if token.text == token.lemma_:
                    return True
                else:
                    break
            i += 1
        return False
    
    def relative_pronoun(self):
        doc = self.nlp(self.data['question_text'])
        relative_pronouns_words = ["who", "whom", "whose", "which", "that", "where"]
        options = ['A', 'B', 'C', 'D']
        for token in doc:
            if token.dep_ == "relcl":
                for opt in options:
                    for item in self.data[opt]:
                        if item[1] in relative_pronouns_words:
                            return True
                break
        return False
    
    def is_passive(self):
        doc = self.nlp(self.data['question_text'])
        passive = ['auxpass', 'nsubjpass', 'csubjpass']
        for token in doc:
            if token.dep_ in passive:
                return True
        return False
    
    def subjunctive(self):
        doc = self.nlp(self.data['question_text'])
        options = ['A', 'B', 'C', 'D']

        for token in doc:
            if token.dep_ == "ccomp" or token.dep_ == "advcl":
                for opt in options:
                    for item in self.data[opt]:
                        if item[1] == token.text:
                            return True
                    break
        return False
    
    def check_opt_tag(self):
        response = {}
        options = ['A', 'B', 'C', 'D']
        response['participle'] = False
        response['word_form'] = False
        response['singular_plural'] = False
        response['articles'] = False
        response['demonstratives'] = False
        response['gerund'] = False
        response['infinitive'] = False
        response['irregular_verb'] = False
        articles = ['a', 'the', 'an']
        demonstratives = ['this', 'that', 'these', 'those']

        for opt in options:
            for item in self.data[opt]:
                if item[2].startswith('VB'): ## Check if the options has word form type
                    response['word_form'] = True
                    if item[2] == "VBN": ## Check if the options has participle type
                        response['participle'] = True
                    if item[2] == "VBG":
                        response['participle'] = True
                        response['gerund'] = True
                    if item[2] == "VBD":
                        response['irregular_verb'] = True
                if item[2].startswith('NN'): ## Check if the options has singular plural type
                    response['singular_plural'] = True
                if item[2].startswith('DT'): ## Check if the options has determiner types
                    if item[1] in articles:
                        response['articles'] = True
                    elif item[1] in demonstratives:
                        response['demonstratives'] = True
                if item[2].startswith('TO'):
                    response['infinitive'] = self.infinitives(item[0]) # Use the index as the args

        return response
    
    def subject_verb_agreement(self):
        suggested_words = []
        suggested_words_aux = []

        doc = self.nlp(self.data['question_text'])
        for token in doc:
            if token.dep_ == "nsubj":
                for anc in token.ancestors:
                    if anc.pos_ == "VERB" and anc.text not in suggested_words:
                        suggested_words.append(anc.text)
                        if len(list(anc.children)) != 0:
                            for child in anc.children:
                                if child.pos_ == "AUX" and child.text not in suggested_words_aux:
                                    suggested_words_aux.append(child.text)
        return suggested_words, suggested_words_aux
    
    def check_sva_aux_opt(self):
        suggested_words, suggested_words_aux = self.subject_verb_agreement()

        sva = False
        aux = False
        for opt in self.data['opt_pos']:
            if opt[0] in suggested_words or opt[0] in suggested_words_aux:
                sva = True
            if opt[0] in suggested_words_aux:
                aux = True
        return sva, aux    
        