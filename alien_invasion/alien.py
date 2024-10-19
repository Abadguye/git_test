import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        """初始化外星人并设置起始位置"""
        super().__init__()
        self.screen = ai_game.screen

        # 加载外星人图像并设置其 rect 属性
        self.image = pygame.image.load('alien_invasion\images\\alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确水平位置
        self.x = float(self.rect.x)
