import random

#Extra functions:
def br_collision(ship_blue, ship_red): #Bluefor/redfor collision
    c = random.randint(1,10) #rolls a d10 and assigns result to c
    if c <= 3: #30% chance that both ships take 1 damage
        ship_blue.health -= 1
        ship_red.health -= 1
        print(f"Collision! {ship_blue.name} and {ship_red.name} each take 1 damage.")
        if ship_blue.health <= 0:
            print(f"  {ship_blue.name} has been destroyed!")
        if ship_red.health <= 0:
            print(f"  {ship_red.name} has been destroyed!")
    else:
        print("No Collision")

def bb_collision(ship_blue1, ship_blue2): #blue on blue collision
    c = random.randint(1,10)#rolls a d10 and assigns result to c
    if c <=1: #10% chance that ships take 1 damage
        ship_blue1.health -=1
        ship_blue2.health -=1
        print(f"Collision! {ship_blue1.name} and {ship_blue2.name} each take 1 damage.")
        if ship_blue1.health <= 0:
            print(f"  {ship_blue1.name} has been destroyed!")
        if ship_blue2.health <= 0:
            print(f"  {ship_blue2.name} has been destroyed!")
    else:
        print("No Collision")

def initiative_order_generator(num_inputs):
    ships_in_combat = []
    for i in range(num_inputs):
        user_input = input("Enter ship: ")
        ships_in_combat.append((user_input, random.randint(1,100)))
    ships_in_combat.sort(key=lambda x: x[1], reverse=True)
    print("\n--- Initiative Order ---")
    for rank, (ship_name, roll) in enumerate(ships_in_combat, 1):
        print(f"  {rank}. {ship_name} (rolled {roll})")
    print()

#Meat and potatoes
def combatround(attacker, defender): #This is the actual how a combat works function
    attack_roll = sum(random.randint(1,8) for i in range(attacker.attack)) #sums random number d8 depending on attack value
    defense_roll = sum(random.randint(1,8) for j in range(defender.defense)) #sums random number d8 depending on defense values
    print(f"  {attacker.name} rolls {attacker.attack}d8 = {attack_roll}")
    print(f"  {defender.name} defends {defender.defense}d8 = {defense_roll}")
    damage = attack_roll - defense_roll
    if damage >= 1:
        defender.health = max(0, defender.health - damage)
        if defender.health <= 0:
            print(f"  {damage} damage! {defender.name} is sunk!")
        else:
            print(f"  {damage} damage! {defender.name} has {defender.health} health remaining")
    else:
        print(f"  {defender.name} successfully defended against attack")

def navalbattle(shipA, shipD):
    #naval battle function, shipA is attacking ship, shipD is defending ship
    if shipA.health <= 0:
        print(f"Error: {shipA.name} is already sunk (health: {shipA.health})")
        return
    if shipD.health <= 0:
        print(f"Error: {shipD.name} is already sunk (health: {shipD.health})")
        return

    defender_range_var = shipD.combat_range - shipA.combat_range
    print(f"\n--- {shipA.name} vs {shipD.name} ---")
    if defender_range_var < 0:
        print(f"{shipA.name} fires (defender out of range)")
        combatround(shipA, shipD)
    else:
        print(f"Both ships in range")
        combatround(shipA, shipD)
        if shipD.health > 0: #if Defender is still alive they get to shoot back
            combatround(shipD, shipA)
    print()
