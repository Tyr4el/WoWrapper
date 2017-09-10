import json

parsed_json = None
with open('ItemSparse.json') as file:
    parsed_json = json.load(file)

new_data = []
for item in parsed_json:
    new_json = {'name': parsed_json['Name'], 'item level': parsed_json['ItemLevel'], 'quality':
        parsed_json['Quality']}
    new_data.append(new_json)

with open('Items.json', 'w') as new_file:
    json.dump(new_data, new_file)