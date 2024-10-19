import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self) -> None:
        """初始化游戏并创建游戏资源"""
        # 初始化背景
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 创建一个显示窗口，指定游戏窗口的尺寸
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))

        # 全屏
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 设置标题
        pygame.display.set_caption("Alien Invasion")

        """Ship(self):此处的self指向的是当前AlienInvasion实例"""
        self.ship = Ship(self)
        # 存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 存储外星人的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # # 设置背景色
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            """检测新发⽣的事件、更新屏幕并让时钟计时"""
            self._check_events()
            self.ship.update()
            self._update_bullet()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # 侦听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
            # 按ESC退出游戏
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        """更新子弹的位置，删除已消失的子弹"""
        """对编组调⽤ update() 时，编组会⾃动对其中的每个精灵调用update()"""
        self.bullets.update()
        """在使⽤ for 循环遍历列表（或 Pygame 编组）时，
            Python要求该列表的⻓度在整个循环中保持不变。这意味着
            不能从 for 循环遍历的列表或编组中删除元素，因此必须遍历编组的副本
            """
        # 删除已消失子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            # print(len(self.bullets))
    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人,再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # current_x 表⽰我们要在屏幕上放置的下⼀个外星⼈的⽔平位置
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height-3*alien_height):
            # 只要余下的空间超过外星⼈宽度的两倍,就继续执⾏循环，再添加⼀个外星⼈
            while current_x < (self.settings.screen_width-alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """创建一个外星人，并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position

        self.aliens.add(new_alien)

    def _update_screen(self):
        # 每次循环时，重绘屏幕
        """绘制背景"""
        self.screen.fill(self.settings.bg_color)
        """bullets.sprites() ⽅法返回⼀个列表，其中包含 bullets 编组中的所有精灵。"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        """绘制飞船"""
        self.ship.blitme()
        """当对编组调⽤ draw() 时，Pygame 将把编组中的每个元素绘制到属性rect 指定的位置上。
        ⽅法 draw() 接受⼀个参数，这个参数指定了要将编组中的元素绘制到哪个 surface 上。"""
        self.aliens.draw(self.screen)

        # 不断更新屏幕，以显⽰新位置上的元素并隐藏原来位置上的元素
        """
        当你对屏幕上的像素进行绘制或更改后，这些更改并不会立即
        反映在屏幕上，而是被保存在一个称为“屏幕缓冲区”或“帧缓冲区”的
        区域中。pygame.display.flip() 函数的作用就是将这个缓冲区
        的内容复制到实际的显示屏幕上，从而让你看到最新的绘制结果。
        """
        pygame.display.flip()


"""
在Python中，每个Python文件（也被称为模块）都有一个内置的属性 __name__。
当这个文件被直接运行时，__name__ 的值会被设置为 '__main__'。
而当这个文件被其他文件导入（作为一个模块）时，
 __name__ 的值则会被设置为该文件的模块名。
"""
if __name__ == '__main__':
    # 创建实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
