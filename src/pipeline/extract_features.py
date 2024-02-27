from src.models.feature_extraction_v2 import FeatureExtractionV2
from src.utils.file_handling import set_training_data
import spacy

def extract_features(data):
    nlp = spacy.load("en_core_web_sm")
    extracted_features = []
    for item in data:
        response = {}
        response['question_text'] = item['question_text']
        featex_v2 = FeatureExtractionV2(item, nlp)
        opt_tags = featex_v2.option_tags()
        response['v1'] = opt_tags['v1']
        response['v2'] = opt_tags['v2']
        response['v3'] = opt_tags['v3']
        response['v4'] = featex_v2.subjunctives()
        response['v5'] = opt_tags['v5']
        response['v6'], response['v7'] = featex_v2.passives()
        opt_deps = featex_v2.option_deps()
        response['v8'] = opt_deps['v8']
        response['v9'] = opt_deps['v9']
        response['pro1'] = opt_deps['pro1']
        response['pro2'] = opt_deps['pro2']
        response['n1'] = opt_deps['n1']
        response['n2'] = opt_deps['n2']
        response['n3'] = opt_deps['n3']
        response['a1'] = opt_deps['a1']
        response['a2'] = opt_deps['a2']

        if response['a2'] == True:
            print(item['question_text'])
        extracted_features.append(response)
    set_training_data('feature_extraction_v2', extracted_features)

    return extracted_features