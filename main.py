# main.py
import pygame
import sys
import math
import random
from config import *
from physics_engine import PhysicsWorld

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.life = 1.0
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.02

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * self.life)
            color_with_alpha = (*self.color[:3], alpha)
            surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(surf, color_with_alpha, (4, 4), int(4 * self.life))
            surface.blit(surf, (self.x - 4, self.y - 4))


def draw_rounded_rect_with_shadow(surface, color, rect, radius, shadow_offset=5, shadow_blur=5):
    # Draw Shadow
    shadow_surf = pygame.Surface((rect.width + shadow_blur*2, rect.height + shadow_blur*2), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 100), (shadow_blur, shadow_blur, rect.width, rect.height), border_radius=radius)
    surface.blit(shadow_surf, (rect.x - shadow_blur + shadow_offset, rect.y - shadow_blur + shadow_offset))
    # Draw Main Rect
    pygame.draw.rect(surface, color, rect, border_radius=radius)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pendulum Stacker")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        try:
            self.font_large = pygame.font.SysFont("Segoe UI", 64, bold=True)
            self.font_medium = pygame.font.SysFont("Segoe UI", 32, bold=True)
            self.font_small = pygame.font.SysFont("Segoe UI", 24)
        except:
            self.font_large = pygame.font.Font(None, 64)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)

        self.state = "START"
        self.particles = []
        self.reset_game()

    def reset_game(self):
        self.world = PhysicsWorld()
        self.score = 0
        self.wind_force = 0
        self.last_wind_change = 0
        self.particles.clear()
        self.state = "PLAYING"

    def handle_environment(self):
        now = pygame.time.get_ticks() / 1000
        if now - self.last_wind_change > WIND_CHANGE_TIME:
            self.wind_force = random.choice([-WIND_STRENGTH, 0, WIND_STRENGTH])
            self.last_wind_change = now

        self.world.crane_body.apply_force_at_world_point((self.wind_force, 0), self.world.crane_body.position)
        for shape in self.world.blocks:
            if shape.body.position.y < HEIGHT - 80:
                shape.body.apply_force_at_world_point((self.wind_force * 0.3, 0), shape.body.position)

    def draw_background(self):
        # Draw gradient background (top to bottom)
        color_top = (22, 24, 36)
        color_bottom = DARK_BG
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
            
        # Draw simple stylized floor
        pygame.draw.rect(self.screen, (30, 32, 45), (0, HEIGHT - 20, WIDTH, 20))
        pygame.draw.rect(self.screen, BLUE, (0, HEIGHT - 20, WIDTH, 2))

    def draw_glass_panel(self, rect):
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, GLASS_BG, (0, 0, rect.width, rect.height), border_radius=20)
        pygame.draw.rect(panel, (255, 255, 255, 30), (0, 0, rect.width, rect.height), width=2, border_radius=20)
        self.screen.blit(panel, rect.topleft)

    def run(self):
        self.state = "START"
        while True:
            dt = 1/FPS
            self.draw_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.state == "START":
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                    elif self.state == "PLAYING":
                        if event.key == pygame.K_SPACE:
                            spawn_pos = self.world.crane_body.position + (0, 25)
                            inheritance = self.world.crane_body.velocity
                            self.world.create_block(spawn_pos, inheritance)
                            self.score += 1
                            # Add particles
                            for _ in range(15):
                                self.particles.append(Particle(spawn_pos.x, spawn_pos.y, BLUE))
                    elif self.state == "GAME_OVER":
                        if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                            self.reset_game()

            if self.state == "PLAYING":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and self.world.anchor_body.position.x > 50:
                    self.world.anchor_body.position -= (CRANE_SPEED, 0)
                if keys[pygame.K_RIGHT] and self.world.anchor_body.position.x < WIDTH - 50:
                    self.world.anchor_body.position += (CRANE_SPEED, 0)

                self.handle_environment()
                self.world.update(dt)

                for shape in self.world.blocks:
                    if shape.body.position.x < -100 or shape.body.position.x > WIDTH + 100 or shape.body.position.y > HEIGHT + 100:
                        self.state = "GAME_OVER"
                        
            # Update particles
            for p in self.particles[:]:
                p.update()
                if p.life <= 0:
                    self.particles.remove(p)

            # --- RENDER GAME WORLD ---
            # 1. Draw Rope (Line between anchor and crane)
            pygame.draw.line(self.screen, (200, 200, 200), self.world.anchor_body.position, self.world.crane_body.position, 3)
            pygame.draw.circle(self.screen, WHITE, (int(self.world.anchor_body.position.x), int(self.world.anchor_body.position.y)), 6)
            
            # 2. Draw Crane Head (Rotating)
            c_pos = self.world.crane_body.position
            c_angle = math.degrees(self.world.crane_body.angle)
            c_surf = pygame.Surface((100, 20), pygame.SRCALPHA)
            pygame.draw.rect(c_surf, RED, (0, 0, 100, 20), border_radius=5)
            # Add crane highlight
            pygame.draw.rect(c_surf, (255, 100, 150), (2, 2, 96, 4), border_radius=2)
            c_rot = pygame.transform.rotate(c_surf, -c_angle)
            self.screen.blit(c_rot, c_rot.get_rect(center=(c_pos.x, c_pos.y)))

            # 3. Draw Blocks
            for shape in self.world.blocks:
                pos = shape.body.position
                angle = math.degrees(shape.body.angle)
                
                # We need a surface large enough to rotate
                b_surf = pygame.Surface((BLOCK_SIZE[0]+20, BLOCK_SIZE[1]+20), pygame.SRCALPHA)
                
                # Draw main block
                rect_obj = pygame.Rect(10, 10, BLOCK_SIZE[0], BLOCK_SIZE[1])
                pygame.draw.rect(b_surf, BLUE, rect_obj, border_radius=8)
                pygame.draw.rect(b_surf, WHITE, rect_obj, width=2, border_radius=8)
                
                # Inner glow/detail
                inner_rect = pygame.Rect(15, 15, BLOCK_SIZE[0]-10, BLOCK_SIZE[1]-10)
                pygame.draw.rect(b_surf, (255, 255, 255, 60), inner_rect, border_radius=4)

                b_rot = pygame.transform.rotate(b_surf, -angle)
                self.screen.blit(b_rot, b_rot.get_rect(center=(pos.x, pos.y)))

            # Draw particles
            for p in self.particles:
                p.draw(self.screen)

            # --- RENDER UI ---
            score_text = self.font_medium.render(f"SCORE: {self.score}", True, BLUE)
            self.screen.blit(score_text, (20, 20))
            
            if self.wind_force != 0 and self.state == "PLAYING":
                wind_dir = ">>" if self.wind_force > 0 else "<<"
                wind_color = (200, 200, 255, max(0, int(abs(math.sin(pygame.time.get_ticks()/200)) * 255)))
                wind_surf = self.font_medium.render(f"WIND {wind_dir}", True, WHITE)
                wind_surf.set_alpha(wind_color[3])
                self.screen.blit(wind_surf, (WIDTH - 150, 20))

            if self.state == "START":
                panel_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 300)
                self.draw_glass_panel(panel_rect)
                
                title = self.font_large.render("STACKER", True, RED)
                subtitle = self.font_small.render("Press SPACE to play & drop blocks", True, TEXT_COLOR)
                controls = self.font_small.render("Use LEFT / RIGHT arrows to move", True, TEXT_COLOR)
                
                self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
                self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))
                self.screen.blit(controls, controls.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))

            elif self.state == "GAME_OVER":
                panel_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 300)
                self.draw_glass_panel(panel_rect)
                
                title = self.font_large.render("GAME OVER", True, RED)
                score_display = self.font_medium.render(f"Final Score: {self.score}", True, BLUE)
                subtitle = self.font_small.render("Press SPACE to restart", True, TEXT_COLOR)
                
                self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)))
                self.screen.blit(score_display, score_display.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))
                self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 70)))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()