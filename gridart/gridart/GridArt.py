import pygame
import button
import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

#fps limiter
clock = pygame.time.Clock()
fps = 60

#window screen
screen_width = 800
screen_height = 640
lower_margin = 100
side_margin = 300

screen = pygame.display.set_mode((screen_width + side_margin, screen_height + lower_margin))
pygame.display.set_caption('Map Maker')

#var
rows = 16
max_cols = 150
grid_size = screen_height // rows
tile_types = 15 #number changes based on number of assets
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#load images
sky_bg = pygame.image.load('sky.png').convert_alpha()
grass_bg = pygame.image.load('background.png').convert_alpha()
tile_list = []
for x in range(tile_types):
    tile = pygame.image.load(f'{x}.png').convert_alpha() #f = formatting
    tile = pygame.transform.scale(tile,(grid_size, grid_size))
    tile_list.append(tile)

save_btn = pygame.image.load('save.png').convert_alpha()
load_btn = pygame.image.load('load.png').convert_alpha()

#colors
green = (144, 201, 120)
white = (255, 255, 255)
red = (255, 30, 30)
grey = (80, 80, 80)
black = (0, 0, 0)

#font
font = pygame.font.SysFont('Comic Sans', 20)

#empty tile list
world_data = []
for row in range(rows):
    r = [-1] * max_cols
    world_data.append(r)

#create ground
for tile in range(0, max_cols):
    world_data[rows - 1][tile] = 0


#draw function for bg
def draw_bg():
    screen.fill(green) #background base color
    width = grass_bg.get_width()
    for x in range(5):
        #use for multiple bg layers; -scroll is used so bg will move left if right input and vice versa
        screen.blit(grass_bg, ((x * width) - scroll, screen_height - grass_bg.get_height() + 100))

#draw grid
def draw_grid():
    #vertical
    for x in range(max_cols + 1):
        pygame.draw.line(screen, black, (x * grid_size - scroll, 0), (x * grid_size - scroll, screen_height))
    #horizontal
    for x in range(rows + 1):
        pygame.draw.line(screen, black, (0, x * grid_size), (screen_width, x * grid_size))

#draw base tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_list[tile], (x * grid_size - scroll, y * grid_size))

#text
def draw_text(text, font, text_col, x, y):
    pic = font.render(text, True, text_col)
    screen.blit(pic, (x, y))

#buttons
save_button = button.Button(screen_width // 2 + 580, screen_height + lower_margin - 85, save_btn, 1)
load_button = button.Button(screen_width // 2 + 580, screen_height + lower_margin - 40, load_btn, 1)
button_list = []
button_col = 0
button_row = 0
for i in range(len(tile_list)):
    tile_button = button.Button(screen_width + (75 * button_col) + 50, 75 * button_row + 50, tile_list[i], 1) #setup class
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

#game loop
run = True
while run:

    #implement limiter
    clock.tick(fps)

    #draw layout
    draw_bg()
    draw_grid()
    draw_world()

    #draw text
    draw_text(f'Save State: {level}', font, black, 825, screen_height + lower_margin - 40)
    draw_text('UP / DOWN = change save state', font, black, 10, screen_height + lower_margin - 100)
    draw_text('LEFT / RIGHT = move the screen', font, black, 10, screen_height + lower_margin - 70)
    draw_text('LEFT CLIK = add color', font, black, 400, screen_height + lower_margin - 100)
    draw_text('RIGHT CLICK = remove color', font, black, 400, screen_height + lower_margin - 70)
    draw_text('Hold L.SHIFT = move faster', font, black, 10, screen_height + lower_margin - 40)

    #save/load data
    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',') #delimiter = to separate the values
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',') #delimiter = to separate the values
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

                
    
    #draw panel and tiles
    pygame.draw.rect(screen, grey, (screen_width, 0, side_margin, screen_height))
    #choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    #highlight selected tile
    pygame.draw.rect(screen, red, button_list[current_tile].rect, 3)


    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed #move to left
    if scroll_right == True and scroll < (max_cols * grid_size) - screen_width:
        scroll += 5 * scroll_speed #move to right

    #add tiles
    #mouse movement
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // grid_size
    y = pos[1] // grid_size
    #detect mouse position
    if pos[0] < screen_width and pos[1] < screen_height:
        #add tile
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        #remove tile
        if pygame.mouse.get_pressed()[2] == 1: #0 is left click, 1 is middle mouse, 2 is right click
            world_data[y][x] = -1

    for event in pygame.event.get():

        #detect keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 3

        #detect  no keyboard input
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

        #update screen
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()