import math
import random
import PIL
import arcade

TITLE = "Python"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CHUNK_SIZE = 20

MOVEMENT_SPEED = 5
ANGLE_SPEED = 10
CHUNK_DIST = 5
INIT_CHUNK_COUNT = 5
RABBIT_COUNT = 200

TONG_WIDTH = 1
TONG_HEIGHT = 10


class Chunk(arcade.Sprite):

    def __init__(self, first=True):

        super().__init__()
        self.speed = 1 if first else 0

        color = arcade.color.GREEN if first else arcade.color.GO_GREEN
        image = PIL.Image.new('RGBA', (CHUNK_SIZE, CHUNK_SIZE), color)
        texture = arcade.Texture(str(color), image=image)
        self.append_texture(texture)
        self.set_texture(0)        


    def update(self):

        angle_rad = math.radians(self.angle)
        self.angle += self.change_angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)


class Rabbit(arcade.Sprite):

    def __init__(self):

        super().__init__()

        color = arcade.color.WHITE
        image = PIL.Image.new('RGBA', (CHUNK_SIZE, CHUNK_SIZE), color)
        texture = arcade.Texture(str(color), image=image)
        self.append_texture(texture)
        self.set_texture(0)
        self.angle = random.randrange(0, 360)
        self.center_x = random.randrange(0, SCREEN_WIDTH)
        self.center_y = random.randrange(0, SCREEN_HEIGHT)


    def update(self):
        pass
      

class MyProg(arcade.Window):

    def __init_(self, width, height, title):
        
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)


    def create_chunk(self):

        chunk = Chunk(len(self.chunk_list) == 0)

        last_chunk = None
        if len(self.chunk_list) > 0:
            last_chunk = self.chunk_list[-1]

        x = SCREEN_WIDTH // 2 if last_chunk == None else last_chunk.center_x
        y = SCREEN_HEIGHT // 2 if last_chunk == None else last_chunk.center_y

        chunk.center_x = x
        chunk.center_y = y
        
        self.sprite_list.append(chunk)
        self.chunk_list.append(chunk)
        self.make_tail()


    def first_chunk(self):

        return self.chunk_list[0]

    def make_tail(self):

        for junk in self.junk_list:
            junk.change_angle = 0
        for chunk in self.chunk_list:
            chunk.change_angle = 0
        self.chunk_list[-1].change_angle = 45
    

    def setup(self):
        
        self.sprite_list = arcade.SpriteList()
        self.chunk_list = arcade.SpriteList()
        self.junk_list = arcade.SpriteList()
        self.rabbit_list = arcade.SpriteList()

        self.track = list()
        self.tick = 0

        for i in range(INIT_CHUNK_COUNT):
            self.create_chunk()

        for i in range(RABBIT_COUNT):
            rabbit = Rabbit()
            self.rabbit_list.append(rabbit)
            self.sprite_list.append(rabbit)

        color = arcade.color.RED
        image = PIL.Image.new('RGBA', (TONG_WIDTH, TONG_HEIGHT), color)
        texture = arcade.Texture(str(color), image=image)
        self.tong = arcade.Sprite()
        self.tong.append_texture(texture)
        self.tong.set_texture(0)
        self.sprite_list.append(self.tong)
        self.update_tong()
        

    def update_tong(self):

        self.tong.center_x = self.first_chunk().center_x + ((CHUNK_SIZE + TONG_HEIGHT) / 2) * math.cos(math.radians(self.first_chunk().angle + 90))
        self.tong.center_y = self.first_chunk().center_y + ((CHUNK_SIZE + TONG_HEIGHT) / 2) * math.sin(math.radians(self.first_chunk().angle + 90))
        self.tong.angle = self.first_chunk().angle + random.randrange(-30, 31)


    def update(self, dt):

        self.sprite_list.update()
        self.update_tong()

        if self.first_chunk().speed > 1:
            self.to_track()
            for t, chunk in zip(self.track[-1::-CHUNK_DIST], self.chunk_list):
                if chunk is not self.first_chunk():
                    chunk.center_x = t[0]
                    chunk.center_y = t[1]
                    chunk.angle = t[2]
        elif self.first_chunk().speed == 1:
            self.to_track()
            for t, chunk in zip(self.track[-1::-CHUNK_DIST], self.chunk_list):
                if chunk is not self.first_chunk():
                    chunk.center_x = t[0]
                    chunk.center_y = t[1]
                    chunk.angle = t[2]
        else:
            for chunk in self.chunk_list:
                chunk.angle += random.randrange(-1, 2)

        if self.first_chunk().speed != 0:
            self.tick += 0.6
            if self.first_chunk().change_angle > 5:
                self.first_chunk().change_angle = ANGLE_SPEED + 5 * math.cos(self.tick)
            elif self.first_chunk().change_angle < -5:
                self.first_chunk().change_angle = -ANGLE_SPEED + 5 * math.cos(self.tick)
            else:
                self.first_chunk().change_angle = 5 * math.cos(self.tick)
        elif -5 <= self.first_chunk().change_angle <= 5:
            self.first_chunk().change_angle = 0

        # Rabbit
        
        rabbit_hit_list = arcade.check_for_collision_with_list(self.first_chunk(), self.rabbit_list)
        for rabbit in rabbit_hit_list:
            self.rabbit_list.remove(rabbit)
            self.sprite_list.remove(rabbit)
            self.create_chunk()

        for rabbit in self.rabbit_list:
            if random.randrange(len(self.rabbit_list)) == 1:
                rabbit.center_x += random.randrange(-20, 21)
                rabbit.center_y += random.randrange(-20, 21)
                rabbit.angle += random.randrange(-45, 46)
            rabbit.angle += random.randrange(-2, 3)

        # Chunks
        
        chunk_hit_list = arcade.check_for_collision_with_list(self.tong, self.chunk_list)
        for chunk in self.chunk_list[:INIT_CHUNK_COUNT]:
            try:
                chunk_hit_list.remove(chunk)
            except Exception:
                pass
            
        if len(chunk_hit_list) > 0:
            while True:
                chunk = self.chunk_list.pop()
                self.junk_list.append(chunk)
                if chunk is chunk_hit_list[0]:
                    break
            self.make_tail()
            
        # Junk

        for junk in self.junk_list:
            junk.center_x += random.randrange(-1, 2)
            junk.center_y += random.randrange(-1, 2)
            junk.angle += random.randrange(-5, 6)

        # Rabbit Junk

        remove_list = []
        for junk in self.junk_list:
            junk_hit_list = arcade.check_for_collision_with_list(junk, self.rabbit_list)
            if len(junk_hit_list) > 0:
                rabbit = Rabbit()
                rabbit.center_x = junk.center_x
                rabbit.center_y = junk.center_y
                self.rabbit_list.append(rabbit)
                self.sprite_list.append(rabbit)
                remove_list.append(junk)
        for junk in remove_list:
            self.junk_list.remove(junk)
            self.sprite_list.remove(junk)
                
          
        
    def on_draw(self):

        arcade.start_render()
        self.sprite_list.draw()
        arcade.draw_text(f"Rabbits: {len(self.rabbit_list)}", 5, SCREEN_HEIGHT - 20, arcade.color.WHITE)


    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.first_chunk().speed = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.first_chunk().speed = 0

        elif key == arcade.key.LEFT:
            self.first_chunk().change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT:
            self.first_chunk().change_angle = -ANGLE_SPEED


    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.first_chunk().speed = 1
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.first_chunk().change_angle = 0

    def to_track(self):

        self.track.append([self.first_chunk().center_x,
                           self.first_chunk().center_y,
                           self.first_chunk().angle])
        

            
def main():

    prog = MyProg(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    prog.setup()
    arcade.run()

if __name__ == "__main__":
    main()
