import pygame


HEADER = pygame.Rect(0, 0, 800, 50)
NAV = pygame.Rect(0, 50, 200, 390)
MAIN = pygame.Rect(200, 50, 600, 390)
FOOTER = pygame.Rect(0, 440, 800, 40)

def draw_layout(surface):

    pygame.draw.rect(surface, (40,40,40), HEADER)
    pygame.draw.rect(surface, (30,30,30), NAV)
    pygame.draw.rect(surface, (20,20,20), MAIN)
    pygame.draw.rect(surface, (40,40,40), FOOTER)

    pygame.draw.rect(surface, "#6A0505", HEADER, 1)
    pygame.draw.rect(surface, "#6A0505", NAV, 1)
    pygame.draw.rect(surface, "#6A0505", MAIN, 1)
    pygame.draw.rect(surface, "#6A0505", FOOTER, 1)