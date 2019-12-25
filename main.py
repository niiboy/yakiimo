import sys
import random
from argparse import ArgumentParser
from time import sleep

class Dice():
    def __init__(self, face):
        self.face = face

    def roll(self):
        return random.randrange(1, self.face + 1)


class ButtleSystem():
    def __init__(self, players, option):
        self.players = players
        self.hero = players[0]
        self.enemy = players[1]
        self.luck_mode = option.luck
        self.slow_mode = option.slow

    def dice_roll(self, face, times):
        dice = Dice(face)
        result = [dice.roll() for i in range(times)]
        print(f"dice roll results is {result}")
        return result

    def judge(self):
        hero_tech = self.hero.get_tech_pt() + sum(self.dice_roll(6, 2))
        print(f"hero has {hero_tech} tech pt.")

        enemy_tech = self.enemy.get_tech_pt() + sum(self.dice_roll(6, 2))
        print(f"enemy has {enemy_tech} tech pt.")

        if hero_tech < enemy_tech:
            print("hero has damage!")
            self.hero.get_damage()
        elif enemy_tech < hero_tech:
            print("enemy has damage")
            self.enemy.get_damage()
        else:
            print("draw!\n")


    def buttle(self):
        while min(self.hero.get_hp(), self.enemy.get_hp()) > 0:
            self.judge()
            if self.slow_mode is True:
                sleep(2)



class Player():
    def __init__(self, name):
        self.name = name
        self.status = self._input_status()

    def _input_status(self):
        l = input(f"input status {self.name}. hp, tech_pt >> ").split()
        if len(l) != 2:
            raise ValueError("invalid value!")

        status = {}
        status["name"] = self.name
        status["hp"] = int(l[0])
        status["tech_pt"] = int(l[1])

        return status

    def set_luck(self):
        l = input(f"input status {self.name}. luck point >> ")
        self.status["luck"] = int(l)

    def loss_luck(self):
        self.status["luck"] -= 1

    def get_hp(self):
        return self.status["hp"]

    def get_tech_pt(self):
        return self.status["tech_pt"]

    def get_status(self):
        return self.status

    def get_damage(self):
        self.status["hp"] -= 2
        print(f"{self.name} has {self.status['hp']} hp!\n")
        if self.status["hp"] <= 0:
            print(f"{self.name} has dead!")


def nake_players():
    players = []
    hero = Player("hero")
    enemy = Player("enemy")
    players.append(hero)
    players.append(enemy)
    return players

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-s', '--slow',
                            action="store_true",
                            help='use slow mode.')

    argparser.add_argument('-l', '--luck',
                            action="store_true",
                            help='confirm the luck point.')

    return argparser.parse_args()

def main():
    option = get_option()
    players = nake_players()
    buttle_system = ButtleSystem(players, option)
    buttle_system.buttle()


if __name__=="__main__":
    main()
