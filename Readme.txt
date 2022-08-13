Readme:

Name: 112 Tower Defense
-------------------
I’m making my own take on the game, Bloons Tower Defense. I’m calling it 112 Tower Defense (so original!). Essentially, the way the game will work is that balloons will move down a path that is randomly generated based on a given number of vertices. As balloons move down the path, turrets that you can purchase using cash are placed off the track, and these turrets (each with their own unique parameters) will attack the balloons and pop them before they reach the end of the track. If they reach the house at the end, you lose health points. Health points reach zero, game over. Otherwise, the game will continue. The game will continue arcade style until the player either gives up or loses: but as the game progresses, the balloons get more and more tough, move faster, and present more of a challenge.

How to run?
-------------------
Simply open the file 'tp3.py' with a python code editor (VSCode). 
In terms of libraries that aren't standard with the latest version of Python 3, be sure to be using the latest version of cmu_112_graphics/Tkinter.

Shortcuts
-------------------
To add more vertices to the randomly generated path, modify the value app.verteces within the function makeVerteces(app).
To skip though levels, give extra cash or lives, scroll down slightly to the Player object class definition. There, you can modify how much cash and lives you start with, with the variables 'cash', 'health', and 'self.level'.