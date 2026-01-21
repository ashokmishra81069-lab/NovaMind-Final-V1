import os
import json
from datetime import datetime
from groq import Groq
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# API Key - Direct and working
API_KEY = "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"

class NovaMindApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        self.client = Groq(api_key=API_KEY)
        
        # Path for Android: Private internal storage
        self.db_path = os.path.join(os.getcwd(), "chat_history.json")
        
        # Check and create JSON if missing
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump([], f)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Dynamic chat display
        self.chat_label = MDLabel(
            text="[color=00FFFF]NovaMind Lite[/color]\nSawal puchiye bhai...", 
            halign="left", 
            size_hint_y=None,
            theme_text_color="Custom",
            text_color=(0, 1, 1, 1),
            markup=True
        )
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.chat_label)
        
        self.input_field = MDTextField(
            hint_text="Ask Vikramaditya's AI...", 
            mode="rectangle",
            multiline=False
        )
        
        send_btn = MDRaisedButton(
            text="SEND CHAT", 
            on_release=self.chat_logic, 
            pos_hint={"center_x": 0.5}
        )
        
        layout.add_widget(scroll)
        layout.add_widget(self.input_field)
        layout.add_widget(send_btn)
        return layout

    def chat_logic(self, *args):
        query = self.input_field.text.strip()
        if not query: return
        
        self.chat_label.text += f"\n\n[b]YOU:[/b] {query}\n\n[b]NOVAMIND:[/b] Thinking..."
        self.input_field.text = ""
        # API call in a slight delay to keep UI smooth
        Clock.schedule_once(lambda dt: self.get_api_response(query), 0.1)

    def get_api_response(self, user_text):
        try:
            res = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": user_text}]
            )
            ans = res.choices[0].message.content
            # Update UI
            self.chat_label.text = self.chat_label.text.replace("Thinking...", ans)
            
            # Reliable JSON Saving
            self.save_to_json(user_text, ans)
                
        except Exception as e:
            self.chat_label.text = self.chat_label.text.replace("Thinking...", "Network Error! Check data/WiFi.")

    def save_to_json(self, q, a):
        try:
            data = []
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
            
            data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "question": q,
                "answer": a
            })
            
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)
        except:
            pass # Don't crash if file writing fails

if __name__ == "__main__":
    NovaMindApp().run()
    
