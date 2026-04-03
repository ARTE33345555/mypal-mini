# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from http_client import CertManager

IS_ANDROID = platform == "android"

if IS_ANDROID:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
else:
    def run_on_ui_thread(func):
        return func

class MiniMyPal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Поле URL
        self.url_input = TextInput(
            text='https://www.google.com',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.url_input)

        # Кнопка "Перейти"
        self.go_button = Button(text="Go", size_hint_y=None, height=50)
        self.go_button.bind(on_press=self.load_url)
        self.add_widget(self.go_button)

        self.status_label = Label(
            text="Enter a URL and press Go.",
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.status_label)

        self.cert_manager = CertManager()
        self.cert_manager.prepare_certs()

        self.webview = None
        self.create_webview()

    @run_on_ui_thread
    def create_webview(self):
        if not IS_ANDROID:
            self.status_label.text = "Desktop mode: WebView is only available on Android."
            return

        self.activity = PythonActivity.mActivity
        self.webview = WebView(self.activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        self.activity.setContentView(self.webview)
        self.webview.loadUrl(self.url_input.text)
        self.status_label.text = f"Loading {self.url_input.text}"

    @run_on_ui_thread
    def load_url(self, *args):
        url = self.url_input.text
        if not url.startswith("http"):
            url = "http://" + url

        if self.webview is None:
            self.status_label.text = f"WebView unavailable here. URL: {url}"
            return

        self.webview.loadUrl(url)
        self.status_label.text = f"Loading {url}"


class MiniMyPalApp(App):
    def build(self):
        return MiniMyPal()


if __name__ == '__main__':
    MiniMyPalApp().run()
