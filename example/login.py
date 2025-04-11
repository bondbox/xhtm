# coding:utf-8

from flask import Flask
from flask import redirect
from flask import request
from flask import session

from xhtml.element import Div
from xhtml.element import Form
from xhtml.element import HtmlDoc
from xhtml.element import Input
from xhtml.element import Span

USERNAME = "admin"
PASSWORD = "secret"

app = Flask(__name__)
app.secret_key = "your_secret_key"


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


class LoginHtml(HtmlDoc):
    def __init__(self, title: str = "Login"):
        super().__init__()
        self.__user: Input = Input({"type": "text", "name": "username", "placeholder": "Username"})  # noqa:E501
        self.__user.attrs.std_style.width.v = "200px"
        self.__user.attrs.std_style.height.v = "30px"
        self.__pass: Input = Input({"type": "password", "name": "password", "placeholder": "Password"})  # noqa:E501
        self.__pass.attrs.std_style.width.v = "200px"
        self.__pass.attrs.std_style.height.v = "30px"
        self.__post: Input = Input({"type": "submit", "value": "Submit"})
        self.__post.attrs.std_style.width.v = "200px"
        self.__post.attrs.std_style.height.v = "30px"
        self.__form: Form = Form({"method": "post"})
        self.__form.add(Div(attrs={"style": "text-align: center;"}, child=[self.__user]))  # noqa: E501
        self.__form.add(Span(attrs={"style": "display: block; margin-bottom: 10px;"}))  # noqa: E501
        self.__form.add(Div(attrs={"style": "text-align: center;"}, child=[self.__pass]))  # noqa: E501
        self.__form.add(Span(attrs={"style": "display: block; margin-bottom: 20px;"}))  # noqa: E501
        self.__form.add(Div(attrs={"style": "text-align: center;"}, child=[self.__post]))  # noqa: E501
        self.__root: Div = Div()
        self.__root.add(self.__form)
        self.__root.attrs.std_style.height.v = "60vh"
        self.__root.attrs.std_style.display.v = "grid"
        self.__root.attrs.std_style.place_items.v = "center"
        self.head.title.text = title
        self.body.add(self.__root)

    @property
    def root(self) -> Div:
        return self.__root

    @property
    def form(self) -> Form:
        return self.__form

    @property
    def username(self) -> Input:
        return self.__user

    @property
    def password(self) -> Input:
        return self.__pass

    @property
    def submit(self) -> Input:
        return self.__post


@app.route("/", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if check_auth(username, password):
        session["user_token"] = True
        return redirect("/")
    else:
        return "Invalid username or password", 401


@app.route("/", methods=["GET"])
def login_get():
    html = LoginHtml()
    print(html)
    return str(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
