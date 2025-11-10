import ollama
import subprocess
import json

class VERAAndroid:
    """VERA with full Android control"""
    
    def __init__(self):
        self.model = "llama3.2:1b"
        print("✓ VERA Android Edition initialized")
    
    def speak(self, text):
        """Speak using Android TTS"""
        print(f"[VERA]: {text}")
        try:
            subprocess.run(['termux-tts-speak', text])
        except:
            pass
    
    def notify(self, title, message):
        """Show Android notification"""
        subprocess.run([
            'termux-notification',
            '-t', title,
            '-c', message
        ])
    
    def open_app(self, app_name):
        """Open Android apps"""
        apps = {
            'chrome': 'com.android.chrome',
            'youtube': 'com.google.android.youtube',
            'spotify': 'com.spotify.music',
        }
        
        if app_name in apps:
            subprocess.run([
                'am', 'start',
                '-n', apps[app_name]
            ])
    
    def get_battery(self):
        """Get battery status"""
        result = subprocess.run(
            ['termux-battery-status'],
            capture_output=True,
            text=True
        )
        
        battery = json.loads(result.stdout)
        return f"Battery at {battery['percentage']}%"
    
    def process_command(self, user_input):
        """Process commands with Android integration"""
        text_lower = user_input.lower()
        
        # Battery check
        if 'battery' in text_lower:
            status = self.get_battery()
            self.speak(status)
            return
        
        # Open apps
        if 'open' in text_lower:
            for app in ['chrome', 'youtube', 'spotify']:
                if app in text_lower:
                    self.open_app(app)
                    self.speak(f"Opening {app}.")
                    return
        
        # Send notification
        if 'notify' in text_lower or 'remind' in text_lower:
            self.notify("VERA", "Reminder set!")
            self.speak("Notification sent.")
            return
        
        # AI response
        self.ai_respond(user_input)
    
    def ai_respond(self, user_input):
        """AI conversation"""
        try:
            stream = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are VERA. Concise. 1-2 sentences.'},
                    {'role': 'user', 'content': user_input}
                ],
                stream=True
            )
            
            print("[VERA]: ", end='', flush=True)
            
            full_response = ""
            for chunk in stream:
                if chunk['message']['content']:
                    text = chunk['message']['content']
                    full_response += text
                    print(text, end='', flush=True)
            
            print()
            
            # Speak response
            self.speak(full_response)
            
        except:
            self.speak("Issue connecting to AI.")
    
    def start(self):
        """Start VERA"""
        print("=" * 50)
        print("VERA Android Edition")
        print("=" * 50)
        
        self.speak("VERA Android systems online.")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    self.speak("Shutting down.")
                    break
                
                self.process_command(user_input)
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    vera = VERAAndroid()
    vera.start()
