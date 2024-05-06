import pygame
from random import randint, random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('My Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

myfont = pygame.font.SysFont('monospace', 50)

print("Pong6")
screen.fill(BLACK)
title = myfont.render("Single Player Pong:", False, GREEN)
screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() * 2))
pygame.display.update()
pygame.time.delay(1000)

# Countdown before start game
for i in range(3, 0, -1):
    screen.fill(BLACK)
    count_text = myfont.render(str(i), False, BLUE)
    screen.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - count_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1000)

def read_scores():
    try:
        with open("scores.txt", "r") as file:
            return [int(score) for score in file.readlines()]
    except FileNotFoundError:
        return []

def write_scores(scores):
    with open("scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")

def game():
    radius = 10
    x = WIDTH // 2
    y = radius
    score = 0
    ball_count = 1
    additional_ball = False

    pygame.draw.circle(screen, WHITE, (x, y), radius)  # Position is the center of the circle.

    paddle = {"width": 200,
              "height": 20,
              "color": YELLOW,
              "x": 0,
              "y": HEIGHT}
    paddle["x"] = WIDTH // 2 - paddle["width"] // 2
    paddle["y"] = HEIGHT - paddle["height"]
    pygame.draw.rect(screen, paddle["color"], (paddle["x"], paddle["y"], paddle["width"], paddle["height"]))

    speed = 5
    x_sens = y_sens = 1
    pause = False

    end = False
    while not end:
        screen.fill(BLACK)
        # Control the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle["x"] > 0:
            paddle["x"] -= speed
        if keys[pygame.K_RIGHT] and paddle["x"] < WIDTH - paddle["width"]:
            paddle["x"] += speed

        x += x_sens * speed
        y += y_sens * speed

        if x >= WIDTH - radius or x <= radius:
            x_sens *= -1

        if y <= radius:
            y_sens *= -1

        if paddle["x"] < x < paddle["x"] + paddle["width"] and paddle["y"] < y + radius < paddle["y"] + paddle["height"]:
            y_sens *= -1
            score += 1
            if score % 10 == 0:  # Accelerate every 10 points
                speed += 1
            if score % 50 == 0:  # Reduce paddle size every 50 points
                paddle["width"] -= 20
                paddle["x"] += 10  # Keep paddle centered
                if paddle["width"] < 20:
                    paddle["width"] = 20  # Minimum width for paddle

        if y >= HEIGHT - radius:
            end = True

        pygame.draw.circle(screen, RED, (x, y), radius)
        pygame.draw.rect(screen, paddle["color"], (paddle["x"], paddle["y"], paddle["width"], paddle["height"]))

        # Display the score in position (10, 0) (top left on the screen)
        score_text = myfont.render("Score: " + str(score), False, BLUE)
        screen.blit(score_text, (10, 0))

        pygame.display.update()
        pygame.time.delay(10)

    return score

# Main game loop
while True:
    current_score = game()
    best_scores = read_scores()
    best_scores.append(current_score)
    best_scores.sort(reverse=True)
    best_scores = best_scores[:5]  # Keep only the top 5 scores
    write_scores(best_scores)

    # Display Game Over message with best scores
    game_over_text = myfont.render("Game Over! Best Scores:", False, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    for i, score in enumerate(best_scores):
        score_text = myfont.render(str(i+1) + ": " + str(score), False, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + i * 50 + 50))
    pygame.display.update()

    # Wait for user input to play again or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    break
        else:
            continue
        break