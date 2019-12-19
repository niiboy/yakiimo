import sys
import random


class Dice():
    def __init__(self, face):
        self.face = face

    def roll(self):
        return random.randrange(1, self.face + 1)


class ButtleSystem():
    def __init__(self, players):
        self.players = players
        self.hero = players[0]
        self.enemy = players[1]

    def dice_roll(self, face, times):
        dice = Dice(face)
        return [dice.roll() for i in range(times)]

    def buttle(self):
        tmp_record = {}

        # なんか書く
        # for player in self.players:
        #     status = player.get_status()
        #     tmp_tech_pt = status["tech_pt"]

        #     dice_resutls = self.dice_roll(face=6, times=2)
        #     tmp_tech_pt += sum(dice_resutls)
        #     tmp_record[status["name"]] = tmp_tech_pt



        # return tmp_record
        pass

class Player():
    def __init__(self, name):
        self.name = name
        self.status = self._input_status()

    def _input_status(self):
        l = input("input status {}. hp, tech_pt >>".format(self.name)).split()
        if len(l) != 2:
            raise ValueError("invalid value!")

        status = {}
        status["name"] = self.name
        status["hp"] = int(l[0])
        status["tech_pt"] = int(l[1])

        return status

    def get_hp(self):
        return self.status["hp"]

    def get_tech_pt(self):
        return self.status["tech_pt"]

    def get_status(self):
        return self.status

    def get_damage(self):
        self.status["hp"] -= 2


def nake_players():
    players = []
    hero = Player("hero")
    enemy = Player("enemy")
    players.append(hero)
    players.append(enemy)
    return players

def main():
    players = nake_players()
    buttle_system = ButtleSystem(players)
    buttle_system.buttle()


if __name__=="__main__":
    main()
