Testing how to teach a computer to play the hash game by using reinforcement
learning. 

# Base classes

This repo also contains some useful classes for general reinforcement learning problems, such as the BaseGameState and BaseGame classes defined at the base_game_env.py file, which contain the structure of a learning environment. Another useful class is the BaseTablePlayer (defined at base_player.py), which defines a standard reinforcement learning actor that uses
Q tables.

# Usage

In order to use this code, first train the model using 
train_hash_player.py, then modify the play_hash.py file to load 
the latest player and play. 

The train_hash_player.py code will save the player versions at a folder named "players" by default. To change it, modify the FOLDER_TO_SAVE var:

Example: 

```
FOLDER_TO_SAVE = 'players'
```

To load a player, modify the player var at the play_hash.py scrip.

Example: 

```
player = pickle.load(open(os.path.join('players', 'player_20000.pickle'), 'rb'))
```

When playing the hash game, you will need to type the numeric index
of the house you want to play. The hash game house numeration is as follows:
<br>

0 1 2<br>
3 4 5<br>
6 7 8
