import pygame
from plane_sprites import *

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")

        # 1. 创建游戏的窗口
        self.screen = pygame.dis#这个模块放一些常用的工具和基础类和精灵类
#在其他模块调用
import pygame
import random
#设置游戏屏幕大小 这是一个常量
SCREEN_RECT = pygame.Rect(0,0,580,700)
#敌机的定时器事件常量
CREATE_ENEMY_EVENT = pygame.USEREVENT

#定制一个精灵类，需要继承pygame提供的精灵类
#需要定义的属性有：
#image图片
#rect坐标
#speed速度

#接下来开始写敌机方面的内容 产生敌机
#先定义一个事件常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
#我们还可以定义一个事件常量(发射子弹)
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,new_image,new_speed=1):
        super().__init__()
        #图片
        self.image = pygame.image.load(new_image)
        #速度
        self.speed = new_speed
        #位置 获取图片的宽和高 get_rect()(0,0,宽，高)
        self.rect = self.image.get_rect()
        #精灵移动的速度 包括英雄精灵 背景精灵 敌机精灵 子弹精灵
        self.speed = new_speed

    def update(self):
        #默认垂直方向移动 y轴控制垂直方向
        self.rect.y += self.speed
        #self.rect.x += 1
#以上是游戏的基础类，接下来设置背景类
#明确背景类继承自游戏的精灵类
class Background(GameSprite):
    def __init__(self,is_alt = False):
        #is_alt判断是否为另一张图像
        #False表示第一张图像
        #Ture表示另外一张图像
        #两张图像交替循环
        #传图片
        super().__init__("/home/liutingting/下载/beijing.png")
        if is_alt:
            #如果是第二张图片 初始位置为-self.rect.height
            self.rect.y = -self.rect.height
    #def __init__(self,new_image):
    #   super().init__(new_image)
    def update(self):
        #调用父类方法
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height
#敌机出场
class Enemy(GameSprite):
    #敌机精灵
    def __init__(self):
        #1 调用父类方法 创建敌机精灵 并且指定敌机图像
        super().__init__("/home/liutingting/桌面/images/enemy1.png")

        #2 设置敌机的随机初始速度1~3
        self.speed = random.randint(2,6)
        #3 设置敌机的随机初始位置
        self.rect.bottom = 0
        max_x =SCREEN_RECT.width -self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):
        #1 调用父类方法 让敌机在垂直方向运动
        super().update()

        #2 判断是否飞出屏幕 如果是 需要将敌机从精灵组删除
        if self.rect.y >= SCREEN_RECT.height:
            #print("敌机飞出屏幕")
            #将精灵从精灵组中删除
            self.kill()

#英雄出场
class Hero(GameSprite):
    def __init__(self):
        super().__init__("/home/liutingting/桌面/images/life.png",0)
        self.bullet = pygame.sprite.Group()
        #设置初始位置
        self.rect.center =SCREEN_RECT.center
        self.rect.bottom =SCREEN_RECT.bottom-120
        self.move = False
    def update(self):
        #super().update()
        if not self.move:
            self.rect.x += self.speed
        else:
            self.rect.y += self.speed

        #self.rect.y += self.speed
        #飞机飞出屏幕
        if self.rect.bottom <= 0:
            self.rect.y = self.rect.bottom+SCREEN_RECT.height
        elif self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height

        if self.rect.right <= 0:
            self.rect.x = self.rect.right+SCREEN_RECT.width
        elif self.rect.x >= SCREEN_RECT.width:
            self.rect.x = -self.rect.width
    def fire(self):
        #print("发射子弹")

        for i in (1,2,3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y-i*20
            bullet.rect.center = self.rect.center
            self.bullet.add(bullet)


#子弹精灵
class Bullet(GameSprite):

    def __init__(self):
        super().__init__("/home/liutingting/桌面/images/bullet1.png",-5)
    def update(self, play=None):
        super().update()

        #判断是否超出屏幕 如果是 从精灵组删除
        if self.rect.bottom < 0:
            self.kill()
            play.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        # 4. 设置定时器事件 - 创建敌机　1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):

        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出场...")
                # 创建敌机精灵
                enemy = Enemy()

                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右移动...")

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):

        # 1. 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 2. 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表时候有内容
        if len(enemies) > 0:

            # 让英雄牺牲
            self.hero.kill()

            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("游戏结束")

        pygame.quit()
        exit()

if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()

    # 启动游戏
    game.start_game()
