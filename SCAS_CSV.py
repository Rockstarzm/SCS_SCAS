import csv
#This is for the csv function because it has some interesting quirks

class Ships: #creates a class for the csv file to be imported into

    def __init__(self, team, name, type, ship_class, starting_zone, notes, attack, defense, health, combat_range, movement):
        self.team = team
        self.name = name
        self.type = type
        self.ship_class = ship_class
        self.starting_zone = starting_zone
        self.notes = notes
        self.attack = attack
        self.defense = defense
        self.health = health
        self.combat_range = combat_range
        self.movement =  movement


def import_obat(filename):
    ships = {}
    with open(filename, "r") as f:
        reader = csv.reader(f)#opens and reads the csv file
        next(reader) #skips header row
        for row in reader: #turns numbers from strings to integers, need to keep things in right row on csv
            row[-5] = int(row[-5])
            row[-4] = int(row[-4])
            row[-3] = int(row[-3])
            row[-2] = int(row[-2])
            row[-1] = int(row[-1])
            #this part turns the abbrivations from the csv into callable objects
            object_name = row[0] #abbrivations must the first row
            values = row[1:] #everything else gets assigned to a class
            data = Ships(*values) #actually assigning everything
            ships[object_name] = data
    print(f"Opening {filename}")
    return ships









#x = eval(input())
#y = eval(input())
#combatround(x, y)
#combatround(y, x)
    #for row in reader:
       # data_list = []
      #  for row in reader:
          #  data_list.append(Ships(*row))
       # for data in data_list:
          #  print(data.Team)
#for row in data_list:
  # variable_name = row[1].Abbriv
  # value = row[1]
  # exec(f"{variable_name} = {value}")
#
#print(usscl1)
#if __name__ == "__main__":
    #test = {}
    #df = pd.read_csv("SCSKinetics_MasterCopy.csv", usecols=["attack", "defense"])
    #test = df.to_dict()


#print(test)
#if __name__ == "__main__":
    #Name = {}
   # df = pd.read_csv("SCSKinetics_MasterCopy.csv", usecols=["Name"])
   # Name = df.to_dict()

#class SurfaceShip(): #creates a class of surface ships with 4 variables, attack, defense, range, health
   # def __init__(self, test):
 #       for key in test:
 #           setattr(self, key, test[key])

#if __name__ == "__main__":
      
  #  result = SurfaceShip(test)
      
    # printing the result
 #   print("After Converting Dictionary to Class : ")
 #   print(result.attack)
    
    #dict((Name[key], value) for (key, value) in result.attack)
