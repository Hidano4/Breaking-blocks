import sys
import mains2 as m
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QTimer
from game import BreakoutGameLogic

class BreakoutGame(QGraphicsView):
    def __init__(self):
        super(BreakoutGame, self).__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.game_logic = BreakoutGameLogic()
        self.scene.addItem(self.game_logic.ball)
        self.scene.addItem(self.game_logic.paddle)
        self.scene.addItem(self.game_logic.score_display)
        self.scene.addItem(self.game_logic.clear_display)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setGeometry(100, 100, 480, 640)
        self.setWindowTitle("Breakout Game")

    def keyPressEvent(self, event):
        self.game_logic.keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = BreakoutGame()
    game.show()
    sys.exit(app.exec_())
