import turtle
import random
import time

#   Slowing down problem, and enemy bullet eventually out of range

# List of assets
player_fired_bullets = []
enemy_fired_bullets = []
cur_enemies = []
cur_asteroids = []

# Window Setup
wn = turtle.Screen()
wn.height = 600
wn.width = 700
wn.upper_bound = wn.height / 2
wn.lower_bound = wn.height / -2
wn.right_bound = wn.width / 2
wn.left_bound = wn.width / -2
wn.setup(width=wn.width, height=wn.height)
wn.bgcolor("black")
wn.title("Space Rogue by @snolink")
wn.tracer(0)

# Custom Shapes
tri_player = turtle.Shape("compound")
tri_player.vertices = ((5,0),(0,10),(-5,0))
tri_player.addcomponent(tri_player.vertices, fill="black", outline="#04d9ff")
turtle.addshape("tri_player", shape=tri_player)

tri_enemy = turtle.Shape("compound")
tri_enemy.vertices = ((5,0),(0,10),(-5,0))
tri_enemy.addcomponent(tri_enemy.vertices, fill="black", outline="#E10600")
turtle.addshape("tri_enemy", shape=tri_enemy)

line = turtle.Shape("compound")
line.vertices = ((0,10), (0,0))
line.addcomponent(line.vertices, fill="white", outline="white")
turtle.addshape("line", shape=line)

sq_asteroid = turtle.Shape("compound")
sq_asteroid.vertices = ((0,10), (-10,10), (-10,0), (0,0))
sq_asteroid.addcomponent(sq_asteroid.vertices, fill="black", outline="white")
turtle.addshape("asteroid", shape=sq_asteroid)

# Spaceship/Player
spaceship = turtle.Turtle()
spaceship.shape("tri_player")
spaceship.pu()
spaceship.goto(0,0)
spaceship.setheading(90)
#spaceship.shapesize(stretch_wid=1, stretch_len=1, outline=2)
spaceship.turn_speed = 8
spaceship.forward_speed = 1
spaceship.speed(0)

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.score = 0
scoreboard.speed(0)
scoreboard.color("#63666A")
scoreboard.pu()
scoreboard.ht()
scoreboard.goto(0,0)
scoreboard.write(arg=scoreboard.score, align="center", font=("courier new", 30, "normal"))

def spawn_enemy():
    enemy = turtle.Turtle()
    enemy.shape("tri_enemy")
    enemy.pu()
    set_loc(enemy)
    cur_enemies.append(enemy)

def spawn_asteroid():
    asteroid = turtle.Turtle()
    asteroid.shape("asteroid")
    asteroid.pu()
    set_loc(asteroid)
    cur_asteroids.append(asteroid)
     
def set_loc(r):
    spawn_loc = random.choice(["N", "E", "W", "S"])
    if spawn_loc == "N":
        x, y = random.randint(wn.left_bound, wn.right_bound), wn.upper_bound + 20
        head_dir = random.randint(180, 360)
        
    elif spawn_loc == "E":
        x, y = wn.right_bound + 20, random.randint(wn.lower_bound, wn.upper_bound)
        head_dir = random.randint(90, 270)
        
    elif spawn_loc == "W":
        x, y = wn.left_bound - 20, random.randint(wn.lower_bound, wn.upper_bound)
        head_dir = random.randint(-90, 90)
        
    else:
        x, y = random.randint(wn.left_bound, wn.right_bound), wn.lower_bound - 20
        head_dir = random.randint(0, 180)
        
    r.goto(x, y)
    r.setheading(head_dir)

# Controls
def turn_right():
    spaceship.rt(spaceship.turn_speed)

def turn_left():
    spaceship.lt(spaceship.turn_speed)  

def inc_forward():
    if spaceship.forward_speed <= 3:
        spaceship.forward_speed += 1

def dec_forward():
    if spaceship.forward_speed > 1:
        spaceship.forward_speed -= 1
    
def fire_bullet():
    if len(player_fired_bullets) < 3:
        bullet = turtle.Turtle()
        bullet.shape("line")
        bullet.goto(spaceship.pos())
        bullet.setheading(spaceship.heading())
        player_fired_bullets.append(bullet)
    
wn.listen()
wn.onkeypress(turn_right, "d")
wn.onkeypress(turn_left, "a")
wn.onkeypress(inc_forward, "w")
wn.onkeypress(dec_forward, "s")
wn.onkeypress(fire_bullet, "space")

def reset_game():
    time.sleep(1)
    scoreboard.score = 0
    scoreboard.clear()
    scoreboard.write(arg=scoreboard.score, align="center", font=("courier new", 30, "normal"))
    spaceship.goto(0,0)
    spaceship.setheading(90)
    for asteroid in cur_asteroids:
        asteroid.ht()
    cur_asteroids.clear()
    for enemy in cur_enemies:
        enemy.ht()
    cur_enemies.clear()

while True:
    wn.update()
    
    # Tp player to the opposite side once edge is reached
    if spaceship.xcor() >= wn.right_bound or spaceship.xcor() <= wn.left_bound:
        spaceship.goto(spaceship.xcor() * -1, spaceship.ycor())
    if spaceship.ycor() >= wn.upper_bound or spaceship.ycor() <= wn.lower_bound:
        spaceship.goto(spaceship.xcor(), spaceship.ycor() * -1)
    spaceship.fd(spaceship.forward_speed)
    
    # Delete out of frame player bullets
    for i, bullet in enumerate(player_fired_bullets[:]):
        bullet.fd(spaceship.turn_speed)
        if bullet.xcor() > wn.right_bound or bullet.xcor() < wn.left_bound or bullet.ycor() > wn.upper_bound or bullet.ycor() < wn.lower_bound:
            player_fired_bullets[i].ht()
            del player_fired_bullets[i]
        
        # Bullet collides to asteroid
        for asteroid in cur_asteroids:
            if bullet.distance(asteroid) <= 20:
                set_loc(asteroid)
                player_fired_bullets[i].ht()
                del player_fired_bullets[i]
        
        for enemy in cur_enemies:
            if bullet.distance(enemy) <= 20:
                set_loc(enemy)
                scoreboard.score += 1
                scoreboard.clear()
                scoreboard.write(arg=scoreboard.score, align="center", font=("courier new", 30, "normal"))
                remove_player_bullets.append(bullet)
                player_fired_bullets[i].ht()
                del player_fired_bullets[i]
    remove_player_bullets = []
    for bullet in remove_player_bullets[:]:
        i = player_fired_bullets.index(bullet)
        player_fired_bullets[i].ht()
        del player_fired_bullets[i]
    # Spawn resources
    while len(cur_asteroids) < 10:
        spawn_asteroid()
        
    while len(cur_enemies) < 4:
        spawn_enemy()
        
    # Enemy controls
    for enemy in cur_enemies:
        enemy.fd(1.5)

        choice = random.randint(0, 10)
        while choice == 10 and len(enemy_fired_bullets) < 5:
            bullet = turtle.Turtle()
            bullet.shape("line")
            bullet.goto(enemy.pos())
            bullet.setheading(enemy.heading())
            enemy_fired_bullets.append(bullet)

        if enemy.xcor() > wn.right_bound+20 or enemy.xcor() < wn.left_bound-20 or enemy.ycor() > wn.upper_bound+20 or enemy.ycor() < wn.lower_bound-20:
            set_loc(enemy)
        
        if enemy.distance(spaceship) <= 15:
            reset_game()
    
    remove_enemy_bullets = []
    for i, bullet in enumerate(enemy_fired_bullets[:]):
        bullet.fd(spaceship.turn_speed)
        if bullet.xcor() > wn.right_bound+20 or bullet.xcor() < wn.left_bound-20 or bullet.ycor() > wn.upper_bound+20 or bullet.ycor() < wn.lower_bound-20:
            remove_enemy_bullets.append(bullet)
    
    for bullet in remove_enemy_bullets[:]:
        i = enemy_fired_bullets.index(bullet)
        enemy_fired_bullets[i].ht()
        del enemy_fired_bullets[i]
        
        if bullet.distance(spaceship) <= 15:
            reset_game()
    
    # Asteroid controls
    for asteroid in cur_asteroids:
        asteroid.fd(1)
        asteroid.tilt(2)
        if asteroid.xcor() > wn.right_bound+20 or asteroid.xcor() < wn.left_bound-20 or asteroid.ycor() > wn.upper_bound+20 or asteroid.ycor() < wn.lower_bound-20:
            set_loc(asteroid)
        
        if spaceship.distance(asteroid) <= 16:
            reset_game()
            
turtle.mainloop()