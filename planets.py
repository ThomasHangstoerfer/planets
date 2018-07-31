
# https://developer.akamai.com/blog/2017/06/21/building-virtual-python-environment/
#
# Export requirements to a file:
# pip freeze > requirements.txt

# After cloning the repo, install requirements in virtualenv:
# virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt


import sys, math, pygame
pygame.init()

size = width, height = 800, 600
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("ball.gif")
#ballrect = ball.get_rect()

ticks = pygame.time.get_ticks()
clck = pygame.time.Clock()

font_planet_name = pygame.font.SysFont("Monospaced", 18)
#text = font.render("(%i, %i)" % (speed[0], speed[1]), True, (0, 128, 0))

show_names = False
pause = True
days = 0
show_orbits = False 

red = (255, 0, 0)
yellow = (255, 255, 0)
lightyellow = (255, 255, 150)
blue = (0, 0, 255)
lightblue = (100, 100, 255)

sun = [width//2, height//2]


class Planet:
    def __init__(self, name, size, angle, distance, color, orbital_period):
        self.name = name
        self.size = size  # Äquatordurchmesser [km]
        self.angle = angle
        self.distance = distance  # Perihel [AE]
        self.color = color
        self.orbital_period = orbital_period  # Siderische Umlaufzeit [days]
        self.text = font_planet_name.render(self.name, True, self.color)

    def draw(self, days):
        planet_day = days % self.orbital_period
        self.angle = 360 * planet_day / self.orbital_period
        # print("angle = %f days = %i orbital_period = %i math.cos(self.angle) = %f" % (self.angle, days, self.orbital_period, math.cos(self.angle*math.pi/180.0)))

        x = int(sun[0]) + math.cos(self.angle*math.pi/180.0) * self.distance*100
        y = int(sun[1]) + math.sin(self.angle*math.pi/180.0) * self.distance*100

        if show_orbits:
            pygame.draw.circle(screen, self.color, (int(sun[0]), int(sun[1])), int(self.distance*100), 1)

        pygame.draw.circle(screen, self.color, (int(x), int(y)), int(self.size), 0)
        # print("%s: %i %i" % (self.name, x, y))
        # screen.blit(self.text, (320 - self.text.get_width() // 2, 240 - self.text.get_height() // 2))
        global show_names
        if show_names:
            screen.blit(self.text, (x + self.size//2 + 20 + self.text.get_width() // 2, y - self.text.get_height() // 2))


mercury = Planet("Mercury", size=4.879, angle=16, distance=0.307498, color=lightyellow, orbital_period=87.969)
venus = Planet("Venus", size=12.103, angle=246, distance=0.718, color=lightblue, orbital_period=224.701)
earth = Planet("Earth", size=12.756, angle=36, distance=0.983, color=blue, orbital_period=365.256363004)
mars = Planet("Mars", size=6.792, angle=110, distance=1.381, color=red, orbital_period=686.980)
jupiter = Planet("Jupiter", size=142.984, angle=190, distance=4.95, color=(188, 143, 143), orbital_period=4330)


def drawSun():
    #pass
    pygame.draw.circle(screen, yellow, (sun[0], sun[1]), 20, 0)


while True:
    clck.tick(40)
    #print("ticks: %i" % ticks)
    for event in pygame.event.get():
        #print('event: ', event)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            print('KEYDOWN event.unicode = %s' % event.unicode)
            #print('KEYDOWN pygame.K_q = %s' % pygame.K_q)
            if event.key == pygame.K_q:
                print('Q')
                sys.exit()
            if event.key == pygame.K_n:
                show_names = not show_names
                print('show names: ', show_names)
            if event.key == pygame.K_p:
                pause = not pause
                print('pause: ', pause)
            if event.key == pygame.K_o:
                show_orbits = not show_orbits
                print('show_orbits: ', show_orbits)
            if event.key == pygame.K_d:
                days = days + 1
                print('days: ', days)
            if event.key == pygame.K_r:
                days = 0
                print('reset days: ', days)
            if event.key == pygame.K_LEFT:
                print('LEFT')
            if event.key == pygame.K_RIGHT:
                print('RIGHT')

    if pygame.time.get_ticks() - ticks > 50:
        screen.fill(black)
        #ballrect = ballrect.move(speed)
        ticks = pygame.time.get_ticks()

        drawSun()

        pygame.display.set_caption('Day %i' % days)
        if not pause:
            days = days + 1
        #print("days: %i" % days)

        mercury.draw(days)
        venus.draw(days)
        earth.draw(days)
        mars.draw(days)
        jupiter.draw(days)

        #pygame.draw.circle(screen, red, (20, 20), 20, 0)
        #screen.blit(ball, ballrect)
        #screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))
        pygame.display.flip()
