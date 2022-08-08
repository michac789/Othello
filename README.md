# Othello

## Overview

This is a fully functional Othello game with complete user interface. The game features are as follows:

- Full user interface using mouse clicks, including hover effects, popovers, multiple fonts, various icons, and resizable (and adaptable) game menus and board depending on your window size
- Complete bgm and sfx to make everything fun, toogleable from everywhere on the game (you are able to turn it on or off using the UI)
- Classic Mode where you can choose between 'Human VS Human', 'Human VS AI' or 'AI vs AI' in a regular 8x8 board, along with various customization
- Undo feature that can be turned on or off from the menu and can be used in-game (if it's turned on)
- Time constraint feature customizable from the menu
- AI of 6 difficulty levels created using negamax with alpha-beta pruning and heuristic function trained by supervised learning (training data is created by automating bot to play another bot from million times and exporting all the positional data)
- Custom Mode where you can customize board's height & width, and you can set your own starting position as well (you can be crazy and have something like 20x18 board with your own starting position, and play for fun with each other)

## How To Launch

The game executable is not created yet, so if you want to try it, you have to clone the repository, or download all the files required for the game. The files involved for the game itself is only runner.py, helper.py, othello.py and othello_ai.py. The other files are only used during the AI learning process and evaluation of the various AI heuristic functions. Be sure though, to have all these 4 files and the assets folder (containing all bgm, sfx, fonts, icons, images) in the same directory. In order to launch the game, make sure to have python and pygame installed.

Please follow these steps to download and play the game, it assumes you have python version 3+ installed. First, open your command prompt / terminal, then change directory to a folder where you want all of these to be downloaded. Then, execute these comments:

```powershell
    # clone entire repository, or you may also choose to download only the files needed
    git clone https://github.com/michac789/Othello.git

    # change your directory to the newly cloned folder
    cd OTHELLO

    # do this if you haven't had pygame installed
    pip install requirements.txt

    # execute runner.py to run the game
    python runner.py
```

Warning!!! Please execute runner.py, and NOT othello.py itself. In othello.py, it only contains the basic othello logic and on-terminal gameplay for early development and debugging purpose. The full game with complete user interfaces are to be launched from runner.py.

The other files (such as simulator.py, tests.py, trainer.py, etc.) and 'learning_data' folder is not used for the game itself, but was used during the development for the learning process. You do not need to open or have any of those files to play the game. Those files might contain other modules such as scikit-learn to train the model.

## Future Improvements

The 'puzzle' feature is not completely done yet, so don't click that option :(
Also, the 'about' page is not yet implemented as well :(
And I might not be able to complete it in near time due to some other work, afterall the project itself might need some restructuring as well and it has been a while since I last touched this project.
I am also considering to develop a stronger AI and create the game executable or zip file so people do not have to download everything.
All of these coming soon...
