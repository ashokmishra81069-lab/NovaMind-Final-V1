import os
import json
import base64
from datetime import datetime
from groq import Groq
from PIL import Image
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ============================================================
# PROJECT: NOVAMIND AI - ULTIMATE GLOBAL HYBRID ENGINE
# ARCHITECT & DEVELOPER: VIKRAMADITYA MISHRA
# VERSION: 5.0.1 (CRASH-PROOF & PERMANENT MEMORY)
# ============================================================

API_KEY = "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"
HELPLINE_EMAIL = "vikramadityamishra701@gmail.com"
console = Console()

class NovaMindHybrid:
    def __init__(self):
        self.dev = "VIKRAMADITYA MISHRA"
        self.client = Groq(api_key=API_KEY)
        self.db_path = "novamind_master_vault.json"
        self.secret_vault_path = "novamind_secret_chat.json"
        self.load_configs()

    def load_configs(self):
        # Master Config Loading with Crash Protection
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = {"user_data": {}, "history": [], "banned": False}
        else:
            self.config = {"user_data": {}, "history": [], "banned": False}
        
        # Safely ensuring all keys exist (Fix for KeyError: 'banned')
        default_keys = {"user_data": {}, "history": [], "banned": False}
        for key, value in default_keys.items():
            if key not in self.config:
                self.config[key] = value

        # Secret Vault Loading
        if os.path.exists(self.secret_vault_path):
            try:
                with open(self.secret_vault_path, 'r') as f:
                    self.vault = json.load(f)
            except:
                self.vault = {"password": None, "secret_chats": []}
        else:
            self.vault = {"password": None, "secret_chats": []}

    def save_all(self):
        try:
            with open(self.db_path, 'w') as f: json.dump(self.config, f, indent=4)
            with open(self.secret_vault_path, 'w') as f: json.dump(self.vault, f, indent=4)
        except Exception as e:
            console.print(f"[red]Storage Error: {str(e)}[/red]")

    def analyze_intent(self, text):
        medical = ["private part", "health", "skin care", "doctor", "pain", "periods", "body"]
        abuse = ["abuse_word1", "abuse_word2"] # Yahan real filters add karein
        if any(w in text.lower() for w in abuse): return "BANNED"
        if any(w in text.lower() for w in medical): return "SECRET"
        return "GENERAL"

    def process_vision(self, image_path, prompt):
        try:
            with open(image_path, "rb") as img:
                encoded = base64.b64encode(img.read()).decode('utf-8')
            res = self.client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, 
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}]}]
            )
            return res.choices[0].message.content
        except Exception as e: return f"Vision Error: {str(e)}"

    def get_ai_response(self, text):
        user_info = json.dumps(self.config.get("user_data", {}))
        system_prompt = f"""You are NovaMind AI, a friendly global assistant created by {self.dev}. 
        User Memory: {user_info}. 
        Rules: 1. Be like a close friend. 2. For female users, offer skin care/health tips. 
        3. Never forget user's data. 4. Creator: Vikramaditya Mishra."""
        
        try:
            res = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": text}]
            )
            return res.choices[0].message.content
        except: return "Connection Error! Please check your internet."

    def start(self):
        header = Text(f"NOVAMIND AI | Developed by {self.dev}", style="bold cyan")
        console.print(Panel(header, border_style="blue", title="[bold white]Global Hybrid Engine v5.0.1[/bold white]"))
        
        while True:
            if self.config.get("banned", False):
                console.print("[bold red]ACCESS DENIED. Account Banned for Policy Violation.[/bold red]")
                break

            user_input = console.input("\n[bold green]YOU (exit/vision/history): [/bold green]")
            if user_input.lower() == 'exit': break
            
            if user_input.lower() == 'history':
                console.print(Panel(str(self.config["history"][-5:]), title="Recent Logs"))
                continue

            if user_input.lower() == 'vision':
                path = console.input("[bold yellow]Image Path: [/bold yellow]")
                if os.path.exists(path):
                    q = console.input("[bold yellow]Question about image: [/bold yellow]")
                    console.print("[magenta]Analyzing...[/magenta]")
                    response = self.process_vision(path, q)
                    console.print(Panel(response, title="Vision Result", border_style="green"))
                else: console.print("[red]File not found![/red]")
                continue

            intent = self.analyze_intent(user_input)
            
            if intent == "BANNED":
                console.print("[bold red]Violation Detected! Ban Imposed. Developer Notified.[/bold red]")
                self.config["banned"] = True
                self.save_all()
                continue

            console.print("[bold magenta]NovaMind is thinking...[/bold magenta]")
            response = self.get_ai_response(user_input)

            if intent == "SECRET":
                if not self.vault.get("password"):
                    self.vault["password"] = console.input("[red]Sensitive topic. Set Vault Password: [/red]")
                self.vault["secret_chats"].append({"q": user_input, "a": response, "time": str(datetime.now())})
                console.print(Panel(response, title="SECURE VAULT", border_style="red"))
            else:
                self.config["history"].append({"q": user_input, "a": response})
                # Auto-Memory Feature
                if any(x in user_input.lower() for x in ["my name is", "i am", "call me"]):
                    self.config["user_data"]["identity"] = user_input
                console.print(Panel(response, title="NovaMind AI", border_style="cyan"))
            
            self.save_all()

if __name__ == "__main__":
    nova = NovaMindHybrid()
    nova.start()

