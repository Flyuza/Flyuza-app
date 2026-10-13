from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex("#F5F5F5")

class Flyunza(App):

def build(self):  
    self.posts = [  
        {  
            "user": "flyunza_official",  
            "text": "Flyunza'ga xush kelibsiz! 🚀",  
            "likes": 0  
        },  
        {  
            "user": "uzbekistan",  
            "text": "Yangi kun, yangi imkoniyatlar! 🇺🇿",  
            "likes": 0  
        }  
    ]  

    self.liked_posts = set()  
    self.page = BoxLayout(  
        orientation="vertical",  
        spacing=dp(5),  
        padding=dp(10)  
    )  

    self.show_home()  
    return self.page  

def make_button(self, text, callback):  
    btn = Button(  
        text=text,  
        size_hint_y=None,  
        height=dp(48),  
        background_normal="",  
        background_color=get_color_from_hex("#222222"),  
        color=(1, 1, 1, 1),  
        font_size=dp(15)  
    )  
    btn.bind(on_release=callback)  
    return btn  

def header(self):  
    top = BoxLayout(  
        size_hint_y=None,  
        height=dp(55)  
    )  

    title = Label(  
        text="[b]FLYUNZA[/b]",  
        markup=True,  
        font_size=dp(25),  
        color=get_color_from_hex("#222222")  
    )  

    top.add_widget(title)  
    return top  

def bottom_menu(self):  
    menu = GridLayout(  
        cols=5,  
        size_hint_y=None,  
        height=dp(58),  
        spacing=dp(3)  
    )  

    items = [  
        ("Home", self.show_home),  
        ("Search", self.show_search),  
        ("Post +", self.show_add_post),  
        ("Likes", self.show_likes),  
        ("Profile", self.show_profile)  
    ]  

    for name, func in items:  
        btn = Button(  
            text=name,  
            font_size=dp(12),  
            background_normal="",  
            background_color=get_color_from_hex("#292929"),  
            color=(1, 1, 1, 1)  
        )  
        btn.bind(on_release=func)  
        menu.add_widget(btn)  

    return menu  

def reset_page(self, title):  
    self.page.clear_widgets()  
    self.page.add_widget(self.header())  

    heading = Label(  
        text=title,  
        size_hint_y=None,  
        height=dp(40),  
        font_size=dp(19),  
        color=get_color_from_hex("#222222")  
    )  
    self.page.add_widget(heading)  

def finish_page(self, content):  
    self.page.add_widget(content)  
    self.page.add_widget(self.bottom_menu())  

def show_home(self, *args):  
    self.reset_page("Bosh sahifa")  

    scroll = ScrollView()  
    posts_box = BoxLayout(  
        orientation="vertical",  
        spacing=dp(12),  
        padding=dp(4),  
        size_hint_y=None  
    )  
    posts_box.bind(  
        minimum_height=posts_box.setter("height")  
    )  

    for index, post in enumerate(self.posts):  
        card = BoxLayout(  
            orientation="vertical",  
            spacing=dp(8),  
            padding=dp(12),  
            size_hint_y=None,  
            height=dp(185)  
        )  

        with card.canvas.before:  
            Color(1, 1, 1, 1)  
            rect = RoundedRectangle(  
                pos=card.pos,  
                size=card.size,  
                radius=[dp(12)]  
            )  

        card.bind(  
            pos=lambda obj, val, r=rect: setattr(r, "pos", val),  
            size=lambda obj, val, r=rect: setattr(r, "size", val)  
        )  

        user = Label(  
            text="[b]@" + post["user"] + "[/b]",  
            markup=True,  
            size_hint_y=None,  
            height=dp(28),  
            color=get_color_from_hex("#222222")  
        )  

        text = Label(  
            text=post["text"],  
            size_hint_y=None,  
            height=dp(45),  
            color=get_color_from_hex("#333333")  
        )  

        like_text = "❤️ " + str(post["likes"]) + "  Like"  
        like_btn = Button(  
            text=like_text,  
            size_hint_y=None,  
            height=dp(42),  
            background_normal="",  
            background_color=get_color_from_hex("#E1306C"),  
            color=(1, 1, 1, 1)  
        )  

        like_btn.bind(  
            on_release=lambda btn, i=index: self.like_post(i)  
        )  

        card.add_widget(user)  
        card.add_widget(text)  
        card.add_widget(like_btn)  
        posts_box.add_widget(card)  

    scroll.add_widget(posts_box)  
    self.finish_page(scroll)  

def like_post(self, index):  
    if index in self.liked_posts:  
        self.posts[index]["likes"] -= 1  
        self.liked_posts.remove(index)  
    else:  
        self.posts[index]["likes"] += 1  
        self.liked_posts.add(index)  

    self.show_home()  

def show_search(self, *args):  
    self.reset_page("Qidiruv 🔍")  

    box = BoxLayout(  
        orientation="vertical",  
        spacing=dp(10),  
        padding=dp(10)  
    )  

    field = TextInput(  
        hint_text="Foydalanuvchi yoki postni qidirish...",  
        size_hint_y=None,  
        height=dp(50),  
        multiline=False  
    )  

    results = Label(  
        text="Qidiruv natijalari shu yerda chiqadi.",  
        color=get_color_from_hex("#222222"),  
        halign="left",  
        valign="top"  
    )  
    results.bind(  
        size=lambda obj, val: setattr(obj, "text_size", val)  
    )  

    def search(*_):  
        query = field.text.strip().lower()  
        found = []  

        for post in self.posts:  
            if (  
                query in post["user"].lower()  
                or query in post["text"].lower()  
            ):  
                found.append(  
                    "@" + post["user"] + "\n" + post["text"]  
                )  

        results.text = (  
            "\n\n".join(found) if found  
            else "Hech narsa topilmadi."  
        )  

    box.add_widget(field)  
    box.add_widget(self.make_button("Qidirish", search))  
    box.add_widget(results)  

    self.finish_page(box)  

def show_add_post(self, *args):  
    self.reset_page("Yangi post ➕")  

    box = BoxLayout(  
        orientation="vertical",  
        spacing=dp(12),  
        padding=dp(10)  
    )  

    username = TextInput(  
        hint_text="Isming yoki username",  
        text="flyunza_user",  
        size_hint_y=None,  
        height=dp(50),  
        multiline=False  
    )  

    content = TextInput(  
        hint_text="Posting matnini yoz...",  
        size_hint_y=None,  
        height=dp(120)  
    )  

    status = Label(  
        text="",  
        color=get_color_from_hex("#218838")  
    )  

    def publish(*_):  
        text = content.text.strip()  
        user = username.text.strip().replace("@", "")  

        if not user or not text:  
            status.text = "Username va post matnini kiriting."  
            return  

        self.posts.insert(0, {  
            "user": user,  
            "text": text,  
            "likes": 0  
        })  

        self.liked_posts = {  
            i + 1 for i in self.liked_posts  
        }  

        self.show_home()  

    box.add_widget(username)  
    box.add_widget(content)  
    box.add_widget(  
        self.make_button("Postni joylash", publish)  
    )  
    box.add_widget(status)  

    self.finish_page(box)  

def show_likes(self, *args):  
    self.reset_page("Yoqtirgan postlar ❤️")  

    scroll = ScrollView()  
    box = BoxLayout(  
        orientation="vertical",  
        spacing=dp(10),  
        size_hint_y=None  
    )  
    box.bind(minimum_height=box.setter("height"))  

    for i in sorted(self.liked_posts):  
        if i < len(self.posts):  
            post = self.posts[i]  
            label = Label(  
                text="@" + post["user"] + "\n" + post["text"],  
                size_hint_y=None,  
                height=dp(75),  
                color=get_color_from_hex("#222222")  
            )  
            box.add_widget(label)  

    if not self.liked_posts:  
        box.add_widget(  
            Label(  
                text="Hozircha yoqtirgan postingiz yo'q.",  
                size_hint_y=None,  
                height=dp(60),  
                color=get_color_from_hex("#222222")  
            )  
        )  

    scroll.add_widget(box)  
    self.finish_page(scroll)  

def show_profile(self, *args):  
    self.reset_page("Mening profilim 👤")  

    box = BoxLayout(  
        orientation="vertical",  
        spacing=dp(12),  
        padding=dp(15)  
    )  

    box.add_widget(  
        Label(  
            text="[b]Flyunza User[/b]",  
            markup=True,  
            font_size=dp(23),  
            color=get_color_from_hex("#222222")  
        )  
    )  

    box.add_widget(  
        Label(  
            text=(  
                "Postlar: " + str(len(self.posts))  
                + "\nYoqtirgan postlar: "  
                + str(len(self.liked_posts))  
                + "\n\nFlyunza foydalanuvchisi"  
            ),  
            color=get_color_from_hex("#333333")  
        )  
    )  

    username = TextInput(  
        hint_text="Yangi username",  
        text="flyunza_user",  
        size_hint_y=None,  
        height=dp(48),  
        multiline=False  
    )  

    message = Label(  
        text="",  
        color=get_color_from_hex("#218838")  
    )  

    def save_profile(*_):  
        if username.text.strip():  
            message.text = (  
                "Username: @" + username.text.strip()  
            )  
        else:  
            message.text = "Username kiriting."  

    box.add_widget(username)  
    box.add_widget(  
        self.make_button("Profilni tahrirlash", save_profile)  
    )  
    box.add_widget(message)  

    self.finish_page(box)

if name == "main":
Flyunza().run()
