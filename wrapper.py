import aiohttp
import asyncio
import json
from apikey import api_key


class WowAPI:
    def __init__(self):  # Initiate the constructor
        self.session = aiohttp.ClientSession()
        self.api_key = api_key
        self.base_url = 'https://eu.api.battle.net/wow/'  # Define the base URL for all API calls
        self.base_cdn = 'https://blzmedia-a.akamaihd.net/wow/icons/'

    def create_icon_url(self, icon):
        small = self.base_cdn + '18/' + icon + '.jpg'
        med = self.base_cdn + '36/' + icon + '.jpg'
        large = self.base_cdn + '56/' + icon + '.jpg'

        return small, med, large

    def parse_gear(self, item):
        return {'name': item['name'], 'icon': self.create_icon_url(item['icon']), 'quality': item['quality']}

    def close(self):
        self.session.close()

    # Get the character stats of a selected character in a selected realm
    async def get_character_stats(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=stats&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            name = parsed_json['name']                            # Character name
            intellect = parsed_json['stats']['int']               # Intellect
            strength = parsed_json['stats']['str']                # Strength
            agility = parsed_json['stats']['agi']                 # Agility
            stamina = parsed_json['stats']['sta']                 # Stamina
            haste = parsed_json['stats']['haste']                 # Haste
            crit = parsed_json['stats']['crit']                   # Crit
            versatility = parsed_json['stats']['versatility']     # Versatility

        if resp.status == 200:  # Check for a 200 response code and return the variables as a dict
            return True, {'name': name, 'intellect': intellect, 'strength': strength, 'agility': agility, 'stamina':
                stamina, 'haste': haste, 'crit': crit, 'versatility': versatility}
        elif resp.status == 404:  # If the code comes back as 404, return the reason as a dict value
            reason = parsed_json['reason']
            return False, reason

    async def get_realm_status(self, realm):
        async with self.session.get(self.base_url + 'realm/status?locale=en_GB&realms={0}&apikey={apikey}'.format(
                realm, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            realm = [{'status': p['status'], 'name': p['name']} for p in parsed_json['realms']]

        if resp.status == 200:
            return True, realm
        elif resp.status == 404:
            reason = parsed_json['reason']
            return False, reason

    async def get_talents(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=talents&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']

            talents = []
            for item in parsed_json['talents']:
                for item2 in item['talents']:
                    talent = {
                        'tier': item2['tier'],
                        'name': item2['spell']['name'],
                        'icon': self.create_icon_url(item2['spell']['icon'])}
                    if 'spec' in item2:
                        talent.update({'spec': item2['spec']['name']})
                    talents.append(talent)

        if resp.status == 200:
            return True, char_name, realm, talents
        elif resp.status == 404:
            reason = parsed_json['reason']
            return False, reason

    async def get_professions(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=professions&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']
            professions = [{
                'name': p['name'],
                'icon': self.create_icon_url(p['icon']),
                'rank': p['rank'],
                'max': p['max']} for p in parsed_json['professions']['primary']]

        if resp.status == 200:
            return True, char_name, realm, professions
        elif resp.status == 404:
            reason = parsed_json['reason']
            return False, reason

    async def get_reputation(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=reputation&locale=en_GB&apikey='
                                            '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']
            faction = [{'name': p['name'], 'standing': p['standing'], 'value': p['value'], 'max': p['max']} for p in
                       parsed_json['reputation']]

        if resp.status == 200:
            return True, char_name, realm, faction
        elif resp.status == 404:
            reason = parsed_json['reason']
            return False, reason

    async def get_gear(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=items&locale=en_GB&apikey={apikey}'.format(
                                                realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']
            average_item_level = parsed_json['items']['averageItemLevel']
            average_item_level_equipped = parsed_json['items']['averageItemLevelEquipped']

            head = self.parse_gear(parsed_json['items']['head'])
            neck = self.parse_gear(parsed_json['items']['neck'])
            shoulder = self.parse_gear(parsed_json['items']['shoulder'])
            back = self.parse_gear(parsed_json['items']['back'])
            chest = self.parse_gear(parsed_json['items']['chest'])
            wrist = self.parse_gear(parsed_json['items']['wrist'])
            hands = self.parse_gear(parsed_json['items']['hands'])
            waist = self.parse_gear(parsed_json['items']['waist'])
            legs = self.parse_gear(parsed_json['items']['legs'])
            feet = self.parse_gear(parsed_json['items']['feet'])
            finger1 = self.parse_gear(parsed_json['items']['finger1'])
            finger2 = self.parse_gear(parsed_json['items']['finger2'])
            trinket1 = self.parse_gear(parsed_json['items']['trinket1'])
            trinket2 = self.parse_gear(parsed_json['items']['trinket2'])

            if resp.status == 200:
                return True, char_name, realm, average_item_level, average_item_level_equipped, head, neck, shoulder,\
                       back, chest, wrist, hands, waist, legs, feet, finger1, finger2, trinket1, trinket2
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_mounts(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=mounts&locale=en_GB&apikey='
                                            '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']
            mounts_collected = parsed_json['mounts']['numCollected']
            mounts_not_collected = parsed_json['mounts']['numNotCollected']
            mounts = [{
                'name': mount['name'],
                'icon': self.create_icon_url(mount['icon'])} for mount in parsed_json['mounts']['collected']]

            if resp.status == 200:
                return True, char_name, realm, mounts_collected, mounts_not_collected, mounts
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_progression(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=progression&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']

            progression = []
            for raid in parsed_json['progression']['raids']:
                bosses = []
                completed_raid = {
                    'name': raid['name'],
                    'lfr': raid['lfr'],
                    'normal': raid['normal'],
                    'heroic': raid['heroic'],
                    'mythic': raid['mythic'],
                    'bosses': bosses
                }
                for boss in raid['bosses']:
                    completed_boss = {'name': boss['name']}
                    if 'lfrKills' in boss:
                        completed_boss.update({'lfrKills': boss['lfrKills']})
                    if 'normalKills' in boss:
                        completed_boss.update({'normalKills': boss['normalKills']})
                    if 'heroicKills' in boss:
                        completed_boss.update({'heroicKills': boss['heroicKills']})
                    if 'mythicKills' in boss:
                        completed_boss.update({'mythicKills': boss['mythicKills']})
                    bosses.append(completed_boss)
                    progression.append(completed_raid)

            if resp.status == 200:
                return True, char_name, realm, progression
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_pvp(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=pvp&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']

            pvp_bracket = []
            for bracket in parsed_json['pvp']['brackets']:
                b = parsed_json['pvp']['brackets'][bracket]
                pvp_info = {
                    'bracket': bracket,
                    'slug': b['slug'],
                    'rating': b['rating'],
                    'weekly played': b['weeklyPlayed'],
                    'weeklyWon': b['weeklyWon'],
                    'weeklyLost': b['weeklyLost'],
                    'seasonPlayed': b['seasonPlayed'],
                    'seasonWon': b['seasonWon'],
                    'seasonLost': b['seasonLost']
                }
                pvp_bracket.append(pvp_info)

            if resp.status == 200:
                return True, char_name, realm, pvp_bracket
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_titles(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=titles&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']

            titles_collected = []
            for title in parsed_json['titles']:
                title_name = {'name': title['name']}
                titles_collected.append(title_name)

            if resp.status == 200:
                return True, char_name, realm, titles_collected
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_guild_members(self, realm, guild):
        async with self.session.get(self.base_url + 'guild/{0}/{1}?fields=members&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, guild, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            guild_name = parsed_json['name']
            realm = parsed_json['realm']

            members = []
            for member in parsed_json['members']:
                mchar = member['character']
                character = {
                    'name': mchar['name'],
                    'class': mchar['class'],
                    'race': mchar['race'],
                    'gender': mchar['gender'],
                    'level': mchar['level'],
                    'achievementPoints': mchar['achievementPoints']
                }

                spec = None
                if 'spec' in mchar:
                    spec = mchar['spec']
                    character['name'] = spec['name']

                character['icon'] = self.create_icon_url(spec['icon'])
                members.append(character)

            if resp.status == 200:
                return True, guild_name, realm, members
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

    async def get_pets(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=pets&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json['name']
            realm = parsed_json['realm']

            pets = []
            num_collected = parsed_json['pets']['numCollected']
            num_not_collected = parsed_json['pets']['numNotCollected']
            for pet in parsed_json['pets']['collected']:
                pet_collected = {
                    'name': pet['name'],
                    'icon': self.create_icon_url(pet['icon'])
                    }

                pets.append(pet_collected)

                stats = pet['stats']

                pet_stats = {
                    'level': stats['level'],
                    'health': stats['health'],
                    'power': stats['power'],
                    'speed': stats['speed']
                }

                pet_collected.update(pet_stats)

            if resp.status == 200:
                return True, char_name, realm, num_collected, num_not_collected, pets
            elif resp.status == 404:
                reason = parsed_json['reason']
                return False, reason

async def main():
    w = WowAPI()
    print(await w.get_pets('Silvermoon', 'Selariaana'))
    w.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



