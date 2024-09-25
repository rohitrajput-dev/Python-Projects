import time
import numpy as np
import sys
import random

# Delay printing

def delay_print(s):
    # print one character at a time
    # https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
    try:
        for c in s:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting...")
        sys.exit(0)  # This will stop the program immediately.

# Create the class
class Pokemon:
    def __init__(self, name, types, moves, EVs, health='==================='):
        # save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = EVs['ATTACK']
        self.defense = EVs['DEFENSE']
        self.health = health
        self.bars = 20 # Amount of health bars


    def fight(self, Pokemon2):
        

        # Allow two pokemon to fight each other
        # Print fight information
        print("-----POKEMONE BATTLE-----")
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", 3*(1+np.mean([self.attack,self.defense])))
        print("\nVS")
        print(f"\n{Pokemon2.name}")
        print("TYPE/", Pokemon2.types)
        print("ATTACK/", Pokemon2.attack)
        print("DEFENSE/", Pokemon2.defense)
        print("LVL/", 3*(1+np.mean([Pokemon2.attack,Pokemon2.defense])))

        time.sleep(2)

        # Consider type advantages
        version = ['Fire', 'Water', 'Grass']
        for i,k in enumerate(version):
            if self.types == k:
                # Both are same type
                if Pokemon2.types == k:
                    string_1_attack = '\nIts not very effective...'
                    string_2_attack = '\nIts not very effective...'

                # Pokemon2 is STRONG
                if Pokemon2.types == version[(i+1)%3]:
                    Pokemon2.attack *= 2
                    Pokemon2.defense *= 2
                    self.attack /= 2
                    self.defense /= 2
                    string_1_attack = '\nIts not very effective...\n\n'
                    string_2_attack = '\nIts super effective!\n\n'

                # Pokemon2 is WEAK
                if Pokemon2.types == version[(i+2)%3]:
                    self.attack *= 2
                    self.defense *= 2
                    Pokemon2.attack /= 2
                    Pokemon2.defense /= 2
                    string_1_attack = '\nIts super effective!\n\n'
                    string_2_attack = '\nIts not very effective...\n\n'


        # Now for the actual fighting...
        # Continue while pokemon still have health
        money = np.random.randint(200,5000)
        name_width = 20
        health_width = 20

        # Print header
        print(f"\n{'Name'.ljust(name_width)}\tHLTH")
        print(f"{'-' * name_width}\t{'-' * health_width}")

        # Print details for this Pokémon and the other Pokémon
        print(f"{self.name.ljust(name_width)}\t{str(self.health).ljust(health_width)}")
        print(f"{Pokemon2.name.ljust(name_width)}\t{str(Pokemon2.health).ljust(health_width)}\n")

        while (self.bars > 0) and (Pokemon2.bars > 0):

            print(f"Go {self.name}!\n")
            for i, x in enumerate(self.moves):
                print(f"{i+1}.", x)
            mov_len = len(self.moves)
            move_skip = False
            try:
                index = int(input('Pick a move: '))
                if index > 0 and index <= mov_len: 
                    delay_print(f"\n{self.name} used {self.moves[index-1]}!")
                    move_skip = False
                else:
                    print(1/0)
                time.sleep(0.5)
                delay_print(string_1_attack)
            except KeyboardInterrupt:
                print("\nProcess interrupted by the user. Exiting...")
                sys.exit(0)  # This will stop the program immediately.
            except:
                move_skip = True
                delay_print("\nYou didn't select your move from the options...\n")
                delay_print("\nYou have wasted your move!\n\n")


            # Determine damage
            if not move_skip:
                Pokemon2.bars -= self.attack
                Pokemon2.health = ""

                # Add back bars plus defense boost
                for j in range(int(Pokemon2.bars+.1*Pokemon2.defense)):
                    Pokemon2.health += "="

            time.sleep(1)
            # Print header
            print(f"\n{'Name'.ljust(name_width)}\tHLTH")
            print(f"{'-' * name_width}\t{'-' * health_width}")

            # Print details for this Pokémon and the other Pokémon
            print(f"{self.name.ljust(name_width)}\t{str(self.health).ljust(health_width)}")
            print(f"{Pokemon2.name.ljust(name_width)}\t{str(Pokemon2.health).ljust(health_width)}")
            time.sleep(.5)

            # Check to see if Pokemon fainted
            if Pokemon2.bars <= 0:
                delay_print("\n..." + Pokemon2.name + ' fainted.')
                delay_print(f"\nOpponent paid you ${money}.\n\n")
                break

            # Pokemon2s turn

            print(f"\n{Pokemon2.name}'s turn!")
            time.sleep(0.5)
            index = random.randint(1, len(Pokemon2.moves))
            delay_print(f"\n{Pokemon2.name} used {Pokemon2.moves[index-1]}!\n")
            time.sleep(1)
            delay_print(string_2_attack)

            # Determine damage
            self.bars -= Pokemon2.attack
            self.health = ""

            # Add back bars plus defense boost
            for j in range(int(self.bars+.1*self.defense)):
                self.health += "="

            time.sleep(1)
            # Print header
            print(f"{'Name'.ljust(name_width)}\tHLTH")
            print(f"{'-' * name_width}\t{'-' * health_width}")

            # Print details for this Pokémon and the other Pokémon
            print(f"{self.name.ljust(name_width)}\t{str(self.health).ljust(health_width)}")
            print(f"{Pokemon2.name.ljust(name_width)}\t{str(Pokemon2.health).ljust(health_width)}")
            time.sleep(0.5)

            # Check to see if Pokemon fainted
            if self.bars <= 0:
                delay_print("\n..." + self.name + ' fainted.')
                delay_print(f"\nYou paid your opponent ${money}.\n\n")
                break

if __name__ == '__main__':

    pokemons = [
    ['Charizard', 'Fire', ['Flamethrower', 'Fly', 'Blast Burn', 'Fire Punch'], {'ATTACK':12, 'DEFENSE': 8}],
    ['Charmeleon', 'Fire', ['Ember', 'Scratch', 'Flamethrower', 'Fire Punch'], {'ATTACK': 6, 'DEFENSE': 5}],
    ['Charmander', 'Fire', ['Ember', 'Scratch', 'Tackle', 'Fire Punch'], {'ATTACK': 4, 'DEFENSE': 2}],
    ['Squirtle', 'Water', ['Bubblebeam', 'Tackle', 'Headbutt', 'Surf'], {'ATTACK': 3, 'DEFENSE': 3}],
    ['Blastoise', 'Water', ['Water Gun', 'Bubblebeam', 'Hydro Pump', 'Surf'], {'ATTACK': 10, 'DEFENSE': 10}],
    ['Wartortle', 'Water', ['Bubblebeam', 'Water Gun', 'Headbutt', 'Surf'], {'ATTACK': 5, 'DEFENSE': 5}],
    ['Venusaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Earthquake', 'Frenzy Plant'], {'ATTACK': 8, 'DEFENSE': 12}],
    ['Bulbasaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Tackle', 'Leech Seed'], {'ATTACK': 2, 'DEFENSE': 4}],
    ['Ivysaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Bullet Seed', 'Leech Seed'], {'ATTACK': 4, 'DEFENSE': 6}]
]
    delay_print("\n-----Welcom to Pokemon BattleGround-----\n\n")
    delay_print("Hello Trainer.\n")
    delay_print("Choose the type of your Pokemon for the battle!\n")
    time.sleep(0.05)

    typeNindex = {
        1 : "Fire",
        2 : "Water",
        3 : "Grass"
    }
    print(f"\n1.  Fire\n2. Water \n3. Grass\nChoose: ", end="")
    try:
        pok_type = int(input().strip())
        if pok_type < 4 and pok_type >0:
            print("\n\nYour  Pokemon Type is: ", end="")
        else:
            print(1/0)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting...")
        sys.exit(0)
    except:
        pok_type = random.randint(1,3)
        delay_print("\nYour Choice wasn't valid, so randomly Choosing your Pokemon Type.\n")
        print("Your  Pokemon Type is: ", end="")
    delay_print(f"{typeNindex[pok_type]}.\n")


    if  pok_type == 1:
        random_range = list(range(1,4))
    elif  pok_type == 2:
        random_range = list(range(4,7))
    else:
        random_range = list(range(7,10))

    delay_print("\nChoose any Pokemon from below:\n")
    for i, j in  enumerate(random_range):
        print(f"{i+1}. {pokemons[j-1][0]}")
    print("Choose: ", end="")
    try:
        pok_index = int(input().strip())
        indexForList = random_range[pok_index-1]
        if pok_index < 4 and pok_index >0:
            print("\n\nYour Pokemon is: ", end="")
            delay_print(f"{pokemons[indexForList][0]}\n")
        else:
            print(1/0)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting...")
        sys.exit(0)  # This will stop the program immediately.
    except:
        indexForList = random.randint(random_range[0],random_range[-1])-1
        delay_print("\nYou didn't choose Pokemon from the list below...\n")
        delay_print("Randomly choosing Pokemon for you.\n")

    opp_random_pok = random.randint(1,len(pokemons))


    opp_pok_index = opp_random_pok - 1

    while indexForList == opp_random_pok:
        opp_pok_index = random.randint(1,9) - 1
    time.sleep(1)
    delay_print(f"*** You got {pokemons[indexForList][0]} ***\n\n")

    pok1 = Pokemon(pokemons[indexForList][0], pokemons[indexForList][1], pokemons[indexForList][2],pokemons[indexForList][3])
    pok2 = Pokemon(pokemons[opp_pok_index][0], pokemons[opp_pok_index][1], pokemons[opp_pok_index][2],pokemons[opp_pok_index][3])

    pok1.fight(pok2) # Get them to fight