# Import modules
import pygame
import pygame.mixer
import random


# Initialize pygame and mixer modules
pygame.init()
pygame.mixer.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Define the possible states
MENU = 0
PLAY = 1
GAME_OVER = 2

# Create a variable to store the current state
state = MENU


# Define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FONT_SIZE = 32
FONT_NAME = "Arial"
TITLE_SCREEN_DELAY = None
GAME_OVER_DELAY = None
# Create the screen surface
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load game images
game_over_screen = pygame.image.load("img/game_over.jpg")
title_screen = pygame.image.load("img/title.jpg")
enemy_image2 = pygame.image.load("img/enemy2.png")
enemy_image1 = pygame.image.load("img/enemy1.png")
explosion_images = pygame.image.load("img/explosion1.png")
background = pygame.image.load("img/background.png")
spaceship = pygame.image.load("img/spaceship.png")
bullet_image = pygame.image.load("img/spacebullet.png")
print(bullet_image)

# Load game sounds
shoot_sound = pygame.mixer.Sound("sound/shoot.mp3")
explode_sound = pygame.mixer.Sound("sound/explode.mp3")
gameover_song = pygame.mixer.Sound("sound/gameover_song.mp3")
title_song = pygame.mixer.Sound("sound/title_song.mp3")
cyberpunk_song = pygame.mixer.Sound("sound/cyberpunk_song.mp3")
deathscream_sound = pygame.mixer.Sound("sound/deathscream_sound.mp3")

original_width, original_height = spaceship.get_size()
new_width = int(original_width * 0.1)
new_height = int(original_height * 0.1)
spaceship = pygame.transform.scale(spaceship, (new_width, new_height))

original_width, original_height = bullet_image.get_size()
new_width = int(original_width * 0.1)
new_height = int(original_height * 0.1)
bullet_image = pygame.transform.scale(bullet_image, (new_width, new_height))

original_width, original_height = enemy_image1.get_size()
new_width = int(original_width * 0.1)
new_height = int(original_height * 0.1)
enemy_image1 = pygame.transform.scale(enemy_image1, (new_width, new_height))

original_width, original_height = enemy_image2.get_size()
new_width = int(original_width * 0.1)
new_height = int(original_height * 0.1)
enemy_image2 = pygame.transform.scale(enemy_image2, (new_width, new_height))

original_width, original_height = title_screen.get_size()
new_width = SCREEN_WIDTH
new_height = SCREEN_HEIGHT
title_screen = pygame.transform.scale(title_screen, (new_width, new_height))

original_width, original_height = background.get_size()
new_width = SCREEN_WIDTH
new_height = SCREEN_HEIGHT
background = pygame.transform.scale(background, (new_width, new_height))

original_width, original_height = game_over_screen.get_size()
new_width = SCREEN_WIDTH
new_height = SCREEN_HEIGHT
game_over_screen = pygame.transform.scale(game_over_screen, (new_width, new_height))

# Set the volume of the gameover_song to 0.2 (20% volume)
gameover_song.set_volume(0.15)
title_song.set_volume(0.15)
cyberpunk_song.set_volume(0.15)
deathscream_sound.set_volume(0.15)
explode_sound.set_volume(0.15)
shoot_sound.set_volume(0.15)


all_sprites = pygame.sprite.Group()
# Create a timer event for spawning enemies
SPAWN_ENEMY = pygame.USEREVENT + 1
bullets = pygame.sprite.Group()


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_image):
        print("Creating bullet...")
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the bullet image
        self.image = bullet_image
        # Set the initial position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # Set the initial speed
        self.speedy = -10
        # Assign the Bullet object to the variable bullet
        bullet = self
        # Add the bullet to the sprites and bullets groups
        all_sprites.add(bullet)
        bullets.add(bullet)

    # Update the bullet position and speed
    def update(self):
        self.rect.y += self.speedy
        # Remove the bullet if it goes off the screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Define the player class
class Player(pygame.sprite.Sprite):
    # Initialize the player object
    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the image and the rect attributes
        self.image = spaceship
        self.rect = self.image.get_rect()
        # Set the initial position
        self.rect.centerx = x
        self.rect.bottom = y
        # Set the initial speed
        self.speedx = 0
        # Set the initial health
        self.health = 100
        # Set the shooting delay
        self.shoot_delay = 250
        # Set the last shoot time
        self.last_shoot = pygame.time.get_ticks()

    # Update the player position and speed
    def update(self):
        # Move the player according to the speed
        self.rect.x += self.speedx
        # Keep the player within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    # Shoot a bullet
    def shoot(self):
        print("Shooting...")
        # Get the current time
        now = pygame.time.get_ticks()
        # Check if the shooting delay is over
        if now - self.last_shoot > self.shoot_delay:
            # Update the last shoot time
            self.last_shoot = now
            # Create a bullet object
            bullet = Bullet(self.rect.centerx, self.rect.top, self.imgae)
            # Add the bullet to the sprites group
            all_sprites.add(bullet)
            print("Bullet fired:")
            # Play the shoot sound
            shoot_sound.play()
            # Set the speedy attribute of the bullet to move it up
            bullet.speedy = -10
            # Draw the bullet image on the screen
            screen.blit(bullet_image, (bullet.rect.x, bullet.rect.y))


ENEMY_SPEED = 2
# Enemy class
# Define the base enemy class
class Enemy(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, x, y, image, speed):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the enemy image and scale it
        self.image = pygame.transform.scale(image, (50, 50))
        # Set the initial position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Set the initial speed
        self.speedx = speed
        self.speedy = speed
        # Set the movement pattern
        self.move_right = True
        self.move_down = False

    # Update the enemy position and speed
    def update(self):
        # Move left or right
        if self.move_right:
            self.rect.x += self.speedx
        else:
            self.rect.x -= self.speedx
        # Change direction if the enemy hits the edge of the screen
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.move_right = not self.move_right
            self.move_down = True
        # Move down if needed
        if self.move_down:
            self.rect.y += self.speedy
            self.move_down = False
        # Check if the enemy is off the screen
        if self.rect.top > SCREEN_HEIGHT:
            # Remove the enemy from the sprites group and the enemies group
            self.kill()


# Define the first enemy subclass
class Enemy1(Enemy):
    # Constructor
    def __init__(self, x, y):
        # Call the parent class constructor with the specific image and speed
        Enemy.__init__(self, x, y, enemy_image1, ENEMY_SPEED)
        # Set the movement pattern
        self.move_right = False  # Start moving left
        self.move_down = True  # Start moving down

    # Override the update method to add some randomness
    def update(self):
        # Call the parent class update method
        Enemy.update(self)
        # Add some randomness to the enemy movement
        # Change the speed by a random amount between -2 and 2
        self.speedx += random.randint(-2, 2)
        self.speedy += random.randint(-2, 2)
        # Change the direction by a random chance of 10%
        if random.random() < 0.1:
            self.move_right = not self.move_right


# Define the second enemy subclass
class Enemy2(Enemy):
    # Constructor
    def __init__(self, x, y):
        # Call the parent class constructor with the specific image and speed
        Enemy.__init__(self, x, y, enemy_image2, ENEMY_SPEED * 2)  # Double the speed
        # Set the movement pattern
        self.move_right = True  # Start moving right
        self.move_down = False  # Start moving up

    # Override the update method to add some bouncing
    def update(self):
        # Call the parent class update method
        Enemy.update(self)
        # Add some bouncing to the enemy movement
        # Reverse the vertical speed if the enemy hits the top or bottom of the screen
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speedy = -self.speedy


# Explosion class
class Explosion(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, x, y):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Load the explosion image and scale it
        self.image = pygame.transform.scale(explosion_images, (50, 50))
        # Set the initial position
        self.rect.centerx = x
        self.rect.centery = y
        # Set the initial frame
        self.frame = 0
        # Set the animation speed
        self.speed = 10
        # Set the last update time
        self.last_update = pygame.time.get_ticks()

    # Update the explosion animation
    def update(self):
        # Get the current time
        now = pygame.time.get_ticks()
        # Check if the animation speed is over
        if now - self.last_update > self.speed:
            # Update the last update time
            self.last_update = now
            # Increase the frame
            self.frame += 1
            # Check if the frame is out of range
            if self.frame > 3:
                # Remove the explosion from the sprites group
                self.kill()
            else:
                # Crop the image to show the next frame
                self.image = self.image.subsurface((self.frame * 50, 0, 50, 50))


# Game class
class Game12():
    # Initialize game variables
    def __init__(self, screen):
    
        # Set the screen
        self.screen = screen
        # Create a font object
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # Create a sprites group
        self.all_sprites = pygame.sprite.Group()  # <-- Add this line
        # Create a bullets group
        self.bullets = pygame.sprite.Group()
        # Create an enemies group
        self.enemies = pygame.sprite.Group()
        # Create a player object
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
        self.all_sprites.add(self.player)
        # Create some enemies
        self.create_enemies(None)
        # Set the initial score
        self.score = 0
        # Set the initial lives
        self.lives = 3
        # Set the initial level
        self.level = 1
        # Set the game over flag
        self.game_over = False
        # Update the sprites
        self.all_sprites.update()
        
 

    # Create some enemies
    def create_enemies(self, event): # <-- Add the event parameter
        # Choose a random number of enemies
        num_enemies = random.randint(5, 10)
        # Choose a random speed for the enemies
        speed = random.randint(1, 5)
        # Choose a random image for the enemies
        image = random.choice([enemy_image1, enemy_image2])
        # Loop through the number of enemies
        for i in range(num_enemies):
            # Choose a random x position for the enemy
            x = random.randint(0, SCREEN_WIDTH - 50)
            # Choose a random y position for the enemy
            y = random.randint(-100, -50)
            # Create an enemy object
            enemy = Enemy(x, y, image, speed)
            # Add the enemy to the sprites group and the enemies group
            self.all_sprites.add(enemy)
            self.enemies.add(enemy) # Add the enemy to the enemies group
            
        
# Spawn an enemy if the timer event occurs
        for event in pygame.event.get():
            if event.type == SPAWN_ENEMY:
                self.create_enemies(event)         
            

        # Update the game state
    def update(self):
        # Update the sprites
        self.all_sprites.update()
        # Check for collisions between bullets and enemies
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for collision in collisions:
            # If a bullet hits an enemy, remove both from the game
            self.bullets.remove(collision)
            self.enemies.remove(collision)

        # Loop through the hits
        for hit in hits:
            # Decrease the player health
            self.player.health -= 25
            # Play the deathscream sound
            deathscream_sound.play()
            # Create an explosion object
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            # Add the explosion to the sprites group
            self.all_sprites.add(explosion)
        # Check if the player health is zero or less
        if self.player.health <= 0:
            # Decrease the lives
            self.lives -= 1
            # Reset the player health
            self.player.health = 100
            # Check if the lives are zero or less
            if self.lives <= 0:
                # Set the game over flag to True
                self.game_over = True
        # Check if the game is over
        if self.game_over:
            # Play the game over sound
            gameover_song.play()
            deathscream_sound.play
            # Reset the game
            self.reset_game()

        # Draw the game screen
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draw the bullets on top of other sprites
        bullets = pygame.sprite.Group()
        bullets.add(*all_sprites)
        bullets.draw(self.screen)
        # draw the rest of the sprites
        all_sprites.draw(self.screen)
        # Draw the background image
        self.screen.blit(background, (0, 0))
        # Draw the sprites
        self.all_sprites.draw(self.screen)
        # Draw the score
        self.draw_text("Score: " + str(self.score), WHITE, 10, 10)
        # Draw the lives
        self.draw_text("Lives: " + str(self.lives), WHITE, SCREEN_WIDTH - 110, 10)
        # Draw the level
        self.draw_text("Level: " + str(self.level), WHITE, SCREEN_WIDTH / 2 - 50, 10)
        # Draw the health bar
        self.draw_health_bar()

        # Draw some text on the screen
    def draw_text(self, text, color, x, y):
        # Render the text using the font object
        text_surface = self.font.render(text, True, color)
        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        # Set the position of the text
        text_rect.midtop = (x, y)
        # Blit the text surface onto the screen
        self.screen.blit(text_surface, text_rect)

        # Draw the health bar
    def draw_health_bar(self):
         # Set the position and size of the health bar
        x = 10
        y = 50
        width = 100
        height = 10
        # Calculate the percentage of health
        percentage = self.player.health / 100
        # Calculate the fill width
        fill_width = int(width * percentage)
        # Create a border rectangle
        border_rect = pygame.Rect(x, y, width, height)
         # Create a fill rectangle
        fill_rect = pygame.Rect(x, y, fill_width, height)
        # Choose a color for the fill rectangle based on the percentage
        if percentage > 0.6:
            color = GREEN
        elif percentage > 0.3:
            color = YELLOW
        else:
            color = RED
            # Draw the border rectangle
            pygame.draw.rect(self.screen, WHITE, border_rect, 2)
            # Draw the fill rectangle
            pygame.draw.rect(self.screen, color, fill_rect)

    # Show the title screen
    def show_title_screen(self):
        # Draw the title screen image
        self.screen.blit(title_screen, (0, 0))
        # Draw some text
        self.draw_text(
            "Press any key to start",
            WHITE,
            SCREEN_WIDTH / 2 - 150,
            SCREEN_HEIGHT / 2 + 100,
        )
        # Update the display
        pygame.display.update()
        # Wait for a key press
        self.wait_for_key()
         # Reset the game over flag
        self.game_over = False

    # Show the game over screen
    def show_game_over_screen(self,):
        # Draw the game over screen image
        self.screen.blit(game_over_screen, (0, 0))
        # Draw some text
        self.draw_text(
            "Your final score is: " + str(self.score),
            WHITE,
            SCREEN_WIDTH / 2 - 150,
            SCREEN_HEIGHT / 2 + 100,
        )
        # Update the display
        pygame.display.update()
        # Wait for a key press
        self.wait_for_key()


    # Wait for a key press
    def wait_for_key(self):
        # Set the waiting flag
        waiting = True
        # Loop while waiting
        while waiting:
            # Get the events
            for event in pygame.event.get():
                # Quit the game if the user closes the window or presses ESC
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    pygame.mixer.quit()
                # Stop waiting if the user presses any key
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
        
def main():
    # Declare; state; as a variable
    global state
    # Create thegame window
    # (= pygame..set_modeSCREEN_WIDTH SCREEN_HE))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set the window and icon
    pygame.display.set_icon(spaceship)
    # Create a clock object to track the frame rate
    clock = pygame.time.Clock()
    # Create a game object
    state = MENU
    game = Game12(screen)
    # Play the title song
    title_song.play(-1)

    # Start the game loop
    running = True
    while running:
        # Set the frame rate
        clock.tick(FPS)
        # Handle the events
        events = pygame.event.get()
        for event in events:
            # Quit the game if the user closes the window or presses ESC
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                running = False

        # Check the current state
        for event in events:  # Move this line here
            if state == MENU:
                # Show the title screen
                game.show_title_screen()
                # Play the title song
                title_song.play(-1)
                # Change the state to play if the user presses SPACE
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    state = PLAY
                    # Stop the title song
                    title_song.stop()
                    # Play the cyberpunk song
                    cyberpunk_song.play(-1)

            elif state == PLAY:
                # Show the background screen

                # Spawn an enemy if the timer event occurs
                if event.type == SPAWN_ENEMY:
                    game.create_enemies(event)
                # Move the player left or right if the user presses LEFT or RIGHT
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("Left key pressed")
                        game.player.speedx = -5
                    if event.key == pygame.K_RIGHT:
                        print("Right key pressed")
                        game.player.speedx = 5
                    # Shoot a bullet if the user presses SPACE
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        print("Space key pressed")
                        game.player.shoot()
                # Check if the user has released a key
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            print("Left or Right key released")
                            game.player.speedx = 0
                    # Check for collisions between bullets and enemies
                if event.type == pygame.KEYUP:
                    collisions = pygame.sprite.groupcollide(
                        game.bullets, game.enemies, True, True, pygame.sprite.collide_mask
                    )
                    for bullet in collisions.keys():
                        # If a bullet hits an enemy, remove both from the game
                        game.bullets.remove(bullet)
                        # Get the list of enemies that the bullet hit
                        enemies = collisions[bullet]
                    for enemy in enemies:
                        game.enemies.remove(enemy)
                        # Add score for destroying an enemy
                        game.score += 10
                        # Call these methods only once per frame
                        game.all_sprites.update()
                        game.all_sprites.draw(screen)
                        # Draw the game screen
                        game.draw()
                        # Update the display
                        pygame.display.flip()
                        # Update the game state
                        game.update()
                        # Check if the game is over
                if game.game_over:
                    # Change the state to game over
                    state = GAME_OVER
                    # Stop the cyberpunk song
                    cyberpunk_song.stop()
                    # Play the game over song
                    gameover_song.play()
        else:  # state == GAME_OVER
            # Show the game over screen
            game.show_game_over_screen()
            # Quit pygame and mixer modules
            pygame.quit()
            pygame.mixer.quit()
            # Break the game loop
            break
        
# Call the main function
if __name__ == "__main__":
    main()
