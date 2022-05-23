import arcade
import math
import random
import PIL
import winsound

TITLE = "Ball"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

PLAT_SPEED = 30
PLAT_WIDTH = 200
PLAT_HEIGHT = 15

BALL_SPEED = 20
BALL_SIZE = 10

BRICK_WIDTH = 40
BRICK_HEIGHT = 20

def sign(x):
    return -1 if x < 0 else 1

class MyProg(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)


    def sound_plat(self):
        winsound.Beep(1000, 10)


    def sound_wall(self):
        winsound.Beep(500, 10)


    def sound_bottom(self):
        winsound.Beep(100, 30)


    def sound_brick(self):
        pass # winsound.Beep(50, 2)


    def create_sprites(self):

        self.sprites_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.plat_list = arcade.SpriteList()
        self.brick_list = arcade.SpriteList()
        
        color = arcade.color.GREEN

        # Ball

        imageBall = PIL.Image.new('RGBA', (BALL_SIZE, BALL_SIZE), arcade.color.WHITE)

        textureBall = arcade.Texture(str(color), image=imageBall)
        self.ball_sprite = arcade.Sprite()
        self.ball_sprite.append_texture(textureBall)
        self.ball_sprite.set_texture(0)
        self.ball_sprite.center_x = SCREEN_WIDTH // 2
        self.ball_sprite.center_y = SCREEN_HEIGHT // 2
        self.sprites_list.append(self.ball_sprite)
        self.ball_list.append(self.ball_sprite)

        self.ball_sprite.change_x = int(random.randrange(-BALL_SPEED, BALL_SPEED))
        self.ball_sprite.change_y = int(math.sqrt(BALL_SPEED ** 2 - self.ball_sprite.change_x ** 2))

        # Plat

        imagePlat = PIL.Image.new('RGBA', (PLAT_WIDTH, PLAT_HEIGHT), arcade.color.YELLOW)

        texturePlat = arcade.Texture(str(arcade.color.YELLOW), image=imagePlat)
        self.plat_sprite = arcade.Sprite()
        self.plat_sprite.append_texture(texturePlat)
        self.plat_sprite.set_texture(0)
        self.plat_sprite.center_x = SCREEN_WIDTH // 2
        self.plat_sprite.center_y = PLAT_HEIGHT
        self.sprites_list.append(self.plat_sprite)
        self.plat_list.append(self.plat_sprite)

        # Brick

        for y in range(5):
            for x in range(SCREEN_WIDTH // (BRICK_WIDTH + 1) + 1):
                self.create_brick(x * (BRICK_WIDTH + 1), SCREEN_HEIGHT - 100 - y * (BRICK_HEIGHT + 1))


    def create_brick(self, x, y):
        
        color = (random.randrange(50, 256), random.randrange(50, 256), random.randrange(50, 256))
        imageBrick = PIL.Image.new('RGBA', (random.randrange(BRICK_WIDTH, BRICK_WIDTH + 10),
                                           random.randrange(BRICK_HEIGHT, BRICK_HEIGHT + 10)),
                                    color)

        textureBrick = arcade.Texture(str(color), image=imageBrick)
        sprite = arcade.Sprite()
        sprite.append_texture(textureBrick)
        sprite.set_texture(0)
        sprite.center_x = x
        sprite.center_y = y
        self.sprites_list.append(sprite)
        self.brick_list.append(sprite)
        

    def create_rand_brick(self):

        if random.randrange(10) == 5:
            y = random.choice(range(5))
            x = random.choice(range(SCREEN_WIDTH // (BRICK_WIDTH + 1) + 1))
            self.create_brick(x * (BRICK_WIDTH + 1), SCREEN_HEIGHT - 100 - y * (BRICK_HEIGHT + 1))


    def setup(self):

        self.create_sprites()
        self._score = 0


    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT and not self.is_hit_left(self.plat_sprite):
            self.plat_sprite.change_x = -PLAT_SPEED
        elif key == arcade.key.RIGHT and not self.is_hit_right(self.plat_sprite):
            self.plat_sprite.change_x = PLAT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.plat_sprite.change_x = 0            


    def is_hit_left(self, sprite):
        return  sprite.center_x <= sprite.width // 2


    def is_hit_right(self, sprite):
        return  sprite.center_x >= SCREEN_WIDTH - sprite.width // 2


    def is_hit_top(self, sprite):
        return  sprite.center_y >= SCREEN_HEIGHT - sprite.height // 2


    def is_hit_bottom(self, sprite):
        return  sprite.center_y <= sprite.height // 2

    
    def update(self, dt):

        self.sprites_list.update()

        # Ball Wall
        
        if self.is_hit_left(self.ball_sprite):
            self.ball_sprite.change_x = abs(self.ball_sprite.change_x)
            self.rand_move()
            self.create_rand_brick()
            self.sound_wall()
            self.score(-1)

        if self.is_hit_right(self.ball_sprite):
            self.ball_sprite.change_x = -abs(self.ball_sprite.change_x)
            self.rand_move()
            self.create_rand_brick()
            self.sound_wall()
            self.score(-1)

        if self.is_hit_top(self.ball_sprite):
            self.ball_sprite.change_y = -abs(self.ball_sprite.change_y)
            self.rand_move()
            self.create_rand_brick()
            self.sound_wall()
            self.score(-1)

        if self.is_hit_bottom(self.ball_sprite):
            self.ball_sprite.change_y = abs(self.ball_sprite.change_y)
            self.ball_sprite.change_y = abs(self.ball_sprite.change_y)
            self.ball_sprite.center_y = self.plat_sprite.center_y + BALL_SIZE // 2
            self.create_rand_brick()
            self.sound_bottom()
            self.score(-500)

        # Ball Plat
        
        plat_hit_list = arcade.check_for_collision_with_list(self.ball_sprite, self.plat_list)
        
        if self.plat_sprite in plat_hit_list:
            dx = self.ball_sprite.center_x - self.plat_sprite.center_x
            dx = int(100 * (dx / PLAT_WIDTH))
            
            if (dx > 0 and self.ball_sprite.change_x >= 0) or (dx < 0 and self.ball_sprite.change_x <= 0):
                dy = int(self.ball_sprite.change_y * (1 - abs(dx) / 100))
                if dy == 0:
                    dy = sign(self.ball_sprite.change_y)
                self.ball_sprite.change_x = sign(self.ball_sprite.change_x) * int(math.sqrt(BALL_SPEED ** 2 - dy ** 2))
                self.ball_sprite.change_y = dy
            elif (dx < 0 and self.ball_sprite.change_x >= 0) or (dx > 0 and self.ball_sprite.change_x <= 0):
                dy = int(self.ball_sprite.change_y / (1 - abs(dx) / 100))
                if abs(dy) >= BALL_SPEED:
                    dy = sign(self.ball_sprite.change_y) * (BALL_SPEED - 1)
                self.ball_sprite.change_x = sign(self.ball_sprite.change_x) * int(math.sqrt(BALL_SPEED ** 2 - dy ** 2))
                self.ball_sprite.change_y = dy

            self.ball_sprite.change_y = abs(self.ball_sprite.change_y)
            self.ball_sprite.center_y = self.plat_sprite.center_y + BALL_SIZE // 2
            self.score(1)
            self.sound_plat()

        # Plat Wall
        
        if self.is_hit_left(self.plat_sprite) or self.is_hit_right(self.plat_sprite):
            self.plat_sprite.change_x = 0

        # Ball Brick

        brick_hit_list = arcade.check_for_collision_with_list(self.ball_sprite, self.brick_list)
        for brick in brick_hit_list:
            brick.change_y -= 1
            brick.change_x = self.ball_sprite.change_x // 20
            brick.center_x += random.randrange(-3, 4)
            brick.center_y += random.randrange(-3, 4)
            self.rand_move()
            self.sound_brick()
            self.score(1)

        # Brick

        for brick in self.brick_list:
            if brick.change_y != 0:
                if random.randrange(30) == 10:
                    brick.change_y -= 1
            if brick.center_y <= -brick.height // 2:
                self.brick_list.remove(brick)
                self.sprites_list.remove(brick)

        # Plat Brick
        
        brick_hit_list = arcade.check_for_collision_with_list(self.plat_sprite, self.brick_list)
        for brick in brick_hit_list:
            self.brick_list.remove(brick)
            self.sprites_list.remove(brick)
            self.score(10)


    def rand_move(self):

        self.ball_sprite.change_x += random.randrange(-1, 2)

        if abs(self.ball_sprite.change_x) > BALL_SPEED:
            self.ball_sprite.change_x = sign(self.ball_sprite.change_x) * BALL_SPEED

        self.ball_sprite.change_y = sign(self.ball_sprite.change_y) * int(math.sqrt(BALL_SPEED ** 2 - self.ball_sprite.change_x ** 2))


    def on_draw(self):

        arcade.start_render()
        self.sprites_list.draw()
        arcade.draw_text(f"Score: {self._score}", 5, SCREEN_HEIGHT - 20, arcade.color.WHITE)


    def score(self, s):

        self._score += s

        
def main():

    prog = MyProg(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    prog.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        
