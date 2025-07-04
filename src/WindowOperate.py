import typing
from tkinter import *
from PIL import Image, ImageTk
from basic import *


class WindowBackground:
    """
    ### 控制一个窗口（例如主窗口、子窗口，即Tk对象、Toplevel对象）的背景颜色/图片等属性。
    **其他程序只负责调用`__init__`方法**

    **不需要调用其他方法**
    """


    def __init__(self, win: Tk | Toplevel) -> None:
        self.root = win
        self.backgroundImage = jsonSettings["window"]["backgroundImage"]
        self.last_length = jsonSettings["window"]["length"] # 调整前的窗口长度
        self.last_height = jsonSettings["window"]["width"] # 调整前的窗口高度
        self.resize_threshold =  jsonSettings["window"]["resizeThreshold"] # 阈值，只有当窗口大小变化超过这个阈值时才进行图片处理
        self.root.iconbitmap(jsonSettings["window"]["icon"]) # 设置图标
        self.root.geometry(f"{str(jsonSettings['window']['length'])}x{str(jsonSettings['window']['width'])}") # 设置窗口大小
        self.root.title(lang["title"]) # 设置窗口标题
        self.root.attributes("-alpha", jsonSettings['window']['alpha']) # 设置窗口透明度，0.0为完全透明，1.0为不透明
        self.root.resizable(jsonSettings['window']['Allow length adjustment'], jsonSettings['window']['Allow width adjustment']) # 允许/禁止调整窗口的长、高


    def setBackgroundColor(self, color= "#FFFFFF") -> None:
        """
        ### 直接设置窗口的颜色。
        
        `color`: 该颜色的单词或短语
        """
        self.root.configure(bg=color)


    def loadImage(self, image_path: str = '../image/a.jpeg'):
        """
        ### 使用`PIL`加载图片

        返回一个元组，分别为`Image.open`函数的返回值、`PhotoImage`对象。
        """
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        return (photo, image)


    def setBackgroundImage(self, image_path: str = '../image/a.jpeg') -> None:
        """
        ### 设置主窗口的背景图片，不做拉伸等操作
        """
        self.backgroundImage = self.loadImage(image_path)
        if self.backgroundImage[0] is not None:
            self.background_label.image = self.backgroundImage[0]
            # 创建一个 Label 并设置图片
            self.background_label = Label(self.root, image=self.background_label.image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            log(logging.ERROR, "Failed to set background image.")


    def resize_image(self, event) -> None:
        """
        ### 当窗口大小改变时，自动调整背景图片的大小。
        """
        # 获取窗口的当前大小
        new_length = event.width
        new_height = event.height

        # 只有当窗口大小变化超过阈值时才进行图片处理
        if abs(new_length - self.last_length) > self.resize_threshold or abs(new_height - self.last_height) > self.resize_threshold:
            # 调整图片大小
            resized_image = self.backgroundImage[1].resize((new_length, new_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            # 更新 Label 的图片
            self.background_label.config(image=photo)

            self.background_label.image = photo  # 保持对 PhotoImage 对象的引用

            # 更新上次窗口大小
            self.last_length = new_length
            self.last_height = new_height

    def setBackgroundImageWithResize(self, image_path: str = '../image/a.jpeg') -> None:
        """
        ### 设置背景图片，且图片会根据窗口大小做实时拉伸。

        绑定窗口大小改变事件。

        `image_path`: 图片路径，可以是绝对路径或相对路径（建议选择后者）。
        """
        self.setBackgroundImage(image_path)
        self.root.bind('<Configure>', self.resize_image)


