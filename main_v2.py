from src.pipeline.extract_features_v2 import extract_features_v2
from src.data.preprocess import DataPreprocess
from src.utils.file_handling import csv_to_json
import spacy
import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Input file name in data/ folder (.csv)", required=True)
parser.add_argument("--type", help="Input question type (snc/err)", required=True)
try:
    args = parser.parse_args()
except SystemExit:
    parser.print_help()
    exit(1)

filename = os.path.splitext(str(args.filename))[0]
question_type = os.path.splitext(str(args.type))[0]
nlp = spacy.load("en_core_web_sm")
data = csv_to_json(filename)

print('Start preprocessing...')
preprocess = DataPreprocess(data, nlp, filename, question_type)
preprocess.start()
print('Done')

path = os.path.join(os.getcwd(), 'data', f'{filename}_preprocessed.json')
print('Start feature extraction...')
with open(path, 'r') as f:
    data = json.load(f)
    featex = extract_features_v2(data, filename, nlp)
print('Done')
