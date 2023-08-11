import pygame
import sys
import random

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置游戏窗口大小
width, height = 1067, 600
window = pygame.display.set_mode((width, height))

# 设置颜色
black = (0, 0, 0)
white = (255, 255, 255)

# 设置字体
font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over", True, white)
restart_text = font.render("Press 'R' to Restart", True, white)

# 加载背景图片和背景音乐（相对路径）
background = pygame.image.load('.background.0rh')
background = pygame.transform.scale(background, (width, height))
pygame.mixer.music.load('.background_music.0rh')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 设置子弹颜色和半径
bullet_color = white
bullet_radius = 5

# 设置飞船
ship_radius = 25
ship_color = white
ship_pos = [width // 2, height - 50]
ship_speed = 5

# 设置障碍物列表
obstacles = []

# 设置子弹列表
bullets = []

# 设置装弹时间
reload_time = 5000  # 5秒，单位为毫秒
last_shot_time = pygame.time.get_ticks()

# 设置游戏循环
clock = pygame.time.Clock()
running = True
is_dead = False
score = 0
scroll_speed = 3
start_time = pygame.time.get_ticks()

# 显示结束文本的标志
show_end_text = False
end_text_time = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if is_dead:
                is_dead = False
                ship_pos = [width // 2, height - 50]
                obstacles = []
                score = 0
                start_time = pygame.time.get_ticks()
                scroll_speed = 3
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            show_end_text = True
            end_text_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查装弹时间
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= reload_time:
                bullets.append([ship_pos[0], ship_pos[1] - ship_radius])
                last_shot_time = current_time

    if show_end_text:
        # 显示结束文本
        window.fill(black)  # 清空窗口为黑色背景
        text = font.render("0rhendX", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        pygame.display.flip()

        # 等待三秒
        current_time = pygame.time.get_ticks()
        if current_time - end_text_time >= 3000:
            pygame.quit()
            sys.exit()

    if not is_dead:
        # 获取鼠标位置
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # 平滑移动飞船位置
        target_x = mouse_x - ship_radius
        ship_pos[0] += (target_x - ship_pos[0]) * 0.1

        # 添加障碍物
        if random.randint(0, 100) < 5:
            obstacle_width = random.randint(50, 200)
            obstacle_height = random.randint(20, 50)
            obstacle_x = random.randint(0, width - obstacle_width)
            obstacle = pygame.Rect(obstacle_x, -50, obstacle_width, obstacle_height)
            obstacles.append(obstacle)

        # 移动障碍物并检测碰撞
        for obstacle in obstacles:
            obstacle.move_ip(0, scroll_speed)
            if obstacle.colliderect(pygame.Rect(ship_pos[0] - ship_radius, ship_pos[1] - ship_radius, ship_radius * 2, ship_radius * 2)):
                is_dead = True

        # 移除超出屏幕的障碍物
        obstacles = [obstacle for obstacle in obstacles if obstacle.bottom <= height]

        # 移动子弹
        for bullet in bullets:
            bullet[1] -= 10  # 控制子弹速度
            for obstacle in obstacles:
                if pygame.Rect(bullet[0] - bullet_radius, bullet[1] - bullet_radius, bullet_radius * 2, bullet_radius * 2).colliderect(obstacle):
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)
                    break  # 一颗子弹只能击破一个障碍物

        # 更新得分
        score += 1

        # 一分钟后逐渐加快滚动速度
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time >= 60:
            scroll_speed += 0.01

    # 绘制游戏界面
    window.blit(background, (0, 0))

    # 绘制障碍物
    for obstacle in obstacles:
        pygame.draw.rect(window, white, obstacle)

    # 绘制子弹
    for bullet in bullets:
        pygame.draw.circle(window, bullet_color, (int(bullet[0]), int(bullet[1])), bullet_radius)

    # 绘制飞船
    pygame.draw.circle(window, ship_color, (int(ship_pos[0]), ship_pos[1]), ship_radius)

    # 绘制分数
    score_text = font.render(f"Score: {score}", True, white)
    window.blit(score_text, (10, 10))

    # 绘制游戏结束画面
    if is_dead:
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
        window.blit(game_over_text, game_over_rect)
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 50))
        window.blit(restart_text, restart_rect)

    pygame.display.flip()

    # 控制游戏速度
    clock.tick(60)

# 停止背景音乐
pygame.mixer.music.stop()

# 退出游戏
pygame.quit()
sys.exit()