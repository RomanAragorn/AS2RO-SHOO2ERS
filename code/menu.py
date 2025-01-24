import pygame
import sys

#--------------------Game Menu--------------------#
class Menu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font('font\\Pixeled.ttf', 30)
        self.items_font = pygame.font.Font('font\\Pixeled.ttf', 15)
        self.menu_items = ["Start Game","High Scores", "Quit"]
        self.selected_item = 0

    def display_title(self):
        title_image = pygame.image.load('images\\text logo.png').convert_alpha()
        title_image = pygame.transform.scale(title_image, (776, 200))
        title_rect = title_image.get_rect(center=(self.screen_width / 2, 500))
        self.screen.blit(title_image, title_rect)

    def display_us(self):
        us_surf = self.items_font.render("Group 4", True, (255, 255, 255))
        us_rect = us_surf.get_rect(center=(self.screen_width / 2, 600))
        self.screen.blit(us_surf, us_rect)

    def display_menu(self):
        for index, item in enumerate(self.menu_items):
            color = 'white' if index == self.selected_item else 'gray'
            item_surf = self.items_font.render(item, True, color)
            item_rect = item_surf.get_rect(center=(self.screen_width / 2, 700 + index * 50))
            self.screen.blit(item_surf, item_rect)

    def run(self):
        # Draw the title and menu options
        self.display_title()
        self.display_us()
        self.display_menu()

class High_Scores:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.title_font = pygame.font.Font('font\\Pixeled.ttf', 30)
        self.items_font = pygame.font.Font('font\\Pixeled.ttf', 15)
        
        self.WHITE =  (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.FONT = pygame.font.Font('font\\Pixeled.ttf', 20)
        self.TITLE_FONT = pygame.font.Font('font\\Pixeled.ttf', 45)
        self.MESSAGE_FONT= pygame.font.Font('font\\Pixeled.ttf', 25)
        self.read_highscores() 

    def read_highscores(self):
        with open('records\\high_scores.txt', 'r') as file:
            content = file.readlines()
            cleaned_scores = []
            for i in range(3):
                if int(content[i]) > 0:
                    cleaned_scores.append(content[i].strip('\n').lstrip('0'))
                else:  
                    cleaned_scores.append('0')
            self.first_score = cleaned_scores[0]
            self.second_score = cleaned_scores[1] 
            self.third_score = cleaned_scores[2]

    def display_title(self):
        title_image = pygame.image.load('images\\high score.png').convert_alpha()
        title_image = pygame.transform.scale(title_image, (583, 150))
        title_rect = title_image.get_rect(center=(self.SCREEN_WIDTH / 2, 450))
        self.screen.blit(title_image, title_rect)  
    
    def display_trophies(self):
        self.trophies = pygame.image.load('images\\trophies.png').convert_alpha()
        self.trophies = pygame.transform.scale(self.trophies, (625, 573))
        self.trophies_rect = self.trophies.get_rect(center=(self.SCREEN_WIDTH / 2 + 35, self.SCREEN_HEIGHT/2 + 110))
        self.screen.blit(self.trophies, self.trophies_rect)

    def display_scores(self):
        
        # Displays 1st place score
        one_text = self.FONT.render(f"{self.first_score}", True, "gold")
        one_rect = one_text.get_rect(center = (self.SCREEN_WIDTH // 2 + 50, 610))
        self.screen.blit(one_text,one_rect)

        # Displays 1st place score
        two_text = self.FONT.render(f"{self.second_score}", True, "silver")
        two_rect = two_text.get_rect(center = (self.SCREEN_WIDTH // 2 + 50, 710))
        self.screen.blit(two_text,two_rect)

        # Displays 1st place score
        three_text = self.FONT.render(f"{self.third_score}", True, "brown")
        three_rect = three_text.get_rect(center = (self.SCREEN_WIDTH // 2 + 50, 810))
        self.screen.blit(three_text,three_rect)

    def display_esc(self):
        esc_message = self.MESSAGE_FONT.render("Press Esc to return", True, self.WHITE)
        esc_message_rect = esc_message.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 100))
        self.screen.blit(esc_message, esc_message_rect)

    def run(self):
        # Draw the title and menu options
        self.screen.fill((0,0,0))
        self.display_title()
        self.display_trophies()
        self.display_scores()
        self.display_esc()

class Pause:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font('font\\Pixeled.ttf', 30)
        self.items_font = pygame.font.Font('font\\Pixeled.ttf', 15)
        self.selected_item = 0

    def display_title(self):
        title_surf = self.title_font.render("PAUSED", False, 'white')
        title_rect = title_surf.get_rect(center=(self.screen_width / 2, 500))
        self.screen.blit(title_surf, title_rect)

    def display_return(self):
        return_surf = self.title_font.render("Return = Unpause", False, 'white')
        return_rect = return_surf.get_rect(center=(self.screen_width / 2, 700))
        self.screen.blit(return_surf, return_rect)

    def run(self):
        # Draw the title and menu options
        self.display_title()
        self.display_return()

class Game_Over:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font('font\\Pixeled.ttf', 30)
        self.items_font = pygame.font.Font('font\\Pixeled.ttf', 15)
        self.menu_items = ["Restart","Menu", "Quit"]
        self.selected_item = 0

    def display_title(self):
        title_image= pygame.image.load('images\\game over.png')
        title_image = pygame.transform.scale(title_image, (776, 200))
        title_rect = title_image.get_rect(center=(self.screen_width / 2, 500))
        self.screen.fill((0,0,0))
        self.screen.blit(title_image, title_rect)
    
    def display_menu(self):
        for index, item in enumerate(self.menu_items):
            color = 'red' if index == self.selected_item else 'gray'
            item_surf = self.items_font.render(item, True, color)
            item_rect = item_surf.get_rect(center=(self.screen_width / 2, 700 + index * 50))
            self.screen.blit(item_surf, item_rect)

    def run(self):
        # Draw the title and menu options
        self.display_title()
        self.display_menu()


    
   