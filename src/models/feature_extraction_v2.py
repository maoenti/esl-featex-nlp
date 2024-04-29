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
        response['pro1'] = False
        response['pro2'] = False
        response['pro3'] = False
        response['n1'] = False
        response['n2'] = False
        response['n3'] = False
        response['a1'] = False
        response['a2'] = False
        response['a3'] = False
        response['a4'] = False
        response['pre1'] = False
        response['pre2'] = False

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
                    
                    pronouns = self.pronouns(token, item)
                    if not response['pro1']:
                        response['pro1'] = pronouns[0]
                    if not response['pro2']:
                        response['pro2'] = pronouns[1]
                    if not response['pro3']:
                        response['pro3'] = pronouns[2]

                    nouns = self.nouns(token, item)
                    if not response['n1']:
                        response['n1'] = nouns[0]
                    if not response['n2']:
                        response['n2'] = nouns[1]
                    if not response['n3']:
                        response['n3'] = nouns[2]

                    adj = self.adjectives(token, item)
                    if not response['a1']:
                        response['a1'] = adj[0]
                    if not response['a2']:
                        response['a2'] = adj[1]
                    if not response['a3']:
                        response['a3'] = adj[2]
                    if not response['a4']:
                        response['a4'] = adj[3]

                    prep = self.prepositions(token, item)
                    if not response['pre1']:
                        response['pre1'] = prep[0]
                    if not response['pre2']:
                        response['pre2'] = prep[0]
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
                    return True
        return False

    def pronouns(self, token, opt_item):
        pro1 = False
        pro2 = False
        pro3 = False

        if token.tag_.startswith('PRP'):
            if token.text == opt_item[1]:
                pro1 = True
        pro2 = self.object_pronouns(token, opt_item)
        pro3 = self.relative_pronouns(token, opt_item)

        return pro1, pro2, pro3

    def object_pronouns(self, token, opt_item):
        if token.dep_ == 'pobj':
            for anc in token.ancestors:
                if anc.tag_ == 'IN' and (anc.text == opt_item[1] or token.text == opt_item[1]):
                    return True
        return False
    
    def relative_pronouns(self, token, opt_item):
        relative_pronouns_words = ["who", "whom", "whose", "which", "that", "where"]
        if token.dep_ == "relcl":
            if opt_item[1].lower() in relative_pronouns_words:
                return True
        return False
    
    def nouns(self, token, opt_item):
        n1 = False
        if token.pos_ == 'NOUN':
            n1 = True
        n2 = self.infinitive_ing_subject(token, opt_item)
        n3 = self.nominal_that_clause(token, opt_item)
        return n1, n2, n3
    
    def infinitive_ing_subject(self, token, opt_item):
        subject = ['csubj', 'csubjpass']
        if token.dep_ in subject and token.text == opt_item[1]:
            return True
        return False
    
    def nominal_that_clause(self, token, opt_item):
        if token.dep_ == 'mark' and token.text == opt_item[1] and token.text.lower() == 'that':
            return True
        return False
    
    def adjectives(self, token, opt_item):
        a1 = self.noun_qualifying_phrases(token, opt_item)
        a2 = self.no_mean_not_any(token, opt_item)
        a3 = self.adjective_noun(token, opt_item)
        a4 = self.adjective_so(token, opt_item)

        return a1, a2, a3, a4

    def noun_qualifying_phrases(self, token, opt_item):
        if token.text.lower() == 'the':
            for anc in token.ancestors:
                if anc.pos_ == 'NOUN' and anc.text == opt_item[1] and anc.morph.get('Number') == ['Sing']:
                    return True
        return False
    
    def no_mean_not_any(self, token, opt_item):
        if token.tag_ == 'DT' and token.text.lower() == 'no':
            for anc in token.ancestors:
                if anc.text == opt_item[1] or token.text == opt_item[1]:
                    return True
        return False
    
    def adjective_noun(self, token, opt_item):
        if token.pos_ == 'NOUN' and token.dep_ == 'compound':
            for anc in token.ancestors:
                if token.text == opt_item[1] or anc.text == opt_item[1]:
                    return True
                else:
                    break
        return False
    
    def adjective_so(self, token, opt_item):
        if token.text.lower() == 'so' and token.dep_ == 'advmod':
            for anc in token.ancestors:
                if token.text == opt_item[1] or anc.text == opt_item[1]:
                    return True
                else:
                    break
        return False
    
    def prepositions(self, token, opt_item):
        pre1 = self.prep_addition(token, opt_item)
        pre2 = self.prep_cause(token, opt_item)

        return pre1, pre2

    def prep_addition(self, token, opt_item):
        if token.text.lower() == 'besides' and token.dep_ == 'prep' and token.pos_ == 'SCONJ':
            for child in token.children:
                if token.text == opt_item[1] or child.text == opt_item[1]:
                    return True
        return False
    
    def prep_cause(self, token, opt_item):
        if token.text.lower() == 'because' and token.dep_ == 'mark':
            for anc in token.ancestors:
                if token.text == opt_item[1] or anc.text == opt_item[1]:
                    return True
        elif token.text.lower() == 'because' and token.dep_ == 'prep':
            for child in token.children:
                if token.text == opt_item[1] or child.text == opt_item[1]:
                    return True
        return False
    