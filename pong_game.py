import pygame
import sys
import os
import wave
import struct
import math

# --- Utility function to generate .wav sounds ---
def generate_beep(filename, freq=440.0, duration=0.2, volume=0.5, samplerate=44100):
    """Generate a simple beep .wav file."""
    if os.path.exists(filename):
        return  # Don't overwrite if already exists

    n_samples = int(samplerate * duration)
    wav_file = wave.open(filename, 'w')
    wav_file.setparams((1, 2, samplerate, n_samples, 'NONE', 'not compressed'))

    for i in range(n_samples):
        value = int(volume * 32767.0 * math.sin(2.0 * math.pi * freq * (i / samplerate)))
        wav_file.writeframes(struct.pack('<h', value))

    wav_file.close()


# --- Game setup ---
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Sound")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddles and ball
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20

player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

ball_speed = [4, 4]
paddle_speed = 6

# --- Ensure sound files exist ---
generate_beep("hit_sound.wav", freq=600.0, duration=0.1)   # higher pitch
generate_beep("score_sound.wav", freq=200.0, duration=0.3) # lower pitch

# Load sounds
hit_sound = pygame.mixer.Sound("hit_sound.wav")
score_sound = pygame.mixer.Sound("score_sound.wav")

# Score
player_score = 0
ai_score = 0
font = pygame.font.SysFont(None, 48)


# --- Main game loop ---
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.top > 0:
        player_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_s] and player_paddle.bottom < HEIGHT:
        player_paddle.move_ip(0, paddle_speed)

    # Ball movement
    ball.move_ip(ball_speed[0], ball_speed[1])

    # Collision with top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed[0] = -ball_speed[0]
        hit_sound.play()

    # AI paddle follows the ball
    if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
        ai_paddle.move_ip(0, paddle_speed)
    elif ai_paddle.centery > ball.centery and ai_paddle.top > 0:
        ai_paddle.move_ip(0, -paddle_speed)

    # Score check
    if ball.left <= 0:
        ai_score += 1
        score_sound.play()
        ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        ball_speed = [4, 4]

    if ball.right >= WIDTH:
        player_score += 1
        score_sound.play()
        ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        ball_speed = [-4, 4]

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    player_text = font.render(str(player_score), True, WHITE)
    ai_text = font.render(str(ai_score), True, WHITE)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(ai_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(60)
