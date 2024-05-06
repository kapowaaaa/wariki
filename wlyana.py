def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton and self.current_ball is None:
        self.current_ball = [self.width() // 2 - self.ball_size // 2, self.height() - self.ball_size * 1.5, 'Green']
        self.shooting_angle = self.shooter_angle + 180 if self.shooter_angle < 0 else self.shooter_angle
        self.timer = self.startTimer(50)  # Запускаем таймер для обновления положения шарика

def timerEvent(self, event):
    if self.current_ball is not None:
        dx = math.cos(math.radians(self.shooting_angle - 180)) * self.shooting_power
        dy = math.sin(math.radians(self.shooting_angle)) * self.shooting_power
        self.current_ball[0] += dx
        self.current_ball[1] -= dy

        ball_x, ball_y, _ = self.current_ball
        if ball_x <= 0 or ball_x + self.ball_size >= screen_width:
            self.shooting_angle = 180 - self.shooting_angle
        if ball_y <= 0 or ball_y + self.ball_size >= screen_height:
            self.shooting_angle = -self.shooting_angle

        if self.check_collision():
            self.attach_ball()
            self.killTimer(self.timer)  # Останавливаем таймер после столкновения
            self.timer = None

        self.update()  # Обновляем окно для отрисовки нового положения шарика
        
        
'Можно добавить это чтобы шарик двигался без движения мышки'