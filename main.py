from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

# --- Encryption Logic ---

special_mapping = {
    '"': '֣', '-': '֤', '=': '֦', '(': 'ְ', ')': 'ֲ',
    ',': '؞', '[': 'ִ', '_': 'ֻ', "'": 'ֵ', '<': 'Ṝ', '>': 'Ṩ'
}

def calculate_shift_pattern(password):
    shifts = []
    for i in range(len(password) - 1):
        shifts.append(ord(password[i + 1]) - ord(password[i]))
    return shifts if shifts else [0]

def apply_shift(char, shift):
    if char.isalpha() or char == " ":
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        is_upper = char.isupper()
        c = char.lower()
        if c in alphabet:
            idx = alphabet.index(c)
            new_char = alphabet[(idx + shift) % 27]
            return new_char.upper() if is_upper else new_char
        return char
    elif char.isdigit():
        return str((int(char) + shift) % 10)
    else:
        return char

def replace_special_chars(text):
    for char, replacement in special_mapping.items():
        text = text.replace(char, replacement)
    return text

def revert_special_chars(text):
    reverse_mapping = {v: k for k, v in special_mapping.items()}
    for replacement, char in reverse_mapping.items():
        text = text.replace(replacement, char)
    return text

def encrypt_text(text, password):
    if not text or not password:
        return text
    shifts = calculate_shift_pattern(password)
    encrypted = ""
    idx = 0
    text = replace_special_chars(text)
    for char in text:
        encrypted += apply_shift(char, shifts[idx])
        idx = (idx + 1) % len(shifts)
    return encrypted

def decrypt_text(text, password):
    if not text or not password:
        return text
    shifts = calculate_shift_pattern(password)
    decrypted = ""
    idx = 0
    for char in text:
        decrypted += apply_shift(char, -shifts[idx])
        idx = (idx + 1) % len(shifts)
    return revert_special_chars(decrypted)

# --- Password Popup ---

class PasswordPopup(Popup):
    def __init__(self, on_confirm, **kwargs):
        super().__init__(**kwargs)
        self.on_confirm = on_confirm
        self.title = "Enter Password"
        self.size_hint = (0.85, None)
        self.height = Window.height * 0.35

        layout = BoxLayout(orientation='vertical', padding=16, spacing=12)

        self.password_input = TextInput(
            password=True,
            multiline=False,
            hint_text="Password",
            font_size='18sp',
            size_hint_y=None,
            height=48,
        )

        btn_row = BoxLayout(size_hint_y=None, height=48, spacing=10)

        ok_btn = Button(text="OK", background_color=(0.2, 0.6, 1, 1))
        ok_btn.bind(on_press=self._confirm)

        cancel_btn = Button(text="Cancel", background_color=(0.5, 0.5, 0.5, 1))
        cancel_btn.bind(on_press=self.dismiss)

        btn_row.add_widget(ok_btn)
        btn_row.add_widget(cancel_btn)

        layout.add_widget(Label(text="Enter password:", size_hint_y=None, height=32, font_size='16sp'))
        layout.add_widget(self.password_input)
        layout.add_widget(btn_row)

        self.content = layout

    def _confirm(self, _):
        self.on_confirm(self.password_input.text)
        self.dismiss()

# --- Main Layout ---

class CrepeLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=10, **kwargs)

        self.text_area = TextInput(
            hint_text="Enter text here...",
            font_size='16sp',
            size_hint=(1, 1),
        )
        self.add_widget(self.text_area)

        btn_row = BoxLayout(size_hint=(1, None), height=56, spacing=10)

        encrypt_btn = Button(
            text="Encrypt",
            font_size='18sp',
            background_color=(0.2, 0.7, 0.3, 1),
        )
        encrypt_btn.bind(on_press=self._on_encrypt)

        decrypt_btn = Button(
            text="Decrypt",
            font_size='18sp',
            background_color=(0.2, 0.5, 0.9, 1),
        )
        decrypt_btn.bind(on_press=self._on_decrypt)

        btn_row.add_widget(encrypt_btn)
        btn_row.add_widget(decrypt_btn)
        self.add_widget(btn_row)

    def _on_encrypt(self, _):
        def do_encrypt(password):
            if password:
                self.text_area.text = encrypt_text(self.text_area.text, password)
        PasswordPopup(on_confirm=do_encrypt).open()

    def _on_decrypt(self, _):
        def do_decrypt(password):
            if password:
                self.text_area.text = decrypt_text(self.text_area.text, password)
        PasswordPopup(on_confirm=do_decrypt).open()

# --- App Entry Point ---

class CrepeApp(App):
    def build(self):
        self.title = "Crepe"
        return CrepeLayout()

if __name__ == "__main__":
    CrepeApp().run()
