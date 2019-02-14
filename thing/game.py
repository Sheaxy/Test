import pygame
import random
from os import path

WIDTH,HEIGHT=480,600
BLOCK=(0,0,0)

NEW_ENEMY_GENERATE_INTERVAL=500
last_enemy_generate_time=0
MISSILE_LIFETIME=1000
MISSILE_INTERVAL=500
game_state=0

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.flip(player_img,False,True)
		self.image=pygame.transform.scale(player_img,(80,80))
		#self.image.fill(GREEN)
		self.image.set_colorkey(BLOCK)
		self.rect=self.image.get_rect()
		self.radius=40
		#self.direction = 1
		self.rect.centerx=WIDTH/2
		self.rect.bottom=HEIGHT

		self.hp=100
		self.lives=3
		self.score=0
		self.hidden=False
		self.hid_time=0

		self.is_missile_firing=False
		self.strat_missile_time=0
		self.last_missile_time=0

	def update(self):
		keystate=pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.rect.x-=5
		if keystate[pygame.K_RIGHT]:
			self.rect.x+=5
		if keystate[pygame.K_UP]:
			self.rect.y-=5
		if keystate[pygame.K_DOWN]:
			self.rect.y+=5

		if self.rect.right>=WIDTH:
			self.rect.right=WIDTH
		if self.rect.left<=0:
			self.rect.left=0
		if self.rect.bottom>=HEIGHT:
			self.rect.bottom=HEIGHT
		#if self.rect.top<=0:
		#	self.rect.top=0

		now=pygame.time.get_ticks()
		if self.hidden and now-self.hid_time>1000:
			self.hidden=False
			self.rect.bottom=HEIGHT

		if  self.is_missile_firing:
			if now-self.strat_missile_time<MISSILE_LIFETIME:
				if now-self.last_missile_time>MISSILE_INTERVAL:
					missile=Missile(self.rect.center)
					missiles.add(missile)
					self.last_missile_time=now
			else:
				self.is_missile_firing=False
		#self.rect.x+=self.direction*5
		#if self.rect.right>=WIDTH:
		#	self.direction = -1
		#if self.rect.left <= 0
		#	self.direction = 1

	def shoot(self):
		bullet=Bullet(self.rect.centerx,self.rect.centery)
		bullets.add(bullet)
		shoot_sound.play()

	def fire_missile(self):
		self.is_missile_firing=True
		self.strat_missile_time=pygame.time.get_ticks()

	def hide(self):
		self.hidden=True
		self.rect.y=-200
		self.hid_time=pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		img_width=random.randint(20,120)
		self.image=pygame.transform.scale(enemy_img,(img_width,img_width))
		self.image.set_colorkey(BLOCK)
		self.image_origin=self.image.copy()
		#self.image.fill(BLUE)
		self.rect=self.image.get_rect()
		self.radius=img_width/2
		#pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
		self.direction = 1
		self.rect.centerx=random.randint(0,WIDTH)
		self.rect.bottom=0 

		self.vx=random.randint(-2,2)
		self.vy=random.randint(2,10)

		self.last_rotate_time=pygame.time.get_ticks()
		self.rotate_speed=random.randint(-5,5)
		self.rotate_angle=0

	def update(self):
		self.rect.x+=self.vx
		self.rect.y+=self.vy

		old_center=self.rect.center
		self.rotate()
		self.rect=self.image.get_rect()
		self.rect.center=old_center

	def rotate(self):
		now=pygame.time.get_ticks()
		if now-self.last_rotate_time>30:
			self.rotate_angle=(self.rotate_angle+self.rotate_speed)%360
			self.image=pygame.transform.rotate(self.image_origin,self.rotate_angle)
			self.last_rotate_time=now

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(bullet_img,(30,30))
		self.image.set_colorkey(BLOCK)
		#self.image.fill(BLOCK)
		self.rect=self.image.get_rect()
		self.rect.centerx=x
		self.rect.centery=y

	def update(self):
		self.rect.y-=10

#class Explosion(pygame.sprite.Sprite):
#	def __init__(self,center):
#		pygame.sprite.Sprite.__init__(self)
#		self.image = explosion_animation[0]
#		self.image = pygame.transform.scale(explosion_img,(40,40))
#		self.image.set_colorkey(BLOCK)
#		self.rect = self.image.get_rect()
#		self.rect.center = center
#		self.frame = 0
#		self.last_time = pygame.time.get_ticks()

#	def updata(self):
#		now=pygame.time.get_ticks()
#		if now-self.last_time>30:
#			if self.frame<len(explosion_animation):
#				self.image = explosion_animation[self.frame]
#				self.image = pygame.transform.scale(explosion_img,(40,40))
#				self.image.set_colorkey(BLOCK)
#				self.frame+=1
#				self.last_time = now
#			else:
#				self.kill()

class Explosion(pygame.sprite.Sprite):
	"""docstring for Explosion"""
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		#self.image=explosion_animation[0]
		self.image=pygame.transform.scale(explosion_animation[0],(60,60))
		self.image.set_colorkey(BLOCK)
		self.rect=self.image.get_rect()
		self.rect.center=center
		self.frame=0
		self.last_time=pygame.time.get_ticks()
		explosion_sound.play()

	def update(self):
		now=pygame.time.get_ticks()
		if now-self.last_time>30:
			if self.frame<len(explosion_animation):
				self.image=pygame.transform.scale(explosion_animation[self.frame],(60,60))
					#亮点：改大小
				self.image.set_colorkey(BLOCK)
				self.frame+=1
				self.last_time=now
			else:
				self.kill()
		
def draw_ui():
	pygame.draw.rect(screen,(0,255,0),(10,10,player.hp,15))
	pygame.draw.rect(screen,(255,255,255),(10,10,100,15),2)

	draw_text(str(player.score),screen,(255,255,255),20,WIDTH/2,10)

	img_rect=player_img_small.get_rect()
	img_rect.x=WIDTH-(img_rect.width+10)
	img_rect.y=10
	for i in range(player.lives):
		screen.blit(player_img_small,img_rect)
		img_rect.x-=img_rect.width+10

def draw_text(text,surface,color,font_size,x,y):
	font_name=pygame.font.match_font('arial')
	font=pygame.font.Font(font_name,font_size)
	text_surface=font.render(text,True,color)
	text_rect=text_surface.get_rect()
	text_rect.midtop=(x,y)
	screen.blit(text_surface,text_rect)

class PowerUp(pygame.sprite.Sprite):
	def __init__(self,center):
		pygame.sprite.Sprite.__init__(self)
		random_num=random.random()
		if random_num<0.5:
			self.type='add_hp'
		elif random_num<0.8:
			self.type='add_missile'
		else:
			self.type='add_life'
		self.image=powerup_imgs[self.type]
		self.rect=self.image.get_rect()
		self.image.set_colorkey(BLOCK)
		self.rect.center=center
	def update(self):
		self.rect.y+=7

class Missile(pygame.sprite.Sprite):
	"""docstring for Missile"""
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.image=missile_img
		self.rect=self.image.get_rect()
		self.image.set_colorkey(BLOCK)
		self.rect.center=center
	def update(self):
		self.rect.y-=5

def show_menu():
	global game_state,screen
	screen.blit(background,background_rect)
	draw_text('Space Shooter!',screen,(255,255,255),40,WIDTH/2,100)
	draw_text('Press Space key to start',screen,(255,255,255),20,WIDTH/2,300)
	draw_text('Press Esc key to quit',screen,(255,255,255),20,WIDTH/2,350)
	event_list=pygame.event.get()
	for event in event_list:
		if event.type==pygame.QUIT:
			pygame.quit()
			quit()
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_ESCAPE:
				pygame.quit()
				quit()
			if event.key==pygame.K_SPACE:
				game_state=1
	pygame.display.flip()

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init()
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("My Game")
clock=pygame.time.Clock()

img_dir=path.join(path.dirname(__file__),'img')

background_dir=path.join(img_dir,'background.png')
background=pygame.image.load(background_dir).convert()

background_rect=background.get_rect()

player_dir=path.join(img_dir,'spaceShips_002.png')
player_img=pygame.image.load(player_dir).convert()
enemy_dir=path.join(img_dir,'spaceMeteors_002.png')
enemy_img=pygame.image.load(enemy_dir).convert()
bullet_dir=path.join(img_dir,'spaceMissiles_007.png')
bullet_img=pygame.image.load(bullet_dir).convert()
player_img_small=pygame.transform.scale(player_img,(26,20))
player_img_small.set_colorkey((0,0,0))

sound_dir=path.join(path.dirname(__file__),'song')
shoot_sound=pygame.mixer.Sound(path.join(sound_dir,'Laser_Shoot2.wav'))
explosion_sound=pygame.mixer.Sound(path.join(sound_dir,'Explosion.wav'))
pygame.mixer.music.load(path.join(sound_dir,'Dynamedion.ogg'))

powerup_imgs = {}
powerup_add_hp_dir=path.join(img_dir,'gem_red.png')
powerup_imgs['add_hp']=pygame.image.load(powerup_add_hp_dir).convert()
powerup_add_life_dir=path.join(img_dir,'heartFull.png')
powerup_imgs['add_life']=pygame.image.load(powerup_add_life_dir).convert()
powerup_add_missile_dir=path.join(img_dir,'gem_yellow.png')
powerup_imgs['add_missile']=pygame.image.load(powerup_add_missile_dir).convert()

missile_dir=path.join(img_dir,'spaceMissiles_007.png')
missile_img=pygame.image.load(missile_dir).convert()

#explosion_animation=[]
#for i in range(9):
#	explosion_dir=path.join(img_dir,'regularExplosion0{}.png'.format(i))
#	explosion_img=pygame.image.load(explosion_dir).convert()
#	explosion_animation.append(explosion_img)

explosion_animation=[]
for i in range(9):
	explosion_dir=path.join(img_dir,'regularExplosion0{}.png'.format(i))
	explosion_img=pygame.image.load(explosion_dir).convert()
	explosion_animation.append(explosion_img)

player=Player()
enemys=pygame.sprite.Group()
#for i in range(10):
#	enemy = Enemy()
#	enemys.add(enemy)
bullets=pygame.sprite.Group()
explosions=pygame.sprite.Group()
powerups=pygame.sprite.Group()
missiles=pygame.sprite.Group()

game_over=False
pygame.mixer.music.play(loops=-1)
while not game_over:
	clock.tick(60)
	if game_state==0:
		show_menu()
	elif game_state==1:
		now=pygame.time.get_ticks()
		if now-last_enemy_generate_time>NEW_ENEMY_GENERATE_INTERVAL:
			enemy=Enemy()
			enemys.add(enemy)
			last_enemy_generate_time=now
		event_list=pygame.event.get()
		for event in event_list:
			if event.type==pygame.QUIT:
				game_over=True
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					game_over=True
				if event.key==pygame.K_SPACE:
					player.shoot()

	#mouse_x,mouse_y=pygame.mouse.get_pos()
	#print(mouse_x,mouse_y)

	#hits = pygame.sprite.spritecollide(player,enemys,False,pygame.sprite.collide_rect_ratio(0.7))
		hits=pygame.sprite.spritecollide(player,enemys,True,pygame.sprite.collide_circle)
		for hit in hits:	
			player.hp-=hit.radius
			if player.hp<0:
				player.lives-=1
				player.hp=100
				player.hide()
				if player.lives==0:
					game_over=True
		hits=pygame.sprite.groupcollide(enemys,bullets,True,True)
		for hit in hits:
			explosion=Explosion(hit.rect.center)
			explosions.add(explosion)
			player.score+=140-hit.radius
		#print(player.score)
			if random.random()>0.9:
				powerup=PowerUp(hit.rect.center)
				powerups.add(powerup)

		hits=pygame.sprite.groupcollide(enemys,missiles,True,True)
		for hit in hits:
			explosion=Explosion(hit.rect.center)
			explosions.add(explosion)
			player.score+=140-hit.radius
		#print(player.score)
			if random.random()>0.3:
				powerup=PowerUp(hit.rect.center)
				powerups.add(powerup)

		hits=pygame.sprite.spritecollide(player,powerups,True)
		for hit in hits:
			if hit.type=='add_hp':
				player.hp +=50
				if player.hp>100:
					player.hp=100
			elif hit.type=='add_life':
				player.lives+=1
				if  player.lives>3:
					player.lives=3
			else:
				player.fire_missile()

		player.update()
		enemys.update()
		bullets.update()
		explosions.update()
		powerups.update()
		missiles.update()

		screen.blit(background,background_rect)

		screen.blit(player.image,player.rect)
		enemys.draw(screen)
		bullets.draw(screen)
		explosions.draw(screen)
		powerups.draw(screen)
		missiles.draw(screen)

		draw_ui()

		pygame.display.flip() 