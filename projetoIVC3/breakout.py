"""
 Sample Breakout Game

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""

# --- Import libraries used for this program

import math
import cv2
import pygame
import tracker

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Size of break-out blocks
block_width = 23
block_height = 15


class Block(pygame.sprite.Sprite):
    """This class represents each block that will get knocked out by the ball
    It derives from the "Sprite" class in Pygame """

    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block,
            and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])

        # Fill the image with the appropriate color
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """ This class represents the ball
        It derives from the "Sprite" class in Pygame """

    # Speed in pixels per cycle
    speed = 4.0

    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # Direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        """ This function will bounce the ball
            off a horizontal surface (not a vertical one) """

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls. """

    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        super().__init__()

        self.speed = 5
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height
    def update(self, center):
        """ Update the player position. """

        #mexer o player com as setas do teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if abs(self.rect.x - center) > self.speed:
            if self.rect.x < center:
                self.rect.x += self.speed  # Move right
            else:
                self.rect.x -= self.speed  # Move left

            # Obrigar o player a ficar dentro dos limites
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x + self.width > self.screenwidth:
                self.rect.x = self.screenwidth - self.width

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Breakout')

# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create the player paddle object
player = Player()
allsprites.add(player)

# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the block (y position)
top = 80

# Number of blocks to create
blockcount = 32

# --- Create blocks

# Five rows of blocks
for row in range(5):
    # 32 columns of blocks
    for column in range(0, blockcount):
        # Create a block (color,x,y)
        block = Block(blue, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # Move the top of the next row down
    top += block_height + 2

# Clock to limit speed
clock = pygame.time.Clock()

# Is the game over?
game_over = False

# Exit the program?
exit_program = False

def start_screen():
    waiting = True
    while waiting:
        screen.fill(black)
        # Display start message
        start_text = font.render("Press any key to start", True, white)
        textpos = start_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(start_text, textpos)
        pygame.display.flip()

        # Wait for a key press to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

start_screen()

def game_loop():
    global exit_program, game_over, player, ball, blocks, screen, clock

    # Main program loop
    while not exit_program:
        # chamar o loop da camara e encontrar o centro
        center = tracker.camara_loop()

        # Limit to 30 fps
        clock.tick(30)

        # Clear the screen
        screen.fill(black)

        # Process the events in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True

        # Update the ball and player position as long
        # as the game is not over.
        if not game_over:
            # Update the player and ball positions
            player.update(center)
            game_over = ball.update()

        # If we are done, print game over
        if game_over:
            game_over = False
            text = font.render("Game Over", True, white)
            textpos = text.get_rect(centerx=background.get_width() / 2)
            textpos.top = 300
            screen.blit(text, textpos)
            game_loop()

        # See if the ball hits the player paddle
        if pygame.sprite.spritecollide(player, balls, False):
            # The 'diff' lets you try to bounce the ball left or right
            # depending where on the paddle you hit it
            diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)

            # Set the ball's y position in case
            # we hit the ball on the edge of the paddle
            ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(diff)

        # Check for collisions between the ball and the blocks
        deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

        # If we actually hit a block, bounce the ball
        if len(deadblocks) > 0:
            ball.bounce(0)

            # Game ends if all the blocks are gone
            if len(blocks) == 0:
                game_over = True

        # Draw Everything
        allsprites.draw(screen)

        # Flip the screen and show what we've drawn
        pygame.display.flip()

# Call the game loop function to start the game
game_loop()
cv2.destroyWindow()
pygame.quit()