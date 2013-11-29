from random import randint
import os, sys, csv, pygame, eztext
from pygame.locals import *


#
# ------ I have been getting fatal python errors: segmentation fault randomly when running the game, I don't know why, I think it has something
# to do with my setup but if it happens  while you're testing the game,
# ------ Run the game again and it should be fine....I've ran the complete game many times and the error seems random ---------
#
#
#
#
#
#

# Things To Do:
# be able to create holes through barriers ( probably going to make each pixel an object and delete it with impact..this may effect frame rate however)(done)
# add in other aliens(part done...made a function that makes a row of aliens...should be easy to add in other aliens now)(done)
# add in animations for each alien(done)
# add death animations across the board(done)
# have the game actually have an end....endless space ship shooting is awesome but....(done)
# add more levels(done * needs animations)(done)
# add different score earned based on alien type(done)
# learn to animate a score screen...probably star field in the background...something easy(done)
# add in other ships at least three in all with different images and rates of fire and maybe special weapons :D(done...no specials)
# start screen ..get away from the terminal output (doneish..doesn't look pretty but it's functional)
# game over screen...right now it's kind of anti climactic...hopfully with a leader board :D
# add player lives....becaue i suck at space invaders (done)
# add stat recording probably saved in a csv file but maybe just a text document (bullets shot, time taken, aliens killed, etc...)(maybe)
# 
# creates the player
class player(pygame.sprite.Sprite):

	def __init__(self, name, ship, shields, movement, rate_of_fire):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
		self.image, self.rect = load_image(ship, [138,43,226])
		self.score = 0
		self.rect.y = 500
		self.lives = 3
		self.shields = shields
		self.movement = movement
		self.rof = rate_of_fire

	def move_left(self):
		if self.rect.x > 20:
			self.rect.x -= self.movement
	def move_right(self):
		if self.rect.x < 730:
			self.rect.x += self.movement
# makes some things that kill other things
class bullet(pygame.sprite.Sprite):
	def __init__(self, thing_shooting, entity):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([3,8])
		self.image.fill([255,255,255])
		self.rect = self.image.get_rect()
		if entity == 'alien':
			self.rect.x = thing_shooting.rect.centerx 
			self.rect.y = thing_shooting.rect.centery + thing_shooting.rect[3]/2
		elif entity =='player':
			self.rect.x = thing_shooting.rect.centerx 
			self.rect.y = thing_shooting.rect.centery - thing_shooting.rect[3]/2
	def update(self, direction ):
		if direction == 'up':
			if self.rect.y > 0:
				self.rect.y -= 10
			else:
				self.kill()
		elif direction == 'down':
			if self.rect.y < 600:
				self.rect.y += 10
			else:
				self.kill()

#makes some dang aliens
class alien_sprite(pygame.sprite.Sprite):
	def __init__(self, model, start_x, start_y, score, alien_class):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image('%s.bmp' %(model), [138,43,226])
		self.rect.x = start_x
		self.rect.y = start_y
		self.step_counter = 0
		self.step = 10
		self.speed = 2
		self.score = score
		self.alien_class = alien_class
		self.image_state = 1
		self.model = model
	def update(self, hitswall, death = False):
		if death == True:
			self.image_state = 3
			if self.image_state == 3:
				self.image = pygame.image.load(os.path.join('sprites','death.bmp')).convert()
				self.image.set_colorkey([138,43,226])
				self.image_state = 4
		if death != True:

			if hitswall == True:
				self.rect.y += 10
				self.step = self.step*-1
				self.rect.x += self.step
			else:
				self.rect.x += self.step
			if self.rect.y > 600:
				self.kill()
			if self.image_state == 1:
				self.model = self.model.replace('1','2')
				self.image = pygame.image.load(os.path.join('sprites',self.model+'.bmp')).convert()
				self.image.set_colorkey([138,43,226])
				self.image_state = 2
			elif self.image_state == 2:
				self.model = self.model.replace('2','1')						
				self.image = pygame.image.load(os.path.join('sprites',self.model+'.bmp')).convert()
				self.image.set_colorkey([138,43,226])
				self.image_state = 1
			elif self.image_state == 4:
				self.kill()
	def get_rid_of():
		self.kill()

		
#class that defines a barrier peice each barrier is made up of many barrier pieces
class barrier(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([4,4])
		self.image.fill([100,200,0])
		self.rect = self.image.get_rect()
		self.rect.x = start_x
		self.rect.y = start_y
# creates a peice of the star field
class star(pygame.sprite.Sprite):
	def __init__(self, screen):
		star_color = randint(0,100)
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([2,2])
		self.image.fill([star_color,star_color,star_color])
		self.rect = self.image.get_rect()
		self.rect.x = randint(0, screen.get_width() - 1)
		self.rect.y = randint(0, screen.get_height() - 1)
	def update(self):
		self.rect.y += 5
		if self.rect.y > 600:
			self.rect.y = -5
			self.rect.x = randint(0,screen.get_width() -1)

# loads our images so they look purdy
def load_image( name, colorkey= None):
	fullname = os.path.join('sprites', name)
	image = pygame.image.load(fullname).convert()
	if colorkey is not None:
		image.set_colorkey(colorkey)
	return image, image.get_rect()

# creates the background starfield
def create_starfield(num_stars, screen):
	for i in range(num_stars):
		new_star = star(screen)
		star_field.append(new_star)
		all_sprites.add(new_star)
# shows the HUD
def Display_player_stats(player, the_screen):
	text = pygame.font.Font('ca.ttf', 15)
	score = text.render('SCORE:%s'%(player.score),1,(255,255,255))
	player_lives = text.render('LIVES:%s' %(player.lives), 1, (255,255,255))
	the_screen.blit(score, (650,0))
	the_screen.blit(player_lives, (550,0))


# creates a barrier with he top left corner at the starting_x and y posstions with a height and width provided
def create_barrier(height, width, starting_x, starting_y):
	x_counter = 0
	y_counter = 0
	while y_counter <= height:
		while x_counter <= width:
			barrier_peice = barrier(x_counter+starting_x, starting_y+y_counter)
			barriers.add(barrier_peice)
			all_sprites.add(barrier_peice)
			x_counter += 4
		y_counter += 4
		x_counter = 0
# creates a row of aliens at the given y position
def create_alien_row(model, create_alien_row_y_position, score, alien_class):
	row_width = (screen.get_size()[1])-50
	alien_width = pygame.image.load(os.path.join('sprites',model+'.bmp')).get_height()+15
	row_can_hold = int(row_width/alien_width)
	number_of_aliens = range(row_can_hold+1)
	create_alien_row_x_position = 100
	for alien in number_of_aliens:
		new_alien = alien_sprite(model, create_alien_row_x_position, create_alien_row_y_position, score, alien_class)
		aliens.add(new_alien)
		all_sprites.add(new_alien)
		create_alien_row_x_position += alien_width
#creates all of the aliens on the screen
def create_aliens(model,number_of_lines, start_y, score, alien_class):
	for i in range(number_of_lines):
		create_alien_row(model, start_y, score, alien_class)
		start_y += pygame.image.load(os.path.join('sprites',model+'.bmp')).get_height()+10
def create_all_aliens():
	create_starfield(300, screen)
	create_aliens('alien_jelly1',1, 50, 50, 'jelly')
	create_aliens('alien_spider1',2,82,40,'spider')
	create_aliens('alien_mushroom1',2,147, 30,'mushroom')


pygame.init()
#let's set some variables, sprite groups and the screen and you know fun things like that..
sound_enabled = pygame.mixer.get_init()
screen = pygame.display.set_mode([800,600])
aliens = pygame.sprite.Group()
bullets_from_player = pygame.sprite.Group()
bullets_from_aliens = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
the_player = pygame.sprite.Group()
barriers = pygame.sprite.Group()
star_field = []
ships = {}
alien_y_step = False
#let's make some aliens
create_all_aliens()
#Those aliens shoot fast, let's make some barriers to slow them down
barrier_top_left = 50
for i in range(4):
	create_barrier(10,100,barrier_top_left, 450)
	barrier_top_left += 180
clock = pygame.time.Clock()
done = False
alien_position_tracker = False
alien_tick = 0
player_exists = False
name_box = eztext.Input(maxlength = 55, color=(255,255,255), prompt='Name: ',x= 300, y = 300)
ship_exists = False

#begin the actual loop that controls the game
while not done:
	#the next two while loops let players select a ship and a name soo....let's do it
	while ship_exists == False:
		#reset values so things don't display when mouse off
		show_text=False
		text_y = 0
		text_x = 300
		shields_bar_start = 225
		fire_rate_bar_start = 405
		movement_bar_start = 575
		set_shields = 0
		fire_rate = 0
		speed = 0
		#load the ship images
		ship1 = pygame.image.load(os.path.join('sprites', 'ship1.bmp'))
		ship2 = pygame.image.load(os.path.join('sprites', 'ship2.bmp'))
		ship3 = pygame.image.load(os.path.join('sprites', 'ship3.bmp'))
		#draw the ship images
		screen.blit(ship1, (305, 50))
		screen.blit(ship2, (300, 150))
		screen.blit(ship3, (300, 300))
		#get some events
		events = pygame.event.get()
		#get the mouse position
		mouse_position = pygame.mouse.get_pos()
		#find the mosue position and see if there is something that needs to be displayed then set appropriate variabels for the stats bar
		if mouse_position[0] > 304 and mouse_position[0] < 370:
			if mouse_position[1] > 49 and mouse_position[1] < 119:
				text_y = 124
				set_shields = 0
				speed = 40
				fire_rate = 50
				show_text = True
			if mouse_position[1] > 149 and mouse_position[1] < 235:
				text_y = 245
				set_shields = 50
				speed = 10
				fire_rate = 10
				show_text = True
			if mouse_position[1] > 299 and mouse_position[1] < 384:
				text_y = 400
				set_shields = 20
				speed = 20
				fire_rate = 20
				show_text = True

		if show_text:
			text_color = [255,255,255]
		else: 
			text_color = [0,0,0]
		mouse_buttons = pygame.mouse.get_pressed()
		if mouse_position [0] > 304 and mouse_position[0] < 370:
			if mouse_position[1] > 49 and mouse_position[1] < 119 and mouse_buttons[0]:
				ship = 'ship1.bmp'
				set_shields = 0
				set_fire_rate = 5
				set_movement = 25
				ship_exists = True
			elif mouse_position[1] > 149 and mouse_position[1] < 235 and mouse_buttons[0]:
				ship = 'ship2.bmp'
				set_shields = 5
				set_fire_rate = 1
				set_movement = 3
				ship_exists = True
			elif mouse_position[1] > 299 and mouse_position[1] < 384 and mouse_buttons[0]:
				ship = 'ship3.bmp'
				set_shields = 2
				set_fire_rate = 2
				set_movement = 10

				ship_exists = True
			#set a bunch of stuff and psition it propperly to be written to the screen
		ship_select_text = pygame.font.Font('ca.ttf', 15)
		shield_text = ship_select_text.render('SHEILDS:', 1, text_color)
		fire_rate_text = ship_select_text.render('FIRE RATE:', 1, text_color)
		movement_text = ship_select_text.render('MOVEMENT:', 1, text_color)
		ship_text_stuff = ship_select_text.render('SELECT YOUR COMBAT VEHICLE',1,(255,255,255))
		shields_bar =  pygame.Surface([set_shields, 5])
		shields_bar.fill([100,200,0])
		fire_rate_bar = pygame.Surface([fire_rate, 5])
		fire_rate_bar.fill([100,200,0])
		movement_bar = pygame.Surface([speed, 5])
		movement_bar.fill([100,200,0])
		screen.blit(shields_bar, (shields_bar_start, text_y))
		screen.blit(fire_rate_bar,(fire_rate_bar_start,text_y ))
		screen.blit(movement_bar, (movement_bar_start, text_y))
		screen.blit(shield_text, (shields_bar_start -100, text_y-5))
		screen.blit(fire_rate_text, (fire_rate_bar_start -115, text_y-5))
		screen.blit(movement_text, (movement_bar_start-110, text_y-5))
		screen.blit(ship_text_stuff, (200,550))
		pygame.display.flip()
		screen.fill((0,0,0))

	while player_exists == False:
		events = pygame.event.get()
		name_box.update(events)
		name_box.draw(screen)
		pygame.display.flip()
		screen.fill((0,0,0))
		keystate = pygame.key.get_pressed()
		if keystate[K_RETURN]:
			Player = player(name_box.value, ship, set_shields, set_movement, set_fire_rate)
			the_player.add(Player)
			all_sprites.add(Player)
			player_exists = True

	# sets alien move rate based on the number of aliens on the board
	alien_move = len(aliens)/4
	alien_y_step == False
	#check to see if the close button got hit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	keystate = pygame.key.get_pressed()
	#check for player movement
	if keystate[K_RIGHT]:
		Player.move_right()
	if keystate[K_LEFT]:
		Player.move_left()
	if keystate[K_SPACE]:
	#check to see if a bullet is ready to be fired
		if len(bullets_from_player) < Player.rof :
			the_new_bullet = bullet(Player,'player')
			bullets_from_player.add(the_new_bullet)
			all_sprites.add(the_new_bullet)
			if sound_enabled:
				shooting_noise = pygame.mixer.Sound(os.path.join('sounds','shoot.wav'))
				shooting_noise.play()
	#check to see if it's time to move the aliens
	if alien_tick >= alien_move:
		if sound_enabled:
			alien_move_sound = pygame.mixer.Sound(os.path.join('sounds','fastinvader2.wav')).play()				
		for alien in aliens:
			# if we hit the right wall we want to tell the aliens to move down and change direction
			if alien.rect.x >= 750:
				alien_position_tracker = True
				alien_y_step = True
				break
			# same as above except with the left wall
			elif alien.rect.x <= 0:
				alien_position_tracker = True
				alien_y_step = True
				break
		# update the aliens with the direction and spaces they sould be moving
		aliens.update(alien_position_tracker,False)
		# reset the counter for the next alien movement
		alien_tick = 0
	else:
		#if the aliens didn't move...add one to the counter to see if they move next time
		alien_tick += 1
	#reset the position tracker each time to make sure the aliens move in the right dirrection
	alien_position_tracker = False
	# update all of the bullets on the screen, if it's from an alien we want them to move down if it's from a player we want them to go up
	bullets_from_aliens.update('down')
	bullets_from_player.update('up')
	# check to see if the player kills any aliens
	for alien in pygame.sprite.groupcollide(aliens, bullets_from_player, False, True).keys():
		Player.score += alien.score
		alien.score = 0
		alien.update(False,True)
		if sound_enabled:
			alien_dead_sound = pygame.mixer.Sound(os.path.join('sounds','invaderkilled.wav'))
			alien_dead_sound.play()
	# time to see if the aliens shoot back
	for alien in aliens:
		# basically each alien has a percent chance to shoot based on the number of alines left on the board
		# less aliens, the better chance they have of shooting
		if randint(1,len(aliens)*20) == 1:
			# if they do shoot make a new bullet at the position of the alien and add it to the approrite lists
			new_bullet = bullet(alien, 'alien')
			bullets_from_aliens.add(new_bullet)
			all_sprites.add(new_bullet)
	# time to see if the player died..this might want to go at the top but whatever
	for bullets in pygame.sprite.groupcollide(bullets_from_aliens, the_player, True, False).keys():
		if Player.shields < 0:
			Player.lives -=1
			Player.rect.x = 400
			Player.shields = set_shields
			for each in bullets_from_aliens:
				each.kill()
			#if the player is dead let's start the high score screen
			if Player.lives < 1:
				print('GAME OVER')
				screen.fill((0,0,0))
				for each in all_sprites:
					each.kill()
				display_end_game = True
				score_list = []
				the_end_text = pygame.font.Font('ca.ttf', 15)
				
				with open('highscores.csv', 'a') as highscores:
					csv_file_write = csv.writer(highscores, delimiter=',', quotechar='|', quoting =csv.QUOTE_MINIMAL)
					csv_file_write.writerow([Player.name, Player.score,])
				with open('highscores.csv','r') as highscores:
					reader = csv.reader(highscores)
					for row in reader:
						score_list.append([int(row[1]),row[0]])
				high_score_list = sorted(score_list, key=lambda x:x[0], reverse= True)
				while display_end_game:
					scorescreen_starting_y = 200
					counter=1
					for score in high_score_list:
						screen.blit(the_end_text.render('%s. %s...........%s'%(counter,score[1],score[0]),1,(255,255,255)), (200, scorescreen_starting_y))
						scorescreen_starting_y +=20
						counter +=1
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()						
					scorescreen_starting_y = 200
					game_over_image= pygame.image.load(os.path.join('sprites','game-over.bmp'))
					screen.blit(game_over_image,(200,0))
					pygame.display.flip()
					screen.fill((0,0,0))

		else:
			Player.shields -= 1
	# check to see if a peice of the barrier got blown up either from the player or the alines
	for barrier in pygame.sprite.groupcollide(barriers, bullets_from_aliens, True, True).keys():
		barrier.update()
	for barrier in pygame.sprite.groupcollide(barriers, bullets_from_player, True, True).keys():
		barrier.update()
	# check if the aliens have hit the barrier becaus science!
	pygame.sprite.groupcollide(aliens, barriers, False, True)
	
	# basically checks to see if the level has ended or not
	if len(aliens) == 0:
		#this desperatly needs an animation of some kind
		create_all_aliens()

	#lets update the background
		# set the fps to 30 which so far has been okay
	clock.tick(30)
	# erease the screen to black
	screen.fill([0,0,0])
	for s1 in star_field:
		s1.update()
	# draw everything we updated in this entire loop
	Display_player_stats(Player, screen)
	all_sprites.draw(screen)
	# and show it to the good people so they can relive the classic game from 1978 
	pygame.display.flip()
















