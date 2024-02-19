from src.models.feature_extraction import FeatureExtraction
from src.data.preprocess import DataPreprocess
from src.utils.file_handling import csv_to_json
import spacy
import os
import json

path = os.path.join(os.getcwd(), 'data', 'test.json')
nlp = spacy.load("en_core_web_sm")

data = csv_to_json('question_examples')

print('Start preprocessing...')
preprocess = DataPreprocess(data, nlp)
preprocess.start()
print('Done')

print('Start feature extraction...')
featex = FeatureExtraction(data, nlp)
with open(path, 'r') as f:
    data = json.load(f)
    # print(featex.start())
    featex.start()
print('Done')
