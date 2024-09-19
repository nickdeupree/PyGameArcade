import pygame
import random
import math
import sys

# Initialize Pygame modules
pygame.init()

# Define colors using RGB tuples (Black and White theme)
white = (255, 255, 255)
black = (0, 0, 0)

# Set display dimensions
dis_width = 800  # Width of the game window
dis_height = 600  # Height of the game window

# Create the display surface (the game window)
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Retro Arcade Game')  # Set the window title

# Create a clock object to manage the game's frame rate
clock = pygame.time.Clock()

# Fonts for rendering text
font_style = pygame.font.SysFont(None, 30)   # Font for messages
score_font = pygame.font.SysFont(None, 100)  # Font for the score display
button_font = pygame.font.SysFont(None, 30)  # Font for buttons

# Global variables for game settings
num_cherries = 1        # Default number of cherries in Snake
pong_difficulty = 'Medium'  # Default difficulty level for Pong
score_limit = 5         # Default score limit for Pong

def draw_button(text, x, y, width, height, inactive_color, active_color, action=None, events=None):
    """
    Draw a clickable button on the screen.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and click[0]:
            if x + width > mouse[0] > x and y + height > mouse[1] > y:
                if action is not None:
                    return action

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, width, height))
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, width, height))

    text_surf = button_font.render(text, True, black)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    dis.blit(text_surf, text_rect)
    return None

def message(msg, color, y_displace=0):
    """
    Display a message on the screen.
    """
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
    dis.blit(mesg, mesg_rect)

def arcade_menu():
    """
    Display the arcade menu where the player can choose between games.
    """
    while True:
        dis.fill(black)
        message("Retro Arcade Menu", white, -200)  # Position the title

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake_action = draw_button("Snake", 250, 120, 300, 50, white, white, 'snake_menu', events)
        pong_action = draw_button("Pong", 250, 190, 300, 50, white, white, 'pong_menu', events)
        asteroids_action = draw_button("Asteroids", 250, 260, 300, 50, white, white, 'asteroids_menu', events)
        space_invaders_action = draw_button("Space Invaders", 250, 330, 300, 50, white, white, 'space_invaders_menu', events)
        quit_action = draw_button("Quit", 250, 400, 300, 50, white, white, 'quit_game', events)
        pygame.display.update()

        if snake_action == 'snake_menu':
            snake_menu()
        elif pong_action == 'pong_menu':
            pong_menu()
        elif asteroids_action == 'asteroids_menu':
            asteroids_menu()
        elif space_invaders_action == 'space_invaders_menu':
            space_invaders_menu()
        elif quit_action == 'quit_game':
            pygame.quit()
            sys.exit()

        clock.tick(60)

# ---------------------- Snake Game Functions ----------------------

def snake_menu():
    """
    Display the Snake game menu with Start, Options, and Back buttons.
    """
    global num_cherries
    while True:
        dis.fill(black)
        message("Snake Game", white, -200)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_action = draw_button("Start", 250, 200, 300, 50, white, white, 'start_game', events)
        options_action = draw_button("Options", 250, 270, 300, 50, white, white, 'options_menu', events)
        back_action = draw_button("Back", 250, 340, 300, 50, white, white, 'back_to_arcade', events)
        pygame.display.update()

        if start_action == 'start_game':
            snake_game()
        elif options_action == 'options_menu':
            snake_options_menu()
        elif back_action == 'back_to_arcade':
            arcade_menu()

        clock.tick(60)

def snake_options_menu():
    """
    The options menu for the Snake game.
    """
    global num_cherries
    while True:
        dis.fill(black)
        message("Snake Options", white, -200)
        message(f"Current cherries: {num_cherries}", white, -150)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        cherry1_action = draw_button("1 Cherry", 150, 200, 200, 50, white, white, lambda: set_cherries(1), events)
        cherry2_action = draw_button("2 Cherries", 450, 200, 200, 50, white, white, lambda: set_cherries(2), events)
        cherry3_action = draw_button("3 Cherries", 150, 270, 200, 50, white, white, lambda: set_cherries(3), events)
        random_action = draw_button("Random", 450, 270, 200, 50, white, white, lambda: set_cherries('random'), events)
        back_action = draw_button("Back", 250, 340, 300, 50, white, white, 'back_to_snake_menu', events)
        pygame.display.update()

        if callable(cherry1_action):
            cherry1_action()
        if callable(cherry2_action):
            cherry2_action()
        if callable(cherry3_action):
            cherry3_action()
        if callable(random_action):
            random_action()
        if back_action == 'back_to_snake_menu':
            snake_menu()

        clock.tick(60)

def set_cherries(number):
    """
    Set the global number of cherries based on user selection.
    """
    global num_cherries
    num_cherries = number

def snake_game():
    """
    The main game loop for Snake.
    """
    global num_cherries
    snake_block = 10
    snake_speed = 15

    game_over = False
    game_close = False
    paused = False  # Pause flag

    x1 = dis_width // 2
    y1 = dis_height // 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    food_positions = []
    if num_cherries == 'random':
        num_current_cherries = random.randint(1, 3)
    else:
        num_current_cherries = num_cherries

    for _ in range(num_current_cherries):
        foodx = random.randrange(0, dis_width - snake_block, snake_block)
        foody = random.randrange(0, dis_height - snake_block, snake_block)
        food_positions.append([foodx, foody])

    while not game_over:

        while game_close:
            dis.fill(black)
            message("You Lost! Press B-Back or C-Play Again", white, -50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        snake_menu()
                    if event.key == pygame.K_c:
                        snake_game()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change != snake_block:
                        x1_change = -snake_block
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change != -snake_block:
                        x1_change = snake_block
                        y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change != snake_block:
                        y1_change = -snake_block
                        x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change != -snake_block:
                        y1_change = snake_block
                        x1_change = 0
                elif event.key == pygame.K_p:
                    paused = True

        while paused:
            dis.fill(black)
            message("Paused", white, -50)
            message("Press 'B' for Main Menu", white, 0)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        snake_menu()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(black)

        # Draw cherries
        for pos in food_positions:
            pygame.draw.rect(dis, white, [pos[0], pos[1], snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for self-collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        for x in snake_List:
            pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

        # Display the score
        display_snake_score(Length_of_snake - 1)

        pygame.display.update()

        # Check for collision with cherries
        eaten_cherries = []
        for pos in food_positions:
            if x1 == pos[0] and y1 == pos[1]:
                eaten_cherries.append(pos)
                Length_of_snake += 1

        # Remove eaten cherries
        for pos in eaten_cherries:
            food_positions.remove(pos)

        # Spawn new cherries
        if eaten_cherries:
            if num_cherries == 'random':
                num_new_cherries = random.randint(1, 3)
                for _ in range(num_new_cherries):
                    while True:
                        foodx = random.randrange(0, dis_width - snake_block, snake_block)
                        foody = random.randrange(0, dis_height - snake_block, snake_block)
                        new_cherry = [foodx, foody]
                        if new_cherry not in food_positions and new_cherry not in snake_List:
                            food_positions.append(new_cherry)
                            break
            else:
                for _ in eaten_cherries:
                    while True:
                        foodx = random.randrange(0, dis_width - snake_block, snake_block)
                        foody = random.randrange(0, dis_height - snake_block, snake_block)
                        new_cherry = [foodx, foody]
                        if new_cherry not in food_positions and new_cherry not in snake_List:
                            food_positions.append(new_cherry)
                            break

        clock.tick(snake_speed)

def display_snake_score(score):
    """
    Display the Snake score in the center of the screen.
    """
    score_surf = score_font.render(str(score), True, white)
    score_surf.set_alpha(50)
    score_rect = score_surf.get_rect(center=(dis_width // 2, dis_height // 2))
    dis.blit(score_surf, score_rect)

# ---------------------- Pong Game Functions ----------------------

def pong_menu():
    """
    Display the Pong game menu with Start, Options, and Back buttons.
    """
    global pong_difficulty, score_limit
    while True:
        dis.fill(black)
        message("Pong Game", white, -200)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_action = draw_button("Start", 250, 150, 300, 50, white, white, 'start_pong', events)
        difficulty_action = draw_button("Difficulty", 250, 220, 300, 50, white, white, 'pong_options_menu', events)
        score_limit_action = draw_button("Score Limit", 250, 290, 300, 50, white, white, 'pong_score_limit_menu', events)
        back_action = draw_button("Back", 250, 360, 300, 50, white, white, 'back_to_arcade', events)
        pygame.display.update()

        if start_action == 'start_pong':
            pong_game()
        elif difficulty_action == 'pong_options_menu':
            pong_options_menu()
        elif score_limit_action == 'pong_score_limit_menu':
            pong_score_limit_menu()
        elif back_action == 'back_to_arcade':
            arcade_menu()

        clock.tick(60)

def pong_options_menu():
    """
    The options menu for the Pong game, allowing selection of difficulty.
    """
    global pong_difficulty
    while True:
        dis.fill(black)
        message("Pong Difficulty", white, -200)
        message(f"Current difficulty: {pong_difficulty}", white, -150)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        easy_action = draw_button("Easy", 150, 200, 200, 50, white, white, lambda: set_pong_difficulty('Easy'), events)
        medium_action = draw_button("Medium", 450, 200, 200, 50, white, white, lambda: set_pong_difficulty('Medium'), events)
        hard_action = draw_button("Hard", 300, 270, 200, 50, white, white, lambda: set_pong_difficulty('Hard'), events)
        back_action = draw_button("Back", 250, 340, 300, 50, white, white, 'back_to_pong_menu', events)
        pygame.display.update()

        if callable(easy_action):
            easy_action()
        if callable(medium_action):
            medium_action()
        if callable(hard_action):
            hard_action()
        if back_action == 'back_to_pong_menu':
            pong_menu()

        clock.tick(60)

def pong_score_limit_menu():
    """
    The score limit menu for the Pong game.
    """
    global score_limit
    while True:
        dis.fill(black)
        message("Pong Score Limit", white, -200)
        message(f"Current score limit: {score_limit}", white, -150)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        limit_3_action = draw_button("3 Points", 150, 200, 200, 50, white, white, lambda: set_score_limit(3), events)
        limit_5_action = draw_button("5 Points", 450, 200, 200, 50, white, white, lambda: set_score_limit(5), events)
        limit_7_action = draw_button("7 Points", 150, 270, 200, 50, white, white, lambda: set_score_limit(7), events)
        limit_10_action = draw_button("10 Points", 450, 270, 200, 50, white, white, lambda: set_score_limit(10), events)
        back_action = draw_button("Back", 250, 340, 300, 50, white, white, 'back_to_pong_menu', events)
        pygame.display.update()

        if callable(limit_3_action):
            limit_3_action()
        if callable(limit_5_action):
            limit_5_action()
        if callable(limit_7_action):
            limit_7_action()
        if callable(limit_10_action):
            limit_10_action()
        if back_action == 'back_to_pong_menu':
            pong_menu()

        clock.tick(60)

def set_pong_difficulty(level):
    """
    Set the difficulty level for Pong.
    """
    global pong_difficulty
    pong_difficulty = level

def set_score_limit(limit):
    """
    Set the score limit for Pong.
    """
    global score_limit
    score_limit = limit

def pong_game():
    """
    The main game loop for Pong.
    """
    # Initialize positions
    paddle_width = 10
    paddle_height = 100
    ball_radius = 10

    # Set paddle speeds and AI settings based on difficulty
    if pong_difficulty == 'Easy':
        player_paddle_speed = 7
        ai_paddle_speed = 4
        ai_error_margin = 30
        speed_increment = 0.05
    elif pong_difficulty == 'Medium':
        player_paddle_speed = 7
        ai_paddle_speed = 5
        ai_error_margin = 20
        speed_increment = 0.1
    else:  # Hard
        player_paddle_speed = 7
        ai_paddle_speed = 6
        ai_error_margin = 10
        speed_increment = 0.15

    ball_speed_x = 5
    ball_speed_y = 5

    paddle1_y = dis_height // 2 - paddle_height // 2
    paddle2_y = dis_height // 2 - paddle_height // 2
    ball_x = dis_width // 2
    ball_y = dis_height // 2
    ball_dir_x = random.choice([-ball_speed_x, ball_speed_x])
    ball_dir_y = random.choice([-ball_speed_y, ball_speed_y])

    player_score = 0
    ai_score = 0

    game_over = False
    paused = False  # Pause flag

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Pause the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

        while paused:
            dis.fill(black)
            message("Paused", white, -50)
            message("Press 'B' for Main Menu", white, 0)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        pong_menu()

        # Get keys pressed
        keys = pygame.key.get_pressed()
        # Move player's paddle (W/S or Up/Down keys)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            paddle1_y -= player_paddle_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            paddle1_y += player_paddle_speed

        # Keep paddle on screen
        if paddle1_y < 0:
            paddle1_y = 0
        if paddle1_y > dis_height - paddle_height:
            paddle1_y = dis_height - paddle_height

        # AI paddle movement
        # AI tries to follow the ball but with some error margin based on difficulty
        if ball_dir_x > 0:  # Only move when ball is heading towards AI
            if paddle2_y + paddle_height / 2 < ball_y - ai_error_margin:
                paddle2_y += ai_paddle_speed
            elif paddle2_y + paddle_height / 2 > ball_y + ai_error_margin:
                paddle2_y -= ai_paddle_speed

        # Keep AI paddle on screen
        if paddle2_y < 0:
            paddle2_y = 0
        if paddle2_y > dis_height - paddle_height:
            paddle2_y = dis_height - paddle_height

        # Update ball position
        ball_x += ball_dir_x
        ball_y += ball_dir_y

        # Collision with top and bottom
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= dis_height:
            ball_dir_y = -ball_dir_y

        # Collision with paddles
        if (ball_x - ball_radius <= paddle_width and
            paddle1_y <= ball_y <= paddle1_y + paddle_height):
            ball_dir_x = -ball_dir_x
            # Increase ball speed
            ball_dir_x *= 1 + speed_increment
            ball_dir_y *= 1 + speed_increment
        elif (ball_x + ball_radius >= dis_width - paddle_width and
              paddle2_y <= ball_y <= paddle2_y + paddle_height):
            ball_dir_x = -ball_dir_x
            # Increase ball speed
            ball_dir_x *= 1 + speed_increment
            ball_dir_y *= 1 + speed_increment

        # Scoring
        if ball_x - ball_radius <= 0:
            ai_score += 1
            # Check for score limit
            if ai_score >= score_limit:
                game_over = True
                winner = 'AI'
            else:
                # Reset ball
                ball_x = dis_width // 2
                ball_y = dis_height // 2
                ball_speed_x = 5
                ball_speed_y = 5
                ball_dir_x = ball_speed_x
                ball_dir_y = random.choice([-ball_speed_y, ball_speed_y])
        elif ball_x + ball_radius >= dis_width:
            player_score += 1
            # Check for score limit
            if player_score >= score_limit:
                game_over = True
                winner = 'Player'
            else:
                # Reset ball
                ball_x = dis_width // 2
                ball_y = dis_height // 2
                ball_speed_x = 5
                ball_speed_y = 5
                ball_dir_x = -ball_speed_x
                ball_dir_y = random.choice([-ball_speed_y, ball_speed_y])

        # Fill the screen
        dis.fill(black)

        # Draw paddles
        pygame.draw.rect(dis, white, (0, paddle1_y, paddle_width, paddle_height))
        pygame.draw.rect(dis, white, (dis_width - paddle_width, paddle2_y, paddle_width, paddle_height))

        # Draw ball
        pygame.draw.circle(dis, white, (int(ball_x), int(ball_y)), ball_radius)

        # Display scores
        display_pong_score(player_score, ai_score)

        # Update display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

    # Game over, display winner
    pong_game_over(winner)

def display_pong_score(player_score, ai_score):
    """
    Display the Pong scores in the center of the screen.
    """
    score_text = f"{player_score}  {ai_score}"
    score_surf = score_font.render(score_text, True, white)
    score_surf.set_alpha(50)
    score_rect = score_surf.get_rect(center=(dis_width // 2, dis_height // 2))
    dis.blit(score_surf, score_rect)

def pong_game_over(winner):
    """
    Display the game over screen for Pong.
    """
    while True:
        dis.fill(black)
        message(f"{winner} Wins!", white, -50)
        message("Press P-Play Again or B-Back", white, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pong_game()
                elif event.key == pygame.K_b:
                    pong_menu()

        clock.tick(60)

# ---------------------- Asteroids Game Functions ----------------------

def asteroids_menu():
    """
    Display the Asteroids game menu with Start and Back buttons.
    """
    while True:
        dis.fill(black)
        message("Asteroids Game", white, -200)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_action = draw_button("Start", 250, 200, 300, 50, white, white, 'start_asteroids', events)
        back_action = draw_button("Back", 250, 270, 300, 50, white, white, 'back_to_arcade', events)
        pygame.display.update()

        if start_action == 'start_asteroids':
            asteroids_game()
        elif back_action == 'back_to_arcade':
            arcade_menu()

        clock.tick(60)

def asteroids_game():
    """
    The main game loop for Asteroids.
    """
    # Define ship properties
    ship_size = 15
    ship_x = dis_width / 2
    ship_y = dis_height / 2
    ship_angle = 0  # In degrees
    ship_dx = 0
    ship_dy = 0
    ship_max_speed = 5
    acceleration = 0.1
    friction = 0.99  # Simulate friction in space
    bullets = []
    bullet_speed = 7
    bullet_lifetime = 60  # Frames
    asteroids = []
    num_asteroids = 5
    asteroid_min_size = 20
    asteroid_max_size = 50
    asteroid_speed_range = [1, 3]
    score = 0
    paused = False  # Pause flag

    def create_asteroid():
        """
        Create a new asteroid with random properties.
        """
        size = random.uniform(30, 50)
        x = random.uniform(0, dis_width)
        y = random.uniform(0, dis_height)
        dx = random.uniform(-2, 2)
        dy = random.uniform(-2, 2)
        angle = random.uniform(0, 360)
        points = generate_asteroid_shape(size, angle)
        return {'x': x, 'y': y, 'size': size, 'dx': dx, 'dy': dy, 'points': points, 'angle': angle}

    def generate_asteroid_shape(size, angle):
        """
        Generate a random polygon shape for the asteroid.
        """
        points = []
        for i in range(7):
            theta = math.radians(i * (360 / 7) + random.uniform(-10, 10))
            r = size * random.uniform(0.8, 1.2)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append((x, y))
        return points

    def rotate_point(x, y, angle):
        """
        Rotate a point around the origin by angle degrees.
        """
        rad = math.radians(angle)
        cos_theta = math.cos(rad)
        sin_theta = math.sin(rad)
        x_new = x * cos_theta - y * sin_theta
        y_new = x * sin_theta + y * cos_theta
        return x_new, y_new

    def draw_ship(x, y, angle):
        """
        Draw the spaceship at given position and angle.
        """
        # Create a triangle shape for the ship
        angle_rad = math.radians(angle)
        nose_x = x + ship_size * math.cos(angle_rad)
        nose_y = y - ship_size * math.sin(angle_rad)
        left_x = x + ship_size * math.cos(angle_rad + 135 * math.pi / 180)
        left_y = y - ship_size * math.sin(angle_rad + 135 * math.pi / 180)
        right_x = x + ship_size * math.cos(angle_rad - 135 * math.pi / 180)
        right_y = y - ship_size * math.sin(angle_rad - 135 * math.pi / 180)
        pygame.draw.polygon(dis, white, [(nose_x, nose_y), (left_x, left_y), (right_x, right_y)], 1)
        return [(nose_x, nose_y), (left_x, left_y), (right_x, right_y)]

    def asteroids_game_over(score):
        """
        Display the game over screen for Asteroids.
        """
        while True:
            dis.fill(black)
            message("Game Over!", white, -50)
            message(f"Score: {score}", white, 0)
            message("Press P-Play Again or B-Back", white, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        asteroids_game()
                    elif event.key == pygame.K_b:
                        asteroids_menu()

            clock.tick(60)

    # Generate initial asteroids
    for _ in range(num_asteroids):
        asteroid = create_asteroid()
        asteroids.append(asteroid)

    game_over = False

    # Generate stars for the background
    num_stars = 100  # Adjust the number of stars as desired
    stars = []
    for _ in range(num_stars):
        star_x = random.randint(0, dis_width - 1)
        star_y = random.randint(0, dis_height - 1)
        # Random brightness for twinkling effect
        brightness = random.randint(100, 255)
        stars.append({'x': star_x, 'y': star_y, 'brightness': brightness})

    while not game_over:
        dis.fill(black)
        # Draw and update stars
        for star in stars:
            # Slightly change brightness for twinkling effect
            star['brightness'] += random.randint(-10, 10)
            # Clamp brightness between 100 and 255
            star['brightness'] = max(100, min(255, star['brightness']))
            star_color = (star['brightness'], star['brightness'], star['brightness'])
            dis.set_at((star['x'], star['y']), star_color)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Pause the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

        while paused:
            dis.fill(black)
            message("Paused", white, -50)
            message("Press 'B' for Main Menu", white, 0)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        asteroids_menu()

        # Get keys pressed
        keys = pygame.key.get_pressed()
        # Rotate ship
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship_angle += 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship_angle -= 5
        # Accelerate ship
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ship_dx += acceleration * math.cos(math.radians(ship_angle))
            ship_dy -= acceleration * math.sin(math.radians(ship_angle))
            # Limit speed
            speed = math.hypot(ship_dx, ship_dy)
            if speed > ship_max_speed:
                scale = ship_max_speed / speed
                ship_dx *= scale
                ship_dy *= scale
        else:
            ship_dx *= friction
            ship_dy *= friction
        # Fire bullets
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullet = {
                    'x': ship_x,
                    'y': ship_y,
                    'dx': bullet_speed * math.cos(math.radians(ship_angle)),
                    'dy': -bullet_speed * math.sin(math.radians(ship_angle)),
                    'lifetime': bullet_lifetime
                }
                bullets.append(bullet)

        # Update ship position
        ship_x += ship_dx
        ship_y += ship_dy

        # Screen wrapping
        ship_x %= dis_width
        ship_y %= dis_height

        # Update bullets
        for bullet in bullets[:]:
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            bullet['lifetime'] -= 1
            bullet['x'] %= dis_width
            bullet['y'] %= dis_height
            if bullet['lifetime'] <= 0:
                bullets.remove(bullet)

        # Update asteroids
        for asteroid in asteroids:
            asteroid['x'] += asteroid['dx']
            asteroid['y'] += asteroid['dy']
            asteroid['angle'] += 1  # Rotate asteroid
            asteroid['x'] %= dis_width
            asteroid['y'] %= dis_height

        # Draw asteroids
        for asteroid in asteroids:
            asteroid_shape = []
            for point in asteroid['points']:
                rotated_point = rotate_point(point[0], point[1], asteroid['angle'])
                x = asteroid['x'] + rotated_point[0]
                y = asteroid['y'] + rotated_point[1]
                asteroid_shape.append((x, y))
            pygame.draw.polygon(dis, white, asteroid_shape, 1)

        # Check for collisions between bullets and asteroids
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                dist = math.hypot(bullet['x'] - asteroid['x'], bullet['y'] - asteroid['y'])
                if dist < asteroid['size']:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10
                    # Split asteroid into smaller ones
                    if asteroid['size'] > asteroid_min_size:
                        for _ in range(2):
                            new_size = asteroid['size'] / 2
                            new_asteroid = {
                                'x': asteroid['x'],
                                'y': asteroid['y'],
                                'size': new_size,
                                'dx': random.uniform(-3, 3),
                                'dy': random.uniform(-3, 3),
                                'angle': random.uniform(0, 360),
                                'points': generate_asteroid_shape(new_size, asteroid['angle'])
                            }
                            asteroids.append(new_asteroid)
                    else:
                        # Chance to spawn a new asteroid when the smallest is destroyed
                        if random.random() < 0.5:  # 50% chance to spawn a new asteroid
                            new_asteroid = create_asteroid()
                            asteroids.append(new_asteroid)
                    break

        # Draw ship
        ship_shape = draw_ship(ship_x, ship_y, ship_angle)

        # Check for collisions between ship and asteroids
        for asteroid in asteroids:
            asteroid_shape = []
            for point in asteroid['points']:
                rotated_point = rotate_point(point[0], point[1], asteroid['angle'])
                x = asteroid['x'] + rotated_point[0]
                y = asteroid['y'] + rotated_point[1]
                asteroid_shape.append((x, y))
            if polygon_collision(ship_shape, asteroid_shape):
                game_over = True
                break

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(dis, white, (int(bullet['x']), int(bullet['y'])), 2)

        # Display score
        score_surf = font_style.render(f"Score: {score}", True, white)
        dis.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    asteroids_game_over(score)

def polygon_collision(poly1, poly2):
    """
    Check if two polygons (lists of points) are colliding using the Separating Axis Theorem.
    """
    for polygon in [poly1, poly2]:
        for i1 in range(len(polygon)):
            i2 = (i1 + 1) % len(polygon)
            p1 = polygon[i1]
            p2 = polygon[i2]

            normal = (p2[1] - p1[1], p1[0] - p2[0])

            minA, maxA = None, None
            for p in poly1:
                projected = normal[0] * p[0] + normal[1] * p[1]
                if minA is None or projected < minA:
                    minA = projected
                if maxA is None or projected > maxA:
                    maxA = projected

            minB, maxB = None, None
            for p in poly2:
                projected = normal[0] * p[0] + normal[1] * p[1]
                if minB is None or projected < minB:
                    minB = projected
                if maxB is None or projected > maxB:
                    maxB = projected

            if maxA < minB or maxB < minA:
                return False  # No collision
    return True  # Collision detected

# ---------------------- Space Invaders Game Functions ----------------------

def space_invaders_menu():
    """
    Display the Space Invaders game menu with Start and Back buttons.
    """
    while True:
        dis.fill(black)
        message("Space Invaders", white, -200)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        start_action = draw_button("Start", 250, 200, 300, 50, white, white, 'start_space_invaders', events)
        back_action = draw_button("Back", 250, 270, 300, 50, white, white, 'back_to_arcade', events)
        pygame.display.update()

        if start_action == 'start_space_invaders':
            space_invaders_game()
        elif back_action == 'back_to_arcade':
            arcade_menu()

        clock.tick(60)

def space_invaders_game():
    """
    The main game loop for Space Invaders.
    All related functions are encapsulated within this function.
    """
    # Helper function for game over screen
    def space_invaders_game_over(score):
        """
        Display the game over screen for Space Invaders.
        """
        while True:
            dis.fill(black)
            message("Game Over!", white, -50)
            message(f"Score: {score}", white, 0)
            message("Press P-Play Again or B-Back", white, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        space_invaders_game()  # Restart the game
                        return
                    elif event.key == pygame.K_b:
                        space_invaders_menu()  # Return to the game's main menu
                        return

            clock.tick(60)

    # Game settings
    player_speed = 5
    bullet_speed = -7
    enemy_speed = 1
    enemy_drop = 10
    enemy_bullet_speed = 5
    player_lives = 3
    score = 0
    paused = False  # Pause flag
    player_hit_timer = 0  # Timer for player hit effect

    # Initialize player
    player_width = 40
    player_height = 20
    player_x = dis_width / 2 - player_width / 2
    player_y = dis_height - player_height - 10
    player_bullets = []

    # Initialize bunkers
    bunker_width = 60
    bunker_height = 40
    bunkers = []
    bunker_count = 4
    for i in range(bunker_count):
        bunker_x = (dis_width / (bunker_count + 1)) * (i + 1) - bunker_width / 2
        bunker_y = dis_height - player_height - bunker_height - 30
        # Create a surface for the bunker
        bunker_surface = pygame.Surface((bunker_width, bunker_height))
        bunker_surface.fill(white)
        bunkers.append({'x': bunker_x, 'y': bunker_y, 'surface': bunker_surface})

    # Initialize enemies
    enemy_rows = 5
    enemy_cols = 11
    enemy_width = 30
    enemy_height = 20
    enemies = []
    direction = 1  # 1 for right, -1 for left

    # Enemy shapes (simple representations of original sprites)
    enemy_shapes = [
        # Bottom two rows (small alien)
        [(0, 0), (enemy_width, 0), (enemy_width, enemy_height), (0, enemy_height)],
        # Middle two rows (medium alien)
        [(0, 0), (enemy_width, 0), (enemy_width, enemy_height), (0, enemy_height)],
        # Top row (large alien)
        [(0, 0), (enemy_width, 0), (enemy_width, enemy_height), (0, enemy_height)],
    ]

    # Create enemy formation
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            enemy_x = col * (enemy_width + 10) + 50
            enemy_y = row * (enemy_height + 10) + 50
            # Select shape based on row
            if row < 1:
                shape = enemy_shapes[2]  # Top row (large alien)
            elif row < 3:
                shape = enemy_shapes[1]  # Middle rows (medium alien)
            else:
                shape = enemy_shapes[0]  # Bottom rows (small alien)
            enemies.append({'x': enemy_x, 'y': enemy_y, 'alive': True, 'shape': shape})

    enemy_bullets = []

    # Main game loop
    game_over = False

    while not game_over:
        dis.fill(black)

        # Event handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

        # Pause handling
        while paused:
            dis.fill(black)
            message("Paused", white, -50)
            message("Press 'P' to Resume or 'B' for Main Menu", white, 0)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_b:
                        space_invaders_menu()  # Return to the game's main menu
                        return

        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
            if player_x < 0:
                player_x = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
            if player_x > dis_width - player_width:
                player_x = dis_width - player_width
        if keys[pygame.K_SPACE]:
            if len(player_bullets) < 3:
                bullet_x = player_x + player_width / 2
                bullet_y = player_y
                player_bullets.append({'x': bullet_x, 'y': bullet_y})

        # Update player bullets
        for bullet in player_bullets[:]:
            bullet['y'] += bullet_speed
            if bullet['y'] < 0:
                player_bullets.remove(bullet)

        # Update enemies
        move_down = False
        for enemy in enemies:
            if enemy['alive']:
                enemy['x'] += enemy_speed * direction
                if enemy['x'] > dis_width - enemy_width or enemy['x'] < 0:
                    move_down = True

        if move_down:
            direction *= -1
            for enemy in enemies:
                enemy['y'] += enemy_drop

        # Enemy shooting
        if random.randint(0, 100) < 3:
            alive_enemies = [e for e in enemies if e['alive']]
            if alive_enemies:
                shooting_enemy = random.choice(alive_enemies)
                enemy_bullets.append({
                    'x': shooting_enemy['x'] + enemy_width / 2,
                    'y': shooting_enemy['y'] + enemy_height
                })

        # Update enemy bullets
        for bullet in enemy_bullets[:]:
            bullet['y'] += enemy_bullet_speed
            if bullet['y'] > dis_height:
                enemy_bullets.remove(bullet)

        # Collision detection between player bullets and enemies
        for bullet in player_bullets[:]:
            for enemy in enemies:
                if enemy['alive']:
                    if (enemy['x'] < bullet['x'] < enemy['x'] + enemy_width and
                            enemy['y'] < bullet['y'] < enemy['y'] + enemy_height):
                        enemy['alive'] = False
                        player_bullets.remove(bullet)
                        score += 10
                        break

        # Collision detection between enemy bullets and player
        for bullet in enemy_bullets[:]:
            if (player_x < bullet['x'] < player_x + player_width and
                    player_y < bullet['y'] < player_y + player_height):
                enemy_bullets.remove(bullet)
                player_lives -= 1
                player_hit_timer = 30  # Set hit effect timer
                if player_lives == 0:
                    game_over = True
                break

        # Collision detection between enemies and player
        for enemy in enemies:
            if enemy['alive']:
                if (enemy['x'] < player_x + player_width and
                        enemy['x'] + enemy_width > player_x and
                        enemy['y'] + enemy_height > player_y):
                    game_over = True
                    break

        # Collision detection between enemy bullets and bunkers
        for bullet in enemy_bullets[:]:
            for bunker in bunkers:
                bunker_rect = pygame.Rect(bunker['x'], bunker['y'], bunker_width, bunker_height)
                if bunker_rect.collidepoint(bullet['x'], bullet['y']):
                    # Remove part of the bunker where it was hit
                    bx = int(bullet['x'] - bunker['x'])
                    by = int(bullet['y'] - bunker['y'])
                    pygame.draw.circle(bunker['surface'], black, (bx, by), 5)
                    enemy_bullets.remove(bullet)
                    break

        # Collision detection between player bullets and bunkers
        for bullet in player_bullets[:]:
            for bunker in bunkers:
                bunker_rect = pygame.Rect(bunker['x'], bunker['y'], bunker_width, bunker_height)
                if bunker_rect.collidepoint(bullet['x'], bullet['y']):
                    # Remove part of the bunker where it was hit
                    bx = int(bullet['x'] - bunker['x'])
                    by = int(bullet['y'] - bunker['y'])
                    pygame.draw.circle(bunker['surface'], black, (bx, by), 5)
                    player_bullets.remove(bullet)
                    break

        # Draw bunkers
        for bunker in bunkers:
            dis.blit(bunker['surface'], (bunker['x'], bunker['y']))

        # Draw player with hit effect
        if player_hit_timer > 0:
            if player_hit_timer % 10 < 5:
                # Flashing effect
                pygame.draw.rect(dis, white, (player_x, player_y, player_width, player_height))
                pygame.draw.rect(dis, white, (player_x + player_width / 2 - 5, player_y - 10, 10, 10))
            player_hit_timer -= 1
        else:
            pygame.draw.rect(dis, white, (player_x, player_y, player_width, player_height))
            # Draw turret (to resemble the traditional sprite)
            pygame.draw.rect(dis, white, (player_x + player_width / 2 - 5, player_y - 10, 10, 10))

        # Draw player bullets
        for bullet in player_bullets:
            pygame.draw.rect(dis, white, (bullet['x'], bullet['y'], 2, 10))

        # Draw enemies
        for enemy in enemies:
            if enemy['alive']:
                # Draw enemy shape
                points = []
                for point in enemy['shape']:
                    points.append((enemy['x'] + point[0], enemy['y'] + point[1]))
                pygame.draw.polygon(dis, white, points)

        # Draw enemy bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(dis, white, (bullet['x'], bullet['y'], 2, 10))

        # Display score and lives
        score_surf = font_style.render(f"Score: {score}", True, white)
        lives_surf = font_style.render(f"Lives: {player_lives}", True, white)
        dis.blit(score_surf, (10, 10))
        dis.blit(lives_surf, (dis_width - 100, 10))

        # Check if all enemies are defeated
        if all(not enemy['alive'] for enemy in enemies):
            game_over = True  # You can implement level progression here

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    space_invaders_game_over(score)

# Start the game by calling the arcade menu
arcade_menu()
