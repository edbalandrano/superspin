import kivy 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

from user_manager import UserManager

# Set window size
Window.size = (800, 600)

class UserPickerApp(App):
    def build(self):
        self.title = 'Random User Picker'
        self.user_manager = UserManager()
        self.user_manager.load_users()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Random User Picker',
            font_size=24,
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(header)
        
        # Content area with two columns
        content = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        
        # Left column - Controls
        left_column = BoxLayout(orientation='vertical', size_hint=(0.4, 1), spacing=10)
        
        # Settings button
        settings_button = Button(
            text='Settings',
            size_hint=(1, None),
            height=50,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        settings_button.bind(on_press=self.show_settings)
        
        # Inactive users dropdown (keep this in main UI)
        inactive_dropdown_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=90, spacing=5)
        inactive_label = Label(text='Inactive Users', size_hint=(1, None), height=20)
        self.inactive_spinner = Spinner(
            text='Select inactive user',
            values=[],
            size_hint=(1, None),
            height=40
        )
        reactivate_button = Button(
            text='Reactivate User',
            size_hint=(1, None),
            height=40,
            background_color=(0.3, 0.5, 0.7, 1)
        )
        reactivate_button.bind(on_press=self.reactivate_user)
        
        inactive_dropdown_layout.add_widget(inactive_label)
        inactive_dropdown_layout.add_widget(self.inactive_spinner)
        inactive_dropdown_layout.add_widget(reactivate_button)
        
        # Create a layout for the main controls (without add user which will be in settings)
        main_controls_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5)
        main_controls_layout.add_widget(settings_button)
        main_controls_layout.add_widget(inactive_dropdown_layout)
        
        # Pick user button
        pick_user_button = Button(
            text='Pick Random User',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.3, 0.7, 1),
            font_size=20
        )
        pick_user_button.bind(on_press=self.pick_user)
        
        # I quit button (only enabled when a user is selected)
        self.quit_button = Button(
            text='I Quit',
            size_hint=(1, 0.15),
            background_color=(0.7, 0.2, 0.2, 1),
            disabled=True
        )
        self.quit_button.bind(on_press=self.user_quit)
        
        # Exit button
        exit_button = Button(
            text='Save & Exit',
            size_hint=(1, 0.15),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        exit_button.bind(on_press=self.save_and_exit)
        
        # Add widgets to left column
        left_column.add_widget(main_controls_layout)
        left_column.add_widget(pick_user_button)
        left_column.add_widget(self.quit_button)
        left_column.add_widget(exit_button)
        
        # Right column - User Lists
        right_column = BoxLayout(orientation='vertical', size_hint=(0.6, 1), spacing=10)
        
        # Selected user display
        self.selected_user_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        self.selected_user_label = Label(
            text='No User Selected',
            font_size=22,
            color=(1, 0.8, 0, 1),
            size_hint=(1, 0.7)
        )
        self.selected_user_stats = Label(
            text='',
            font_size=16,
            size_hint=(1, 0.3)
        )
        self.selected_user_layout.add_widget(self.selected_user_label)
        self.selected_user_layout.add_widget(self.selected_user_stats)
        
        # Tabs for active and inactive users
        tabs_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.active_tab_button = Button(
            text='Active Users',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.inactive_tab_button = Button(
            text='Inactive Users',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.active_tab_button.bind(on_press=lambda x: self.switch_tab('active'))
        self.inactive_tab_button.bind(on_press=lambda x: self.switch_tab('inactive'))
        tabs_layout.add_widget(self.active_tab_button)
        tabs_layout.add_widget(self.inactive_tab_button)
        
        # User list area
        self.users_scroll = ScrollView(size_hint=(1, 0.6))
        self.users_grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.users_grid.bind(minimum_height=self.users_grid.setter('height'))
        self.users_scroll.add_widget(self.users_grid)
        
        # Add all to right column
        right_column.add_widget(self.selected_user_layout)
        right_column.add_widget(tabs_layout)
        right_column.add_widget(self.users_scroll)
        
        # Add columns to content area
        content.add_widget(left_column)
        content.add_widget(right_column)
        
        # Add content to main layout
        main_layout.add_widget(content)
        
        # Status bar
        self.status_bar = Label(
            text='Ready',
            size_hint=(1, 0.05),
            halign='left'
        )
        main_layout.add_widget(self.status_bar)
        
        # Initialize the display
        self.current_tab = 'active'
        self.update_user_list()
        
        return main_layout
    
    def update_user_list(self):
        # Clear the grid
        self.users_grid.clear_widgets()
        
        # Get the appropriate user list
        if self.current_tab == 'active':
            users = self.user_manager.get_active_users()
            if not users:
                info = Label(text='No active users', size_hint_y=None, height=40)
                self.users_grid.add_widget(info)
        else:
            users = self.user_manager.get_inactive_users()
            if not users:
                info = Label(text='No inactive users', size_hint_y=None, height=40)
                self.users_grid.add_widget(info)
        
        # Add users to the grid
        for user in users:
            user_item = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            name_label = Label(text=user.name, size_hint=(0.5, 1), halign='left')
            session_label = Label(text=f'This session: {user.picked_this_instance}', size_hint=(0.25, 1))
            all_time_label = Label(text=f'All time: {user.times_picked}', size_hint=(0.25, 1))
            user_item.add_widget(name_label)
            user_item.add_widget(session_label)
            user_item.add_widget(all_time_label)
            self.users_grid.add_widget(user_item)
        
        # Update inactive users dropdown
        inactive_users = self.user_manager.get_inactive_users()
        inactive_names = [user.name for user in inactive_users]
        self.inactive_spinner.values = inactive_names
        if not inactive_names:
            self.inactive_spinner.text = 'No inactive users'
        elif self.inactive_spinner.text not in inactive_names:
            self.inactive_spinner.text = 'Select User'
        
        # Update status bar
        active_count = len(self.user_manager.get_active_users())
        inactive_count = len(self.user_manager.get_inactive_users())
        self.status_bar.text = f'Active Users: {active_count} | Inactive Users: {inactive_count}'
    
    def switch_tab(self, tab):
        self.current_tab = tab
        if tab == 'active':
            self.active_tab_button.background_color = (0.2, 0.7, 0.3, 1)
            self.inactive_tab_button.background_color = (0.5, 0.5, 0.5, 1)
        else:
            self.active_tab_button.background_color = (0.5, 0.5, 0.5, 1)
            self.inactive_tab_button.background_color = (0.2, 0.7, 0.3, 1)
        self.update_user_list()
    
    def add_user(self, instance):
        username = self.add_user_input.text.strip()
        if username:
            result = self.user_manager.add_user(username)
            if result == 'added':
                self.status_bar.text = f'Added new user: {username}'
            elif result == 'reactivated':
                self.status_bar.text = f'Reactivated user: {username}'
            elif result == 'exists':
                self.status_bar.text = f'User {username} already exists'
            self.add_user_input.text = ''
            self.update_user_list()
        else:
            self.status_bar.text = 'Please enter a username'
    
    def pick_user(self, instance):
        if self.user_manager.get_active_user_count() < 2:
            self.show_popup('Not Enough Users', 'You need at least 2 active users to pick.')
            return
        
        selected_user = self.user_manager.pick_random_user()
        if selected_user:
            self.selected_user_label.text = f'Selected: {selected_user.name}'
            self.selected_user_stats.text = f'Times Picked: {selected_user.times_picked}'
            self.quit_button.disabled = False
            self.status_bar.text = f'Picked user: {selected_user.name}'
            self.update_user_list()
        else:
            self.status_bar.text = 'No active users to pick from'
    
    def user_quit(self, instance):
        if self.user_manager.last_selected_user:
            user_name = self.user_manager.last_selected_user.name
            self.user_manager.user_quit(user_name)
            self.selected_user_label.text = 'No User Selected'
            self.selected_user_stats.text = ''
            self.quit_button.disabled = True
            self.status_bar.text = f'User {user_name} has quit'
            
            # Check if only one user remains
            if self.user_manager.get_active_user_count() <= 1:
                self.show_popup('Game Over', 'Only one or no active users remain. The game will exit.')
                self.save_and_exit(None)
            else:
                self.update_user_list()
    
    def reactivate_user(self, instance):
        selected_name = self.inactive_spinner.text
        if selected_name and selected_name not in ['Select User', 'No inactive users']:
            success, user = self.user_manager.add_user(selected_name)
            if success:
                self.status_bar.text = f'Reactivated user: {selected_name}'
                self.update_user_list()
            else:
                self.status_bar.text = f'Failed to reactivate user: {selected_name}'
        else:
            self.status_bar.text = 'Please select an inactive user first'
    
    def save_and_exit(self, instance):
        moved_count = self.user_manager.move_all_active_to_inactive()
        self.user_manager.save_users()
        self.status_bar.text = f'Moved {moved_count} active users to inactive and saved data'
        self.show_popup('Goodbye', 'All user stats have been saved.', self.stop)
    
    def show_settings(self, instance):
        """Show the settings popup with options."""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add New User section
        add_user_section = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, None), height=120)
        add_user_label = Label(text='Add New User', font_size=18, size_hint=(1, None), height=30)
        self.settings_add_user_input = TextInput(
            hint_text='Enter username',
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        add_user_button = Button(
            text='Add User',
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        add_user_button.bind(on_press=self.add_user_from_settings)
        
        add_user_section.add_widget(add_user_label)
        add_user_section.add_widget(self.settings_add_user_input)
        add_user_section.add_widget(add_user_button)
        
        # Reset All Users button
        reset_section = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, None), height=90)
        reset_label = Label(text='Reset All Users', font_size=18, size_hint=(1, None), height=30)
        reset_button = Button(
            text='Reset All Users',
            size_hint=(1, None),
            height=50,
            background_color=(0.7, 0.3, 0.3, 1)
        )
        reset_button.bind(on_press=self.reset_all_users)
        
        reset_section.add_widget(reset_label)
        reset_section.add_widget(reset_button)
        
        # Close button
        close_button = Button(
            text='Close',
            size_hint=(1, None),
            height=50
        )
        
        # Add all sections to content
        content.add_widget(add_user_section)
        content.add_widget(reset_section)
        content.add_widget(Label(size_hint=(1, 1)))  # Spacer
        content.add_widget(close_button)
        
        # Create and open popup
        settings_popup = Popup(
            title='Settings',
            content=content,
            size_hint=(0.8, 0.8)
        )
        
        # Bind close button
        close_button.bind(on_press=settings_popup.dismiss)
        
        settings_popup.open()
    
    def add_user_from_settings(self, instance):
        """Add a user from the settings popup."""
        name = self.settings_add_user_input.text.strip()
        if name:
            success, user = self.user_manager.add_user(name)
            if success:
                self.status_bar.text = f'Added user: {name}'
                self.settings_add_user_input.text = ''
                self.update_user_list()
            else:
                self.status_bar.text = f'User {name} already exists'
        else:
            self.status_bar.text = 'Please enter a username'
    
    def reset_all_users(self, instance):
        """Reset both picked_this_instance and times_picked counters for all users."""
        for user in self.user_manager.get_active_users() + self.user_manager.get_inactive_users():
            user.picked_this_instance = 0
            user.times_picked = 0
        self.user_manager.save_users()
        self.update_user_list()
        self.status_bar.text = 'Reset all users (both session and historical data)'
    
    def show_popup(self, title, message, callback=None):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='OK', size_hint=(1, 0.5))
        content.add_widget(btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.3))
        
        if callback:
            btn.bind(on_press=lambda x: (popup.dismiss(), callback()))
        else:
            btn.bind(on_press=popup.dismiss)
            
        popup.open()

if __name__ == '__main__':
    UserPickerApp().run()