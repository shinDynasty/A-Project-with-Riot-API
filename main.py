import requests
import json
import urllib.parse
import pandas as pd



# Game%20n%C3%A0y%20r%C3%A1c%20l%E1%BA%AFm
# api_url = f"https://vn2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"


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
        self.puuid = requests.get(api_url).json()["puuid"]


    # https://sea.api.riotgames.com/lol/match/v5/matches/by-self.puuid/wN1ZV_c8Gzw_iZYEyHyYAvshUreG_h5ZYuvPcF7T7401eov1u9X-kFLKX03DbvGFg92E8ZIYydh3fQ/ids?type=ranked&start=0&count=20&api_key=RGAPI-0013d416-08bd-4d73-b111-eba90aa7e75a

    def get_matches_id(self, region="sea", type="ranked", start=0, count=20):
        api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/match/v5/matches/by-self.puuid/" +
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


    def get_match_data(self, region, match_id):
        api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/match/v5/matches/" +
            match_id +
            "?api_key=" +
            self.__api_key
        )
        return requests.get(api_url).json()
    def find_player_data(self, match_data):
        participants = match_data['metadata']['participants']
        player_index = participants.index(self.puuid)
        player_data = match_data['info']['participants'][player_index]
        return player_data

    def gather_all_data(self, match_ids):
        # We initialise an empty dictionary to store data for each game
        data = {
            'champion': [],
            'kills': [],
            'deaths': [],
            'assists': [],
            'win': []
        }

        for match_id in match_ids:
        #     print(match_id)
        #     # run the two functions to get the player data from the match ID
        #     match_data = self.get_match_data("sea", match_id)
        #     player_data = self.find_player_data(match_data)
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



with open("sample.json", "w") as outfile:


    api_key = "RGAPI-0013d416-08bd-4d73-b111-eba90aa7e75a"
    summoner_name = "Game này rác lắm"
    sever = "vn2"

    player = Player(api_key, summoner_name, sever)
    match_ids = player.get_matches_id()
    #
    data = {
        'champion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': []
    }
    df = player.gather_all_data(match_ids)
    # print(df)
    # df['win'] = df['win'].astype(int)
    # print(df)
    #
    # # Find the averages
    # df.mean(numeric_only=True)  # numeric_only stops it trying to average the "champion" column
    #
    # # Get the averages per champion
    # df.groupby('champion').mean()
    #
    # # or maybe order your games by amount of kills
    # df.sort_values('kills')
# -__________________________________________________________________________
    # for match_id in matches:
    #     # print(match_id)
    #     # print(player.find_player_data(match_id))
    #     match_data = player.get_match_data("sea", match_id)
    #
    #     player_data = player.find_player_data(match_data)
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
    #     # part_index = player.get_match_data("sea", match)["metadata"]["participants"].index(player.self.puuid)
    #     # # print(part_index)
    #     # player_data = player.get_match_data("sea", match)["info"]["participants"][part_index]
    #     #
    #     # data = (
    #     #     player_data["championName"] + " " +
    #     #     str(player_data["kills"]) + " " +
    #     #     str(player_data["deaths"]) + " " +
    #     #     str(player_data["assists"]) + " " +
    #     #     str(player_data["totalDamageDealtToChampions"]) + " " +
    #     #     str(player_data["win"])
    #     # )
    #
    #     # print(data)
    # #
    # # data = player.get_match_data("sea", matches[0])
    # #
    # # part_index = data["metadata"]["participants"].index(player.self.puuid)
    # #
    # #
    #     # print(player_data["win"])
    #     json.dump(data, outfile ,indent = 4)


