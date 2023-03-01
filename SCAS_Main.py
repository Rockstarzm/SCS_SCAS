import random
import SCAS_CSV
from SCAS_Functions import navalbattle, initiative_order_generator, bb_collision, br_collision
from time import sleep
#main loop def and calling it

def main(): #core game function
    #starts with some intro stuff
    running = True 
    print("Hello! Welcome to the Python Script for the Strategic Combat Adjudication System (SCAS)!" 
          "\nWritten and Designed by Zachary Miller"
          "\n---------------------------------------------------------------------------------------")
    sleep(1.5)
    print("You should be able to just type into your terminal to interact with the program."
          "\n---------------------------------------------------------------------------------------")
    sleep(1.5)
    print("You can learn more about this program in the SCAS file on the SCS Drive."
           "\nThis program is only intended to work with the google Sheet/CSV spreadsheet found in the SCAS Folder"
           "\n---------------------------------------------------------------------------------------")
    sleep(2.0)
    while True: #asks user to put in specific style of csv spreadsheet in instructions
        try:
            ships = SCAS_CSV.import_obat(input("Please write the exact file path and name of the .csv file you wish to upload."
                                       "\nThis will look something like /Users/zacharymiller/Downloads/Tranquil Seas OBAT.csv/"
                                       "\nYou can see other examples and more information in the SCAS Drive"
                                       "\nPlease remember to include the .csv "
                                       "\n  Input the file path here: "))
            break
        except FileNotFoundError: #if they do it wrong, then it errors and asks again
            ###bug: right now you have to exit the terminal if you can't input correct filename
            print("Error: File not found.")
            sleep(1.0)
    sleep(1.5)
    while running: #core game loop
        x = input("Please select" #core selector screen
                      "\n1 if you would like to initate a naval combat "
                      "\n2 if you would like to check or change a value on an asset (WIP) "
                      "\n3 if you would like to input a ship collision (Broken) "
                      "\n4 if you would like to generate an initiative order for combat (Defunct) "
                      "\n0 to end the program "
                      "\n  input: ")
                        ###Bug: most of these don't work rn
        if x == "1": #Naval Battle selector
            user_input = input("Please input the number of combats in this sea zone: ") #asks for number of combats, know how many times to iterate
            while True:
                try: 
                    number_of_combats = int(user_input)
                    break
                except ValueError: #error if they don't write down integer
                    print("Error: Please write in a whole integer")
                    user_input = input("Please input the number of combats in this sea zone: ")
        
            ships_in_combat = [] #creates a list for the combats
            for i in range(number_of_combats): #for the number of combats the program will ask for the attacking and defending ship in a pair
                while True:
                    object_name = input("Which ship is attacking: ") #asks for attacking ship
                    if object_name == "0": #can press 0 to skip input for devs
                        print("Skipping")
                        break
                    elif object_name in ships: #if unit exists in the ships list than it is shipA
                        shipA = ships[object_name]
                        break
                    else: #if the ship doesn't exist in the list
                        print("Ship not found")
                    
                while True:
                    object_name = input("Which ship is defending: ") #asks for attacking ship
                    if object_name == "0":
                        print("Skipping")
                        break
                    elif object_name in ships:
                        shipD = ships[object_name]
                        break
                    else:
                        print("Ship not found")
            
                ships_in_combat.append([shipA, shipD]) #adds the ordered pair to the list
                sorted_ships_in_combat = sorted(ships_in_combat, key=lambda x: (x[0].combat_range, random.random()), reverse=True) #sorts all the ships in combat by their combat_range
            for ship_pair in sorted_ships_in_combat: #Need to work on this more, but gives the name in the range of the attacking ship
                print(ship_pair[0].name)
            for ship_pair in sorted_ships_in_combat: #Runs combats starting with first pair on the list
                navalbattle(ship_pair[0], ship_pair[1])

        elif x == "2": #ship###Bug: Doesn't work
            while True:
                object_name = input("What ship's health would you like to check? ") #asks for attacking ship
                if object_name == "0":
                    print("Skipping")
                    break
                elif object_name in ships:
                    shipA = ships[object_name]
                    break
                else:
                    print("Ship not found")
            if shipA.health == 0:
                print(f"{shipA.name} is destroyed and has {shipA.health} health")
            else: 
                print(f"{shipA.name} has {shipA.health} health remaining")
       
        elif x == "3": #Collision sub-menu, no idea if this is really useful
            y = int(input("Press 1 if friendly ships share a tile"
                          "\nPress 2 if enemy ships share a tile"
                          "\nPress 0 to exit back to program select"
                          "\nInput: "))
            if y == 1: #blue on blue collision
                ship_blue1 = eval(input("Friendly ship 1 "))
                ship_blue2 = eval(input("Friendly ship 2 "))
                bb_collision(ship_blue1, ship_blue2)

            elif y == 2: #blue on red collision
                ship_blue = eval(input("Ship 1"))
                ship_red = eval(input("Ship 2 "))
                br_collision(ship_blue, ship_red)

            elif y == 0: #go back
                print("Back to selection")
                
            else: #what the heck
                print("Error: expected 0, 1, or 2")
        elif x == "4": #Defunct dont use
            num_input = int(input("Input the number of ships with the same initiative order: "))
            initiative_order_generator(num_input)

        elif x == "0": #end
            x = input(print("This will close the program and all health statistics will be reset "
                            "\nPlease confirm by pressing y (press n to return back)"
                            "\n (y/n): ")) #want to confirm closing by extra step
            if x == "y":
                print("Closing Program")
                running = False
            elif x=="n":
                running = True
            else:
                print("Error: expexted y or n (lowercase)")
        
        else: #error
            print("error: expected 0, 1, 2, or 3 ")
main()