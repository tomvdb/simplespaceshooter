'''
   Simple Example game for using Pygame Zero on the raspberry pi

    Created for Fakugesi 2019 workshop - http://fakugesi.co.za/events/arcade-box-creating-games-raspberry-pi/

    Code - Tom Van den Bon
    Music - Sawsquarenoise
    Graphics - Kenney
    Font - 8-Bit Madness

'''

import random

# control window size
WIDTH = 800
HEIGHT = 600

# load assets
background = Actor('background', topleft=(0,0))
player = Actor('player', (WIDTH/2, HEIGHT - 100))

# lists for enemies, lasers and explosions
enemies = []
frigginLaserBeams = []
enemyLaserBeams = []
explosions = []

# simple game stats
scoreCounter = 0
healthCounter = 100

# game state, 0 = Start Screen, 1 = Playing Game, 2 = You Died
state = 0

# gets called whenever the screen needs to be updated
def draw():
    # clear screen
    screen.clear()

    # draw background
    background.draw()

    if state == 0:  # show start game screen
        screen.draw.text("Simple Space Shooter", (120, 200), fontname="pixeloperator8bold", fontsize=32)
        screen.draw.text("Press 'Space' to Start", (210, 300), fontname="pixeloperator8bold", fontsize=20)

    elif state == 1:  # play game!

        # draw player
        player.draw()

        # draw laser shots from player
        for laser in frigginLaserBeams:
            laser.draw()

        # draw laser shots from enemy
        for laser in enemyLaserBeams:
            laser.draw()

        # draw emeny ufo's
        for ufo in enemies:
            ufo.draw()

        # draw any explosions
        for exp in explosions:
            exp.draw()

        # draw game stats
        screen.draw.text("Health : " + str(healthCounter) + "%", (20, HEIGHT-50), fontname="pixeloperator", fontsize=29)
        screen.draw.text(str(scoreCounter) + "", (WIDTH-100, 30), fontname="pixeloperator", fontsize=29)

    elif state == 2:    # show player died screen

        screen.draw.text("You died! Final Score is " + str(scoreCounter), (140, 200), fontname="pixeloperator8bold", fontsize=20)

        screen.draw.text("Code - Tom", (140, 300), fontname="pixeloperator8bold", fontsize=20)
        screen.draw.text("Music - Sawsquarenoise", (140, 350), fontname="pixeloperator8bold", fontsize=20)
        screen.draw.text("Graphics - Kenney", (140, 400), fontname="pixeloperator8bold", fontsize=20)
        screen.draw.text("Font - 8-Bit Madness", (140, 450), fontname="pixeloperator8bold", fontsize=20)

# reset game state to 0 - start screen
def resetGame():
    global state
    state = 0

def fireLaser():
    sounds.laser.play()
    frigginLaserBeams.append(Actor('laserplayer', midbottom = (player.midtop)))

def fireEnemyLaser(pos):
    sounds.laser.play()
    enemyLaserBeams.append(Actor('laserenemy', midbottom = pos))

def addEnemy():
    enemies.append(Actor('ufo', center = (900, random.randint(50, 350))))

def addExplosion(pos):
    sounds.boom.play()
    explosions.append(Actor('explosion1', center = pos))
    
def updateExplosion():
    for exp in explosions:
        if exp.image == 'explosion1':
            exp.image = 'explosion2'
        elif exp.image == 'explosion2':
            exp.image = 'explosion3'
        elif exp.image == 'explosion3':
            exp.image = 'explosion4'
        elif exp.image == 'explosion4':
            explosions.remove(exp)

def hidePlayer():
    player.y = HEIGHT + 200

def restorePlayer():
    player.x = WIDTH / 2
    player.y = HEIGHT - 100

def update():
    global scoreCounter
    global healthCounter
    global state

    if state == 0: # wait for user to press 'spacebar' then start game and reset game variables
        if keyboard.space:
            clock.schedule_interval(updateExplosion, 0.1)
            clock.schedule_interval(addEnemy, 5.0) # add new enemy every 5 seconds
            state = 1
            healthCounter = 100
            scoreCounter = 0
            enemies.clear()
            enemyLaserBeams.clear()
            frigginLaserBeams.clear()
            explosions.clear()
            music.play('play')


    elif state == 1: # player is busi playing

        # if we don't have any enemies, add another one
        if len(enemies) == 0:
            addEnemy()

        # move lasers if any
        for laser in frigginLaserBeams:
            laser.y -= 5
            if laser.y < 0:
                frigginLaserBeams.remove(laser)

        for laser in enemyLaserBeams:
            laser.y += 5
            if laser.y > HEIGHT:
                enemyLaserBeams.remove(laser)

        # move enemies and maybe shoot ?
        for ufo in enemies:
            ufo.angle += 1  # just for the effect, lets rotate it
            ufo.x -= 5
            if ufo.y < 40:
                ufo.y = 40
            elif ufo.y > 400:
                ufo.y = 400
            else:
                ufo.y += random.randint(-5, 5)
            if ufo.x < 0:
                ufo.x = WIDTH

            if random.randint(0,100) == 2:
                fireEnemyLaser(ufo.midbottom)


        # player move
        if keyboard.left and player.x > 70:
            player.x -= 5
        
        if keyboard.right and player.x < 730:
            player.x += 5

        if keyboard.space:
            clock.schedule_unique(fireLaser, 0.1)

        # check collision - did our laser beam hit enemy ?
        for laser in frigginLaserBeams:
            for ufo in enemies:
                if laser.colliderect(ufo):
                    addExplosion(ufo.center)
                    frigginLaserBeams.remove(laser)
                    enemies.remove(ufo)
                    scoreCounter += 10

        # check collision - did enemy laser beam hit us ?
        for laser in enemyLaserBeams:
            if laser.colliderect(player):
                addExplosion(player.center)
                enemyLaserBeams.remove(laser)
                hidePlayer()
                clock.schedule_unique(restorePlayer,0.8)
                healthCounter -= 20

                # did player die?
                if healthCounter < 1:
                    state = 2
                    clock.unschedule(updateExplosion)
                    clock.unschedule(addEnemy)
                    music.play('sadending')

    elif state == 2:
        # player died screen, stay there until return pressed
        if keyboard.RETURN:
            resetGame()
