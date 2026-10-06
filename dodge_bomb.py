import os
import random
import sys
import pygame as pg
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = { #  練習1
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool] :
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：移動量の合計値タプルをキー，その向きに回転させた
    こうかとん画像Surfaceを値とした辞書
    """
    kk_img = pg.image.load("fig/3.png")  # 元画像は左向き
    kk_img_flip = pg.transform.flip(kk_img, True, False)  # 右向き
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 0.9),  # キー押下がない場合
        (+5, 0): pg.transform.rotozoom(kk_img_flip, 0, 0.9),  # 右
        (+5, -5): pg.transform.rotozoom(kk_img_flip, 45, 0.9),  # 右上
        (0, -5): pg.transform.rotozoom(kk_img_flip, 90, 0.9),  # 上
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9),  # 左上
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),  # 左
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 0.9),  # 左下
        (0, +5): pg.transform.rotozoom(kk_img_flip, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(kk_img_flip, -45, 0.9),  # 右下
    }
    return kk_dict


def gameover(screen: pg.Surface) -> None:
    """
    引数：画面Surface
    画面をブラックアウトし，泣いているこうかとんと
    「Game Over」の文字列を5秒間表示する
    戻り値：なし
    """
    # 半透明の黒い矩形Surface
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_sfc, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    black_sfc.set_alpha(200)
 
    # 白文字の「Game Over」
    font = pg.font.Font(None, 50)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2
    black_sfc.blit(txt, txt_rct)
 
    # 泣いているこうかとん（文字列の左右に配置）
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    left_rct = cry_img.get_rect()
    left_rct.midright = txt_rct.left - 30, HEIGHT // 2
    right_rct = cry_img.get_rect()
    right_rct.midleft = txt_rct.right + 30, HEIGHT // 2
    black_sfc.blit(cry_img, left_rct)
    black_sfc.blit(cry_img, right_rct)
 
    screen.blit(black_sfc, [0, 0])
    pg.display.update()
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    kk_imgs = get_kk_imgs()  
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    bb_img = pg.Surface((20,20)) #  空のSurface
    pg.draw.circle(bb_img, (255,0,0),(10,10),10) #  赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH) #  横用乱数、
    bb_rct.centery = random.randint(0, HEIGHT) #  縦用乱数
    vx, vy = +5, +5  # 爆弾の初期速度　

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向判定
                sum_mv[1] += tpl[1]  # 縦方向判定  
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True,True): #  どこかしらはみでてる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #  さっきの動きのキャンセル
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら反転
            vx *= -1
        if not tate:  # 縦方向にはみ出たら反転
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
