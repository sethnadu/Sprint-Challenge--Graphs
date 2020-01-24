from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# ===================== Solution Code ==========================

'''
 One function that checks if current room is in visited. If that room has unvisited exits, it
randomly picks one of the unvisted exits(direction) and moves that way. It then adds the next room to
visited if it was not in visited, then adds corresponding (reverse random direction with reverse_direction 
function) room ids to the current and next rooms. If there are no unvisited exits, it runs the custom bfs
function. This goes through each room till it finds an unvisited exit, recorded all the ids of the rooms it
moves through. Each id is then connected with the direction of the id before it, in order to get the direction
it took to move to each room. Each one of the directions are then sent to the player.travel() to move the player.
Then all the directions moved are returned, which are added to the traversal_path.
'''

# Main dictionary containing all rooms, with exits labeled with ? or connecting room id

visited = {}

###############
# Main Function
###############

def travese_map(): 
    # Focus on current player room:
    while len(visited) < len(room_graph):
        # Get player's current room's exits
        current_exits = player.current_room.get_exits()
        # Get player's current room id
        current_room_id = player.current_room.id
        # Get players current room object
        current_room = player.current_room
        # List of exits that have not been visited in a room
        unvisited_directions = []

        # Check if current room id is NOT in visited
        if current_room_id not in visited:
            # Add current room to visited dict with all exits set with "?" 
            # ex {0: "n": "?" "s": "?" "e": "?" "w": "?"}
            room_exits = {}
            for i in current_exits:
                room_exits[i] = "?"
            visited[current_room_id]= room_exits
            
        # Add all unvisited exits to unvisited_directions array
        for i in visited[current_room_id]:
            if visited[current_room_id][i] == '?':
                unvisited_directions.append(i)

        # Check if any unvisited rooms exist from current room
        if len(unvisited_directions) > 0:
            # Choose random direction within unvisited rooms to travel
            random_index = random.randint(0, len(unvisited_directions) - 1)
            random_direction = unvisited_directions[random_index]

            # Have player travel to the random_direction
            # Add random direction to traversal path
            player.travel(random_direction)
            traversal_path.append(random_direction)

            # Save the new room's current id and exits
            next_traveled_id = player.current_room.id
            next_traveled_exits = player.current_room.get_exits()

            # check if new room id is in visited dict
            if next_traveled_id not in visited:
                # Add new room to visited dict with all exits set with "?" 
                # ex {0: "n": "?" "s": "?" "e": "?" "w": "?"} 
                next_room_exits = {}
                for i in next_traveled_exits:
                    next_room_exits[i] = "?"
                visited[next_traveled_id] = next_room_exits

            # Create a reverse of the current rooms random direction
            # Reverse function used, found below
            # Add random direction and reverse to both the current_room_id
            # and new_room_id's visited key and direction value
            reverse = reverse_direction(random_direction)
            visited[current_room_id][random_direction] = next_traveled_id
            visited[next_traveled_id][reverse] = current_room_id

        # If there are no unvisited exits in current room   
        else:

            # Run custom bfs function to find another room with at least
            # One unvisited exit
            # It returns all the directions transversed to get to the next room
            directions_moved = custom_bfs(visited, current_room)

            # Loop through the directions_moved and add each direction to traversal path
            if len(directions_moved) > 0:
                for i in directions_moved:
                    traversal_path.append(i)

    # print("END", visited)
    # print("END PATH", traversal_path)     
       

####################################
# Reverse random direction function
####################################

# Reverse the direction that is passed in, return the reversed direction
def reverse_direction(direction):
    if direction == "n":
        return 's'
    elif direction == "s":
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'


####################################
# Custom BFS to find room with "?"
####################################

# Custom BFS function used to find a room with unvisited exits("?")
def custom_bfs(visited, current_room):
    # Create a set to hold all the directions searched through
    # Set first in queue as the current_room's id
    visited_path = set()
    queue = Queue()
    queue.enqueue([current_room.id])

    # Holds all the moved directions, will return this
    moved_directions = []
    # Copy of path when unvisited room found
    recorded_path = ''

    while queue.size() > 0:

        path = queue.dequeue()
        v = path[-1]

        # Find if any unvisited arrays
        unvisited_array = []
        for i in visited[v]:
            if visited[v][i] == '?':
                unvisited_array.append(i)

        # If any unvisited exits found, break while loop
        # Save the current path to recorded_path
        if len(unvisited_array) > 0:
            recorded_path = path
            break 

        # If no unvisied exits found, continue searching through each current room
        # add the searched room to visited_path
        # Path will constantly update with all the connected_rooms, then using each 
        # of the connect_room id's will be added to the path.
        if v not in visited_path:
            visited_path.add(v)
            for i in visited[v]:
                # Should have room id's
                direction = visited[v][i]
                new_path = list(path)
                new_path.append(direction)
                queue.enqueue(new_path)

    # Since the recorded path has only ids, backtrack and find which direction key has 
    # Each room's id, add that direction to the moved_directions array
    while len(recorded_path) >= 2:
        # Remove first index [0] (id) from recorded path
        room = recorded_path.pop(0)
        for i in visited[room]:
            if visited[room][i] == recorded_path[0]:
                moved_directions.append(i)

      # Take the moved_directions array and loop through it, adding each direction to player.travel() to move the player
    for i in moved_directions:
        player.travel(i)
        
    return moved_directions


travese_map()
# ===================== End Solution Code ==========================



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)
    
if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


#================= OLD CODE USED WHILE WORKING =====================
 # queue = Queue()
    # queue.enqueue([player.current_room])
    # visited = {}
    # current_id = player.current_room.id
    # current_exits = player.current_room.get_exits()
    # random_direction = random.randint(0, len(current_exits) - 1)
    # question = "?"
    # new_room = ''

    # while queue.size() > 0:
    #     path = queue.dequeue()
    #     v = path[-1]
    #     count = 0
    #     print("v", v)
    #     current_exits = v.get_exits()
    #     if v not in visited:
    #         print(v)
    #         for i in range(len(current_exits)):
    #             print(current_exits)
    #             visited[v] = {current_exits[i]:question}
    #             print(visited[v])
    #     elif v in visited:
    #         random_direction = random.randint(0, len(current_exits) - 1)
    #         if current_exits[random_direction] == "?":
    #             visited[v][current_exits[random_direction]] = new_room
    #         while current_exits[random_direction] is not '?' and count == len(current_exits) - 1:
    #             count += 1
    #             random_direction = random.randint(0, len(current_exits) - 1)
    #             print("count", count)
        
                

    #     # Switches room
    #     random_direction = random.randint(0, len(current_exits) - 1)
    #     player.travel(current_exits[random_direction], True)
    #     new_room_id = player.current_room.id
    #     new_room = player.current_room
    #     visited[v][current_exits[random_direction]] = new_room
    #     traversal_path.append(current_exits[random_direction])
    #     new_path = list(path)
    #     new_path.append(new_room)
    #     queue.enqueue(new_path)


        # print(visited[current_id])

#     player.travel(current_exits[random_direction], True)
#     new_room = player.current_room.id
    
    # visited[current_id][current_exits[random_direction]] = new_room
    # print(visited_rooms[current_id])


    
