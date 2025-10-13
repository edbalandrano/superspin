from user_manager import UserManager

def display_menu():
    """Display the main menu options."""
    print("\n===== RANDOM USER PICKER =====")
    print("1. Add a user")
    print("2. I quit")
    print("3. List active players")
    print("4. List inactive players")
    print("5. Pick a random user")
    print("6. Exit")
    print("============================")

def main():
    """Main program function."""
    # Initialize the user manager
    user_manager = UserManager()
    
    while True:
        # Display menu and get user choice
        display_menu()
        choice = input("Enter your choice (1-6): ")
        
        # Process user choice
        if choice == "1":
            # Add a user
            name = input("Enter user name: ")
            if name.strip():
                success, existing_user = user_manager.add_user(name)
                if success:
                    if existing_user:
                        print(f"User '{name}' reactivated with {existing_user.times_picked} previous picks!")
                    else:
                        print(f"User '{name}' added successfully!")
                    user_manager.save_users()
                else:
                    print(f"User '{name}' is already active!")
            else:
                print("Name cannot be empty!")
                
        elif choice == "2":
            # I quit (only the chosen user can quit)
            if user_manager.get_active_user_count() == 0:
                print("No active users!")
                continue
                
            if user_manager.last_selected_user is None:
                print("No user has been selected yet! Use option 5 to pick a random user first.")
                continue
                
            name = input("Enter your name to confirm quitting: ")
            if user_manager.user_quit(name):
                print(f"User '{name}' has quit after being selected!")
                user_manager.save_users()
            else:
                print(f"Only the last selected user ({user_manager.last_selected_user.name}) can quit!")
                
        elif choice == "3":
            # List active users
            users = user_manager.get_active_users()
            if users:
                print("\nActive Players:")
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user}")
            else:
                print("No active players!")
                
        elif choice == "4":
            # List inactive users
            users = user_manager.get_inactive_users()
            if users:
                print("\nInactive Players (Previous Players):")
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user}")
            else:
                print("No inactive players!")
                
        elif choice == "5":
            # Pick a random user
            if user_manager.get_active_user_count() == 0:
                print("No active users to pick from!")
                continue
                
            selected_user = user_manager.pick_random_user()
            print(f"\n🎉 Randomly selected: {selected_user} 🎉")
            print(f"(This user can now use 'I quit' option)")
            user_manager.save_users()
            
            # Check if only one user remains
            if user_manager.get_active_user_count() == 1:
                last_user = user_manager.get_active_users()[0]
                print(f"\nOnly one active user remains: {last_user}")
                user_manager.move_all_active_to_inactive()
                print("Moving all active players to inactive list...")
                print("Saving all user stats and exiting...")
                user_manager.save_users()
                break
                
        elif choice == "6":
            # Exit the program
            moved_count = user_manager.move_all_active_to_inactive()
            print(f"Moving all {moved_count} active players to inactive list...")
            print("Saving all user stats and exiting...")
            user_manager.save_users()
            break
            
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()