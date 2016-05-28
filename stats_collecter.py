import requests
import json
import sys
from collections import defaultdict
from prettytable import PrettyTable

class PlayerStats:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.goals = 0
        self.assists = 0
        self.saves = 0
        self.shots = 0
        self.played = 0

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def add(self, score=0, goals=0,
            assists=0, saves=0, shots=0):
        self.score = self.score * self.played
        self.played += 1
        self.score += score
        self.score = self.score / self.played
        self.goals += goals
        self.assists += assists
        self.saves += saves
        self.shots += shots

    def getstats(self):
        return ([self.name, self.score, self.goals,
            self.assists, self.saves, self.shots])

def get_data (data, players, stats):
    for replay in data["replays"]:
        for player in replay["player_set"]:
            player_name = player["player_name"]
            if (player_name == players[0] or
                    player_name == players[1] or
                    player_name == players[2]):
                previous_stats = stats[player_name]
                if not previous_stats is None:
                    previous_stats.add(
                            score=player['score'],
                            goals=player['goals'],
                            assists=player['assists'],
                            saves=player['saves'],
                            shots=player['shots'])
                    stats[player_name] = previous_stats


def main():
    replay_pack = raw_input("What is the ID of the replay pack? (check the URL): ")
    url = 'https://www.rocketleaguereplays.com/api/replay-packs/'\
            + str(replay_pack)
    print("Accessing RocketLeagueReplays.com...")
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Error in accessing RocketLeagueReplays.com")
        sys.exit(1)
    if response.ok:
        print("Success!\n")
        data = json.loads(response.content)
        title = data["title"]
        stats = defaultdict(dict)
        players = []
        for i in range(0,3):
            players.append(raw_input("Name for player " + str(i + 1)
                + ": "))
            stats[players[i]] = PlayerStats(players[i])

        print ("\n")
        get_data(data, players, stats)

        # We now have all the stats
        table = PrettyTable(['Name', 'Score per game', 'goals',
            'assists', 'saves', 'shots'])
        for i in range(0,3):
            player = stats[players[i]]
            table.add_row(player.getstats())

        print title
        print table

if __name__ == '__main__':
    main()
