# main.py
import webbrowser

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from http_client import CertManager

IS_ANDROID = platform == "android"

if IS_ANDROID:
    try:
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        WebView = autoclass("android.webkit.WebView")
        WebViewClient = autoclass("android.webkit.WebViewClient")
        WebSettings = autoclass("android.webkit.WebSettings")
    except Exception:
        IS_ANDROID = False

        def run_on_ui_thread(func):
            return func
else:
    def run_on_ui_thread(func):
        return func


class MiniMyPal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.url_input = TextInput(
            text="https://www.google.com",
            size_hint_y=None,
            height=50,
            multiline=False
        )
        self.add_widget(self.url_input)

        button_row = BoxLayout(size_hint_y=None, height=50, spacing=10)

        self.go_button = Button(text="Go")
        self.go_button.bind(on_press=self.load_url)
        button_row.add_widget(self.go_button)

        self.external_browser_button = Button(text="Open in system browser")
        self.external_browser_button.bind(on_press=self.open_in_system_browser)
        button_row.add_widget(self.external_browser_button)

        self.add_widget(button_row)

        self.status_label = Label(
            text="Ready",
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.status_label)

        self.cert_manager = CertManager()
        self.cert_manager.prepare_certs()

        self.webview = None
        self.activity = None
        self.create_webview()

    def normalize_url(self, raw_url):
        value = (raw_url or "").strip()
        if not value:
            value = "https://www.google.com"
        if "//" not in value and ":" not in value:
            value = "https://" + value
        if not value.startswith("http://") and not value.startswith("https://"):
            value = "https://" + value
        return value

    @run_on_ui_thread
    def create_webview(self):
        if not IS_ANDROID:
            self.status_label.text = "Desktop mode: app started. The browser will open in the system browser when you press Go."
            return

        try:
            self.activity = PythonActivity.mActivity
            self.webview = WebView(self.activity)

            settings = self.webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setBuiltInZoomControls(True)
            settings.setDisplayZoomControls(False)
            settings.setSupportZoom(True)

            self.webview.setWebViewClient(WebViewClient())
            self.activity.setContentView(self.webview)
            self.webview.loadUrl(self.normalize_url(self.url_input.text))
            self.status_label.text = f"Loading {self.url_input.text}"
        except Exception as exc:
            self.webview = None
            self.status_label.text = f"Android WebView failed to start: {exc}"

    @run_on_ui_thread
    def load_url(self, *args):
        url = self.normalize_url(self.url_input.text)

        if IS_ANDROID and self.webview is not None:
            self.webview.loadUrl(url)
            self.status_label.text = f"Loading {url}"
            return

        self.open_in_system_browser(url)

    def open_in_system_browser(self, *args):
        url = self.normalize_url(self.url_input.text if not args or not isinstance(args[0], str) else args[0])
        try:
            webbrowser.open(url, new=2)
            self.status_label.text = f"Opening {url} in the system browser"
        except Exception as exc:
            self.status_label.text = f"Could not open browser: {exc}"


class MiniMyPalApp(App):
    def build(self):
        return MiniMyPal()


if __name__ == "__main__":
    MiniMyPalApp().run()
