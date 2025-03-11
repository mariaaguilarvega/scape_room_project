import datetime
import os

# define rooms, doors, items and keys

couch = {
    "name": "couch",
    "type": "furniture",
}

piano = {
    "name": "piano",
    "type": "furniture",
}

queenbed = {
    "name": "queen bed",
    "type": "furniture",
}

doublebed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

diningtable = {
    "name": "dining table",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}


key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

game_room = {
    "name": "game room",
    "type": "room",
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

living_room = {
    "name": "living room",
    "type": "room",
}

outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "bedroom 1" :[door_a, door_b, door_c, queenbed],
    "bedroom 2" :[door_b, doublebed, dresser],
    "living room" :[door_c, door_d, diningtable],
    "outside": [door_d],
    "piano": [key_a],
    "queen bed": [key_b],
    "double bed": [key_c],
    "dresser": [key_d],
    "dining table": [],
    "door a": [game_room, bedroom_1], 
    "door b":[bedroom_1,bedroom_2], 
    "door c": [bedroom_1, living_room],
    "door d":[outside, living_room]
}



# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside,
    "users": [],
    "current_user" : ""
}


def new_user():
    #define user dictionary to get name, init time and finish time
    
    name = input("Please enter your name to start the game: ").strip().lower()
    if len(game_state["users"])<1:
        user_data = {
                "name": name,
                "init_time": datetime.datetime.now(), #.strftime("%Y-%m-%d %H:%M%S"),
                "finish_time": ""
            }
        game_state["current_user"] = name
        print(f"New user {name} has been created. You can start the game.")
        game_state["users"].append(user_data)
        return 1
    
    else:    
        for user in game_state["users"]:
            if user["name"] == name:
                print(f"User {name} already exits. Please, enter a new name.")
                return 0
            else:   
                user_data = {
                    "name": name,
                    "init_time": datetime.datetime.now(), #.strftime("%Y-%m-%d %H:%M%S"),
                    "finish_time": ""
                }
                game_state["current_user"] = name
                print(f"New user {name} has been created. You can start the game.")
                game_state["users"].append(user_data)
                return 1


def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def clean_terminal():
    if os.name == 'nt': #Windows
        os.system('cls')
    else:
        os.system('clear')

def start_game():
    """
    Start the game
    """
    while True:
        if new_user() ==1:
            break

    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

#Calculates the finish time, print final message to the user and ask if a new user want to start the game.
def stop_game():
    game_state["users"][0]["finish_time"] = datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M%S")
    game_timing = game_state["users"][0]["finish_time"] - game_state["users"][0]["init_time"]
    clean_terminal()
    print(f"Congrats {game_state['current_user']}! You escaped the room in {game_timing}!")
    valid_response = False
    while not valid_response:
        new_game_answer = input('Would you like to re-start the game for a new user? Type yes or no: ').strip().lower()
        if new_game_answer in ['yes', 'no']:
            valid_response = True
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

    if new_game_answer == 'yes':
        game_state["current_room"] = game_room
        game_state["keys_collected"] = []
        object_relations["piano"] = [key_a]
        object_relations["queen bed"] = [key_b]
        object_relations["double bed"] = [key_c]
        object_relations["dresser"] = [key_d]
        start_game()
    else:
        print("Okay, see you soon. Results found in same directory.")
        for user in game_state['users']:
            results = (f"Name: {user['name']}\n"
                        f"Start Time: {user['init_time']}\n"
                        f"Finish Time: {user['finish_time']}\n"
                        f"Duration: {user['finish_time'] - user['init_time']}\n")
            
            with open(f"scape_rooms_results_{user['name']}.txt", 'w') as file:
                # Escribe los resultados en el archivo
                file.write(results + '\n')


def trivia_question_key_a():
    """Trivia question for Key A."""
    print("\n🎸 TRIVIA CHALLENGE! 🎸")
    print("Which country did AC/DC originate in?")
    print("A. USA")
    print("B. Australia")
    print("C. United Kingdom")

    while True:
        answer = input("Enter A, B, or C: ").strip().upper()
        if answer == "B":
            print("✅ Correct! You found the key for Door A.")
            return True
        else:
            print("❌ Wrong answer! Try again.")        
        
def trivia_question_key_b():
    """Trivia question for Key B."""
    print("\n📱 TRIVIA CHALLENGE! 📱")
    print("What year was the very first model of the iPhone released?")
    print("A. 2007")
    print("B. 2006")
    print("C. 2005")

    while True:
        answer = input("Enter A, B, or C: ").strip().upper()
        if answer == "A":
            print("✅ Correct! You found the key for Door B.")
            return True
        else:
            print("❌ Wrong answer! Try again.")

def trivia_question_key_c():
    """Trivia question for Key C."""
    print("\n📺 TRIVIA CHALLENGE! 📺")
    print("In which location does the new season 3 of 'The White Lotus' take place?")
    print("A. Sicily")
    print("B. Thailand")
    print("C. The Maldives")

    while True:
        answer = input("Enter A, B, or C: ").strip().upper()
        if answer == "B":
            print("✅ Correct! You found the key for Door C.")
            return True
        else:
            print("❌ Wrong answer! Try again.")

def trivia_question_key_d():
    """Trivia question for Key D."""
    print("\n🌍 TRIVIA CHALLENGE! 🌍")
    print("Which country has the longest coastline in the world?")
    print("A. Australia")
    print("B. Russia")
    print("C. Canada")

    while True:
        answer = input("Enter A, B, or C: ").strip().upper()
        if answer == "C":
            print("✅ Correct! You found the key for Door D.")
            return True
        else:
            print("❌ Wrong answer! Try again.")
            

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        stop_game()
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    explore_message = "You explore the room. This is " + room["name"] + ". You find "
    for item in object_relations[room["name"]]:
      explore_message += str(item["name"]) + ", "
    explore_message = explore_message[:-2]+"."
    print(explore_message)


def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the second room.
    """
    connected_rooms = object_relations[door["name"]]

    if connected_rooms[0]["name"] == current_room["name"]:
        return connected_rooms[1]
    else:
        return connected_rooms[0]


def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"] #get the current room the player is in
    next_room = ""   #variable to store the next room
    output = None

    for item in object_relations[current_room["name"]]: #loop all objects in the current room
        if(item["name"] == item_name):     #check if the object examined is in the room
            output = "You examine " + item_name + ". "   
            if(item["type"] == "door"):    #if the object is a door
                have_key = False   #player doesn´t have key
                for key in game_state["keys_collected"]:  #check if the player has the correct key in inventory
                    if(key["target"] == item):
                        have_key = True
                if(have_key):   #if the player has key, unlock the door
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room) #move to next room
                else:
                    output += "It is locked but you don't have the key."
            else:  #if the item is furniture, check if contains a key
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):  #if item exists in object relations, checks if object has anything inside
                    item_found = object_relations[item["name"]].pop()  #take-pop the key

                    if item_found == key_a and trivia_question_key_a(): #if found item is key A and player answer trivia correctly
                        game_state["keys_collected"].append(item_found)  #add key A to the inventory
                        output += "You find " + item_found["name"] + "."
                    elif item_found == key_b and trivia_question_key_b():  #if found item is key B and player answer trivia correctly
                        game_state["keys_collected"].append(item_found)    #add key B to the inventory
                        output += "You find " + item_found["name"] + "."
                    elif item_found == key_c and trivia_question_key_c():  # If Key C is found and trivia is correct
                        game_state["keys_collected"].append(item_found)  # Add Key C to inventory
                        output += "You find " + item_found["name"] + "."
                    elif item_found == key_d and trivia_question_key_d():  # If Key D is found and trivia is correct
                        game_state["keys_collected"].append(item_found)  # Add Key D to inventory
                        output += "You find " + item_found["name"] + "."
                   
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break
            
    if(output is None):  #an error message in case the item was not found in the room
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'): #if a door was unlocked and the player wants to proceed, move to the next room
        play_room(next_room)
    else:
        play_room(current_room) #stay in the current room, if player doesn´t want to move



game_state = INIT_GAME_STATE.copy()
start_game()


