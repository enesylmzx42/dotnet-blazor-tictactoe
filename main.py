import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass Gravity-Space Simulation")

EARTH_MASS = 98
SATELLITE_MASS = EARTH_MASS // 9
SHIP_MASS = 5
G = 5
FPS = 60
EARTH_SIZE = 69
SATELLITE_SIZE = EARTH_SIZE // 4
OBJ_SIZE = 5
VEL_SCALE = 95


BG = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))
EARTH = pygame.transform.scale(pygame.image.load("earth.png"), (EARTH_SIZE * 2, EARTH_SIZE * 2))
SATELLITE = pygame.transform.scale(pygame.image.load("satellite.png"), (SATELLITE_SIZE * 2, SATELLITE_SIZE * 2))


ORANGE = (255,165,0)
WHITE = (255, 255, 255)


class Earth:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(EARTH, (self.x - EARTH_SIZE, self.y - EARTH_SIZE))

class Satellite:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(SATELLITE, (self.x - SATELLITE_SIZE, self.y - SATELLITE_SIZE))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, celestial_bodies):
        for body in celestial_bodies:
            distance = math.sqrt((self.x - body.x)**2 + (self.y - body.y)**2)
            force = (G * self.mass * body.mass) / distance ** 2
            
            acceleration = force / self.mass
            angle = math.atan2(body.y - self.y, body.x - self.x)

            acceleration_x = acceleration * math.cos(angle)
            acceleration_y = acceleration * math.sin(angle)

            self.vel_x += acceleration_x
            self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        pygame.draw.circle(win, ORANGE, (int(self.x), int(self.y)), OBJ_SIZE)

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    earth = Earth(WIDTH // 2, HEIGHT // 2, EARTH_MASS)
    satellite = Satellite(11 * WIDTH // 16, 3 * HEIGHT // 8, SATELLITE_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, ORANGE, temp_obj_pos, OBJ_SIZE)
        
        for obj in objects[:]:
            obj.draw()
            obj.move([earth, satellite])
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - earth.x)**2 + (obj.y - earth.y)**2) <= EARTH_SIZE
            if off_screen or collided:
                objects.remove(obj)

        earth.draw()
        satellite.draw()

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()