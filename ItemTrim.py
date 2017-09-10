import json

parsed_json = None
with open('ItemSparse.json') as file:
    parsed_json = json.load(file)

new_data = []
for item in parsed_json:
    new_json = {'Name': item['Name'], 'ItemLevel': item['ItemLevel'], 'Quality':
        item['Quality'], 'm_ID': item['m_ID']}
    new_data.append(new_json)

with open('Items.json', 'w') as new_file:
    json.dump(new_data, new_file)