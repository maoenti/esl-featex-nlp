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
        response['v8'], response['v9'] = opt_deps

        if response['v9'] == True:
            print(item['question_text'])
        extracted_features.append(response)
    set_training_data('feature_extraction_v2', extracted_features)

    return extracted_features