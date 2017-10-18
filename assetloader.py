import pygame


# Create a Function to handle the Assets
def assetLoader (image, scale, rotateAngle, coords):

    # Creating the Asset
    asset = pygame.image.load(image)

    # To Clip Asset onto a Surface
    assetClip = pygame.Surface( (coords[2], coords[3]) )
    assetClip.blit( asset, (0, 0), coords )

    # To Rotate the Asset
    assetRotate = pygame.transform.rotate( assetClip, rotateAngle )

    # To scale the Asset
    assetScale = (coords[2] * scale, coords[3] * scale)
    assetScale = pygame.transform.scale( assetRotate, (coords[2] * scale, coords[3] * scale)  )

    # Return the Asset
    return assetScale