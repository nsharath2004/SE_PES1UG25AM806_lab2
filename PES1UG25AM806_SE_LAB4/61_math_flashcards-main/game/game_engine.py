
import random
import pygame

from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Score and attempt tracking
        self.score = 0
        self.total_attempts = 0

        # Feedback
        self.feedback_msg = "Solve the card and press Enter!"
        self.feedback_color = (200, 205, 215)

        # Current arithmetic question
        self.num_a = 0
        self.num_b = 0
        self.operator = "+"

        # Timer
        self.question_time = 15.0
        self.time_left = self.question_time
        self.timeout_handled = False

        # Streak and multiplier
        self.streak = 0
        self.multiplier = 1
        self.max_multiplier = 5

        # Input and submit button
        box_w, box_h = 130, 44
        self.input_box = TextBox(
            width // 2 - 110, 260, box_w, box_h
        )
        self.submit_btn = pygame.Rect(
            width // 2 + 30, 260, 90, box_h
        )

        # Fonts
        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 24)
        self.font_card = pygame.font.SysFont(None, 56)
        self.font_btn = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 21)

        self.generate_new_card()

    def generate_new_card(self):
        """Generate an arithmetic question with a valid answer."""

        self.operator = random.choice(["+", "-", "*", "/"])

        if self.operator == "/":
            # Generate division with no remainder.
            divisor = random.randint(2, 12)
            quotient = random.randint(2, 12)

            self.num_a = divisor * quotient
            self.num_b = divisor

        else:
            self.num_a = random.randint(3, 15)
            self.num_b = random.randint(2, 12)

            # Avoid negative subtraction questions.
            if self.operator == "-" and self.num_a < self.num_b:
                self.num_a, self.num_b = self.num_b, self.num_a

        self.time_left = self.question_time
        self.timeout_handled = False
        self.input_box.clear()

    def compute_expected_answer(self):
        """Calculate the answer using the active operator."""

        if self.operator == "+":
            return self.num_a + self.num_b

        if self.operator == "-":
            return self.num_a - self.num_b

        if self.operator == "*":
            return self.num_a * self.num_b

        if self.operator == "/":
            if self.num_b == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")

            if self.num_a % self.num_b != 0:
                raise ValueError("Division must produce a whole number.")

            return self.num_a // self.num_b

        raise ValueError(f"Unsupported operator: {self.operator}")

    def submit_answer(self):
        """Validate the input, score the answer, and update feedback."""

        # Do not accept answers after a timeout.
        if self.timeout_handled:
            return

        val_str = self.input_box.text.strip()

        # Empty input must not crash or consume an attempt.
        if not val_str:
            self.feedback_msg = "Type an answer first!"
            self.feedback_color = (240, 175, 40)
            return

        try:
            user_answer = int(val_str)
        except ValueError:
            self.feedback_msg = "Please enter a valid integer."
            self.feedback_color = (240, 175, 40)
            return

        expected = self.compute_expected_answer()
        self.total_attempts += 1

        if user_answer == expected:
            self.streak += 1

            # Increase multiplier every three consecutive correct answers.
            self.multiplier = min(
                self.max_multiplier,
                1 + (self.streak - 1) // 3
            )

            points = self.multiplier
            self.score += points

            self.feedback_msg = (
                f"CORRECT! {self.num_a} {self.operator} "
                f"{self.num_b} = {expected} | +{points} points"
            )
            self.feedback_color = (80, 230, 110)

            self.generate_new_card()

        else:
            self.streak = 0
            self.multiplier = 1

            self.feedback_msg = f"WRONG! Expected {expected}."
            self.feedback_color = (240, 75, 75)

            self.input_box.clear()

    def handle_timeout(self):
        """Register one missed attempt when the timer expires."""

        if self.timeout_handled:
            return

        self.timeout_handled = True
        self.total_attempts += 1

        self.streak = 0
        self.multiplier = 1

        self.feedback_msg = "TIME UP! The next question is ready."
        self.feedback_color = (240, 100, 90)

        # Generate the next question and reset its timer.
        self.generate_new_card()

        # Preserve the timeout message until the next submission.
        self.timeout_handled = False

    def handle_event(self, event):
        """Handle keyboard and mouse events."""

        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_answer()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_answer()

    def update(self, dt):
        """Update the countdown using elapsed seconds."""

        if self.timeout_handled:
            return

        self.time_left = max(0.0, self.time_left - dt)

        if self.time_left <= 0.0:
            self.handle_timeout()

    def render(self, screen):
        """Draw the complete game interface."""

        screen.fill((25, 29, 37))

        # Title
        title_surf = self.font_title.render(
            "Math Flashcards Arena", True, (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (self.width // 2 - title_surf.get_width() // 2, 15)
        )

        # Score and attempts
        hud_text = (
            f"Score: {self.score}    Attempts: {self.total_attempts}"
        )
        hud_surf = self.font_hud.render(
            hud_text, True, (255, 220, 80)
        )
        screen.blit(
            hud_surf,
            (self.width // 2 - hud_surf.get_width() // 2, 55)
        )

        # Streak and multiplier
        streak_text = (
            f"Streak: {self.streak}    Multiplier: x{self.multiplier}"
        )
        streak_surf = self.font_small.render(
            streak_text, True, (120, 200, 255)
        )
        screen.blit(
            streak_surf,
            (self.width // 2 - streak_surf.get_width() // 2, 82)
        )

        # Arithmetic card
        card_rect = pygame.Rect(
            self.width // 2 - 130, 112, 260, 105
        )

        pygame.draw.rect(
            screen, (240, 242, 245), card_rect, border_radius=12
        )
        pygame.draw.rect(
            screen, (85, 120, 175), card_rect,
            width=3, border_radius=12
        )

        card_str = f"{self.num_a}  {self.operator}  {self.num_b}"
        card_surf = self.font_card.render(
            card_str, True, (25, 30, 42)
        )
        screen.blit(
            card_surf,
            (
                card_rect.centerx - card_surf.get_width() // 2,
                card_rect.centery - card_surf.get_height() // 2
            )
        )

        # Timer label and bar
        timer_label = self.font_small.render(
            f"Time left: {self.time_left:.1f}s",
            True, (225, 230, 240)
        )
        screen.blit(
            timer_label,
            (self.width // 2 - timer_label.get_width() // 2, 225)
        )

        bar_width = 280
        bar_height = 10
        bar_x = self.width // 2 - bar_width // 2
        bar_y = 245

        ratio = max(
            0.0, min(1.0, self.time_left / self.question_time)
        )

        pygame.draw.rect(
            screen, (65, 70, 80),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=5
        )

        if ratio > 0.5:
            timer_color = (70, 220, 110)
        elif ratio > 0.25:
            timer_color = (245, 180, 55)
        else:
            timer_color = (240, 75, 75)

        if ratio > 0:
            pygame.draw.rect(
                screen, timer_color,
                (bar_x, bar_y, int(bar_width * ratio), bar_height),
                border_radius=5
            )

        # Input box and submit button
        self.input_box.render(screen)

        pygame.draw.rect(
            screen, (45, 140, 80),
            self.submit_btn, border_radius=6
        )
        pygame.draw.rect(
            screen, (215, 225, 220),
            self.submit_btn, width=2, border_radius=6
        )

        btn_txt = self.font_btn.render(
            "SUBMIT", True, (255, 255, 255)
        )
        screen.blit(
            btn_txt,
            (
                self.submit_btn.centerx - btn_txt.get_width() // 2,
                self.submit_btn.centery - btn_txt.get_height() // 2
            )
        )

        # Feedback
        msg_surf = self.font_small.render(
            self.feedback_msg, True, self.feedback_color
        )

        # Keep long messages inside the window.
        msg_x = max(
            10, self.width // 2 - msg_surf.get_width() // 2
        )
        screen.blit(msg_surf, (msg_x, 325))
