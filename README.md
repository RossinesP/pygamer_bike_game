# pygamer_bike_game
A game running on the Adagruit PyGamer and using a home bike.

# Context
The game runs on the Py Gamer using CircuitPython (https://www.adafruit.com/product/4242) connected to a home bike, the Sportstech X100-B.
You can probably use any other home bike, as long as uses a reed switch to read the speed and you can wire that reed switch to your Py Gamer.
The X100-B provides a convenient female jack connector directly wired to the reed, so it was easy to connect it.


# Goal
This app lets you :
- Monitor your estimated speed, time, calories count
- Play a mini game in which you have to race against the Pygamer

# How to install
You should install the CircuitPython libraries first on your Pygamer, following the guide available on the adafruit website.

Copy all the files to the CIRCUITPY mount point, and voilà !

# How to use
Use the B button to navigate between "activities"
Use the start button to validate the input in the game activity
You can use the A button to simulate a full wheel rotation.
