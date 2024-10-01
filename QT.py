import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class TextDisplayWindow(QMainWindow):
    def __init__(self, font_size=12):
        super().__init__()

        self.initUI(font_size)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_displayed_text)

        self.resizeEvent = self.on_window_resize

    def initUI(self, font_size):        #设置窗口的大小
        self.setWindowTitle('正常人部分')
        self.setGeometry(100, 100, 600, 300)

        self.font_size = font_size

        # Adding a label for background image
        self.background_label = QLabel(self)
        pixmap = QPixmap("背景.png")  # Replace with your image path
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        self.text_label = QLabel('', self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"font-family: Arial; color: blue; background-color: rgba(255, 255, 255, 150);")

        self.get_text_function = None
        self.timer_interval = 1000

    def set_text_function(self, get_text_function):         #设置显示的内容
        self.get_text_function = get_text_function

    def set_timer_interval(self, interval):                 #设置显示的时间,单位ms.效果是每隔interval毫秒显示一次
        self.timer_interval = interval

    def start_text_timer(self):                         #开始显示
        self.timer.start(self.timer_interval)

    def update_displayed_text(self):                    #更新显示的内容
        if self.get_text_function:
            new_text = self.get_text_function()
            self.display_text_one_by_one(new_text)

    def display_text_one_by_one(self, text):                #显示内容
        #如果text不为空
        if text != self.text_label.text():
            self.text_label.setText('')
            self.current_text = text
            self.text_index = 0
            self.timer_single_letter = QTimer()
            self.timer_single_letter.timeout.connect(self.show_single_letter)
            self.timer_single_letter.start(20)  #每隔100ms显示一个字


    # def display_text_one_by_one(self, text):
    #     if text:
    #         if text != self.text_label.text():
    #             self.text_label.setText('')
    #             self.current_text = text
    #             self.text_index = 0
    #             self.timer_single_letter = QTimer()
    #             self.timer_single_letter.timeout.connect(self.show_single_letter)
    #             self.timer_single_letter.start(10)
    #     else:
    #         self.timer_single_letter = QTimer()
    #         self.timer_single_letter.timeout.connect(self.show_single_letter)
    #         self.timer_single_letter.start(10)

    def show_single_letter(self):#每隔100ms显示一个字          #显示单个字
        if self.text_index < len(self.current_text):
            self.text_label.setText(self.current_text[:self.text_index + 1])
            self.text_index += 1
        else:
            self.timer_single_letter.stop()

    # def on_window_resize(self, event):
    #     # Resize background image label to fit window
    #     self.background_label.setGeometry(0, 0, self.width(), self.height())
    #
    #     # Resize the background pixmap to fit the new window size
    #     pixmap = QPixmap("背景.png")  # Replace with your image path
    #     scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
    #     self.background_label.setPixmap(scaled_pixmap)
    #
    #     # Calculate label dimensions for text display
    #     label_width = self.width() * 9 / 10
    #     label_height = self.height() / 5
    #     label_x = (self.width() - label_width) / 2
    #     label_y = (self.height() - label_height) / 2
    #
    #     # Font size as a fraction of window height
    #     font_size = self.height() // 7
    #
    #     self.text_label.setStyleSheet(
    #         f"font-size: {font_size}px; font-family: Arial; color: blue; background-color: rgba(255, 255, 255, 150);")
    #     self.text_label.setGeometry(int(label_x), int(label_y), int(label_width), int(label_height))
    def on_window_resize(self, event):                              #窗口大小改变时，背景图片也跟着改变
        # Resize background image label to fit window
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Resize the background pixmap to fit the new window size
        pixmap = QPixmap("背景.png")  # Replace with your image path
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.background_label.setPixmap(scaled_pixmap)

        # Calculate label dimensions for text display
        label_width = self.width() * 1
        label_height = self.height() / 5
        label_x = (self.width() - label_width) / 2
        label_y = (self.height() - label_height) / 2

        # Font size as a fraction of window height
        font_size = self.height() // 10

        # Update style and geometry for text label
        self.text_label.setStyleSheet(
            f"font-size: {font_size}px; font-family: Arial; color: blue; background-color: rgba(255, 255, 255, 150);")
        self.text_label.setGeometry(int(label_x), int(label_y), int(label_width), int(label_height))

        # Center the background image label
        self.background_label.setAlignment(Qt.AlignCenter)


def get_text():                                         #显示的内容
    get_text.counter = getattr(get_text, 'counter', 0)
    texts = ["这是新的内容1", "这是新的内容2", "这是新的内容3"]
    text = texts[get_text.counter % len(texts)]
    get_text.counter += 1
    return text


def display_text_window(get_text_function, font_size=20, timer_interval=2000):              #显示窗口
    app = QApplication(sys.argv)
    window = TextDisplayWindow(font_size)
    window.show()

    window.set_text_function(get_text_function)
    window.start_text_timer()

    sys.exit(app.exec_())


if __name__ == '__main__':
    display_text_window(get_text, font_size=30, timer_interval=3000)
