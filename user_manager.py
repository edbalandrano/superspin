import json
import random
import os
from user import User

class UserManager:
    """
    Manages collections of active and inactive users with functionality to add, remove, and randomly select users.
    Also handles persistence of user data between program runs.
    """
    def __init__(self, data_file="users_data.json"):
        """
        Initialize the UserManager with empty active and inactive user lists and data file path.
        
        Args:
            data_file (str, optional): Path to the data file. Defaults to "users_data.json".
        """
        self.active_users = []
        self.inactive_users = []
        self.last_selected_user = None
        self.data_file = data_file
        self.load_users()
        
        # Reset picked_this_instance for all users at startup
        for user in self.active_users + self.inactive_users:
            user.picked_this_instance = 0
    
    def add_user(self, name):
        """
        Add a new user to the active collection, checking for duplicates in both active and inactive lists.
        If the user exists in inactive list, move them to active list.
        
        Args:
            name (str): Name of the user to add
            
        Returns:
            tuple: (bool, User) - (True if user was added/activated, False if active user with same name exists, 
                                  User object if existing user was reactivated, None otherwise)
        """
        # Check if user with this name already exists in active users
        if any(user.name.lower() == name.lower() for user in self.active_users):
            return False, None
        
        # Check if user exists in inactive users
        for i, user in enumerate(self.inactive_users):
            if user.name.lower() == name.lower():
                # Move from inactive to active
                existing_user = self.inactive_users.pop(i)
                self.active_users.append(existing_user)
                return True, existing_user
        
        # Add new user to active list
        new_user = User(name)
        self.active_users.append(new_user)
        return True, None
    
    def user_quit(self, name):
        """
        Move a user from active to inactive list.
        Only the last selected user can quit.
        
        Args:
            name (str): Name of the user to quit
            
        Returns:
            bool: True if user was moved to inactive, False if not allowed or not found
        """
        # Only the last selected user can quit
        if self.last_selected_user is None or self.last_selected_user.name.lower() != name.lower():
            return False
        
        for i, user in enumerate(self.active_users):
            if user.name.lower() == name.lower():
                # Move from active to inactive
                quitting_user = self.active_users.pop(i)
                self.inactive_users.append(quitting_user)
                self.last_selected_user = None
                return True
        return False
    
    def pick_random_user(self):
        """
        Pick a random user from the active collection and increment their times_picked counter.
        
        Returns:
            User or None: The randomly selected user, or None if no active users exist
        """
        if not self.active_users:
            return None
        
        selected_user = random.choice(self.active_users)
        selected_user.increment_times_picked()
        self.last_selected_user = selected_user
        return selected_user
    
    def get_active_users(self):
        """
        Get all active users.
        
        Returns:
            list: List of all active User objects
        """
        return self.active_users
    
    def get_inactive_users(self):
        """
        Get all inactive users.
        
        Returns:
            list: List of all inactive User objects
        """
        return self.inactive_users
    
    def save_users(self):
        """
        Save all users (active and inactive) to the data file.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            data = {
                "active": [user.to_dict() for user in self.active_users],
                "inactive": [user.to_dict() for user in self.inactive_users]
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def load_users(self):
        """
        Load users from the data file into active and inactive lists.
        
        Returns:
            bool: True if load was successful, False otherwise
        """
        if not os.path.exists(self.data_file):
            return False
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            # Handle both old and new format
            if isinstance(data, list):
                # Old format - all users are active
                self.active_users = [User.from_dict(user_data) for user_data in data]
                self.inactive_users = []
            else:
                # New format with active and inactive users
                self.active_users = [User.from_dict(user_data) for user_data in data.get("active", [])]
                self.inactive_users = [User.from_dict(user_data) for user_data in data.get("inactive", [])]
            
            return True
        except Exception as e:
            print(f"Error loading users: {e}")
            return False
    
    def get_active_user_count(self):
        """
        Get the number of active users.
        
        Returns:
            int: Number of active users
        """
        return len(self.active_users)
    
    def get_inactive_user_count(self):
        """
        Get the number of inactive users.
        
        Returns:
            int: Number of inactive users
        """
        return len(self.inactive_users)
        
    def move_all_active_to_inactive(self):
        """
        Move all active users to the inactive list.
        Used when ending the program to save all user stats.
        
        Returns:
            int: Number of users moved
        """
        count = len(self.active_users)
        self.inactive_users.extend(self.active_users)
        self.active_users = []
        self.last_selected_user = None
        return count