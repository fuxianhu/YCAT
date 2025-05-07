import typing
from tkinter import *
from PIL import Image, ImageTk


class WindowBackground:
    """
    控制一个窗口（例如主窗口、子窗口，即Tk对象、Toplevel对象）的背景颜色/图片。
    """

    def __init__(self, win: typing.Union[Tk, Toplevel]) -> None:
        self.root = win
        self.backgroundImage = None
        self.last_width = 0
        self.last_height = 0
        self.resize_threshold = 20  # 设置一个阈值，只有当窗口大小变化超过这个阈值时才进行图片处理


    def setBackgroundColor(self, color: str = 'lightblue') -> None:
        """
        直接设置窗口的颜色。比如'lightblue'为浅蓝色
        :color: 该颜色的单词或短语 str对象
        """
        self.root.configure(bg=color)


    def loadImage(self, image_path: str = '../image/a.jpeg'):
        """
        使用PIL加载图片
        :image_path: 图片路径，可以是绝对路径或相对路径（建议选择后者）。
        :return: 返回一个元组，分别为Image.open函数的返回值、PhotoImage对象。
        """
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        return (photo, image)

    def setBackgroundImage(self, image_path: str = '../image/a.jpeg') -> None:
        """
        设置主窗口的背景图片，不做拉伸等操作
        :image_path: 图片路径，可以是绝对路径或相对路径（建议选择后者）。
        """
        self.backgroundImage = self.loadImage(image_path)
        if self.backgroundImage[0] is not None:
            self.background_label.image = self.backgroundImage[0]
            # 创建一个 Label 并设置图片
            self.background_label = Label(self.root, image=self.background_label.image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print("Failed to set background image.")

    def resize_image(self, event) -> None:
        """
        当窗口大小改变时，自动调整背景图片的大小。
        """
        # 获取窗口的当前大小
        new_width = event.width
        new_height = event.height

        # 只有当窗口大小变化超过阈值时才进行图片处理
        if abs(new_width - self.last_width) > self.resize_threshold or abs(new_height - self.last_height) > self.resize_threshold:
            # 调整图片大小
            resized_image = self.backgroundImage[1].resize((new_width, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            # 更新 Label 的图片
            self.background_label.config(image=photo)

            self.background_label.image = photo  # 保持对 PhotoImage 对象的引用

            # 更新上次窗口大小
            self.last_width = new_width
            self.last_height = new_height

    def setBackgroundImageWithResize(self, image_path: str = '../image/a.jpeg') -> None:
        """
        设置背景图片，且图片会根据窗口大小做实时拉伸。
        绑定窗口大小改变事件。
        :image_path: 图片路径，可以是绝对路径或相对路径（建议选择后者）。
        """
        self.setBackgroundImage(image_path)
        self.root.bind('<Configure>', self.resize_image)