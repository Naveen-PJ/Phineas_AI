from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from src.Phineas_AI import Phineas_AI

# Set the background color to a light grey
Window.clearcolor = (0.95, 0.95, 0.95, 1)

ai = Phineas_AI()

class SubjectSelectPage(BoxLayout):
    def __init__(self, switch_to_subject_page, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        dropdown = DropDown()
        dropdown_btn = Button(text='≡', size_hint=(None, None), size=(60, 60), background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        dropdown_btn.bind(on_release=dropdown.open)
        dropdown.add_widget(Button(text='About Us', size_hint_y=None, height=44, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        header.add_widget(dropdown_btn)
        header.add_widget(Label(text='Phineas AI', size_hint_x=1, halign='left', valign='middle', font_size=24, color=(0, 0, 0, 1)))
        self.add_widget(header)

        # Spacer to move content downwards
        self.add_widget(BoxLayout(size_hint_y=0.1))

        # Main Content
        main_layout = BoxLayout(orientation='vertical', size_hint_y=1, spacing=20)

        # Subject List
        subject_list = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, padding=[50, 20, 50, 20])  # Added padding for margins
        subject_list.bind(minimum_height=subject_list.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.6))
        scroll_view.add_widget(subject_list)

        subjects = ['Python', 'Computer Networks', 'Statistics', 'C Programming']
        for subject in subjects:
            btn = Button(text=subject, size_hint=(None, None), width=Window.width * 0.4, height=50, background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
            btn.bind(on_press=lambda btn: self.animate_button(btn, switch_to_subject_page))
            subject_list.add_widget(btn)

        # Center the subject_list
        center_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        center_layout.add_widget(scroll_view)
        main_layout.add_widget(center_layout)
        self.add_widget(main_layout)

        # Ask Phineas Button
        ask_phineas_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[10, 50])
        ask_phineas_btn = Button(text='Ask Phineas Anything...', size_hint=(None, None), size=(250, 60), background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        ask_phineas_btn.bind(on_press=self.open_phineas_popup)
        ask_phineas_layout.add_widget(ask_phineas_btn)
        self.add_widget(ask_phineas_layout)

    def animate_button(self, button, callback):
        anim = Animation(size=(button.width + 10, button.height + 10), duration=0.1) + Animation(size=(button.width, button.height), duration=0.1)
        anim.bind(on_complete=lambda *args: callback(button.text))
        anim.start(button)

    def open_phineas_popup(self, instance):
        popup = PhineasPopup()
        popup.open()

class SubjectSelectedPage(BoxLayout):
    def __init__(self, subject_name, switch_to_subject_select_page, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        dropdown = DropDown()
        dropdown_btn = Button(text='≡', size_hint=(None, None), size=(60, 60), background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1))
        dropdown_btn.bind(on_release=dropdown.open)
        dropdown.add_widget(Button(text='About Us', size_hint_y=None, height=44, background_color=(0.2, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        header.add_widget(dropdown_btn)
        header.add_widget(Label(text='Phineas AI', size_hint_x=1, halign='left', valign='middle', font_size=24, color=(0, 0, 0, 1)))
        self.add_widget(header)

        # Main Content
        main_layout = BoxLayout(orientation='horizontal', spacing=20)

        # Left Side Content
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=20)

        # Subject and Repo
        subject_repo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        subject_repo_layout.add_widget(Label(text=subject_name, font_size=24, color=(0, 0, 0, 1)))
        accessrepobutton = Button(text='Access Repo', font_size=18, background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1))
        accessrepobutton.bind(on_press=lambda instance: ai.openrepo())
        subject_repo_layout.add_widget(accessrepobutton)
        left_layout.add_widget(subject_repo_layout)

        # Transcription Controls
        transcription_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        startbutton = Button(text='Start Transcription', background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        startbutton.bind(on_press=lambda instance: self.animate_button(instance, lambda *args: ai.start_transcription(subject_name)))
        transcription_layout.add_widget(startbutton)
        puasebutton = Button(text='Pause', background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        puasebutton.bind(on_press=lambda instance: self.animate_button(instance, lambda *args: ai.pause_and_resume()))
        transcription_layout.add_widget(puasebutton)
        stopbutton = Button(text='Stop Transcription', background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        stopbutton.bind(on_press=lambda instance: self.animate_button(instance, lambda *args: ai.stop_transcription()))
        transcription_layout.add_widget(stopbutton)
        left_layout.add_widget(transcription_layout)

        main_layout.add_widget(left_layout)

        # To-Do List
        todo_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, padding=[10, 10])
        todo_layout.add_widget(Label(text='To-do List', font_size=24, color=(0, 0, 0, 1)))
        todo_item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        todo_item_layout.add_widget(Label(text='Lorem Ipsum', color=(0, 0, 0, 1)))
        todo_item_layout.add_widget(Button(text='Delete', size_hint_x=None, width=70, background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1)))
        todo_layout.add_widget(todo_item_layout)
        main_layout.add_widget(todo_layout)

        self.add_widget(main_layout)

        # Ask Phineas Button
        ask_phineas_layout = AnchorLayout(anchor_x='center', anchor_y='bottom', padding=[10, 50])
        ask_phineas_btn = Button(text='Ask Phineas Anything...', size_hint=(None, None), size=(250, 60), background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        ask_phineas_btn.bind(on_press=self.open_phineas_popup)
        ask_phineas_layout.add_widget(ask_phineas_btn)
        self.add_widget(ask_phineas_layout)

        # Leave Button
        leave_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 10])
        leave_btn = Button(text='Leave', size_hint=(None, None), size=(100, 50), background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1), font_size=18)
        leave_btn.bind(on_press=switch_to_subject_select_page)
        leave_layout.add_widget(leave_btn)
        self.add_widget(leave_layout)

    def animate_button(self, button, callback):
        anim = Animation(size=(button.width + 10, button.height + 10), duration=0.1) + Animation(size=(button.width, button.height), duration=0.1)
        anim.bind(on_complete=lambda *args: callback())
        anim.start(button)

    def open_phineas_popup(self, instance):
        popup = PhineasPopup()
        popup.open()

class PhineasPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Phineas AI'
        self.size_hint = (0.8, 0.8)

        # Main layout for the popup
        layout = BoxLayout(orientation='vertical', padding=5, spacing=10)

        # Scrollable chat window
        self.chat_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.chat_layout)
        layout.add_widget(scroll_view)

        # User input area
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.text_input = TextInput(hint_text='Type here...', multiline=False, size_hint_x=0.8, font_size=18)
        enter_button = Button(text='Enter', size_hint_x=0.2, background_color=(0.2, 0.6, 0.8, 1), color=(1, 1, 1, 1), font_size=18)
        enter_button.bind(on_release=self.handle_user_input)

        input_layout.add_widget(self.text_input)
        input_layout.add_widget(enter_button)

        layout.add_widget(input_layout)

        # Close button
        close_btn = Button(text='Close', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5}, background_color=(0.8, 0.2, 0.2, 1), color=(1, 1, 1, 1), font_size=18)
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

    def handle_user_input(self, instance):
        user_message = self.text_input.text.strip()
        if user_message:
            self.add_message("You", user_message)
            self.text_input.text = ""

            # Simulate a response (replace this with actual AI/logic integration)
            self.add_message("Phineas AI", f"Echo: {user_message}")

    def add_message(self, sender, message):
        # Add a message to the chat
        message_label = Label(
            text=f"[b]{sender}:[/b] {message}",
            size_hint_y=None,
            markup=True,
            halign="left",
            valign="middle"
        )
        message_label.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        message_label.bind(texture_size=lambda s, t: s.setter('size')(s, (s.width, t[1])))

        self.chat_layout.add_widget(message_label)
        self.chat_layout.height += message_label.height

        # Scroll to the bottom
        self.chat_layout.parent.scroll_y = 0

class PhineasApp(App):
    def build(self):
        self.root = BoxLayout()
        self.subject_select_page = SubjectSelectPage(self.switch_to_subject_page)
        self.subject_selected_page = None  # Initialize it to None
        self.root.add_widget(self.subject_select_page)
        return self.root

    def switch_to_subject_page(self, subject_name):
        self.subject_selected_page = SubjectSelectedPage(subject_name, self.switch_to_subject_select_page)
        self.root.clear_widgets()
        self.root.add_widget(self.subject_selected_page)

    def switch_to_subject_select_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.subject_select_page)

if __name__=="__main__":
    PhineasApp().run()
