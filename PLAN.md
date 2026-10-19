# Intro info
the file audio of the original intro is in the /temp folder
the real duration of the audio is 4.3336 seconds

knowing that the game is running at 60fps
every frame last $1/60 = 0,016666667 \approx 0.0167$

so the total number of frame of the initial screen to fit into the audio track lenght is:
$$
4.3336 / 0.0167 = 259,497005988 \approx 260 \space frames
$$

the remaining time is in silence, but sticazzi


# REFACTORING NEEDED
 - [x] Create a sprite library (SpriteLibrary) an interface to store all the sprite sheets into one place and let the other parts of the programs to access that variable without creating multiple instances of the same sheet.
 - [x] Create a element ABC class to inherite all the UI elements.
 - [X] Change the Maze renderer to a instanced object to use self and store the maze surface so isnt recalculated every frame.


# REMEMBER
 - [X] In the menu there are two blank space at the edges, in the left i would like to print the character/nickname menu, and in the right the scores

 - [X] Next to do is to make the movement from a cell to another and lerping the animation between


# pipi
 - [X] Frightened ghost animation added but it wont activate. TODO -> make the super pac gusm post the GhostModeToFrightened and make the ghost edible.
 - [X] Make the Game go to the next level if the time goes to 0 or the gums are finished
 - [X] Make the game cross platform
 - [X] Make when the time runs out to lose a life.
 - [X] Make the multiple sounds channel, because the audio that is longer  
      than it should interrupts other, even when it is not needed, 
      ex: the Super Pacgums or the ed0, i think that ed0 and ed1 should be 
      in two separate channels, so they can follow each other.
 - [X] Mettere un contatore o una scritta "ready" prima che inizi il turno, 
   in modo che il giocatore abbia tempo di rimettersi in sesto
 - [X] Aggiustare il tempo di ripartenza del livello, perché alcuni 
   audio personalizzati di morte impiegano piú secondi dell'animazione
 - [X] BUG: a volte quando passo velocemente sopra un fantasma non muoio. 
   Forse perché sono nella fase scatter, da indagare e cercare di 
   riprodurre il bug
 - [X] BUG: quando seleziono audio random, se poi esco dal menú e rientro 
   il dado non è piú verde, ma in realtà è attivo.


# popo
 - [SOLVED] BUG FOUND: in map size: even width mazes, the pacman spawn in the 42 logo, TODO: hardcode the positions to not spawn.
 - [SOLVED] BUG FOUND: in big maps the pacgums are very big
 - [SOLVED] BUG FOUND: the screen when one dies for the time it says that you won but you loose
 - [SOLVED] BUG FOUND: when the seconds are negative they dont appear good EX: 1:-12 s
 - [SOLVED] BUG FOUND: the state of the vfx in the buttons, doesnt take the actual state of the features.
- [SOLVED] BUG FOUND: pacman animation should stop if not moving


# Sound to add
 - Death sound [lenght: 2.95s].
 - Eat dot 0 and 1.	[lenght each: 0.0825s].
 - Eyes sound.	[lenght: 0.265s].
 - Fright firstloop.	[lenght: 0.115s].
 - Pacman eat Super Pacgum.	[lenght: 1s].
 - Pacman eat Ghost.	[lenght: 0.575s]~
 - Ghost moves.		[lenght: 0.4s]
