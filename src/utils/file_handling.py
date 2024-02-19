import os
import csv
import json

def csv_to_json(filename):
    data_path = os.path.join(os.getcwd(), 'data', filename + '.csv')
    csv_data = []

    with open(data_path, 'r', encoding='utf-8', errors='replace') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    json_path = os.path.join(os.getcwd(), 'data', filename + '.json')

    # Write the data to a JSON file
    with open(json_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=4)

    return csv_data

def set_training_data(filename, data):
    path = os.path.join(os.getcwd(), 'data', filename + '.json')

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    return path