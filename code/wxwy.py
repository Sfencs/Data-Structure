# -*- coding: utf-8 -*-
import time
import autopy
time.sleep(1)
print('开始')
time.sleep(4)  # 准备时间去打开游戏对应界面
# autopy.mouse.smooth_move(600,430)
# autopy.mouse.smooth_move(1000,500)
while True:
    # autopy.mouse.move(1750,518)# 出战按钮
    autopy.mouse.smooth_move(950, 300)
    autopy.mouse.click()  # 点击
    time.sleep(2)
    autopy.mouse.move(950, 300)  # 再点一次出战按钮
    autopy.mouse.click()  # 点击
    time.sleep(12)
    autopy.mouse.move(950, 300)  # 然后一直按一会走路
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)  # 按下左键
    time.sleep(4)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    for i in range(40):
        autopy.mouse.move(600, 430)  # 一直按这里攻击
        autopy.mouse.click()
        time.sleep(1)
    autopy.mouse.move(950, 300)  # 然后再一直按一会走路
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)  # 按下左键
    time.sleep(4)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    for i in range(40):
        autopy.mouse.move(600, 430)  # 一直按这里攻击
        autopy.mouse.click()
        time.sleep(1)
    autopy.mouse.move(950, 300)  # 然后再一直按一会走路
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)  # 按下左键
    time.sleep(6)
    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)
    for i in range(63):
        autopy.mouse.move(600, 430)  # 一直按这里攻击
        autopy.mouse.click()
        time.sleep(1)
    time.sleep(5)
    autopy.mouse.move(950, 300)  # 点返回
    time.sleep(8)
