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
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

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

        first_text = FONT.render("1st: ", True, WHITE)
        first_rect = first_text.get_rect(center = (SCREEN_WIDTH // 2, 150))
        screen.blit(first_text,first_rect)

        # Displays 1st place score
        one_text = FONT.render(f"{first_score}", True, WHITE)
        one_rect = one_text.get_rect(center = (SCREEN_WIDTH // 2, 200))
        screen.blit(one_text,one_rect)

        second_text = FONT.render("2nd: ", True, WHITE)
        second_rect = second_text.get_rect(center = (SCREEN_WIDTH // 2, 250))
        screen.blit(second_text,second_rect)

        # Displays 1st place score
        two_text = FONT.render(f"{second_score}", True, WHITE)
        two_rect = two_text.get_rect(center = (SCREEN_WIDTH // 2, 300))
        screen.blit(two_text,two_rect)

        third_text = FONT.render("3rd: ", True, WHITE)
        third_rect = third_text.get_rect(center = (SCREEN_WIDTH // 2, 350))
        screen.blit(third_text,third_rect)

        # Displays 1st place score
        three_text = FONT.render(f"{third_score}", True, WHITE)
        three_rect = three_text.get_rect(center = (SCREEN_WIDTH // 2, 400))
        screen.blit(three_text,three_rect)
       

      # Display the "Press Esc to return" message at the bottom
        esc_message = MESSAGE_FONT.render("Press Esc to return", True, WHITE)
        esc_message_rect = esc_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(esc_message, esc_message_rect)
 
        pygame.display.flip()

        
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to return to the main menu
                    high_score_running = False
