import json


class Spells:
    def __init__(self):
        with open('Spell.json') as data_file:
            self.parsed_json = json.load(data_file)

    def get_spell(self, spell_name):
        for spell in self.parsed_json:
            if spell['Name'] == spell_name:
                return True, {'name': spell_name, 'description': spell['Description'], 'id': spell['m_ID']}
            else:
                return False
