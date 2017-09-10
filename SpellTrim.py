import json

parsed_json = None
with open('Spell.json') as file:
    parsed_json = json.load(file)

new_data = []
for spell in parsed_json:
    new_json = {'Name': spell['Name'], 'Description': spell['Description'], 'm_ID': spell['m_ID']}
    new_data.append(new_json)

with open('Spell_Trimmed.json', 'w') as new_file:
    json.dump(new_data, new_file)
