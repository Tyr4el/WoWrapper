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
            return {'name': name, 'intellect': intellect, 'strength': strength, 'agility': agility, 'stamina':
                stamina, 'haste': haste, 'crit': crit, 'versatility': versatility}
        elif resp.status == 404:  # If the code comes back as 404, return the reason as a dict value
            reason = parsed_json.reason
            return {'reason': reason}

    async def get_realm_status(self, realm):
        async with self.session.get(self.base_url + 'realm/status?locale=en_GB&realms={0}&apikey={apikey}'.format(
                realm, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            realm = [{'status': p.status, 'name': p.name} for p in parsed_json.realms]

        if resp.status == 200:
            return realm
        elif resp.status == 404:
            reason = parsed_json.reason
            return {'reason': reason}

    #TODO: Finish this function - probably doesn't work
    async def get_talents(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=talents&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            name = parsed_json.name
            realm = parsed_json.realm
            talents = [{'name': p.name, 'description': p.description, 'cast time': p.castTime} for p in
                       parsed_json.talents.talents]
            spec = [{'name': p.name} for p in parsed_json.talents.talents]

        if resp.status == 200:
            return [name, realm, talents, spec]
        elif resp.status == 404:
            reason = parsed_json.reason
            return {'reason': reason}

    async def get_professions(self, realm, character):
        async with self.session.get(self.base_url + 'character/{0}/{1}?fields=professions&locale=en_GB&apikey='
                                                    '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            professions = [{'name': p.name} for p in parsed_json.professions.primary]

        if resp.status == 200:
            return professions
        elif resp.status == 404:
            reason = parsed_json.reason
            return reason

    async def get_reputation(self, realm, character):
        async with self.session.get(self.base_url +
                                            'character/{0}/{1}?fields=reputation&locale=en_GB&apikey='
                                            '{apikey}'.format(realm, character, apikey=self.api_key)) as resp:
            parsed_json = json.loads(await resp.text())
            faction = [{'name': p.name, 'standing': p.standing, 'value': p.value, 'max': p.max} for p in
                       parsed_json.reputation]

        if resp.status == 200:
            return faction
        elif resp.status == 404:
            reason = parsed_json.reason
            return reason