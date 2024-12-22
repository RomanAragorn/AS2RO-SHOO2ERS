    def display_game_over(self):
        
        pygame.mixer.music.stop()
        self.laser_audio.stop()
        self.explosion_audio.stop()
        
        screen.fill((0, 0, 0))

        # Display the game over message
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Restart", True, (255, 255, 255))
        quit_text = self.font.render("Quit", True, (255, 255, 255))

        # Center the text
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 4))
        score_rect = score_text.get_rect(center=(screen_width / 2, screen_height / 2))
        restart_rect = restart_text.get_rect(center=(screen_width / 2, screen_height / 1.5))
        quit_rect = quit_text.get_rect(center=(screen_width / 2, screen_height / 1.3))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)

        # Highlight selected option
        if self.selection == 0:
            restart_text = self.font.render("Restart", True, (255, 0, 0))  # Red color for selection
        else:
            quit_text = self.font.render("Quit", True, (255, 0, 0))  # Red color for selection

        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)