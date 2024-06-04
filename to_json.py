import json
import csv

with open('data/aryo_features_v2.json', 'r') as f:
    json_data = json.load(f)

# row = [json_data[0]['question_text']] + list(json_data[0]['level2'].values())
# print(row)

with open('data/output.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    headers = ['question_text'] + list(json_data[0]['level2'].keys())
    csv_writer.writerow(headers)

    for item in json_data:
        row = [item['question_text']] + list(item['level2'].values())
        csv_writer.writerow(row)