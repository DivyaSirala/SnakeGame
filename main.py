import pygame
import time
import random
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR =(37, 99, 54)
TIME = 0.5
DELAY = 0.01
MAX_X = 1000
MAX_Y = 800

class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE
        self.y = SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,(MAX_X//40)-10)*SIZE
        self.y = random.randint(1,(MAX_Y//40)-5)*SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.delay = TIME
        self.length = length
        self.parent_screen = parent_screen
        # adding a block to the screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "down"

    def increase_length(self):
        self.length +=1
        self.x.append(-1)
        self.y.append(-1)
        if self.delay > 0:
            self.delay -= DELAY

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        #for the remaining blocks from end in reverse direction
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        #logic for all the heads
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init() #Sound module
        self.playbackgroundmusic() #Music module

        # this module is used to display the application on screen
        # fill it with desired colour by picking up RGB values from google color picker
        self.surface = pygame.display.set_mode((MAX_X, MAX_Y))
        self.surface.fill(BACKGROUND_COLOR)

        self.snake = Snake(self.surface, 1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collission(self, x1, y1, x2, y2 ):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def speedup(self):
        pass

    def playbackgroundmusic(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def playsound(self, file_path):
        sound = pygame.mixer.Sound(file_path)
        pygame.mixer.Sound.play(sound)

    def renderbackground(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.renderbackground()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        #collision with apple
        if self.is_collission(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.playsound("resources/ding.mp3")
            self.snake.increase_length()
            #self.snake.time.sleep(TIME+DELAY)
            self.apple.move()

        #collision with itself - GAME OVER
        for i in range(3, self.snake.length):
            if self.is_collission(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.playsound("resources/crash.mp3")
                raise "Game Over"

        #collision with boundary - GAME OVER
        if not (0 <= self.snake.x[0] <= MAX_X and  0 <= self.snake.y[0] <= MAX_Y):
                self.playsound("resources/crash.mp3")
                raise "Game Over"

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.renderbackground()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game OVer!! Your Score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play the game again, press Enter. To exit press Exit", True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        #stop game in gameover
        pygame.mixer.music.pause()


    def reset(self):
        #resetting game by reinitiazing Snake an apple
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        # Get the event from the input to perform some action
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    #on pressing Enter
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.snake.delay)


if __name__ == "__main__":
    game = Game()
    game.run()
