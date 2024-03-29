import pygame, sys
from data.classes.player_class import *
from data.content.settings import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//28
        self.cell_height = MAZE_HEIGHT//30
        self.walls = []
        self.coins = []
        self.p_pos = None

        self.load()

        self.player = Player(self, self.p_pos)

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

###################### HELP FUNCTIONS  ######################

    def draw_text(self, words, screen, pos, size, color, font_name, centered = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0]//2
            pos[1] = pos[1] - text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('./assets/images/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        with open('data/content/map.txt','r') as file:
            for yindex, line in enumerate(file):
                for xindex, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xindex, yindex))
                    elif char == 'C':
                        self.coins.append(vec(xindex, yindex))
                    elif char == 'P':
                        self.p_pos = vec(xindex, yindex)

###################### START FUNCTIONS ######################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('HIGH SCORE', self.screen, [10, 5], 28, WHITE, TEXT_FONT)
        self.draw_text('PUSH SPACE BAR TO START', self.screen, [WIDTH//2, HEIGHT//2-50], 40, (170, 132, 58), TEXT_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [WIDTH//2, HEIGHT//2], 32, (33, 137, 156), TEXT_FONT, centered=True)

        pygame.display.update()

###################### PLAYING FUNCTIONS ######################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))

    def playing_update(self):
        self.player.update()

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [60,5], 28, WHITE, TEXT_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, [WIDTH//2+60,5], 28, WHITE, TEXT_FONT)
        
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.player.draw()

        # DRAW COINS
        for coin in self.coins:
            pygame.draw.circle(self.screen, WHITE, (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,int(coin.y*self.cell_width)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 3)

        # DRAW GRID
        '''
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
            for y in range(HEIGHT//self.cell_height):
                pygame.draw.line(self.background, GREY, (0, y*self.cell_height), (WIDTH, y*self.cell_height))
        #'''
        # DRAW WALLS
        '''
        for wall in self.walls:
            pygame.draw.rect(self.background, (112,55,163), (wall.x*self.cell_width, wall.y*self.cell_height, self.cell_width, self.cell_height))
        #'''
            

        pygame.display.update()


