import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

class Ball(QGraphicsEllipseItem):
    def __init__(self):
        super(Ball, self).__init__(0, 0, 15, 15)
        self.setPos(240, 320)
        self.setBrush(QColor(255, 255, 0))
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
        self.setBrush(QColor(0, 0, 255))

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
        self.setBrush(QColor(0, 255, 0))  
        self.hit_count = 0  

    def hit(self):
        self.hit_count += 1
        if self.hit_count == 1:
            self.setBrush(Qt.NoBrush)  

class BreakoutGame(QGraphicsView):
    def __init__(self):
        super(BreakoutGame, self).__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.ball = Ball()
        self.paddle = Paddle()

        self.scene.addItem(self.ball)
        self.scene.addItem(self.paddle)

        self.blocks = []
        for i in range(50):
            for j in range(10):
                block = Block(i * 10, j * 10)
                self.blocks.append(block)
                self.scene.addItem(block)

        self.score_display = QGraphicsTextItem()
        self.score_display.setPlainText(f"残りブロック数: {len(self.blocks)}")
        self.score_display.setPos(10, 150)
        self.scene.addItem(self.score_display)

        self.clear_display = QGraphicsTextItem()
        self.clear_display.setPlainText("")
        self.scene.addItem(self.clear_display)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(20)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setGeometry(100, 100, 500, 680)
        self.setWindowTitle("Breaking-blocks")

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

        self.score_display.setPlainText(f"残りブロック数: {len(self.blocks)}")

        if len(self.blocks) == 0:
            self.clear_display.setPlainText("CLEAR!")
            self.clear_display.setPos(180, 300)
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BreakoutGame()
    game.show()
    sys.exit(app.exec_())
