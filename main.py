import pygame
import sys
import random
import time

# Inicialización de PyGame
pygame.init()

# Configuraciones básicas de pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Supervivencia Zombie")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
celeste = (173, 216, 230)
yellow = (255, 255, 0)
green = (144, 238, 144)  # Verde claro
blue = (0, 0, 255)  # Azul
orange = (255, 165, 0)  # Naranja

# Cargar sonidos
background_music = pygame.mixer.music.load('sounds/background.mp3')

# Reproducir música de fondo
pygame.mixer.music.play(-1)

# Cargar y redimensionar imágenes
player_img = pygame.transform.scale(pygame.image.load('images/player.png'), (50, 50))
zombie_normal_img = pygame.transform.scale(pygame.image.load('images/zombie_normal.png'), (50, 50))
zombie_fast_img = pygame.transform.scale(pygame.image.load('images/zombie_fast.png'), (50, 50))
zombie_strong_img = pygame.transform.scale(pygame.image.load('images/zombie_strong.png'), (50, 50))
refuge_img = pygame.transform.scale(pygame.image.load('images/refuge.png'), (100, 100))

# Crear el objeto clock para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Posición de los obstáculos
obstacles = [
    pygame.Rect(200, 150, 50, 50), 
    pygame.Rect(350, 300, 50, 50), 
    pygame.Rect(500, 450, 50, 50),
    pygame.Rect(350, 150, 50, 50)
]

# Función para dibujar el jugador
def draw_player(x, y):
    screen.blit(player_img, (x, y))

# Función para dibujar un zombie
def draw_zombie(zombie_pos, zombie_type):
    if zombie_type == 'fast':
        screen.blit(zombie_fast_img, (zombie_pos[0], zombie_pos[1]))
    elif zombie_type == 'strong':
        screen.blit(zombie_strong_img, (zombie_pos[0], zombie_pos[1]))
    else:
        screen.blit(zombie_normal_img, (zombie_pos[0], zombie_pos[1]))

# Función para crear un zombie
def create_zombie(player_x, player_y):
    zombie_type = random.choice(['normal', 'fast', 'strong'])
    zombie_speed = 1 if zombie_type == 'normal' else (2 if zombie_type == 'fast' else 0.5)

    while True:
        x, y = random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)
        if abs(x - player_x) > 200 and abs(y - player_y) > 200:
            break

    return [x, y], zombie_type, zombie_speed

# Función para mostrar el conteo regresivo
def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(black)
        text = font.render(str(i), True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

# Función para mostrar el menú
def show_menu():
    title_font = pygame.font.Font(None, 90)
    menu_font = pygame.font.Font(None, 74)
    menu_options = ["Iniciar Juego", "Salir"]
    selected_option = 0
    
    while True:
        screen.fill(black)
        
        # Mostrar título del juego
        title_text = title_font.render("Supervivencia Zombie", True, white)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4 - title_text.get_height() // 2))
        
        # Mostrar opciones del menú
        for i, option in enumerate(menu_options):
            color = green if i == selected_option else white
            text = menu_font.render(option, True, color)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 + i * 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        return  # Iniciar juego
                    elif selected_option == 1:
                        pygame.quit()
                        sys.exit()

# Función principal del juego
def main():
    show_menu()  # Mostrar el menú al inicio
    player_x, player_y = 50, 50
    player_speed = 5
    zombies = [create_zombie(player_x, player_y) for _ in range(5)]
    refuge = pygame.Rect(screen_width - 120, screen_height - 120, 100, 100)
    game_over = False

    # Mostrar el conteo regresivo antes de empezar
    countdown()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        new_player_x, new_player_y = player_x, player_y
        if keys[pygame.K_LEFT]:
            new_player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            new_player_x += player_speed
        if keys[pygame.K_UP]:
            new_player_y -= player_speed
        if keys[pygame.K_DOWN]:
            new_player_y += player_speed

        # Verificar colisión con obstáculos antes de mover al jugador
        player_rect = pygame.Rect(new_player_x, new_player_y, 50, 50)
        if not any(obstacle.colliderect(player_rect) for obstacle in obstacles):
            player_x, player_y = new_player_x, new_player_y

        # Mover zombies hacia el jugador
        for zombie in zombies:
            zombie_pos, zombie_type, zombie_speed = zombie
            new_zombie_x, new_zombie_y = zombie_pos[0], zombie_pos[1]
            
            if new_zombie_x < player_x:
                new_zombie_x += zombie_speed
            elif new_zombie_x > player_x:
                new_zombie_x -= zombie_speed
            if new_zombie_y < player_y:
                new_zombie_y += zombie_speed
            elif new_zombie_y > player_y:
                new_zombie_y -= zombie_speed

            # Verificar colisión con obstáculos antes de mover al zombie
            zombie_rect = pygame.Rect(new_zombie_x, new_zombie_y, 50, 50)
            if not any(obstacle.colliderect(zombie_rect) for obstacle in obstacles):
                zombie_pos[0], zombie_pos[1] = new_zombie_x, new_zombie_y
            else:
                # Rebotar en el obstáculo
                if abs(new_zombie_x - player_x) > abs(new_zombie_y - player_y):
                    new_zombie_x = zombie_pos[0] - zombie_speed if new_zombie_x > player_x else zombie_pos[0] + zombie_speed
                else:
                    new_zombie_y = zombie_pos[1] - zombie_speed if new_zombie_y > player_y else zombie_pos[1] + zombie_speed

                # Mover zombie después de rebotar
                zombie_pos[0], zombie_pos[1] = new_zombie_x, new_zombie_y

            # Verificar colisión con el jugador
            if pygame.Rect(zombie_pos[0], zombie_pos[1], 50, 50).colliderect(pygame.Rect(player_x, player_y, 50, 50)):
                game_over = True

        # Verificar si el jugador llegó al refugio
        if pygame.Rect(player_x, player_y, 50, 50).colliderect(refuge):
            screen.fill(black)
            font = pygame.font.Font(None, 74)
            text = font.render("¡Llegaste al refugio!", True, yellow)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            pygame.display.flip()
            time.sleep(3)
            return

        if game_over:
            screen.fill(black)
            font = pygame.font.Font(None, 74)
            text = font.render("¡Game Over!", True, white)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
            pygame.display.flip()
            time.sleep(3)
            return

        screen.fill(black)
        draw_player(player_x, player_y)
        for zombie in zombies:
            draw_zombie(zombie[0], zombie[1])
        for obstacle in obstacles:
            pygame.draw.rect(screen, blue, obstacle)
            pygame.draw.rect(screen, orange, obstacle.inflate(-4, -4))
        screen.blit(refuge_img, (screen_width - 120, screen_height - 120))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
