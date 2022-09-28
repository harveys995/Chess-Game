import sys
board = [] # Initialise board variable
boardColours = [["⛂","⛀","⛂","⛀","⛂","⛀","⛂","⛀"],["⛀","⛂","⛀","⛂","⛀","⛂","⛀","⛂"]] # Alternating pattern for the board
PIECES = [["♜","♞","♝","♚","♛","♟"],["♖","♘","♗","♔","♕","♙"]] # Player pieces in a list for each colour
PLAYERS = ["White","Black"] # Player names
TEXT = ["a","b","c","d","e","f","g","h"] # Used for the board header and for co-ordinate representation
MAINCOLOURS = ["\033[38;5;4m","\033[38;5;82m","\033[38;5;9m"]  # Colour code for game text
piece_names = ["Rook","Knight","Bishop","King","Queen","Pawn"] # Names for check_valid_moves
xTest = [["♜",0,"♝", "♛","♚",0,"♞",0],[0,"♟","♟","♟","♟","♟",0,0],[0,0,0,0, 0,0,0,0],["♟",0,0,0 ,0,0,"♟","♟"],[0,0,"♜","♙" ,0,"♙",0,"♙"],["♗",0,"♔",0, 0,0,0,0],["♟",0,"♝",0, "♙",0,0,0],["♖",0,0,0,"♕","♗","♘","♖"],]

def vizier_movement(pos,turn,flag1):
    valid_moves = []
    if board[pos[0]][pos[1]] in "♜♖":  # Check if Rook
        base_movement = [[1, 0], [0, -1], [0, 1], [-1, 0]],    [[1, 0], [0, -1], [0, 1], [-1, 0]]
        cycle_num = 7 #Sets number of movement checks for each direction of piece can move
    elif board[pos[0]][pos[1]] in "♟♙": # Check if Pawn
        base_movement = [[-1, -1], [-1, 1]],      [[1, -1], [1, 1]]  #[[-1, -1],[-1, 1]],[[1, -1],[1, 1]]
        cycle_num = 1#Sets number of movement checks for each direction of piece can move
    elif board[pos[0]][pos[1]] in "♝♗": # Check if Bishop
        base_movement = [[-1, -1], [-1, 1], [1, -1], [1, 1]],     [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        cycle_num = 7#Sets number of movement checks for each direction of piece can move
    elif board[pos[0]][pos[1]] in "♚♔" : # Check if King
        base_movement = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]],[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        cycle_num = 1#Sets number of movement checks for each direction of piece can move
    elif board[pos[0]][pos[1]] in "♞♘" : # Check if Knight
        base_movement = [[-1,-2],[-2,-1],[-2,1],[-1,2]] ,[[1,-2],[2,-1],[2,1],[1,2]]
        cycle_num = 1#Sets number of movement checks for each direction of piece can move
    else: # If conditions are true then the piece is a Queen
        base_movement = [[-1, -1], [-1, 1], [1, -1], [1, 1], [1, 0], [0, -1], [0, 1], [-1, 0]],[[-1, -1], [-1, 1], [1, -1], [1, 1], [1, 0], [0, -1], [0, 1], [-1, 0]]
        cycle_num = 7 #Sets number of movement checks for each direction of piece can move
    for move in base_movement[turn]: # Check each direction available to the piece
        x, y ,flag= pos[0],pos[1],False # Resets x, y variables to the piece's position and reset encounter flag to false
        for instance in range(cycle_num):
            try: # Error handling explicitly for out of range issue
                if not flag: # If the piece has not encountered an enemy piece then code executes
                    x+=move[0] ; y+=move[1] # Move x, y to new position in current direction
                    if x >= 0 and y >= 0: # Condition to ensure movement doesn't wrap around the board to other side
                        if board[x][y] in PIECES[turn - 1] : #Checks if an enemy piece is in new location
                            if [TEXT[y].upper() + str(x + 1), [x, y, "YEET"]] not in valid_moves: # Checks if the new location is actually new
                                valid_moves.append([TEXT[y].upper() + str(x + 1), [x, y, "YEET"]]) # Adds the new location to valid_moves
                            if  board[x][y] not in "♚♔" and flag1 is False: # Check to ensure rooks,queens and bishops work
                                flag = True # Flag is True when enemy encountered
                        elif board[x][y] in PIECES[turn] and flag1 is False: # Checks if ally piece is at new location
                            flag = True # Flag is True when enemy encountered
                        elif board[x][y] in PIECES[turn] and flag1 is True:
                            #print([TEXT[y].upper() + str(x + 1)])
                            valid_moves.append([TEXT[y].upper() + str(x + 1)])
                            flag = True  # Flag is True when enemy encountered
                        else:
                            if (board[pos[0]][pos[1]] not in "♟♙" ): # Checks if piece is not a pawn
                                if [TEXT[y].upper() + str(x + 1)] not in valid_moves: # Checks if the new location is actually new
                                    valid_moves.append([TEXT[y].upper() + str(x + 1)]) # Adds the new location to valid_moves
                            elif flag1:
                                if [TEXT[y].upper() + str(x + 1)] not in valid_moves: # Checks if the new location is actually new
                                    valid_moves.append([TEXT[y].upper() + str(x + 1)]) # Adds the new location to valid_moves
            except IndexError: pass #This is to catch out of bounds
    if board[pos[0]][pos[1]] in "♟♙" and flag1 is False: # Checks if pawn
        starting_row = [6, 1] # Sets starting rows for pawn of each colour
        base_movement = [[-1, 0], [1, 0]] # Sets movement type of each colour
        x, y = pos[0] + base_movement[turn][0], pos[1] + base_movement[turn][1] # Sets x,y to new location pos
        if board[x][y] == 0: # If the new location is empty
            valid_moves.append([TEXT[y].upper() + str(x + 1)]) # Add new location to valid_moves
            if pos[0] == starting_row[turn]: # If piece is in it's corresponding starting row
                x, y = x + base_movement[turn][0], y + base_movement[turn][1] # Sets x,y to new location pos
                if board[x][y] == 0: # If the new location is empty
                    valid_moves.append([TEXT[y].upper() + str(x + 1)]) # Add new location to valid_moves
    return valid_moves # Return collected list of valid movements


def create_board():
    [board.append([0]*8) for i in range(8)] # Creates 8 x 8 blank board of 0's
    board[0] = ["♖", "♘", "♗","♕","♔", "♗", "♘", "♖"] ; board[1]= ["♙"] * 8  # Populates top two rows with Black pieces
    board[7]= ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"] ; board[6] = ["♟"] * 8 # Populates bottom two rows with White pieces


def display_board(current=False,highlight=False):
    if highlight: # If true converts input list to numerical values to pass to board
        highlight = [list(convert_location([i[0][1],i[0][0]])) for i in highlight] # Gets possible moves in numerical form
    if current: # If true converts input value into to numerical values to pass to board
        current = list(convert_location([current[1], current[0]]))
    index = 0
    print("  ",end="")
    [print(TEXT[i],end="⛀") for i in range(8)] ;  print() # Prints column names
    for row in range(len(board)): # Loops through each row
        print(index+1, end=" ")
        new_index = 0# Prints the row number
        for tile in board[row]: # Loop through each tile in a row
            colour = MAINCOLOURS[0] # Sets colour to default colour
            if highlight and current: # If highlight contains positions
                if [row,new_index] in highlight: colour = MAINCOLOURS[1] # Change colour to green if current tile is in highlight
                elif [row, new_index] == current: colour = MAINCOLOURS[2] # Changes current piece colour to red if current tile is in current
                else: colour = MAINCOLOURS[0] # Sets colour to default colour
            if not current and highlight:  # If current contains a position
                if [row,new_index] in highlight: colour = MAINCOLOURS[1] # Change colour to green if current tile is in highlight
                else:colour = MAINCOLOURS[0]  # Sets colour to default colour
            if tile == 0: # If tile is empty
                print(colour+boardColours[row%2][new_index]+MAINCOLOURS[0],end=" ") #Alternates the colour on the tiles
            else:
                print(colour+tile+MAINCOLOURS[0], end=" ") #Print the piece in the current tile
            new_index+=1 #Increment to alternate tile colour
        print()
        index+=1


def check_valid_moves(turn,validPieces,flag):
    for row in range(8):  #Iterates through each row
        for tile in range(8): #Iterates through each tile(column) in a row
            if board[row][tile] in PIECES[turn]: #If the current tile has a piece of the current player's colour
                if len(vizier_movement([row,tile],turn,flag)) >0: #If the length of valid moves is over 0
                    validPieces[str(TEXT[tile].upper()) + str(row + 1)] = \
                    {"name": piece_names[PIECES[turn].index(board[row][tile])],
                    "validMoves":vizier_movement([row,tile],turn,flag)}  # Returns valid moves for each piece of the current player's colour


def display_valid_moves(validPieces,turn):
    print()
    for key,value in validPieces.items():
        print(f"{PIECES[-turn][piece_names.index(value['name'])]}  {value['name']}({key}){(' '*(6-len(value['name'])))} can move to: ",end="") # Prints output for each piece move
        for move in value["validMoves"]:
            if len(move) <2:
                print(move[0], end=" ") # Filters out a kill check
            else:
                print(move[0]+">"+board[move[1][0]][move[1][1]], end=" ") # Prints the piece getting killed
        print()
    return


def convert_location(input):
    return int(input[0])-1,TEXT.index(input[1].lower()) # Switches the input representation data into numerical data to access the board


def main():
    global board
    print(MAINCOLOURS[0], end="  ")
    create_board() # Populate board variable with it's default board state TEST PIECE #board[5][3] = "♞" board[4][5] = "♔" board[5][6] = "♟"board[4][3] = "♚"
    turn = 0# Initiate starting player's turn as White
    valid_pieces = {} #Initialise variable to store possible moves
    board = xTest
    while True: # Game Loop
        turn = [0, 1][turn - 1]  # Switch turn to other player
        check_valid_moves([0,1][turn-1], valid_pieces,True) #can take king CHECK
        check_mate_location = [] # List to store all opponents moves
        check,checkmate = False, True # Sets Check, Checkmate to default values
        for i in valid_pieces.values(): ## Get opponent pieces moves
            for move in i["validMoves"]: # Checks each pieces available moves
                if len(move) > 1: #If piece can kill another piece
                    if board[move[1][0]][move[1][1]] == ["♚","♔"][[0,1][turn]]: #If that piece is a king
                        check = True # Makes check True
                else: # Saves location of future check mate
                    check_mate_location.append(move[0]) #print(check_mate_location)
        check_mate_location = list(dict.fromkeys(check_mate_location))
        valid_pieces.clear() # Resets so current player doesn't use other player's pieces
        check_valid_moves(turn,valid_pieces,False) # Checks for valid moves and sets them to valid_pieces
        for i in valid_pieces.values(): # Get current players pieces moves
            if i["name"] == "King": #If piece name is King
                new_moves = [] # Create brand new list for king to avoid checkmate
                for move in i["validMoves"]: # Loops through king's moves
                    if move[0] not in check_mate_location: # If isn't in checkmate
                        new_moves.append([move[0]]) # Move is valid and added to the list
                i["validMoves"] = new_moves # Sets the King's movement to the new list
        if check: # Checks if the King is in check
            temp = {} #Empty dict
            for key,piece in valid_pieces.items(): # Loops through the player's pieces moves
                if piece['name'] == "King": #If King is present
                    #print(piece)
                    if piece["validMoves"]:
                        checkmate = False # Set checkmate to False as King can escape
                        temp = {key:piece}
            if checkmate: #Check if checkmate is True
                print(f"\n{PLAYERS[[0, 1][turn-1]]} has won by checkmate!")  # Check
                sys.exit() #Exits program
            else: # SETS ONLY VALID MOVE TO KING IF IT MOVES
                print(f"\n{PLAYERS[turn]} piece turn:\n")
                print(f"Your King is in check!\n")
                valid_pieces = temp
        else:
            print(f"\n{PLAYERS[turn]} piece turn:\n")
        while True: #Choose piece loop
            try: #Error handling for foreseen KeyError exception
                display_board(False,[[i] for i in valid_pieces.keys()])  # Display current board state with movable pieces highlighted green
                display_valid_moves(valid_pieces, turn)  # Display all possible moves for current player
                temp = input("\nPlease choose a valid piece to move: ").upper()
                move = valid_pieces[temp] # Sets move to selected pieces available moves
                break # Exits loop as purpose is completed
            except KeyError: #Ensures no incorrect inputs are given.
                print(f"\nPiece {str(temp)} is invalid.\n") #Tell user the input is invalid.
        while True: # Loop to select new location for selected piece
            selected_move = "" # Check for if a move has been selected
            print(F"\n{PIECES[-turn][piece_names.index(move['name'])]} {move['name']}({temp})'s possible movements: \n")
            selection = "" # For displaying possible moves
            for chosen_move in move["validMoves"]: # Loops through each possible movement for current piece
                if len(chosen_move) >= 2:
                    selection+= chosen_move[0]+">"+board[chosen_move[1][0]][chosen_move[1][1]]+" " # Text to show possible movements taking a piece
                else:
                    selection+= chosen_move[0]+" "# Text to show possible movements
            print("")
            display_board(temp,move["validMoves"]) # Displays board but with movements highlighted green and current piece highlighted red
            chosen_location = input(f"\nSelect from the follow locations for {temp} to move to ({selection}) : ").upper()  #Input to get new location
            for choice in move["validMoves"]: # Loops through the possible moves
                if choice[0] == chosen_location: #If selected move is found in possible moves
                    selected_move = choice # Change variable to use later
            if selected_move != "":
                break # Break to exit loop and proceed with movement
            else:
                print("Please enter a valid location.") # Check failed so loop resets
        if len(selected_move) > 1: # Checks if chosen move defeats an enemy piece
            board[selected_move[1][0]][selected_move[1][1]] = 0 # Changes previous location to 0
        else:
            x = convert_location([selected_move[0][1],selected_move[0][0]]) # Changes previous location to 0
            board[x[0]][x[1]] = 0
        current,target  = convert_location([temp[1], temp[0]]) ,convert_location([selected_move[0][1], selected_move[0][0]]) # Converts representated data to board data to enable movement
        board[current[0]][current[1]], board[target[0]][target[1]] = board[target[0]][target[1]], board[current[0]][current[1]] # Moves piece to new location
        valid_pieces.clear() # Reset all moves stored from previous player


if __name__ == '__main__':
    main()