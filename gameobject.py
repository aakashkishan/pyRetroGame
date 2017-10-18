import pygame
from assetloader import *
import math
import random


class Background( pygame.sprite.Sprite ):
    def __init__( self, image, backgroundSoundEffect ):

        # Initialising the Background Sound Effect
        self.backgroundSoundEffect = backgroundSoundEffect
        self.backgroundSoundEffect.play(-1)    # The -1 is the Loop Count and hence it loops through Continuosly

        # Creating Nebula Surface
        self.imageAsset = pygame.image.load( image )

        # Set the required variables
        self.nebulaWidth = int ( self.imageAsset.get_width() / 2 )
        self.nebulaHeight = int( self.imageAsset.get_height() / 2 )
        self.dimens = (self.nebulaWidth, self.nebulaHeight)

        # Scale the nebulaSurface to fit the Window
        self.finalAsset = pygame.transform.scale( self.imageAsset, (self.dimens[0], self.dimens[1]) )

        # Create a rect type in the class
        self.rect = self.finalAsset.get_rect()

    # Create update function for frequent rendering
    def update(self):
        return;    


class Player( pygame.sprite.Sprite ):
    def __init__( self, image, scale, rotateAngle, coords, explosionSoundEffect ):

        # Initializing the Explosion Sound Effect
        self.explosionSoundEffect = explosionSoundEffect

        # Render the playerAsset onto the a Surface and also the clip it by providing the required coordinates
        # Rotate the Player Asset
        # Function signature: func( assetImageURL, scaleIndex, rotationAngle, clippingCoordinates )
        self.initialAsset = assetLoader( image, scale, rotateAngle, coords )
        self.finalAsset = self.initialAsset

        # To Set the Color Key Transparent
        self.playerColorKey = (0, 0, 0)
        self.explosionColorKey = 0x454e5b

        # Create a rect type in the class
        self.rect = self.finalAsset.get_rect()
        self.rect.x = 400
        self.rect.y = 300

        # Create Velocity and Acceleration for Game Physics
        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 0
        self.accelerationY = 0

        # Set a Speed, Thrush, Damp, Velocity Limit and Angle for Motion
        # self.pace = 3
        self.angle = 0
        self.thrust = 0.4
        self.damp = 0.3
        self.velocityLimit = 8   # This is the Maximum Velocity an Object can acquire

        # Set the Collision Attributes / Parameters
        self.collision = False     # Boolean value for Collision
        self.collisionObjects = []

        # Set the Delayed Events Attributes / Parameters
        self.isWaitingToRevive = False
        self.timeToRevive = 0

        # Set the Explosion Animation
        self.explosionAnimationFrames = []
        self.currentAnimationFrame = 0
        self.loadExplosionAnimation()
        

    # Load the Required Assets for the Explosion Animation
    def loadExplosionAnimation(self):
        frameWidth = 24
        frameHeight = 25
        # Loop through the Explosion Image Assets
        for i in range(0, 6):
            # Append the Various Stages of the Explosion Animation
            self.explosionAnimationFrames.append(assetLoader("./images/explosionAnimation.bmp", 2, 0, (frameWidth * i, 0, frameWidth, frameHeight)))


    # In case of Spawn of the Object Function
    def onSpawn(self):
        self.reviveObject()

    # In case of Death of the Object Function
    def onDeath(self):
        # onDeath Play the Explosion Sound Effect
        self.explosionSoundEffect.play(1)

        # Set the Delay for onDeath Event
        self.isWaitingToRevive = True
        self.timeToRevive = 120
        self.currentAnimationFrame = 0

    # To Revive the Object
    def reviveObject(self):
        # Use all the Variables required to revive the Object
        self.rect.x = 400
        self.rect.y = 300

        self.velocityX = 0
        self.velocityY = 0
        self.accelerationX = 0
        self.accelerationY = 0
        
        # Collision Attribute
        self.collision = False



    # Create update function to update the Game Physics
    def update(self):

        # Process the Delayed Events
        if self.isWaitingToRevive:
            # Update the Explosion Animation changes
            # Restrict the Animation Asset with a Condition
            if self.currentAnimationFrame < len(self.explosionAnimationFrames):
                self.finalAsset = self.explosionAnimationFrames[self.currentAnimationFrame]
                self.finalAsset.set_colorkey( self.explosionColorKey )   # To make the color key transparent
                self.currentAnimationFrame += 1
            else:
                self.finalAsset = pygame.Surface((0,0))

                # Call the handleEventDelays Function
                self.handleEventDelays()
        
        else:
            # To make the color key transparent
            self.finalAsset.set_colorkey( self.playerColorKey )

            # Get the User Inputs for the Player and Process the User Controls
            userControls = self.getUserInput()
            self.processUserControls(userControls)
            self.finalAsset = pygame.transform.rotate(self.initialAsset, self.angle)

            # Collision Detection Function
            self.checkCollision()

            # Update Motion Function to update the Motion of the Objects 
            self.updateMotion()

    # Handle the Event Delays in the Game
    def handleEventDelays(self):
        
        # Decrement the Time for Object Revival
        self.timeToRevive -= 1
        if self.timeToRevive < 0:
            # Reset the Delay for Events to Default
            self.isWaitingToRevive = False
            self.reviveObject()

    
    def getUserInput(self):

        # Get the User Key Logs using pyGame key function
        up = pygame.key.get_pressed()[pygame.K_UP]
        down = pygame.key.get_pressed()[pygame.K_DOWN]
        right = pygame.key.get_pressed()[pygame.K_RIGHT]
        left = pygame.key.get_pressed()[pygame.K_LEFT]

        # Return an Array of the pressed Keys
        return (up, right, down, left)


    def processUserControls(self, controls):

        # Based on the pressed Keys get the Rotation Angle, Velocity and Acceleration of the Object
        if controls[0] == 1 and controls[1] == 0 and controls[2] == 0 and controls[3] == 0:
            self.angle = 0
        elif controls[0] == 1 and controls[1] == 1 and controls[2] == 0 and controls[3] == 0:
            self.angle = 315
        elif controls[0] == 0 and controls[1] == 1 and controls[2] == 0 and controls[3] == 0:
            self.angle = 270
        elif controls[0] == 0 and controls[1] == 1 and controls[2] == 1 and controls[3] == 0:
            self.angle = 225
        elif controls[0] == 0 and controls[1] == 0 and controls[2] == 1 and controls[3] == 0:
            self.angle = 180
        elif controls[0] == 0 and controls[1] == 0 and controls[2] == 1 and controls[3] == 1:
            self.angle = 135
        elif controls[0] == 0 and controls[1] == 0 and controls[2] == 0 and controls[3] == 1:
            self.angle = 90
        elif controls[0] == 1 and controls[1] == 0 and controls[2] == 0 and controls[3] == 1:
            self.angle = 45

        # Update the Acceleration based on Thrust
        self.accelerationX = self.thrust * (controls[1] - controls[3])
        self.accelerationY = self.thrust * (controls[2] - controls[0])


    # If Collision is Checked and is True then, Reset all Game Objects by calling onDeath Function
    def checkCollision(self):

        # Loop through the Collision Objects and check for Collision
        for collisionObject in self.collisionObjects:
            # collidrect is a pygame function that returns a boolean value by checking for colliding rects
            self.collision = self.rect.colliderect(collisionObject.rect)

            if self.collision:

                self.onDeath()    # Calling the Player Object's onDeath Function
                for gameObject in self.collisionObjects:
                    gameObject.onDeath()

                break



    def updateMotion(self):
        # Update the Game Physics
        # Apply the Acceleration
        self.velocityX += self.accelerationX
        self.velocityY += self.accelerationY

        # Apply the Thruster Damping
        # Apply the Horizontal Damping
        if self.velocityX > 0 + self.damp:
            self.velocityX -= self.damp
        elif self.velocityX < 0 - self.damp:
            self.velocityX += self.damp
        else:
            self.velocityX = 0

        # Apply the Vertical Damping
        if self.velocityY > 0 + self.damp:
            self.velocityY -= self.damp
        elif self.velocityY < 0 - self.damp:
            self.velocityY += self.damp
        else:
            self.velocityY = 0

        # Restrict the Velocity of the Object to the Velocity Limit
        # Horizontal Velocity restriction
        if self.velocityX > self.velocityLimit:
            self.velocityX = self.velocityLimit
        elif self.velocityX < self.velocityLimit * -1:
            self.velocityX = self.velocityLimit * -1

        # Vertical Velocity restriction
        if self.velocityY > self.velocityLimit:
            self.velocityY = self.velocityLimit
        elif self.velocityY < self.velocityLimit * -1:
            self.velocityY = self.velocityLimit * -1


        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
    

class Enemy( pygame.sprite.Sprite ):
    def __init__( self, image, scale, rotateAngle, coords, boundaries, targetObject, enemyWaveHandler ):

        # Render the enemyAsset onto the a Surface and also the clip it by providing the required coordinates
        # Rotate the Enemy Asset
        # Function signature: func( assetImageURL, scaleIndex, rotationAngle, clippingCoordinates )
        self.finalAsset = assetLoader( image, scale, rotateAngle, coords )

        # To make the color key transparent
        self.finalAsset.set_colorkey( 0x454e5b )

        # Create a rect type in the class
        self.rect = self.finalAsset.get_rect()
        self.rect.x = 200
        self.rect.y = 300

        # Create Enemy Attributes like Boundary and Reset Position
        self.boundaryX = boundaries[0]
        self.boundaryY = boundaries[1]


        # Create Speed, Velocity and Acceleration for Game Physics
        self.velocityX = 0
        self.velocityY = 0

        # Set the Delayed Events Attributes / Parameters
        self.isWaitingToRevive = False
        self.timeToRevive = 0

        # Provide the Enemy Object with Attributes to intercept the Target Object
        self.target = targetObject
        self.targetRange = 350
        self.relativeTargetVectorX = 0
        self.relativeTargetVectorY = 0
        self.relativeTargetLeapsX = 0
        self.relativeTargetLeapsY = 0
        self.targetDistance = 0

        # Set a Speed, Thrush, Damp, Velocity Limit and Angle for Motion
        # self.pace = 3
        self.angle = 0
        self.thrust = 0.3
        self.damp = 0.2
        self.velocityLimit = 5   # This is the Maximum Velocity an Object can acquire

        # Enemy Object Chase States
        # 1 - Search Target,  2 - Chase Target,  3 - Lost Target
        self.currentState = 1

        # Get the Enemy Object Wave Handler
        self.waveHandler = enemyWaveHandler

        # Start the Game with the revived Enemy Object
        self.reviveObject()



    # In case of Spawn of the Object Function
    def onSpawn(self):
        self.reviveObject()

    # In case of Death of the Object Function
    def onDeath(self):
        # Set the Delay for onDeath Event
        self.isWaitingToRevive = True
        self.timeToRevive = 120

        # Log the Death of an Enemy Object
        self.waveHandler.enemyDeath()


    # To Revive the Object
    def reviveObject(self):
        # Check if the Enemy Object is capable of Spawm
        if self.waveHandler.allowSpawn():
            # Once the Enemy croses the stipulated boundary Revive the Enemy
            self.currentState = 1
            self.rect.x = random.randrange( 0, self.boundaryX ) * -1
            self.rect.y = random.randrange( 0, self.boundaryY ) * -1

            self.velocityX = 0
            self.velocityY = 0

            # Log the Enemy Spawn Record
            self.waveHandler.enemySpawn()
        else:
            # Reset the Dead Enemies and add those Enemies to be Spawned
            self.subtleReset()
            self.waveHandler.appendEnemySpawn(self)

    # For just the Reset of the Enemy's Coordinates in the Game
    def subtleReset(self):
        self.rect.x = self.boundaryX
        self.rect.y = self.boundaryY


    # Create update function to update the Game Physics
    def update(self):

        # Process the Delayed Events
        if self.isWaitingToRevive:
            # Call the handleEventDelays Function
            self.handleEventDelays()

        else:  
            # Manage the Chase States of the Enemy Object
            self.handleStates()

            # Apply the Thruster Damping for Enemy Object
            # Apply the Horizontal Damping
            if self.velocityX > 0 + self.damp:
                self.velocityX -= self.damp
            elif self.velocityX < 0 - self.damp:
                self.velocityX += self.damp
            else:
                self.velocityX = 0

            # Apply the Vertical Damping
            if self.velocityY > 0 + self.damp:
                self.velocityY -= self.damp
            elif self.velocityY < 0 - self.damp:
                self.velocityY += self.damp
            else:
                self.velocityY = 0

            # Restrict the Velocity of the Enemy Object to the Velocity Limit
            # Horizontal Velocity restriction
            if self.velocityX > self.velocityLimit:
                self.velocityX = self.velocityLimit
            elif self.velocityX < self.velocityLimit * -1:
                self.velocityX = self.velocityLimit * -1

            # Vertical Velocity restriction
            if self.velocityY > self.velocityLimit:
                self.velocityY = self.velocityLimit
            elif self.velocityY < self.velocityLimit * -1:
                self.velocityY = self.velocityLimit * -1

            self.rect.x += self.velocityX
            self.rect.y += self.velocityY

            # If the Rock crosses the Boundary update the revive position of the Rock
            if self.rect.x > self.boundaryX or self.rect.y > self.boundaryY:
                self.onDeath()

    def handleStates(self):
        # Get the Vectors and Distance of the Target Object
        self.relativeTargetVectorX = self.target.rect.x - self.rect.x
        self.relativeTargetVectorY = self.target.rect.y - self.rect.y
        self.targetDistance = math.sqrt( (self.relativeTargetVectorX)**2 + (self.relativeTargetVectorY)**2 )

        # Check for Chase States of the Enemy Objects
        if self.currentState == 1:
            # Check for the Target Object in Range
            if self.targetDistance <= self.targetRange:
                # if True, chase the Target
                self.currentState = 2
            else:
                # Update the Game Physics to catch up to the Target Object
                self.velocityX += self.thrust
                self.velocityY += self.thrust
        
        elif self.currentState == 2:
            # Check for the Target Object out of Range
            if self.targetDistance > self.targetRange:
                # if True, Lost the Target
                self.currentState = 3
            else:
                # Call Chase Target Function
                self.handleChaseTarget()

        elif self.currentState == 3:
            # Check for the Target Object in Range
            if self.targetDistance <= self.targetRange:
                # if True, chase the Target
                # Call Chase Target Function
                self.handleChaseTarget()
            else:
                # Update the Game Physics to catch up to the Target Object
                self.velocityX += self.thrust
                self.velocityY += self.thrust




    def handleChaseTarget(self):
        # Get the Vectors and Distance of the Target Object
        self.relativeTargetVectorX = self.target.rect.x - self.rect.x
        self.relativeTargetVectorY = self.target.rect.y - self.rect.y
        self.targetDistance = math.sqrt( (self.relativeTargetVectorX)**2 + (self.relativeTargetVectorY)**2 )

        # Set the Leaps to the Target Object
        self.relativeTargetLeapsX = self.relativeTargetVectorX / self.targetDistance
        self.relativeTargetLeapsY = self.relativeTargetVectorY / self.targetDistance

        # Update the Game Physics to catch up to the Target Object
        self.velocityX += self.relativeTargetLeapsX * self.thrust
        self.velocityY += self.relativeTargetLeapsY * self.thrust


    # Handle the Event Delays in the Game
    def handleEventDelays(self):
        
        # Decrement the Time for Object Revival
        self.timeToRevive -= 1
        if self.timeToRevive < 0:
            # Reset the Delay for Events to Default
            self.isWaitingToRevive = False
            self.reviveObject()
    


class Rock( pygame.sprite.Sprite ):
    def __init__( self, image, scale, rotateAngle, coords, boundaries ):

        # Render the rockAsset onto the a Surface and also the clip it by providing the required coordinates
        # Rotate the Rock Asset
        # Function signature: func( assetImageURL, scaleIndex, rotationAngle, clippingCoordinates )
        self.finalAsset = assetLoader( image, scale, rotateAngle, coords )

        # To make the color key transparent
        self.finalAsset.set_colorkey( 0x454e5b )

        # Create a rect type in the class
        self.rect = self.finalAsset.get_rect()
        self.rect.x = 100
        self.rect.y = 500

        # Create Velocity and Acceleration for Game Physics
        self.velocityX = 5
        self.velocityY = 5
        self.accelerationX = 0
        self.accelerationY = 0

        # Create Rock Attributes like Boundary and Reset Position
        self.boundaryX = boundaries[0]
        self.boundaryY = boundaries[1]

        # Revive the already passed Rock
        self.reviveObject()

        # Set the Delayed Events Attributes / Parameters
        self.isWaitingToRevive = False
        self.timeToRevive = 0

    # In case of Spawn of the Object Function
    def onSpawn(self):
        self.reviveObject()

    # In case of Death of the Object Function
    def onDeath(self):
        # Set the Delay for onDeath Event
        self.isWaitingToRevive = True
        self.timeToRevive = 120

    # To Revive the Object
    def reviveObject(self):

        # Once the Rock croses the stipulated boundary Revive the Rock
        self.rect.x = random.randrange( 0, self.boundaryX ) * -1
        self.rect.y = random.randrange( 0, self.boundaryY ) * -1


    # Create update function to update the Game Physics
    def update(self):

        # Process the Delayed Events
        if self.isWaitingToRevive:
            # Call the handleEventDelays Function
            self.handleEventDelays()

        else:
            # Update the Game Physics
            self.velocityX += self.accelerationX
            self.velocityY += self.accelerationY

            # If the Rock crosses the Boundary update the revive position of the Rock
            if self.rect.x > self.boundaryX or self.rect.y > self.boundaryY:
                self.onDeath()

            self.rect.x += self.velocityX
            self.rect.y += self.velocityY


    # Handle the Event Delays in the Game
    def handleEventDelays(self):
        
        # Decrement the Time for Object Revival
        self.timeToRevive -= 1
        if self.timeToRevive < 0:
            # Reset the Delay for Events to Default
            self.isWaitingToRevive = False
            self.reviveObject()
    


class WaveHandler():
    # The Constructor for the waveHandler
    def __init__(self, nextWaveSoundEffect):
        # Initialising the Next Wave Sound Effects
        self.nextWaveSoundEffect = nextWaveSoundEffect

        # Declare and Initialize required Next Wave Attributes and Parameters
        self.currentWave = 1
        self.enemySpawnCount = 0
        self.enemyDeadCount = 0
        self.enemiesPerWave = 3
        self.enemyWaitingToSpawn = []
        self.scoreBoard = 0

    # Check if the Enemy Object is capable of Spawn
    def allowSpawn(self):
        # Will Return True if the Spawn Count is below number of enemies per Wave
        if self.enemySpawnCount >= self.enemiesPerWave:
            return False
        else:
            return True

    # Handle the Enemy Spawn
    def enemySpawn(self):
        # Increment the Enemy Spawn Count
        self.enemySpawnCount += 1

    # Handle the Enemy Death
    def enemyDeath(self):
        # Increment the Enemy Dead Count and the Score of the Player
        self.enemyDeadCount += 1
        self.scoreBoard += 1

        # Check if all Enemies in the Wave are Dead
        if self.enemyDeadCount == self.enemiesPerWave:
            # If True, Start the next Wave
            self.nextEnemyWave()

    # Handle the Next Enemy Wave
    def nextEnemyWave(self):
        # On Next Wave Play the Next Wave Sound Effect
        self.nextWaveSoundEffect.play()

        # On Next Enemy Wave Reset the Death, Spawn Counts and Increase the number of Enemies per Wave
        self.enemySpawnCount = 0
        self.enemyDeadCount = 0
        self.enemiesPerWave += 1
        self.currentWave += 1

    # Enemy Object waiting to be Spawn
    def appendEnemySpawn(self, enemyObject):
        self.enemyWaitingToSpawn.append(enemyObject)

    # Update the necessary changes to the Enemy Wave
    def update(self):
        # Check if the Enemy Object can Spawn
        if self.allowSpawn():
            for enemyObject in self.enemyWaitingToSpawn:
                enemyObject.reviveObject()

    




