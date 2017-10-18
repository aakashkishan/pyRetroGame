import sys, pygame
from gameobject import *
from assetloader import *


# Load the Audio Files and To Include pygame Mixer, pygame must be Initialised
pygame.init()
# Load the Sound Object by passing the Audio File URL
gameBackgroundSound = pygame.mixer.Sound("./audio/gameBackgroundSound.wav")
explosionSound = pygame.mixer.Sound("./audio/explosionSound.wav")
nextWaveSound = pygame.mixer.Sound("./audio/nextWaveSound.wav")


# Create a timer to maintain the frames per second
timer = pygame.time.Clock()

# Create a gameObjects list that appends all the objects in the game for future convinience
gameObjects = []

# Calling the Constructor of the Background Class in gameobject.py 
background = Background( "./images/nebulaLight.jpg", gameBackgroundSound )

# Creating a Window
window = pygame.display.set_mode( (background.nebulaWidth, background.nebulaHeight ) )
semiWindowWidth = background.nebulaWidth
semiwindowHeight = background.nebulaHeight

# Calling the Constructor of the Player Class in gameobject.py
# And Rendering the Player Asset
player = Player( "./images/hunterAsset.bmp", 2, 0, (25, 1, 23, 23), explosionSound )
gameObjects.append(player)

# Create a Enemy Wave Handler Object before the Enemy Objects are created
waveHandler = WaveHandler(nextWaveSound)

# Calling the Constructor of the Enemy Class in gameobject.py
# And Rendering the Enemy Asset
# Create a list of Enemy Objects
enemyObjects = []

for i in range(3):
    # Pass all the required attributes along with the Target Object that the Enemy must catch and the Enemy Wave Handler Object
    enemy = Enemy( "./images/enemyShip.bmp", 1, 0, (101, 13, 91, 59), (semiWindowWidth + 91, semiwindowHeight + 59), player, waveHandler )
    enemyObjects.append(enemy)
    gameObjects.append(enemy)
    player.collisionObjects.append(enemy)    # Append the Enemy Object as a Collision Object for Player Object

# Calling the Constructor of the Rock Class in gameobject.py
# And Rendering the Rock Asset
# Create a list of Rock Objects
rockObjects = []

for j in range(5):
    rock = Rock( "./images/spaceRock.bmp", 1, 0, (6, 3, 80, 67), (semiWindowWidth + 80, semiwindowHeight + 67) )
    rockObjects.append(rock)
    gameObjects.append(rock)
    player.collisionObjects.append(rock)     # Append the Rock Object as a Collision Object for Player Object


scoreBoardFrames = []
scoreCardWidth = 30
scoreCardHeight = 49
scoreCardColorKey = (0, 0, 0)
for i in range(0, 10):
    scoreBoardFrames.append( assetLoader("./images/scoreCard.bmp", 1, 0, (scoreCardWidth * i, 0, scoreCardWidth, scoreCardHeight)) )
    # scoreBoardFrames[i].set_colorkey( scoreCardColorKey )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Collision Check Changes
    if player.collision:
        # If Collision turn the Background Green
        window.fill( (0, 255, 0) )
    else:
        # Else set the Normal Game
        window.blit(background.finalAsset, (0, 0))


    # Update the Game Objects in the Game
    for gameObject in gameObjects:
        gameObject.update()


    # Render the Game Objects to the Window
    for gameObject in gameObjects:
        window.blit( gameObject.finalAsset, (gameObject.rect.x, gameObject.rect.y) )

    # Process the Score and Render the ScoreCard onto the Window
    # Use the WaveHandler Object to get the Score of the Player on Enemy Death
    scoreUnitDigit = waveHandler.scoreBoard % 10 
    scoreTenDigit = waveHandler.scoreBoard % 100 - scoreUnitDigit
    scoreHundredDigit = waveHandler.scoreBoard % 1000 - scoreUnitDigit - scoreTenDigit
    window.blit( scoreBoardFrames[scoreUnitDigit], (scoreCardWidth * 2, 0) ) 
    window.blit( scoreBoardFrames[(int(scoreTenDigit / 10))], (scoreCardWidth, 0) ) 
    window.blit( scoreBoardFrames[(int(scoreHundredDigit / 100))], (0, 0) ) 
    

    pygame.display.flip()

    # Set the frames per second
    timer.tick(60) # 60fps




