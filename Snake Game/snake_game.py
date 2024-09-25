import turtle as t
import random

w = 620  # Width of box
h = 620  # Height of box
food_size = 20  # Size of food
delay = 100  # Delay in milliseconds

# Values by which the snake will move in a direction when given

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

global SCORE
SCORE = 0
prev_score = 0
snake_moving = False  # To prevent multiple quick key presses
retry_button_active = False  # Flag to track if retry button is shown

def reset():
    global snake, snake_dir, food_position, pen, snake_moving, game_over_text, retry_button_active, highScore

    # Reset the game elements
    snake = [[-10, -10], [-10, 10], [-10, 30]]
    snake_dir = "up"  # Default snake direction
    food_position = get_random_food_position()
    food.goto(food_position)  # Render food on the scene
    SCORE = 0
    pen.clearstamps()  # Clear previous snake stamps
    snake_moving = False  # Reset snake movement flag
    retry_button_active = False  # Reset retry button flag

    
    # Hide the game over text and retry button
    highScore.clear()
    game_over_text.clear()
    retry_button.clear()

    # Start the game loop again
    move_snake()


def move_snake():
    global snake_dir, SCORE, snake_moving, game_over_text, retry_button_active, highScore,prev_score

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_dir][0]
    new_head[1] += offsets[snake_dir][1]

    # Check for collision with itself
    if new_head in snake[:-1]:
        # Display the game over screen
        game_over_text.write(f"Game Over! Final Score: {SCORE}", align="center", font=("Arial", 24, "bold"))
        prev_score = max(prev_score, SCORE)
        highScore.write(f" Highscore: {prev_score}", align="center", font=("Courier", 20, "bold"))
        retry_button.write("Click to Retry", align="center", font=("Arial", 18, "bold"))
        retry_button_active = True  # Enable retry button
        return
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)

        # Boundary checks to wrap the snake
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < -w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h

        pen.clearstamps()

        pen.color("#142224")
        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()
        snake_moving = False  # Allow next keypress after snake movement
        t.ontimer(move_snake, delay)


def retry(x, y):
    global SCORE
    if retry_button_active and -80 < x < 80 and -80 < y < -20:
        SCORE = 0  # Check if the click is inside the retry button
        reset()  # Reset the game


def food_collision():
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False


def get_random_food_position():
    lst = [-290, -270, -250, -230, -210, -190, -170, -150, -130, -110, -90, -70, -50, -30, -10, 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290]
    x = random.choice(lst)
    y = random.choice(lst)

    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


# Control functions to change snake direction
def go_up():
    global snake_dir, snake_moving
    if snake_dir != "down" and not snake_moving:
        snake_dir = "up"
        snake_moving = True


def go_down():
    global snake_dir, snake_moving
    if snake_dir != "up" and not snake_moving:
        snake_dir = "down"
        snake_moving = True


def go_left():
    global snake_dir, snake_moving
    if snake_dir != "right" and not snake_moving:
        snake_dir = "left"
        snake_moving = True


def go_right():
    global snake_dir, snake_moving
    if snake_dir != "left" and not snake_moving:
        snake_dir = "right"
        snake_moving = True


# Define screen setup
screen = t.Screen()
screen.setup(w, h)
screen.title("Snake Game")
screen.bgcolor("green")
screen.tracer(0)

# Define snake setup
pen = t.Turtle("square")
pen.penup()

# Define food setup
food = t.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

# Define game over text and retry button
game_over_text = t.Turtle()
game_over_text.hideturtle()
game_over_text.color("white")
game_over_text.penup()
game_over_text.goto(0, 50)

# Define highscore

highScore = t.Turtle()
highScore.hideturtle()
highScore.color("#fff")
highScore.penup()
highScore.goto(0, 10)

retry_button = t.Turtle()
retry_button.hideturtle()
retry_button.shape("square")
retry_button.color("yellow")
retry_button.shapesize(2, 8)
retry_button.penup()
retry_button.goto(0, -50)

# Define control setup
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

# Set up click handler for retry button
screen.onclick(retry)

reset()
t.done()
