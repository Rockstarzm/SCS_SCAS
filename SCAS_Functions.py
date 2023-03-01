import random
import SCAS_CSV

#Extra functions:
def br_collision(ship_blue, ship_red): #Bluefor/redfor collision
    c = random.randint(1,10) #rolls a d10 and assigns result to c
    if c <= 3: #30% chance that both ships take 1 damage
        ship_blue.health -= 1
        ship_red.health -= 1
        print("Collision")
    else:
        print("No Collision")

def bb_collision(ship_blue1, ship_blue2): #blue on blue collision
    c = random.randint(1,10)#rolls a d10 and assigns result to c
    if c <=1: #10% chance that ships take 1 damage
        ship_blue1.health -=1
        ship_blue2.health -=1
        print("Collision")
    else:
        print("No Collision")

def initiative_order_generator(num_inputs):
    ships_in_combat = []
    for i in range(num_inputs):
        user_input = input("Enter ship: ")
        ships_in_combat.append((user_input, random.randint(1,100)))
    ships_in_combat.sort(key=lambda x: x[1], reverse=True)
    for user_input, i in ships_in_combat:
        print(f"{user_input}")

#Meat and potatoes
def combatround(attacker, defender): #This is the actual how a combat works function
    x = sum(random.randint(1,8) for i in range(attacker.attack)) #sums random number d8 depending on attack value
    print(x)
    y = sum(random.randint(1,8) for j in range(defender.defense)) #sums random number d8 depending on defense values
    print(y)
    z = x - y #evaluates if attack value is bigger than defense value
    if z >= 1: #if it is then defending ship takes 1 point of damage for each value
        for z in range(0,z):
            defender.health -= 1
            if defender.health <= 0: #if the ship health =0 the ship is sunk
                print(defender.name, "sunk")
                break
        else:
            print(f"{defender.name} has {defender.health} health remaining")
    elif z < 1: #otherwise nothing happens
        print(defender.name, "successfully defended against attack")

def navalbattle (shipA, shipD):
    #naval battle fuction, shipA is attacking ship, shipD is defending ship, cur_combat_range is current combat range
    defender_range_var = shipD.combat_range - shipA.combat_range
    #subtracts defender ship's max range by the current combat range, assigns result to variable 
    if defender_range_var < 0: #checks if defender is out of range, if they are out of range then only attacker fires
        print("Attack ship shoots, defense ship can't")
        if shipA.health <= 0: #if the attack ship's health 
                print(f"Error: attacking ship is already sunk. \nAttacking ship, {shipA.name}, health is reporting as {shipA.health}")
        elif shipD.health <= 0:
                print(f"Error: defending ship is already sunk. \nDefending ship, {shipD.name}, health is reporting as {shipD.health}")
        else:
            combatround(shipA, shipD)
    else: #if both ships are in range than it checks for health
        print(f"Both are in range")
        if shipA.health <= 0: #if the attacking ship is sunk, then errors
                print(f"Error: attacking ship is already sunk. \nAttacking ship, {shipA.name}, health is reporting as {shipA.health}")
        elif shipD.health <= 0:#if the defending ship is sunk, then errors
                print(f"Error: defending ship is already sunk. \nDefending ship, {shipD.name}, health is reporting as {shipD.health}")
        else: #if nothing errors than combat! YAY!
            combatround(shipA, shipD)
            if shipD.health > 0: #if Defender is still alive than they get to shoot back
                combatround(shipD, shipA)

def shipstatchanger (shipA):
    print("IDK yet")

