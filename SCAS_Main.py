import random
import os
import sys
import json
import importlib.util
from time import sleep

# Resolve the script's directory from __file__, handling both absolute and
# relative paths as well as environments where __file__ may not be defined.
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isfile(os.path.join(SCRIPT_DIR, "SCAS_CSV.py")):
        raise ValueError
except (NameError, ValueError):
    # Fallback: search sys.argv and common locations
    for candidate in [os.getcwd()] + sys.path:
        if os.path.isfile(os.path.join(candidate, "SCAS_CSV.py")):
            SCRIPT_DIR = candidate
            break

def _load_local(name):
    """Import a .py file from the same directory as this script by file path."""
    path = os.path.join(SCRIPT_DIR, f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

SCAS_CSV = _load_local("SCAS_CSV")
_funcs = _load_local("SCAS_Functions")
navalbattle = _funcs.navalbattle
initiative_order_generator = _funcs.initiative_order_generator
bb_collision = _funcs.bb_collision
br_collision = _funcs.br_collision
SAVE_FILE = os.path.join(SCRIPT_DIR, "scas_save.json")

def save_health(ships):
    """Save current ship health values to a JSON file."""
    health_data = {abbr: ship.health for abbr, ship in ships.items()}
    with open(SAVE_FILE, "w") as f:
        json.dump(health_data, f, indent=2)
    print(f"Health saved to {SAVE_FILE}")

def load_health(ships):
    """Load saved health values from JSON file if it exists."""
    if not os.path.exists(SAVE_FILE):
        return False
    with open(SAVE_FILE, "r") as f:
        health_data = json.load(f)
    restored = 0
    for abbr, health in health_data.items():
        if abbr in ships:
            ships[abbr].health = health
            restored += 1
    print(f"Restored health for {restored} ships from save file.")
    return True

def find_csv_files():
    """Find all CSV files in the script's directory."""
    return [f for f in os.listdir(SCRIPT_DIR) if f.endswith(".csv")]

def pick_ship(ships, prompt):
    """Prompt user to select a ship by abbreviation. Returns None if skipped."""
    while True:
        abbr = input(prompt)
        if abbr == "0":
            print("Skipping")
            return None
        if abbr in ships:
            return ships[abbr]
        print(f"Ship not found. Available: {', '.join(ships.keys())}")

def show_ship_stats(ship):
    """Display all stats for a ship."""
    print(f"\n--- {ship.name} ---")
    print(f"  Team:          {ship.team}")
    print(f"  Type:          {ship.type}")
    print(f"  Class:         {ship.ship_class}")
    print(f"  Starting Zone: {ship.starting_zone}")
    print(f"  Attack:        {ship.attack}")
    print(f"  Defense:       {ship.defense}")
    print(f"  Health:        {ship.health}")
    print(f"  Combat Range:  {ship.combat_range}")
    print(f"  Movement:      {ship.movement}")
    if ship.notes:
        print(f"  Notes:         {ship.notes}")
    print()

def main():
    print("Welcome to the Strategic Combat Adjudication System (SCAS)!"
          "\nWritten and Designed by Zachary Miller"
          "\n---------------------------------------------------------------------------------------")
    sleep(1.0)

    # --- CSV Loading with auto-detect ---
    csv_files = find_csv_files()
    ships = None
    while ships is None:
        if csv_files:
            print("\nCSV files found in current directory:")
            for i, f in enumerate(csv_files, 1):
                print(f"  {i}. {f}")
            print(f"  0. Enter a file path manually")
            choice = input("Select a file (number): ").strip()
            if choice == "0":
                filepath = input("Enter full file path: ").strip()
            elif choice.isdigit() and 1 <= int(choice) <= len(csv_files):
                filepath = os.path.join(SCRIPT_DIR, csv_files[int(choice) - 1])
            else:
                print("Invalid selection, try again.")
                continue
        else:
            print("\nNo CSV files found in current directory.")
            filepath = input("Enter full file path to your OBAT .csv file: ").strip()

        try:
            ships = SCAS_CSV.import_obat(filepath)
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found. Please try again.")
        except Exception as e:
            print(f"Error reading file: {e}. Please try again.")

    # --- Offer to load saved health ---
    if os.path.exists(SAVE_FILE):
        choice = input("Saved health data found. Load it? (y/n): ").strip().lower()
        if choice == "y":
            load_health(ships)

    # --- Main loop ---
    running = True
    while running:
        x = input("\nPlease select:"
                   "\n  1. Naval combat"
                   "\n  2. Check ship stats"
                   "\n  3. Ship collision"
                   "\n  4. Generate initiative order"
                   "\n  5. Fleet battle (auto-pair by zone)"
                   "\n  6. Save health"
                   "\n  7. List all ships"
                   "\n  0. Exit program"
                   "\n  Input: ").strip()

        if x == "1": # --- Naval Battle ---
            user_input = input("Number of combats in this sea zone: ").strip()
            while True:
                try:
                    number_of_combats = int(user_input)
                    break
                except ValueError:
                    print("Error: Please enter a whole number")
                    user_input = input("Number of combats: ").strip()

            ships_in_combat = []
            for i in range(number_of_combats):
                shipA = pick_ship(ships, "Attacking ship: ")
                if shipA is None:
                    continue
                shipD = pick_ship(ships, "Defending ship: ")
                if shipD is None:
                    continue
                ships_in_combat.append([shipA, shipD])

            if ships_in_combat:
                sorted_ships = sorted(ships_in_combat, key=lambda p: (p[0].combat_range, random.random()), reverse=True)
                print("\n=== Combat Order (by range) ===")
                for pair in sorted_ships:
                    print(f"  {pair[0].name} vs {pair[1].name}")
                print()
                for pair in sorted_ships:
                    navalbattle(pair[0], pair[1])

        elif x == "2": # --- Ship Stats ---
            ship = pick_ship(ships, "Which ship to check? (0 to cancel): ")
            if ship:
                show_ship_stats(ship)

        elif x == "3": # --- Collision ---
            y = input("1. Friendly ships share a tile"
                      "\n2. Enemy ships share a tile"
                      "\n0. Back"
                      "\nInput: ").strip()
            if y == "1":
                ship1 = pick_ship(ships, "Friendly ship 1: ")
                ship2 = pick_ship(ships, "Friendly ship 2: ")
                if ship1 and ship2:
                    bb_collision(ship1, ship2)
            elif y == "2":
                ship1 = pick_ship(ships, "Ship 1: ")
                ship2 = pick_ship(ships, "Ship 2: ")
                if ship1 and ship2:
                    br_collision(ship1, ship2)
            elif y == "0":
                print("Back to selection")
            else:
                print("Error: expected 0, 1, or 2")

        elif x == "4": # --- Initiative Order ---
            user_input = input("Number of ships to roll initiative for: ").strip()
            try:
                num = int(user_input)
                initiative_order_generator(num)
            except ValueError:
                print("Error: Please enter a whole number")

        elif x == "5": # --- Fleet Battle (auto-pair by zone) ---
            # Get all unique zones that have ships from different teams
            zones = {}
            for abbr, ship in ships.items():
                if ship.health <= 0:
                    continue
                zone = ship.starting_zone
                if zone not in zones:
                    zones[zone] = {}
                team = ship.team
                if team not in zones[zone]:
                    zones[zone][team] = []
                zones[zone][team].append(ship)

            contested_zones = {z: teams for z, teams in zones.items() if len(teams) >= 2}

            if not contested_zones:
                print("No contested zones found (need ships from 2+ teams in the same zone).")
            else:
                print("\nContested zones:")
                zone_list = list(contested_zones.keys())
                for i, zone in enumerate(zone_list, 1):
                    teams = contested_zones[zone]
                    ship_count = sum(len(s) for s in teams.values())
                    print(f"  {i}. {zone} ({ship_count} ships, {len(teams)} teams)")

                choice = input("Select zone (number, or 0 to cancel): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(zone_list):
                    zone = zone_list[int(choice) - 1]
                    teams = contested_zones[zone]
                    team_names = list(teams.keys())

                    if len(team_names) == 2:
                        team_a, team_b = team_names
                    else:
                        print("Teams in this zone:")
                        for i, t in enumerate(team_names, 1):
                            print(f"  {i}. {t}")
                        a = int(input("Attacking team (number): ")) - 1
                        b = int(input("Defending team (number): ")) - 1
                        team_a, team_b = team_names[a], team_names[b]

                    attackers = teams[team_a]
                    defenders = teams[team_b]

                    # Pair ships: each attacker engages one defender, cycling if outnumbered
                    pairs = []
                    for i, attacker in enumerate(attackers):
                        defender = defenders[i % len(defenders)]
                        pairs.append([attacker, defender])

                    sorted_pairs = sorted(pairs, key=lambda p: (p[0].combat_range, random.random()), reverse=True)
                    print(f"\n=== Fleet Battle in {zone}: {team_a} vs {team_b} ===")
                    for pair in sorted_pairs:
                        print(f"  {pair[0].name} vs {pair[1].name}")
                    print()
                    for pair in sorted_pairs:
                        navalbattle(pair[0], pair[1])

        elif x == "6": # --- Save Health ---
            save_health(ships)

        elif x == "7": # --- List All Ships ---
            print("\n=== All Ships ===")
            for abbr, ship in ships.items():
                status = "SUNK" if ship.health <= 0 else f"{ship.health} HP"
                print(f"  [{abbr}] {ship.name} ({ship.team}) - {status}")
            print()

        elif x == "0": # --- Exit ---
            confirm = input("Save health before exiting? (y/n): ").strip().lower()
            if confirm == "y":
                save_health(ships)
            print("Closing Program")
            running = False

        else:
            print("Error: invalid selection")

main()
