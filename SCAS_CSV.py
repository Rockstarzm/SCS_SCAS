import csv

class Ships:
    """Represents a naval unit with combat stats loaded from a CSV."""

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
        self.movement = movement


def import_obat(filename):
    """Import ship data from an OBAT CSV file.

    Expected CSV format: Abbreviation, Team, Name, Type, Ship Class,
    Starting Zone, Notes, Attack, Defense, Health, Combat Range, Movement
    """
    ships = {}
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            if not row or not row[0].strip():  # skip empty rows
                continue
            # Convert stat columns from strings to integers
            row[-5] = int(row[-5])
            row[-4] = int(row[-4])
            row[-3] = int(row[-3])
            row[-2] = int(row[-2])
            row[-1] = int(row[-1])
            object_name = row[0]  # abbreviation is the lookup key
            values = row[1:]
            data = Ships(*values)
            ships[object_name] = data
    print(f"Loaded {len(ships)} ships from {filename}")
    return ships
