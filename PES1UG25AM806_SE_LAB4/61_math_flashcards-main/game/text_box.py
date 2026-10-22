
import pygame


class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = True
        self.max_length = 6

        self.font = pygame.font.SysFont(None, 34)

    def handle_event(self, event):
        """Handle clicks, digit input, and Backspace."""

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                # Submission is handled by GameEngine.
                pass

            elif event.unicode.isdigit():
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def clear(self):
        """Clear the answer field."""
        self.text = ""

    def render(self, surface):
        """Draw the input field and its current text."""

        border_color = (
            (70, 140, 240) if self.active
            else (110, 115, 125)
        )

        pygame.draw.rect(
            surface, (255, 255, 255),
            self.rect, border_radius=6
        )

        pygame.draw.rect(
            surface, border_color,
            self.rect, width=3, border_radius=6
        )

        text_surf = self.font.render(
            self.text, True, (25, 25, 30)
        )

        # Vertically center the text in the input field.
        text_x = self.rect.x + 12
        text_y = self.rect.centery - text_surf.get_height() // 2

        surface.blit(text_surf, (text_x, text_y))
