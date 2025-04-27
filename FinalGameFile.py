import time
from character import Character_Creator
from enemy import create_rooms
current_room_index = 0

def explore_room(character, rooms): 
    """room exploration loop. main game function 1. Search room, 2. Move forward, 3. View inventory, 4. End game."""

    global current_room_index
    game_over = False

    while not game_over:
        if not character.lives():
            print(f"{character.name} has been slain. A shame they weren't more useful.")
            game_over = True
            continue

        rooms[current_room_index].visit(character, rooms, current_room_index)
        time.sleep(0.5)

        print("\nChoose your action:")
        print("1. Search the room")
        print("2. Move to the next room")
        print("3. Check Inventory")
        print("4. Quit Game")

        action_choice = input("What would you like to do? (1/2/3/4): ").strip()

        if action_choice == '1':
            rooms[current_room_index].search_room(character)
            print("Room searched", flush=True)

        elif action_choice == '2':
            current_room_index += 1
            print("You move to the next room.")
            time.sleep(0.5)
        
        elif action_choice == '3':
            while True:
                print(f"\n{character.name} | Health: {character.health}/{character.max_health} | Attack: {character.attack} | Defense: {character.defense}")
                character.inventory.view_inventory()

                all_items = character.inventory.small_items + character.inventory.large_items

                if not all_items:
                    print("Your inventory is empty. Nothing to use.")
                    break

                use_item_choice = input("\nWould you like to use an item? (y/n): ").strip().lower()
                if use_item_choice not in ('y', 'yes'):
                    print("You decide not to use an item.")
                    break

                print("\nChoose an item to use:")
                for idx, item in enumerate(all_items, 1):
                    print(f"{idx}. {item.name} - {item.item_description()}")

                item_choice = input("Choose an item number to use (or press Enter to cancel): ").strip()

                if not item_choice:
                    print("You decide not to use an item.")
                    break

                try:
                    item_idx = int(item_choice) - 1
                    if 0 <= item_idx < len(all_items):
                        item = all_items[item_idx]
                        character.use_item(item)
                        character.inventory.remove_item(item)
                        break
                    else:
                        print("Invalid choice, please select a valid item.")
                except ValueError:
                    print("Invalid input, please enter a number.")
        elif action_choice == '4':
            print("Overwhelmed by the vastness of the complex, you go mad and abandon your mission. "
            "\nThis will be noted in your report.")
            game_over = True
            continue
        else:
            print("Invalid action. Please choose again.")
        
def class_pick():
    """Character selection and start up"""
    
    while True:
        rooms = create_rooms()
        creator = Character_Creator()
        character = creator.create_character()
        
        final_choice = input(f"So you are {character.name}? (y/n) ").lower()

        if final_choice in ('y', 'yes'):
            print(f"Welcome {character.name}! \nPlease take the provided {character.weapon}.") 
            print("You have been authorized by the company to explore an anomalous building that has cropped up in a Michigan suburb. "
            "\nThis building appears to have an infinite number of rooms. "
            "\nYou have been tasked with the exploration and documentation of said rooms."
            "\nThere will be no extraction. You are to continue until death. "
            "\nThis is an honor bestowed upon only employees of highest regard."
            )
            explore_room(character, rooms) 
            break
        else: 
            try_again = input("I'm sorry, you don't seem to be in our database. Would you like to try again? (y/n): ").lower()
            if try_again not in ('y', 'yes'):
                print("Server Lockout Initiated.")
                break

if __name__ == "__main__":      
    class_pick()