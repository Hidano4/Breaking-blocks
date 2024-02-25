from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

class Ball(QGraphicsEllipseItem):
    def __init__(self):
        super(Ball, self).__init__(0, 0, 20, 20)
        self.setPos(240, 320)
        self.x_speed = 5
        self.y_speed = -5

    def move(self):
        self.setPos(self.x() + self.x_speed, self.y() + self.y_speed)

        if self.x() <= 0 or self.x() >= 480:
            self.x_speed = -self.x_speed

        if self.y() <= 0 or self.y() >= 640:
            self.y_speed = -self.y_speed

class Paddle(QGraphicsRectItem):
    def __init__(self):
        super(Paddle, self).__init__(0, 0, 80, 10)
        self.setPos(200, 600)

    def move_left(self):
        if self.x() > 0:
            self.setPos(self.x() - 10, self.y())

    def move_right(self):
        if self.x() < 400:
            self.setPos(self.x() + 10, self.y())

class Block(QGraphicsRectItem):
    def __init__(self, x, y):
        super(Block, self).__init__(0, 0, 10, 10)
        self.setPos(x, y)
        self.setBrush(QColor(0, 255, 0))  # 緑色のブロック
        self.hit_count = 0  # ボールに当たった回数

    def hit(self):
        self.hit_count += 1
        if self.hit_count == 1:
            self.setBrush(Qt.NoBrush)  # ボールに一度触れたら色を消す

class BreakoutGameLogic:
    def __init__(self):
        self.ball = Ball()
        self.paddle = Paddle()
        self.blocks = [Block(i * 10, j * 10) for i in range(50) for j in range(10)]
        self.score_display = QGraphicsTextItem()
        self.clear_display = QGraphicsTextItem()
        self.clear_display.setPlainText("")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.paddle.move_left()
        elif event.key() == Qt.Key_Right:
            self.paddle.move_right()

    def update(self):
        self.ball.move()

        if self.ball.collidesWithItem(self.paddle):
            self.ball.y_speed = -self.ball.y_speed

        for block in self.blocks:
            if block in self.scene.items() and self.ball.collidesWithItem(block):
                block.hit()
                if block.hit_count == 1:
                    self.scene.removeItem(block)
                    self.blocks.remove(block)

        self.score_display.setPlainText(f"Blocks left: {len(self.blocks)}")

        if len(self.blocks) == 0:
            self.clear_display.setPlainText("CLEAR!")
            self.clear_display.setPos(180, 300)
            self.timer.stop()
