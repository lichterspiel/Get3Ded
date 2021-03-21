# Tic Tac TOnline
#### URL: https://www.youtube.com/watch?v=m2AIlS5hsBs
#### Description:
This is an tic tac toe implementation to play on a website against a friend.It works with flask and socketio. 
Flask is used to make the webserver work and socketio for the client server communication when playing tic tac toe. 

## How it works.
The player can register himself on the website to get acces to the play mode. He then can create a new room or if already existing join a new room.
THe Board is then loaded up and the players can select a field every turn. The communication is with socketio which triggers an event everytime someone makes a move.
The Server checks the validity and when its valid if someone has won.
Then the game ends.


# In detail
App.py contains all the code for the website. The routes and Socketio code.

There is a login,logout,play,create_room funtion. Login and logout are self explanatory. 

Create_room is as the name says creating a room. It adds the room to the db and who is joining. 

The database cointains the room name,player_ 1 and player_2 the user_count to check if it is already full which is reluctant if you check if player_1 and 2 are not Null.

But it is still simpler to update the user_count and delete the room if someone leaves the game and never rejoins. 

The board is and 2D array wich is filled with 0s. The array is stored in an Dict. The key is the room name and value is the board array.


The helper.py has mostly functions that execute sql so that it is clearer to read the code in app.py and not be full with sql querys. It also has a wrapper for
ttt_logic.py has all the tic tac toe logic to check if someone has won. 
I implemented the checks server side to prevent any cheating.

In the static folder are the css and js files. For js i have the play.js which communicates with the web server when playing a game. 
The TIc tac toe board is a standart html table stylized with plain css to look like a tic tac toe board.
The table cell have an onclick function. When it is clicked an event is fired and the server checks if that move is valid. If so then it sends it to all the clients and updates the dom.
If not it simply return that it is invalid. 
The server checks the validity if either the coordinate in the board array is 0 and if not then the move was already taken => Invalid.
A valid move is stored in the array as the players icon for example "X".
Every time a move is valid the server checks if there is already a winning condition.
IF so then display the overlay and both can return to the home menu to start a new game.

# Launch

Just install all the packages from the requirements.txt and start the app.py
