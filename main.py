#! /usr/bin/env python

# ImposyBird, a game ripped off of flappy bird, but with a twist.

import pygame
import sys
import random
import time

class Game:

    def __init__(self):
        pygame.init() #Start Pygame

        self.clock = pygame.time.Clock() 
        self.FPS = 30
        
        # --- SCREEN --- #
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 480
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption('Imposy Bird')
        
        # --- Obstacles --- #
        self.block_width = 120
        self.gap_height = 150
        self.OBSTACLES = 4
        self.OBSTACLE_REDRAW_TIME = 20 # Lower is quicker
        # making obstacles
        self.rects = []
        for i in range(self.OBSTACLES):
            self.rects.append(Rect(self.SCREEN_HEIGHT, self.gap_height, self.block_width, i * 250 + 250).obstacles())

        # --- BIRD --- #
        self.bird_size = 20
        self.bird_velocity = 20
        self.bird = Bird(self.bird_velocity, self.SCREEN_WIDTH/10, self.SCREEN_HEIGHT/2, self.bird_size, self.bird_size)

    def game_loop(self):
        global running
        running = True
        original_redraw_time = self.OBSTACLE_REDRAW_TIME

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.fill([0,0,0])

            if self.OBSTACLE_REDRAW_TIME == original_redraw_time:
                self.rects = []
                for i in range(self.OBSTACLES):
                    self.rects.append(Rect(self.SCREEN_HEIGHT, self.gap_height, self.block_width, i * 250 + 250).obstacles())
                    for rect in self.rects:
                        pygame.draw.rect(self.screen, (255, 255, 255), rect[0])
                        pygame.draw.rect(self.screen, (255, 255, 255), rect[1])

                self.OBSTACLE_REDRAW_TIME = self.OBSTACLE_REDRAW_TIME - 1
            elif 0 < self.OBSTACLE_REDRAW_TIME < original_redraw_time:
                for rect in self.rects:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect[0])
                    pygame.draw.rect(self.screen, (255, 255, 255), rect[1])

                self.OBSTACLE_REDRAW_TIME = self.OBSTACLE_REDRAW_TIME - 1
            elif self.OBSTACLE_REDRAW_TIME == 0:
                for rect in self.rects:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect[0])
                    pygame.draw.rect(self.screen, (255, 255, 255), rect[1])

                self.OBSTACLE_REDRAW_TIME = original_redraw_time
              
            self.bird.handle_keys(self.screen.get_rect())
            pygame.draw.rect(self.screen, (255, 255, 255), self.bird)

            if self.bird.hit_obstacle(self.rects):
                running = False

            pygame.display.flip()

            if self.bird.hit_end_wall():

                if self.splash_screen() == "Restart":
                    running = False
                    self.restart()
                elif self.splash_screen() == "Quit":
                    running = False
                    pygame.quit()

            self.clock.tick(30)

        if self.bird.hit_obstacle(self.rects):
            self.restart()
        

    def splash_screen(self):
        running = True
                    
        font_buttons = pygame.font.SysFont('Areal', 22)

        # Restart button
        replay_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]/2 - 100, pygame.display.get_surface().get_size()[1]/2 - 50, 100, 50)
        pygame.draw.rect(self.screen, (125, 255, 125), replay_rect, 0)
        self.screen.blit(font_buttons.render('Replay', True, (0,0,0)), ((pygame.display.get_surface().get_size()[0]/2 - 75), (pygame.display.get_surface().get_size()[1]/2) - 30))
        
        # Quit button
        quit_rect = pygame.Rect(pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]/2 - 50, 100, 50)
        pygame.draw.rect(self.screen, (255, 125, 125), quit_rect, 0)
        self.screen.blit(font_buttons.render('Quit', True, (0,0,0)), ((pygame.display.get_surface().get_size()[0]/2 + 35), (pygame.display.get_surface().get_size()[1]/2) - 30))

        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN):# Button actions
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_rect.collidepoint(mouse_pos):
                        return("Restart")

                    elif quit_rect.collidepoint(mouse_pos):
                        return("Quit")
    
    def restart(self):
        game = Game()
        game.game_loop()

class Bird(pygame.Rect):
    def __init__(self, velocity, *args, **kwargs):
        self.velocity = velocity
        self.angle = 0
        self.initial_left = args[0]
        self.initial_top = args[1]
        self.initial_height = args[2]
        self.initial_width = args[3]
        super().__init__(*args, **kwargs)

    # Move bird within limits of the game window
    def handle_keys(self, limit):
        self.limit = limit
        key = pygame.key.get_pressed()
        if not self.clamp_ip(self.limit):
            if key[pygame.K_UP]:
                self.move_ip(0, -self.velocity)
            if key[pygame.K_DOWN]:
                self.move_ip(0, self.velocity)
            if key[pygame.K_LEFT]:
                self.move_ip(-self.velocity, 0)
            if key[pygame.K_RIGHT]:
                self.move_ip(self.velocity, 0)

    def hit_obstacle(self, rects):
        for rect in rects:
            if self.colliderect(rect[0]) or self.colliderect(rect[1]):
                return True

    # Win function
    def hit_end_wall(self):
        if self.left == pygame.display.get_surface().get_size()[0]:
            return True
    
    def redraw_bird(self):
        return Bird(self.velocity, self.initial_left, self.initial_top, self.initial_height, self.initial_width)


class Rect():
    def __init__(self, screen_height, gap_height, block_width, left):
        self.gap_height = gap_height
        self.block_width = block_width
        self.equal = (screen_height - gap_height) / 2
        self.left = left
        self.diff = random.randint(-100, 100)
        self.top = self.equal + self.diff
        self.bottom = self.equal - self.diff

    def obstacles(self):
        return [pygame.Rect(self.left, 0, self.block_width, self.top), pygame.Rect(self.left, self.top + self.gap_height , self.block_width, self.bottom)]

if __name__ == '__main__':
    game = Game()
    game.game_loop()