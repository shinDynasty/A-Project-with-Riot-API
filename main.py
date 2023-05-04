import json
import urllib.parse
import pandas as pd
import time
import requests
summoner_name = "Game này rác lắm"
sever = "vn2"


def getAPI_key():
    return open("API.txt", "r").read()


api_key = getAPI_key()

status = {
    400: "Bad request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Data not found",
    405: "Method not allowed",
    415: "Unsupported media type",
    429: "Rate limit exceeded",
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout"
}

class Player:
    def __init__(self, api_key, summoner_name, sever):
        self.__api_key = api_key
        self.name = urllib.parse.quote(summoner_name)
        api_url = (
                "https://" +
                sever +
                ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
                self.name +
                "?api_key=" +
                self.__api_key
        )
        resp = requests.get(api_url)
        if resp.status_code == 200:
            self.puuid = resp.json()["puuid"]
        else:
            self.puuid = status[resp.status_code]
        self.info = {
            "teammate" : [],
            "enemy" : [],
            "lane" : {
                "TOP" : [],
                "JUNGLE": [],
                "MIDDLE": [],
                "BOTTOM": [],
                "UTILITY": []

            }
        }


    # https://sea.api.riotgames.com/lol/match/v5/matches/by-self.puuid/wN1ZV_c8Gzw_iZYEyHyYAvshUreG_h5ZYuvPcF7T7401eov1u9X-kFLKX03DbvGFg92E8ZIYydh3fQ/ids?type=ranked&start=0&count=20&api_key=RGAPI-0013d416-08bd-4d73-b111-eba90aa7e75a

    def get_matches_id(self, region="sea", type="ranked", start=0, count=1):
        api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
            self.puuid +
            "/ids?type=" +
            type +
            "&start=" +
            str(start) +
            "&count=" +
            str(count) +
            "&api_key=" +
            self.__api_key
        )
        return requests.get(api_url).json()


    def get_match_data(self, match_id, region="sea"):
        api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/match/v5/matches/" +
            match_id +
            "?api_key=" +
            self.__api_key
        )
        while True:
            resp = requests.get(api_url)

            # whenever we see a 429, we sleep for 10 seconds and then restart from the top of the "while" loop
            if resp.status_code == 429:
                print("Rate Limit hit, sleeping for 10 seconds")
                time.sleep(10)
                # continue means start the loop again
                continue

            # if resp.status_code isn't 429, then we carry on to the end of the function and return the data
            match_data = resp.json()
            return match_data
    def find_player_data(self, match_data):
        participants = match_data['metadata']['participants']
        player_index = participants.index(self.puuid)
        player_data = match_data['info']['participants'][player_index]
        return player_data

    def gather_all_data(self, match_ids):
        # We initialise an empty dictionary to store data for each game
        data = {
            "info": {
                "name": [],
                "puuid": [],
                'champion': [],
                "lane": [],
                "cs": [],
                "csBefore10Mins": []
            },
            "baseStatus": {
                'gameTime': [],
                'kills': [],
                'deaths': [],
                'assists': [],
                "kda": [],
            },
            "economics": {
                "goldEarned": [],
                "goldSpent": [],
                "goldPerMinute": [],
            },
            "combat": {
                "totalDamageDealtToChampions": [],
                "damageTakenPerMinute": [],
                "damageTakenPerGold": [],
                "damagePerMinute": [],
                "damagePerGold": [],
            },
            "items": [],

            'win': []
        }
        for match_id in match_ids:

            participants = self.get_match_data(match_id)['metadata']['participants']
            player_index = participants.index(self.puuid)
            match_data = self.get_match_data(match_id)["info"]['participants']
            with open(f"match_data.json", "w") as outfile:

                json.dump(match_data, outfile, indent=4)


            for i in range(10):
                with open(f"player_{i}.json", "w") as outfile:
                    # infor player
                    data["info"]["name"] = match_data[i]["summonerName"]
                    data["info"]["puuid"] = match_data[i]["puuid"]
                    data["info"]["champion"] = match_data[i]["championName"]
                    data["info"]["lane"] = match_data[i]["individualPosition"]
                    data["info"]["cs"] = match_data[i]["totalMinionsKilled"] + match_data[i]["neutralMinionsKilled"]
                    data["info"]["csBefore10Minutes"]


                    # base status
                    game_Length = match_data[i]["challenges"]["gameLength"]
                    minutes = game_Length // 60
                    seconds = game_Length % 60
                    data["baseStatus"]["gameTime"] = (minutes + round(seconds/100, 2))
                    data["baseStatus"]["kills"] = match_data[i]["kills"]
                    data["baseStatus"]["deaths"] = match_data[i]["deaths"]
                    data["baseStatus"]["assists"] = match_data[i]["assists"]
                    data["baseStatus"]["kda"] = (data["baseStatus"]["kills"] + data["baseStatus"]["assists"]) / data["baseStatus"]["deaths"]
                    data["baseStatus"]["kda"] = round(data["baseStatus"]["kda"], 2)
                    #Economics
                    data["economics"]["goldEarned"] = match_data[i]["goldEarned"]
                    data["economics"]["goldSpent"] = match_data[i]["goldSpent"]
                    data["economics"]["goldPerMinute"] = match_data[i]["challenges"]["goldPerMinute"]

                    data["items"] = [match_data[i][f"item{k}"] for k in range(6)]

                    #Combat
                    data["combat"]["totalDamageDealtToChampions"] =  match_data[i]["totalDamageDealtToChampions"]
                    data["combat"]["totalDamageTaken"] = match_data[i]["totalDamageTaken"]
                    data["combat"]["damageTakenPerGold"] = data["combat"]["totalDamageTaken"] / data["economics"]["goldEarned"]
                    data["combat"]["damageTakenPerMinute"] = data["combat"]["totalDamageTaken"] / data["baseStatus"]["gameTime"]

                    data["combat"]["damagePerMinute"] = match_data[i]["challenges"]["damagePerMinute"]
                    data["combat"]["damagePerGold"] = data["combat"]["damagePerMinute"] / data["economics"]["goldPerMinute"]


                    data["win"] = match_data[i]["win"]
                    json.dump(data, outfile, indent=4)
            print("done")




        #
        #     # assign the variables we're interested in
        #     champion = player_data['championName']
        #     k = player_data['kills']
        #     d = player_data['deaths']
        #     a = player_data['assists']
        #     win = player_data['win']
        #
        #     # add them to our dataset
        #     data['champion'].append(champion)
        #     data['kills'].append(k)
        #     data['deaths'].append(d)
        #     data['assists'].append(a)
        #     data['win'].append(win)
        #
        # df = pd.DataFrame(data)
        #
        # return df

#

with open("player.json", "w") as outfile:

    player = Player(api_key, summoner_name, sever)
    match_ids = player.get_matches_id()
    #
    df = player.gather_all_data(match_ids)
    # json.dump(match_player_data, outfile, indent=4)
