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


# BUG FOUND
There is a bug starting the program from the terminal, that is different that starting it from the vs code terminal, the size of the character is also different.
I dont know what could be but is significantly slower in the terminal cause of the pulling a lot of more character every time the time of calculation is higher

## BUG FIXED
I fixed it forcing the window resolution to be 1920x1080 and then asking to pygame to scale it in case of other resolution using pygame.SCALED