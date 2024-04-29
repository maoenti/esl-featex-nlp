from src.models.feature_extraction_v2 import FeatureExtractionV2
from src.utils.file_handling import set_training_data

def extract_features_v2(data, filename, nlp):
    extracted_features = []
    for item in data:
        response = {}

        response['question_text'] = item['question_text']
        featex_v2 = FeatureExtractionV2(item, nlp)
        opt_deps = featex_v2.option_deps()
        response['v1'] = opt_deps['v1']
        response['v2'] = opt_deps['v2']
        response['v3'] = opt_deps['v3']
        response['v4'] = opt_deps['v4']
        response['v5'] = opt_deps['v5']
        response['v6'] = opt_deps['v6']
        response['v7'] = opt_deps['v7']
        response['v8'] = opt_deps['v8']
        response['v9'] = opt_deps['v9']
        response['v10'] = opt_deps['v10']
        response['pro1'] = opt_deps['pro1']
        response['pro2'] = opt_deps['pro2']
        response['pro3'] = opt_deps['pro3']
        response['n1'] = opt_deps['n1']
        response['n2'] = opt_deps['n2']
        response['n3'] = opt_deps['n3']
        response['a1'] = opt_deps['a1']
        response['a2'] = opt_deps['a2']
        response['a3'] = opt_deps['a3']
        response['a4'] = opt_deps['a4']
        response['prep1'] = opt_deps['prep1']
        response['prep2'] = opt_deps['prep2']
        extracted_features.append(response)
        if response['prep2']:
            print(response)
    # set_training_data(f'{filename}_features_v2', extracted_features)

    return extracted_features
