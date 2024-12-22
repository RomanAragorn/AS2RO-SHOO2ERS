import pygame
import sys

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
        title_surf = self.title_font.render("As2ro Shoo2ers", True, 'white')
        title_rect = title_surf.get_rect(center=(self.screen_width / 2, 200))
        self.screen.blit(title_surf, title_rect)

    def display_menu(self):
        for index, item in enumerate(self.menu_items):
            color = 'white' if index == self.selected_item else 'gray'
            item_surf = self.items_font.render(item, True, color)
            item_rect = item_surf.get_rect(center=(self.screen_width / 2, 300 + index * 50))
            self.screen.blit(item_surf, item_rect)

    def run(self):
        # Draw the title and menu options
        self.display_title()
        self.display_menu()