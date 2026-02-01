# Roll-A-Ball Video Game
A game where the user rolls a ball on top of a flat surface, picking up cubes for points.

## Overview
Players start a new game or quit the game from the Main Menu.
When New Game is selected, the Main Menu disappears and the HUD appears.
Players use the mouse or keyboard to "roll" a ball around a playing field.
There are walls to prevent the player from falling off the playfield.
The player spawns in the center of the playing field.
In a new game, there are 12 equidistant cubes spread around the player starting point in a circle.
The player rolls the ball into the cubes.
Each cube is worth 1 point.
The game ends when the player has picked up all 12 cubes or they press ESC.


## Requirements
- Main Menu
	- Game Title
	- New Game Button
	- Quit Game Button
- HUD
	- Score in top, center of screen

## Acceptance Criteria
- The Main Menu contains:
	- Game Title
	- New Game Button
	- Quit Game Button
- Pressing the New Game Button starts a new game.
- Pressing the Quit Game Button exits the game.
- In game:
	- The ball is rolled by user via the mouse or keyboard (WASD).
	- There are 12 cubes at the start of a new game.
	- Cubes disappear when collected (touched by the ball).
	- Player earns 1 point per cube.
	- Player score is updated with each cube picked up.