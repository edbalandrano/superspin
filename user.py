class User:
    """
    Represents a user with attributes that can be tracked across program runs.
    """
    def __init__(self, name, times_picked=0, picked_this_instance=0):
        """
        Initialize a user with a name and optional times_picked counter.
        
        Args:
            name (str): The name of the user
            times_picked (int, optional): Number of times this user has been picked all time. Defaults to 0.
            picked_this_instance (int, optional): Number of times picked in current session. Defaults to 0.
        """
        self.name = name
        self.times_picked = times_picked
        self.picked_this_instance = picked_this_instance
    
    def increment_times_picked(self):
        """Increment both times_picked and picked_this_instance counters by 1."""
        self.times_picked += 1
        self.picked_this_instance += 1
    
    def to_dict(self):
        """
        Convert user to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            'name': self.name,
            'times_picked': self.times_picked,
            'picked_this_instance': self.picked_this_instance
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User instance from dictionary data.
        
        Args:
            data (dict): Dictionary containing user data
            
        Returns:
            User: A new User instance
        """
        return cls(
            name=data['name'],
            times_picked=data['times_picked'],
            picked_this_instance=data.get('picked_this_instance', 0)
        )
    
    def __str__(self):
        """String representation of the user."""
        return f"{self.name} (Picked {self.times_picked} times)"