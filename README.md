# Snake_Game
Snake game is a refreshing take on the beloved arcade classic. More than just eating dots, this version introduces a dynamic, strategic challenge where every bite counts.

# Features
* **Custom Aesthetics:** A calming, pastel colour palette (Pastel Pink and Light Gray) rather than the traditional dark screen.
* **Dynamic Food System:** A hunt for various food types, each offering different point values making the game more challenging.
* **Persistent High Score:** Your personal best is saved locally to challenge you with every new game.
* **Quality of life:** Quick and reliable **Pause/Resume** functionality
* **Intuitive Control:** Directional controls for smooth gameplay.

## Gameplay Screenshot
<img width="1208" height="864" alt="Screenshot 2025-12-10 220146" src="https://github.com/user-attachments/assets/c5de6252-db02-440c-a40c-c7ad1f1da0fb" />

## How to play
### Controls
| Action | Key(s) |
| :--- | :--- |
| **Move Up** | UP Arrow |
| **Move Down** | DOWN Arrow |
| **Move Left** | LEFT Arrow |
| **Move Right** | RIGHT Arrow |
| **Pause/Resume** | P key, ENTER key, or SPACE key |
| **Restart Game (on Game Over)** | R key |
| **Quit Game** | Q key |

### Game Objective
The goal is to guide the snake to eat the food blocks wihtout colliding with the boundaries of the play area or with its own tail. Your score is determined by the type of food you consume.

## Installation and Setup
To run this game locally, you need Python and the Pygame library installed.
### 1. Clore the Repository
```bash
https://github.com/mariadobrescu175-jpg/snake_game.git
```
### 2. Install Dependencies
This game requires the **pygame** library. You can install it using pip: 
```bash
pip install pygame
```
### Run the game
Execute the main Pyhton file to start the game:
```bash
python main.py
```
*(Note:Replace **main.py** if you named your file differently)*
## Project Structure
The code is organised into three main files:
* main.py: Contains the main game loop, event handling, drawing functions, and game state management
* snake.py: Defines the Snake class, managing its body position, movement, and direction changes
* food.py: Defines the Food class, managing food position, type, point values, and the FOOD_TYPES dictionary.
