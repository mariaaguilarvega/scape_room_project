import datetime
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import readchar

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
    "challenge": {
        "question": "Which country did AC/DC originate in?",
        "options": ["USA", "Australia", "United Kingdom"],
        "correct_answer": "Australia",
    }
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
    "challenge": {
        "question": "What year was the very first model of the iPhone released?",
        "options": ["2007", "2006", "2005"],
        "correct_answer": "2007",
    }
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
    "challenge": {
        "question": "In which location does the new season 3 of 'The White Lotus' take place?",
        "options": ["Sicily", "Thailand", "The Maldives"],
        "correct_answer": "Thailand",
    }
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
    "challenge": {
        "question": "Which country has the longest coastline in the world?",
        "options": ["Australia", "Russia", "Canada"],
        "correct_answer": "Canada",
    }
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

def get_current_user_index():
    for index, user in enumerate(game_state["users"]):
        if user["name"] == game_state["current_user"]:
            return index
    return -1


def new_user():
    """define user dictionary to get name, init time and finish time"""
    clean_terminal()
    name = input("\n\nPlease enter your name to start the game: ").strip().lower()

    # check if user name exists
    for user in game_state["users"]:
        if user["name"] == name:
            display_message(f"User {name} already exits. Please, enter a new name.")
            return 0

    # cheatcode :)
    if name.startswith("cheater"):
        object_relations["door a"] = [game_room, outside]

    # create user
    user_data = {
            "name": name,
            "init_time": datetime.datetime.now(),
            "finish_time": ""
        }
    game_state["current_user"] = name
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

    display_user_menu(["Let's go!"], "\nYou wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

    
            

def display_user_menu(options, intro = ""):
    """Display some options for the user to choose, and return the choice"""
    selected = 0

    while True:
        clean_terminal()

        # display intro message
        print("\n\n")
        print(intro)
        print("\n")

        # display all available options
        for i, option in enumerate(options):
            prefix = "→ " if i == selected else "  "
            print(f"{prefix}{option}")
        
        # get user's choice
        key = readchar.readkey()
        if key == readchar.key.UP and selected > 0:
            selected -= 1
        elif key == readchar.key.DOWN and selected < len(options) - 1:
            selected += 1
        elif key == readchar.key.ENTER:
            break
    
    clean_terminal()
    return options[selected]


def display_message(msg = ""):
    """Display a message, and wait for user confirmation"""
    display_user_menu(["Ok!"], msg)


def play_trivia(challenge_data):
    """Display a trivia question and keep asking till user chooses the right option"""
    
    question = challenge_data["question"]
    options = challenge_data["options"]
    correct_answer = challenge_data["correct_answer"]
    
    msg = "\nTRIVIA CHALLENGE! \n\n\n" +  question

    while True:
        answer = display_user_menu(options, msg)
        if answer == correct_answer:
            return True
        else:
            msg = "❌ Wrong answer! Try again." + "\n\n\n" + question


def finish_game():
    user_index = get_current_user_index()
    game_state["users"][user_index]["finish_time"] = datetime.datetime.now()
    game_timing = game_state["users"][user_index]["finish_time"] - game_state["users"][user_index]["init_time"]
    
    message = f"Congrats {game_state['current_user']}! You escaped the room in {game_timing}!\n\n"
    message += "Would you like to re-start the game for a new user?"

    new_game_answer = display_user_menu(["Yes", "No"], message)

    if new_game_answer == 'Yes':
        game_state["current_room"] = game_room
        game_state["keys_collected"] = []
        object_relations["piano"] = [key_a]
        object_relations["queen bed"] = [key_b]
        object_relations["double bed"] = [key_c]
        object_relations["dresser"] = [key_d]
        start_game()
    else:
        display_message("Okay, see you soon. Results will be stored in the same directory.")
        save_results("scape_rooms_results.csv")
        create_bar_chart_from_csv("scape_rooms_results.csv", "scape_rooms_results.png")



def save_results(destination_csv_file):
    """Save results in a CSV file"""
    # Define the header for the CSV file
    header = ['player_name', 'start_time', 'finish_time', 'duration']

    # Open the CSV file in write mode
    with open(destination_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(header)
        
        # Write the data for each user
        for user in game_state['users']:
            duration = user['finish_time'] - user['init_time']
            writer.writerow([user['name'], user['init_time'], user['finish_time'], duration])



def create_bar_chart_from_csv(csv_file, png_file):
    """Create a bar chart from a source csv file"""
    # Read the CSV data
    names = []
    durations = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row['player_name'])
            # Convert the 'duration' string to a timedelta object
            duration_str = row['duration']
            hours, minutes, seconds = map(float, duration_str.split(':'))
            # Convert the duration into total seconds
            duration_in_seconds = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
            durations.append(duration_in_seconds)

    # Calculate the mean duration
    mean_duration = np.mean(durations)

    # Create the bar chart
    plt.bar(names, durations, color='skyblue')

    # Add a line for the mean
    plt.axhline(y=mean_duration, color='r', linestyle='--', label=f'Mean: {mean_duration:.2f} sec')

    # Add titles and labels
    plt.title('Escape Room Duration per Player')
    plt.xlabel('Player Name')
    plt.ylabel('Duration (seconds)')

    # Rotate player names for better readability
    plt.xticks(rotation=45, ha='right')

    # Show the mean label in the legend
    plt.legend()

    # Save the chart as a PNG file
    plt.tight_layout()
    plt.savefig(png_file)  # Save to the provided path

    # Show the chart
    plt.show()



def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        finish_game()
    else:
        msg = (f"You are now in {room["name"]}. What would you like to do?")
        intended_action = display_user_menu(["Explore", "Examine"], msg)

        if intended_action == "Explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "Examine":
            examine_item(input("\n\nWhat would you like to examine? ").strip())
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
    display_message(explore_message)


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
                have_key = False   #player doesn't have key
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

                    if item_found["challenge"]:
                        play_trivia(item_found["challenge"]) #play challenge to collect key
                        output = "Correct! "

                    game_state["keys_collected"].append(item_found)  #add key to the inventory
                    output += f"You found {item_found["name"]}!"

                   
                else:
                    output += "There isn't anything interesting about it."
            display_message(output)
            break
            
    if(output is None):  #an error message in case the item was not found in the room
        display_message("The item you requested is not found in the current room.")
    
    if next_room:
        answer = display_user_menu(["Yes", "No"], "Do you want to go to the next room?")
        if answer == "Yes":
            play_room(next_room) #if a door was unlocked and the player wants to proceed, move to the next room
        else:
            play_room(current_room) #stay in the current room, if player doesn't want to move

    else:
        play_room(current_room) #stay in the current room



game_state = INIT_GAME_STATE.copy()
start_game()


