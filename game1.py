# Simple Snake Game in Python
import turtle
import time
import random

delay = 0.1
level = 1

# Score
score = 0
high_score = 0

# Food Randomizers
food_shapes = ["triangle", "circle", "square"]
food_colors = ["red", "crimson", "maroon", "dark red"]

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("aquamarine")
wn.setup(width=808, height=808)
wn.tracer(0) # Turns off the screen updates

# Set up the border
border_pen = turtle.Turtle()
border_pen.hideturtle()
border_pen.penup()
border_pen.pencolor("black")
border_pen.pensize(10)
border_pen.goto(-394, -393)
border_pen.pendown()
for _ in range(4):
    border_pen.forward(787)
    border_pen.left(90)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("dark green")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape(random.choice(food_shapes))
food.shapesize(stretch_wid=1.25, stretch_len=1.25)
food.color(random.choice(food_colors))
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("dark slate blue")
pen.penup()
pen.hideturtle()
pen.goto(0, 350)
pen.write("Score: 0 | High Score: 0 | Level: 1 | Segments: 0" , align="center", font=("Arial", 20, "bold"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>373 or head.xcor()<-373 or head.ycor()>373 or head.ycor()<-373:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1500, 1500)
        
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1
        
        # Reset level
        level = 1

        pen.clear()
        pen.write("Score: {} | High Score: {} | Level: {} | Segments: {}".format(score, high_score, level, len(segments)), align="center", font=("Arial", 20, "bold"))


    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-357, 357)
        y = random.randint(-357, 357)
        food.shape(random.choice(food_shapes))
        food.color(random.choice(food_colors))
        food.goto(x,y)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("circle")
        # Alternate in color for each segment
        if len(segments) % 2 == 0:  # even
            new_segment.color("olive drab")
        else:  # odd
            new_segment.color("chartreuse")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 12.5

        if score > high_score:
            high_score = score
        
        pen.clear()
        pen.write("Score: {} | High Score: {} | Level: {} | Segments: {}".format(score, high_score, level, len(segments)), align="center", font=("Arial", 20, "bold"))

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"
        
            # Hide the segments
            for segment in segments:
                segment.goto(1500, 1500)
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1
            
            # Reset the level
            level = 1
        
            # Update the score display
            pen.clear()
            pen.write("Score: {} | High Score: {} | Level: {} | Segments: {}".format(score, high_score, level, len(segments)), align="center", font=("Arial", 20, "bold"))

    # Levels
    next_level_score = level * 50
    if score >= next_level_score:
        level += 1      
        delay *= 0.999
        
    
    
    time.sleep(delay)

wn.mainloop()