from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class SubjectSelectPage(BoxLayout):
    def __init__(self, switch_to_subject_page, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        dropdown = DropDown()
        dropdown_btn = Button(text='≡', size_hint=(None, None), size=(50, 50))
        dropdown_btn.bind(on_release=dropdown.open)
        dropdown.add_widget(Button(text='About Us', size_hint_y=None, height=44))
        header.add_widget(dropdown_btn)
        header.add_widget(Label(text='Phineas AI', size_hint_x=1, halign='left', valign='middle'))
        self.add_widget(header)

        # Main Content
        main_layout = BoxLayout(orientation='horizontal')

        # Subject List
        subject_list = BoxLayout(orientation='vertical', size_hint_x=0.3)
        subject_list.add_widget(Label(text='Choose Subject:', size_hint_y=None, height=30, halign='left'))
        
        subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4']
        for subject in subjects:
            btn = Button(text=subject, size_hint_y=None, height=50)
            btn.bind(on_press=switch_to_subject_page)
            subject_list.add_widget(btn)
        
        main_layout.add_widget(subject_list)

        # Empty space
        main_layout.add_widget(BoxLayout())

        # Add main layout to the page
        self.add_widget(main_layout)

        # Ask Phineas Button
        ask_phineas_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 70])
        ask_phineas_btn = Button(text='Ask Phineas Anything...', size_hint=(None, None), size=(200, 50))
        ask_phineas_btn.bind(on_press=self.open_phineas_popup)
        ask_phineas_layout.add_widget(ask_phineas_btn)
        self.add_widget(ask_phineas_layout)

        # Footer
        footer = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 10])
        footer_label = Label(text='Phineas AI Inc.', size_hint=(None, None))
        footer.add_widget(footer_label)
        self.add_widget(footer)

    def open_phineas_popup(self, instance):
        popup = PhineasPopup()
        popup.open()

class SubjectSelectedPage(BoxLayout):
    def __init__(self, switch_to_subject_select_page, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 30

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        dropdown = DropDown()
        dropdown_btn = Button(text='≡', size_hint=(None, None), size=(50, 50))
        dropdown_btn.bind(on_release=dropdown.open)
        dropdown.add_widget(Button(text='About Us', size_hint_y=None, height=44))
        header.add_widget(dropdown_btn)
        header.add_widget(Label(text='Phineas AI', size_hint_x=1, halign='left', valign='middle'))
        self.add_widget(header)

        # Main Content
        main_layout = BoxLayout(orientation='horizontal')

        # Left Side Content
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.7, spacing=10)

        # Subject and Repo
        subject_repo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        subject_repo_layout.add_widget(Label(text='Subject Chosen', font_size=20))
        subject_repo_layout.add_widget(Button(text='Access Repo', font_size=14))
        left_layout.add_widget(subject_repo_layout)

        # Transcription Controls
        transcription_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        transcription_layout.add_widget(Button(text='Start Transcription'))
        transcription_layout.add_widget(Button(text='Pause'))
        transcription_layout.add_widget(Button(text='Stop Transcription'))
        left_layout.add_widget(transcription_layout)

        main_layout.add_widget(left_layout)

        # To-Do List
        todo_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, padding=[10, 10])
        todo_layout.add_widget(Label(text='To-do List', font_size=18))
        todo_item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        todo_item_layout.add_widget(Label(text='Lorem Ipsum'))
        todo_item_layout.add_widget(Button(text='Delete', size_hint_x=None, width=70))
        todo_layout.add_widget(todo_item_layout)
        main_layout.add_widget(todo_layout)

        self.add_widget(main_layout)

        # Ask Phineas Button
        ask_phineas_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 90])
        ask_phineas_btn = Button(text='Ask Phineas Anything...', size_hint=(None, None), size=(200, 50))
        ask_phineas_btn.bind(on_press=self.open_phineas_popup)
        ask_phineas_layout.add_widget(ask_phineas_btn)
        self.add_widget(ask_phineas_layout)

        # Leave Button
        leave_layout = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 10])
        leave_btn = Button(text='Leave', size_hint=(None, None), size=(100, 50), background_color=(1, 0, 0, 1))
        leave_btn.bind(on_press=switch_to_subject_select_page)
        leave_layout.add_widget(leave_btn)
        self.add_widget(leave_layout)

        # Footer
        footer = AnchorLayout(anchor_x='right', anchor_y='bottom', padding=[10, 10])
        footer_label = Label(text='Phineas AI Inc.', size_hint=(None, None))
        footer.add_widget(footer_label)
        self.add_widget(footer)

    def open_phineas_popup(self, instance):
        popup = PhineasPopup()
        popup.open()

class PhineasPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Phineas AI'
        self.size_hint = (0.8, 0.8)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        transcribing_label = Label(text='Transcribing...', size_hint_y=None, height=30, halign='left')
        response_label = Label(text='Response...', size_hint_y=None, height=30, halign='right')
        layout.add_widget(transcribing_label)
        layout.add_widget(response_label)

        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=[0, 10])
        text_input = TextInput(hint_text='Type here...', size_hint_x=0.9)
        mic_button = Button(text='🎤', size_hint_x=0.1)
        input_layout.add_widget(text_input)
        input_layout.add_widget(mic_button)

        layout.add_widget(input_layout)

        # Close Button
        close_btn = Button(text='Close', size_hint=(None, None), size=(100, 50), pos_hint={'right': 1})
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)

        self.content = layout

class PhineasApp(App):
    def build(self):
        self.root = BoxLayout()
        self.subject_select_page = SubjectSelectPage(self.switch_to_subject_page)
        self.subject_selected_page = SubjectSelectedPage(self.switch_to_subject_select_page)
        self.root.add_widget(self.subject_select_page)
        return self.root

    def switch_to_subject_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.subject_selected_page)

    def switch_to_subject_select_page(self, instance):
        self.root.clear_widgets()
        self.root.add_widget(self.subject_select_page)

if __name__ == '__main__':
    PhineasApp().run()
