import json


class Items:
    def __init__(self):
        with open('ItemSparse.json') as data_file:
            self.parsed_json = json.load(data_file)

    def get_item(self, item_name):
        for item in self.parsed_json:
            if item['Name'] == item_name:
                return True, {'name': item_name, 'item level': item['ItemLevel'], 'quality': item['Quality'],
                              'id': item['m_ID']}
            else:
                return False

i = Items()
print(i.get_item('Vestige of Light'))