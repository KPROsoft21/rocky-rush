from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import pygame


WIDTH = 600
HEIGHT = 150
FPS = 60
GROUND_Y = int(HEIGHT * 0.98)
GRAVITY = 0.5

BLACK = (0, 0, 0)
BACKGROUND = (235, 235, 235)

ASSET_DIR = Path(__file__).resolve().parent / "assets" / "sprites"


def asset_path(filename: str) -> str:
    return str(ASSET_DIR / filename)


def load_image(
    filename: str,
    width: int | None = None,
    height: int | None = None,
    colorkey: int | tuple[int, int, int] | None = None,
) -> tuple[pygame.Surface, pygame.Rect]:
    image = pygame.image.load(asset_path(filename)).convert()

    if colorkey is not None:
        key = image.get_at((0, 0)) if colorkey == -1 else colorkey
        image.set_colorkey(key, pygame.RLEACCEL)

    if width is not None or height is not None:
        image = pygame.transform.scale(image, (width or image.get_width(), height or image.get_height()))

    return image, image.get_rect()


def load_sprite_sheet(
    filename: str,
    columns: int,
    rows: int,
    scale_width: int | None = None,
    scale_height: int | None = None,
    colorkey: int | tuple[int, int, int] | None = None,
) -> tuple[list[pygame.Surface], pygame.Rect]:
    sheet = pygame.image.load(asset_path(filename)).convert()
    frame_width = sheet.get_width() // columns
    frame_height = sheet.get_height() // rows
    sprites: list[pygame.Surface] = []

    for row in range(rows):
        for column in range(columns):
            rect = pygame.Rect(column * frame_width, row * frame_height, frame_width, frame_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                key = image.get_at((0, 0)) if colorkey == -1 else colorkey
                image.set_colorkey(key, pygame.RLEACCEL)

            if scale_width is not None or scale_height is not None:
                image = pygame.transform.scale(
                    image,
                    (scale_width or image.get_width(), scale_height or image.get_height()),
                )

            sprites.append(image)

    return sprites, sprites[0].get_rect()


def score_digits(score: int, width: int = 5) -> list[int]:
    return [int(digit) for digit in f"{max(score, 0):0{width}d}"[-width:]]


class Dinosaur(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.running_images, self.rect = load_sprite_sheet("dino.png", 5, 1, 44, 47, -1)
        self.ducking_images, self.ducking_rect = load_sprite_sheet("dino_ducking.png", 2, 1, 59, 47, -1)
        self.rect.bottom = GROUND_Y
        self.rect.left = WIDTH // 15
        self.image = self.running_images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.frame = 0
        self.counter = 0
        self.score = 0
        self.velocity_y = 0.0
        self.is_jumping = False
        self.is_dead = False
        self.is_ducking = False
        self.is_blinking = False
        self.jump_speed = 11.5
        self.standing_width = self.rect.width
        self.ducking_width = self.ducking_rect.width

    def jump(self, jump_sound: pygame.mixer.Sound | None = None) -> None:
        if self.rect.bottom != GROUND_Y:
            return

        self.is_jumping = True
        self.velocity_y = -self.jump_speed
        if jump_sound and pygame.mixer.get_init():
            jump_sound.play()

    def update(self) -> None:
        if self.is_jumping:
            self.velocity_y += GRAVITY
            self.frame = 0
        elif self.is_blinking:
            delay = 400 if self.frame == 0 else 20
            if self.counter % delay == delay - 1:
                self.frame = (self.frame + 1) % 2
        elif self.is_ducking:
            if self.counter % 5 == 0:
                self.frame = (self.frame + 1) % 2
        elif self.counter % 5 == 0:
            self.frame = (self.frame + 1) % 2 + 2

        if self.is_dead:
            self.frame = 4

        if self.is_ducking:
            self.image = self.ducking_images[self.frame % 2]
            self.rect.width = self.ducking_width
        else:
            self.image = self.running_images[self.frame]
            self.rect.width = self.standing_width

        self.rect.y += int(self.velocity_y)
        self._keep_in_bounds()
        self.mask = pygame.mask.from_surface(self.image)

        if not self.is_dead and not self.is_blinking and self.counter % 7 == 6:
            self.score += 1

        self.counter += 1

    def _keep_in_bounds(self) -> None:
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False
            self.velocity_y = 0.0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, filename: str, columns: int, width: int, height: int, speed: int) -> None:
        super().__init__()
        self.images, self.rect = load_sprite_sheet(filename, columns, 1, width, height, -1)
        self.image = random.choice(self.images)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = WIDTH + self.rect.width
        self.speed = speed

    def update(self) -> None:
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Cactus(Obstacle):
    def __init__(self, speed: int) -> None:
        super().__init__("cacti-small.png", 3, 40, 40, speed)
        self.rect.bottom = GROUND_Y


class Ptera(Obstacle):
    def __init__(self, speed: int) -> None:
        super().__init__("ptera.png", 2, 46, 40, speed)
        self.heights = [int(HEIGHT * 0.82), int(HEIGHT * 0.75), int(HEIGHT * 0.60)]
        self.rect.centery = random.choice(self.heights)
        self.frame = 0
        self.counter = 0

    def update(self) -> None:
        if self.counter % 10 == 0:
            self.frame = (self.frame + 1) % 2
            self.image = self.images[self.frame]
            self.mask = pygame.mask.from_surface(self.image)

        self.counter += 1
        super().update()


class Cloud(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image, self.rect = load_image("cloud.png", 64, 30, -1)
        self.rect.left = WIDTH
        self.rect.top = random.randrange(HEIGHT // 5, HEIGHT // 2)

    def update(self) -> None:
        self.rect.x -= 1
        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self, speed: int) -> None:
        self.image, self.rect = load_image("ground.png", colorkey=-1)
        self.image_2, self.rect_2 = load_image("ground.png", colorkey=-1)
        self.rect.bottom = HEIGHT
        self.rect_2.bottom = HEIGHT
        self.rect_2.left = self.rect.right
        self.speed = speed

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.image_2, self.rect_2)

    def update(self) -> None:
        self.rect.x += self.speed
        self.rect_2.x += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect_2.right
        if self.rect_2.right < 0:
            self.rect_2.left = self.rect.right


class Scoreboard:
    def __init__(self, x: int | None = None, y: int | None = None) -> None:
        self.number_images, self.number_rect = load_sprite_sheet("numbers.png", 12, 1, 11, 13, -1)
        self.image = pygame.Surface((55, 13))
        self.rect = self.image.get_rect()
        self.rect.left = int(WIDTH * 0.89) if x is None else x
        self.rect.top = int(HEIGHT * 0.1) if y is None else y

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def update(self, score: int) -> None:
        self.image.fill(BACKGROUND)
        cursor = self.number_rect.copy()

        for digit in score_digits(score):
            self.image.blit(self.number_images[digit], cursor)
            cursor.left += cursor.width


@dataclass
class GameAssets:
    jump_sound: pygame.mixer.Sound | None
    die_sound: pygame.mixer.Sound | None
    checkpoint_sound: pygame.mixer.Sound | None
    replay_button: pygame.Surface
    game_over: pygame.Surface
    logo: pygame.Surface
    callout: pygame.Surface
    hi_label: pygame.Surface


class Game:
    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.display.set_caption("Rocky Rush")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.assets = self._load_assets()

    def run(self) -> None:
        try:
            while self.show_intro():
                self.play_round()
        finally:
            pygame.quit()

    def show_intro(self) -> bool:
        dinosaur = Dinosaur()
        dinosaur.is_blinking = True

        callout_rect = self.assets.callout.get_rect(left=int(WIDTH * 0.05), top=int(HEIGHT * 0.4))
        logo_rect = self.assets.logo.get_rect(center=(int(WIDTH * 0.6), int(HEIGHT * 0.6)))
        ground_frames, ground_rect = load_sprite_sheet("ground.png", 15, 1, colorkey=-1)
        ground_rect.left = WIDTH // 20
        ground_rect.bottom = HEIGHT

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                    dinosaur.is_blinking = False
                    dinosaur.jump()

            dinosaur.update()

            self.screen.fill(BACKGROUND)
            self.screen.blit(ground_frames[0], ground_rect)
            if dinosaur.is_blinking:
                self.screen.blit(self.assets.logo, logo_rect)
                self.screen.blit(self.assets.callout, callout_rect)
            self.screen.blit(dinosaur.image, dinosaur.rect)
            pygame.display.flip()
            self.clock.tick(FPS)

            if not dinosaur.is_jumping and not dinosaur.is_blinking:
                return True

    def play_round(self) -> bool:
        game_speed = 4
        counter = 0
        player = Dinosaur()
        ground = Ground(-game_speed)
        score = Scoreboard()
        high_score = Scoreboard(int(WIDTH * 0.78))
        hi_rect = self.assets.hi_label.get_rect(left=int(WIDTH * 0.73), top=int(HEIGHT * 0.1))

        cacti = pygame.sprite.Group()
        pteras = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        last_obstacle = pygame.sprite.GroupSingle()

        while not player.is_dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        player.jump(self.assets.jump_sound)
                    if event.key == pygame.K_DOWN and not player.is_jumping:
                        player.is_ducking = True
                if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    player.is_ducking = False

            self._spawn_obstacles(game_speed, counter, cacti, pteras, clouds, last_obstacle)
            self._update_world(player, game_speed, ground, score, high_score, cacti, pteras, clouds)
            self._draw_world(player, ground, score, high_score, hi_rect, cacti, pteras, clouds)

            if pygame.sprite.spritecollide(player, cacti, False, pygame.sprite.collide_mask):
                player.is_dead = True
            if pygame.sprite.spritecollide(player, pteras, False, pygame.sprite.collide_mask):
                player.is_dead = True

            if player.is_dead and self.assets.die_sound and pygame.mixer.get_init():
                self.assets.die_sound.play()

            if counter % 700 == 699:
                game_speed += 1
                ground.speed = -game_speed

            if player.score and player.score % 100 == 0 and player.counter % 7 == 0:
                if self.assets.checkpoint_sound and pygame.mixer.get_init():
                    self.assets.checkpoint_sound.play()

            counter += 1
            self.clock.tick(FPS)

        self.high_score = max(self.high_score, player.score)
        return self.show_game_over(high_score, hi_rect)

    def show_game_over(self, high_score: Scoreboard, hi_rect: pygame.Rect) -> bool:
        replay_rect = self.assets.replay_button.get_rect(centerx=WIDTH // 2, top=int(HEIGHT * 0.52))
        game_over_rect = self.assets.game_over.get_rect(centerx=WIDTH // 2, centery=int(HEIGHT * 0.35))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return True

            high_score.update(self.high_score)
            self.screen.blit(self.assets.replay_button, replay_rect)
            self.screen.blit(self.assets.game_over, game_over_rect)
            if self.high_score:
                high_score.draw(self.screen)
                self.screen.blit(self.assets.hi_label, hi_rect)
            pygame.display.flip()
            self.clock.tick(FPS)

    def _spawn_obstacles(
        self,
        game_speed: int,
        counter: int,
        cacti: pygame.sprite.Group,
        pteras: pygame.sprite.Group,
        clouds: pygame.sprite.Group,
        last_obstacle: pygame.sprite.GroupSingle,
    ) -> None:
        if len(cacti) < 2:
            if not cacti:
                cactus = Cactus(game_speed)
                cacti.add(cactus)
                last_obstacle.add(cactus)
            elif last_obstacle.sprite and last_obstacle.sprite.rect.right < WIDTH * 0.7:
                if random.randrange(0, 50) == 10:
                    cactus = Cactus(game_speed)
                    cacti.add(cactus)
                    last_obstacle.add(cactus)

        if not pteras and counter > 500 and random.randrange(0, 200) == 10:
            if last_obstacle.sprite and last_obstacle.sprite.rect.right < WIDTH * 0.8:
                ptera = Ptera(game_speed)
                pteras.add(ptera)
                last_obstacle.add(ptera)

        if len(clouds) < 5 and random.randrange(0, 300) == 10:
            clouds.add(Cloud())

    def _update_world(
        self,
        player: Dinosaur,
        game_speed: int,
        ground: Ground,
        score: Scoreboard,
        high_score: Scoreboard,
        cacti: pygame.sprite.Group,
        pteras: pygame.sprite.Group,
        clouds: pygame.sprite.Group,
    ) -> None:
        for obstacle in [*cacti, *pteras]:
            obstacle.speed = game_speed

        player.update()
        cacti.update()
        pteras.update()
        clouds.update()
        ground.update()
        score.update(player.score)
        high_score.update(self.high_score)

    def _draw_world(
        self,
        player: Dinosaur,
        ground: Ground,
        score: Scoreboard,
        high_score: Scoreboard,
        hi_rect: pygame.Rect,
        cacti: pygame.sprite.Group,
        pteras: pygame.sprite.Group,
        clouds: pygame.sprite.Group,
    ) -> None:
        self.screen.fill(BACKGROUND)
        ground.draw(self.screen)
        clouds.draw(self.screen)
        score.draw(self.screen)
        if self.high_score:
            high_score.draw(self.screen)
            self.screen.blit(self.assets.hi_label, hi_rect)
        cacti.draw(self.screen)
        pteras.draw(self.screen)
        self.screen.blit(player.image, player.rect)
        pygame.display.flip()

    def _load_assets(self) -> GameAssets:
        jump = self._load_sound("jump.wav")
        die = self._load_sound("die.wav")
        checkpoint = self._load_sound("checkPoint.wav")
        replay_button, _ = load_image("replay_button.png", 35, 31, -1)
        game_over, _ = load_image("game_over.png", 190, 11, -1)
        logo, _ = load_image("logo.png", 240, 40, -1)
        callout, _ = load_image("call_out.png", 196, 45, -1)
        number_images, number_rect = load_sprite_sheet("numbers.png", 12, 1, 11, 13, -1)
        hi_label = pygame.Surface((22, 13))
        hi_label.fill(BACKGROUND)
        hi_label.blit(number_images[10], number_rect)
        number_rect.left += number_rect.width
        hi_label.blit(number_images[11], number_rect)

        return GameAssets(jump, die, checkpoint, replay_button, game_over, logo, callout, hi_label)

    @staticmethod
    def _load_sound(filename: str) -> pygame.mixer.Sound | None:
        if not pygame.mixer.get_init():
            return None
        return pygame.mixer.Sound(asset_path(filename))


def main() -> None:
    Game().run()
