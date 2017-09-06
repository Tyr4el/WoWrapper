import aiohttp
import json
from apikey import api_key


class WowAPI:
    def __init__(self):  # Initiate the constructor
        self.session = aiohttp.ClientSession()
        self.api_key = api_key
        self.base_url = 'https://eu.api.battle.net/wow/'  # Define the base URL for all API calls

    # Get the character stats of a selected character in a selected realm
    async def get_character_stats(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=stats&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            name = parsed_json.name                         # Character name
            intellect = parsed_json.stats.int               # Intellect
            strength = parsed_json.stats.str                # Strength
            agility = parsed_json.stats.agi                 # Agility
            stamina = parsed_json.stats.sta                 # Stamina
            haste = parsed_json.stats.haste                 # Haste
            crit = parsed_json.stats.crit                   # Crit
            versatility = parsed_json.stats.versatility     # Versatility

        if resp.status == 200:  # Check for a 200 response code and return the variables as a dict
            return True, {'name': name, 'intellect': intellect, 'strength': strength, 'agility': agility, 'stamina':
                stamina, 'haste': haste, 'crit': crit, 'versatility': versatility}
        elif resp.status == 404:  # If the code comes back as 404, return the reason as a dict value
            reason = parsed_json.reason
            return False, reason

    async def get_realm_status(self, realm):
        async with self.session.get(self.base_url + 'realm/status?locale=en_GB&realms={0}&apikey={apikey}'.format(
                realm, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            realm = [{'status': p.status, 'name': p.name} for p in parsed_json.realms]

        if resp.status == 200:
            return True, realm
        elif resp.status == 404:
            reason = parsed_json.reason
            return False, reason

    async def get_talents(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=talents&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json.name
            realm = parsed_json.realm

            talent = []
            for item in parsed_json.talents:
                for item2 in item.talents:
                    talents = {'tier': item2.tier, 'name': item2.spell.name, 'spec': item2.spec.name,
                               'icon': item2.spell.icon}
                    talent.append(talents)

        if resp.status == 200:
            return True, char_name, realm, talents
        elif resp.status == 404:
            reason = parsed_json.reason
            return False, reason

    async def get_professions(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=professions&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json.name
            realm = parsed_json.realm
            professions = [{'name': p.name, 'icon': p.icon, 'rank': p.rank, 'max': p.max} for p in
                           parsed_json.professions.primary]

        if resp.status == 200:
            return True, char_name, realm, professions
        elif resp.status == 404:
            reason = parsed_json.reason
            return False, reason

    async def get_reputation(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=reputation&locale=en_GB&apikey='
                                            '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json.name
            realm = parsed_json.realm
            faction = [{'name': p.name, 'standing': p.standing, 'value': p.value, 'max': p.max} for p in
                       parsed_json.reputation]

        if resp.status == 200:
            return True, char_name, realm, faction
        elif resp.status == 404:
            reason = parsed_json.reason
            return False, reason

    #  TODO: Finish this function.  Need to get item name, icon, quality and if it's part of a set
    async def get_gear(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=items&locale=en_GB&apikey={apikey}'.format(
                                                realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json.name
            realm = parsed_json.realm
            average_item_level = parsed_json.items.averageItemLevel
            average_item_level_equipped = parsed_json.items.averageItemLevelEquipped
            head = {'name': parsed_json.items.head.name, 'icon': parsed_json.items.head.icon, 'quality':
                parsed_json.items.head.quality}
            neck = {'name': parsed_json.items.neck.name, 'icon': parsed_json.items.neck.icon, 'quality':
                parsed_json.items.neck.quality}
            shoulder = {'name': parsed_json.items.shoulder.name, 'icon': parsed_json.items.shoulder.icon, 'quality':
                parsed_json.items.shoulder.quality}
            back = {'name': parsed_json.items.back.name, 'icon': parsed_json.items.back.icon, 'quality':
                parsed_json.items.back.quality}
            chest = {'name': parsed_json.items.chest.name, 'icon': parsed_json.items.chest.icon, 'quality':
                parsed_json.items.chest.quality}
            wrist = {'name': parsed_json.items.wrist.name, 'icon': parsed_json.items.wrist.icon, 'quality':
                parsed_json.items.wrist.quality}
            hands = {'name': parsed_json.items.hands.name, 'icon': parsed_json.items.hands.icon, 'quality':
                parsed_json.items.hands.quality}
            waist = {'name': parsed_json.items.waist.name, 'icon': parsed_json.items.waist.icon, 'quality':
                parsed_json.items.waist.quality}
            legs = {'name': parsed_json.items.legs.name, 'icon': parsed_json.items.legs.icon, 'quality':
                parsed_json.items.legs.quality}
            feet = {'name': parsed_json.items.feet.name, 'icon': parsed_json.items.feet.icon, 'quality':
                parsed_json.items.feet.quality}
            finger1 = {'name': parsed_json.items.finger1.name, 'icon': parsed_json.items.finger1.icon, 'quality':
                parsed_json.items.finger1.quality}
            finger2 = {'name': parsed_json.items.finger2.name, 'icon': parsed_json.items.finger2.icon, 'quality':
                parsed_json.items.finger2.quality}
            trinket1 = {'name': parsed_json.items.trinket1.name, 'icon': parsed_json.items.trinket1.icon, 'quality':
                parsed_json.items.trinket1.quality}
            trinket2 = {'name': parsed_json.items.trinket2.name, 'icon': parsed_json.items.trinket2.icon, 'quality':
                parsed_json.items.trinket2.quality}

            if resp.status == 200:
                return True, char_name, realm, average_item_level, average_item_level_equipped, head, neck, shoulder,\
                       back, chest, wrist, hands, waist, legs, feet, finger1, finger2, trinket1, trinket2
            elif resp.status == 404:
                reason = parsed_json.reason
                return False, reason

    async def get_mounts(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=mounts&locale=en_GB&apikey='
                                            '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            char_name = parsed_json.name
            realm = parsed_json.realm
            mounts_collected = parsed_json.mounts.numCollected
            mounts_not_collected = parsed_json.mounts.numNotCollected
            mounts = [{'name': mount.name, 'icon': mount.icon} for mount in parsed_json.mounts.collected]

            if resp.status == 200:
                return True, char_name, realm, mounts_collected, mounts_not_collected, mounts
            elif resp.status == 404:
                reason = parsed_json.reason
                return False, reason

