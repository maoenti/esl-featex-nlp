class FeatureExtractionV2:
    def __init__(self, data, nlp):
        self.data = data
        self.nlp = nlp
    
    def option_deps(self):
        doc = self.nlp(self.data['question_text'])
        options = ['A', 'B', 'C', 'D']
        response = {}
        response['v1'] = False
        response['v2'] = False
        response['v3'] = False
        response['v4'] = False
        response['v5'] = False
        response['v6'] = False
        response['v7'] = False
        response['v8'] = False
        response['v9'] = False
        response['v10'] = False

        for token in doc:
            for opt in options:
                for item in self.data[opt]:
                    main_verb = self.main_verbs(token, item)
                    if not response['v1']:
                        response['v1'] = main_verb[0]
                    if not response['v2']:
                        response['v2'] = main_verb[1]
                    if not response['v3']:
                        response['v3'] = main_verb[2]

                    tense = self.tense(token, item)
                    if not response['v4']:
                        response['v4'] = tense[0]
                    if not response['v5']:
                        response['v5'] = tense[1]

                    if not response['v6']:
                        response['v6'] = self.infinitives(token, item)

                    passives = self.passives(token, item)
                    if not response['v7']:
                        response['v7'] = passives[0]
                    if not response['v8']:
                        response['v8'] = passives[1]

                    if not response['v9']:
                        response['v9'] = self.have_participle(token, item)

                    if not response['v10']:
                        response['v10'] = self.auxiliary_verbs(token, item)
        return response
    
    def main_verbs(self, token, opt_item):
        v1 = False
        v2 = False
        v3 = False

        if token.pos_ == 'VERB':
            v1 = self.is_main_verb(token, opt_item)
            if v1:
                for child in token.children:
                    v2 = self.req_infinitive(child, opt_item)
                    v3 = self.req_ing(child, opt_item)
        return [v1, v2, v3]
    
    def is_main_verb(self, token, opt_item):
        if len(list(token.ancestors)) == 0 and token.text == opt_item[1]:
            return True
        return False

    def req_infinitive(self, token, opt_item):
        if token.tag_ != 'VBG' and token.pos_ == 'VERB':
            for item in token.children:
                if item.tag_ == 'TO' and (opt_item[1] == item.text or opt_item[1] == token.text):
                    return True
        return False
    
    def req_ing(self, token, opt_item):
        if token.tag_ == 'VBG' and opt_item[1] == token.text:
            return True
        return False
    
    def tense(self, token, opt_item):
        tense_tag = ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        v4 = False
        v5 = False
        if token.tag_ in tense_tag and token.text == opt_item[1]:
            v4 = True
            v5 = self.irregular_past(token, opt_item[1])

        return v4, v5
    
    def irregular_past(self, token, opt_item):
        if token.tag_ == 'VBD' and token.text == opt_item[1]:
            return True
        return False
    
    def infinitives(self, token, opt_item):
        if token.pos_ == 'VERB':
            for child in token.children:
                if child.tag_ == 'TO' and (child.text == opt_item[1] or token.text == opt_item[1]):
                    return True
        return False
    
    def passives(self, token, opt_item):
        v7 = False
        v8 = False
        passive = ['auxpass', 'nsubjpass', 'csubjpass']

        if token.dep_ in passive:
            v7 = True
            if token.text.lower() == 'it':
                v8 = True
        return v7, v8

    def have_participle(self, token, opt_item):
        if token.pos_ == 'VERB':
            if token.text == opt_item[1]:
                for child in token.children:
                    if child.text.lower() == 'have':
                        return True
        return False
    
    def auxiliary_verbs(self, token, opt_item):
        if token.pos_ == 'VERB':
            for child in token.children:
                if child.dep_ == 'aux' and (opt_item[1] == token.text or opt_item[1] == child.text):
                    print(f'child: {child.text}\ntoken: {token.text}')
                    return True
        return False
    