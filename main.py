from os import system
from time import sleep

def displayMainMenu():
    system("clear")
    print("Main Menu:")
    print("1. View Available Pets")
    print("2. Register as New Adopter")
    print("3. Adopter Login")
    print("4. Staff Menu")
    print("5. Quit")

    options = 5
    user_choice = askOption(options)
    if 1 <= user_choice <= options:
        pass
    else:
        print("Invalid option, reloading page...")
        sleep(1.5)

        displayMainMenu()

def viewAvailablePets():
    pass


def register():
    print("Register Page:")
    print("Fill out the following to register: \n")

    name = input("Full name (must be at least 2 words): ")
    home_type = input("Home type (Flat, House, or Farm only): ")
    experience = input("Experience level (None, Some, or Expert): ")
    pet_size = input("Preferred pet size (Small, Medium, Large, or Any): ")
    energy_level = input("Preferred energy level (Low, Medium, High, or Any): ")


def login():
    pass


def displayStaffMenu():
    system("clear")

    if not check_staff_password(): 
        displayMainMenu()
    else:
        system("clear")
        print("Staff Menu:")
        print("1. Add New Pet")
        print("2. Complete an Adoption")
        print("3. View All pets")
        print("4. View Statistics")
        print("5. Remove a pet")
        print("6. Logout")


def check_staff_password():
    password = "admin123"
    for i in range(3):
        entered_password = input("Enter staff password: ")
        if entered_password == password:
            return True
        else:
            print(f"Incorrect password. Attempts remaining: {2 - i}\n")
    print("Too many incorrect attempts. Returning to main menu.")
    sleep(2)
    return False


def quit():
    pass


def displayAdopterMenu():
    system("clear")
    print("Adopter Menu:")
    print("1. View Available Pets")
    print("2. Apply to Adopt a Pet")
    print("3. View My Applications")
    print("4. Update My Information")
    print("5. Logout")


def askOption(n):
    user_option = int(input(f"\nChoose from options 1-{n}: "))
    return user_option
    

def main():
    displayMainMenu()

main()
