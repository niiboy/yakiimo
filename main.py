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
        self.utils = Utils()

    def judge_loser(self, hero_tech, enemy_tech):
        if hero_tech < enemy_tech:
            print("hero has damage!")
            return self.hero

        elif enemy_tech < hero_tech:
            print("enemy has damage!")
            return self.enemy

        else:
            print("draw!\n")
            return None

    def judge_good_luck(self):
        luck_pt = self.hero.set_luck_pt()
        util = Utils()
        result = util.dice_roll(face=6, times=2)
        if sum(result) <= luck_pt:
            print("Succes!")
            return True
        else:
            print("Falied...")
            return False

    def caluclate_tech_pt(self):
        hero_tech = self.hero.get_tech_pt() + sum(self.utils.dice_roll(6, 2))
        print(f"hero has {hero_tech} tech pt.")

        enemy_tech = self.enemy.get_tech_pt() + sum(self.utils.dice_roll(6, 2))
        print(f"enemy has {enemy_tech} tech pt.")
        return hero_tech, enemy_tech

    def confirm_to_use_luck(self):
        while True:
            answer = input(f"Do you use luck point? [y]/[n] >>")
            if answer == "y":
                print("use luck point!")
                return True
            elif answer == "n":
                return False
            else:
                print("please enter [y]/[n]")

    def ajust_damage(self, loser):
        damage = 2
        if loser.name == "hero":
            if self.judge_good_luck():
                damage -= 1
            else:
                damage += 1
        if loser.name == "enemy":
            if self.judge_good_luck():
                damage += 2
            else:
                damage -= 1
        print(f"damage is {damage}")
        return damage


    def buttle(self):
        counter = 1
        while min(self.hero.get_hp(), self.enemy.get_hp()) > 0:
            print(f"{counter} turn: \n")
            hero_tech, enemy_tech = self.caluclate_tech_pt()
            loser = self.judge_loser(hero_tech, enemy_tech)

            if loser is None:
                continue
            print(f"hero has hp:{self.hero.get_hp()}")
            print(f"enemy has hp:{self.enemy.get_hp()}")

            damage = 2
            if self.luck_mode is True:
                use_luck = self.confirm_to_use_luck()
                if use_luck is True:
                    damage = self.ajust_damage(loser)
                else:
                    damage = 2

            loser.get_damage(damage)
            loser.check_dead()
            sleep(3)
            counter += 1


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

    def set_luck_pt(self):
        l = input(f"input status {self.name}. luck point >> ")
        self.status["luck"] = int(l)
        return self.status["luck"]

    def loss_luck(self):
        self.status["luck"] -= 1

    def get_luck_pt(self):
        return self.status["luck"]

    def get_hp(self):
        return self.status["hp"]

    def get_tech_pt(self):
        return self.status["tech_pt"]

    def get_status(self):
        return self.status

    def check_dead(self):
        if self.status["hp"] <= 0:
            print(f"{self.name} has dead!")

    def get_damage(self, damage):
        self.status["hp"] -= damage
        print(f"{self.name} has {self.status['hp']} hp!\n")


class Utils():
    def __init__(self):
        pass

    def make_players(self):
        players = []
        hero = Player("hero")
        enemy = Player("enemy")
        players.append(hero)
        players.append(enemy)
        return players

    def get_option(self):
        argparser = ArgumentParser()
        argparser.add_argument('-s', '--slow',
                                action="store_true",
                                help='use slow mode.')

        argparser.add_argument('-l', '--luck',
                                action="store_true",
                                help='confirm to use the luck point.')

        argparser.add_argument('-dr', '--diceroll',
                                action="store_true",
                                help='dice roll.')

        return argparser.parse_args()

    def dice_roll(self, face, times):
        dice = Dice(face)
        result = [dice.roll() for i in range(times)]
        print(f"dice roll results is {result}")
        return result


def main():
    utils = Utils()
    option = utils.get_option()
    if option.diceroll is True:
        utils.dice_roll(face=6, times=2)
        sys.exit()

    players = utils.make_players()
    buttle_system = ButtleSystem(players, option)
    buttle_system.buttle()

if __name__=="__main__":
    main()
