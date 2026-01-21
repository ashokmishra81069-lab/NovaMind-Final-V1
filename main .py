import os
import json
import requests
from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

# ⚠️ API KEY (temporarily here; later env/secure storage)
API_KEY = "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"

class NovaMindApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"

        # ✅ ANDROID-SAFE STORAGE PATH
        if platform == "android":
            from android.storage import app_storage_path
            self.base_path = app_storage_path()
        else:
            self.base_path = os.getcwd()

        self.db_path = os.path.join(self.base_path, "chat_history.json")
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.chat_label = MDLabel(
            text="NovaMind AI\nSawal puchiye bhai...",
            halign="left",
            size_hint_y=None,
        )
        self.chat_label.bind(texture_size=self.chat_label.setter("size"))

        scroll = ScrollView()
        scroll.add_widget(self.chat_label)

        self.input_field = MDTextField(
            hint_text="Ask NovaMind...",
            mode="rectangle",
            multiline=False
        )

        send_btn = MDRaisedButton(
            text="SEND",
            on_release=self.chat_logic,
            pos_hint={"center_x": 0.5}
        )

        layout.add_widget(scroll)
        layout.add_widget(self.input_field)
        layout.add_widget(send_btn)
        return layout

    def chat_logic(self, *args):
        query = self.input_field.text.strip()
        if not query:
            return

        self.chat_label.text += f"\n\nYOU: {query}\n\nNOVAMIND: Thinking..."
        self.input_field.text = ""

        Clock.schedule_once(lambda dt: self.fetch_ai(query), 0)

    def fetch_ai(self, text):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": text}]
            }

            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            data = r.json()
            answer = data["choices"][0]["message"]["content"]

            self.chat_label.text = self.chat_label.text.replace(
                "Thinking...", answer
            )
            self.save_chat(text, answer)

        except Exception:
            self.chat_label.text = self.chat_label.text.replace(
                "Thinking...", "Network error! Internet check karo."
            )

    def save_chat(self, q, a):
        try:
            with open(self.db_path, "r") as f:
                data = json.load(f)

            data.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "q": q,
                "a": a
            })

            with open(self.db_path, "w") as f:
                json.dump(data, f, indent=2)

        except:
            pass

if __name__ == "__main__":
    NovaMindApp().run()
