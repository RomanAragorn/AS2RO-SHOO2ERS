import pygame
import sys
import os

def handle_fresh_file():
    with open('records\\high_scores.txt', 'r') as file: 
        content = file.readlines()
        if len(content) == 0:
            with open('records\\high_scores.txt', 'w') as high_scores:
                for i in range(10):
                    high_scores.write('0000000000\n')

def show_highscore_window(screen):  # Accept screen parameter
    # Set the screen dimensions if needed, but use the passed screen
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Fonts
    FONT = pygame.font.Font(None, 36)
    TITLE_FONT = pygame.font.Font('font\\Pixeled.ttf', 45)
    MESSAGE_FONT= pygame.font.Font('font\\Pixeled.ttf', 25)

    with open('records\\high_scores.txt', 'r') as file:
        content = file.readlines()
        first_score = content[0].strip('\n')  
        second_score = content[1].strip('\n')       
        third_score = content[2].strip('\n') 

    
    # Run the high-score window
    high_score_running = True
    while high_score_running:
        # Fill the screen with a color (BLACK)
        screen.fill(BLACK)

        # Display High Score Title
        title_text = TITLE_FONT.render("High Scores", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Top middle of the screen
        screen.blit(title_text, title_rect)


      # Display the "Press Esc to return" message at the bottom
        esc_message = MESSAGE_FONT.render("Press Esc to return", True, WHITE)
        esc_message_rect = esc_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(esc_message, esc_message_rect)
 
        pygame.display.flip()

        
        