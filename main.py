from os import system
from time import sleep


def displayMainMenu():
    system("clear")
    print("Main Menu:\n")
    print("1. View Available Pets")
    print("2. Register as New Adopter")
    print("3. Adopter Login")
    print("4. Staff Menu")
    print("5. Quit")

 
    pages = [viewAvailablePets, register, login, displayStaffMenu, quit_site]
    options = len(pages)
    user_choice = askOption(options)
    if 1 <= user_choice <= options:
        pages[user_choice - 1]()
    else:
        print("Invalid option, reloading page...")
        sleep(1.5)

        displayMainMenu()

def viewAvailablePets():
    pass


def register():
    system("clear")
    print("Register Page:\n")
    print("Fill out the following to register:")

    name = input("1. Full name (must be at least 2 words): ")
    home_type = input("2. Home type (Flat, House, or Farm only): ")
    experience = input("3. Experience level (None, Some, or Expert): ")
    pet_size = input("4. Preferred pet size (Small, Medium, Large, or Any): ")
    energy_level = input("5. Preferred energy level (Low, Medium, High, or Any): ")


def login():
    pass


def displayStaffMenu():
    system("clear")

    if not check_staff_password(): 
        displayMainMenu()
    else:
        system("clear")
        print("Staff Menu:\n")
        print("1. Add New Pet")
        print("2. Complete an Adoption")
        print("3. View All pets")
        print("4. View Statistics")
        print("5. Remove a pet")
        print("6. Logout")


def quit_site():
    system("clear")
    print("Site quit")
    quit()


def check_staff_password():
    password = "admin123"
    for i in range(3):
        entered_password = input("Enter staff password: ")
        if entered_password == password:
            return True
        else:
            print(f"Incorrect password. Attempts remaining: {2 - i}\n")
    print("Too many incorrect attempts. Returning to main menu...")
    sleep(1.5)
    return False


def displayAdopterMenu():
    system("clear")
    print("Adopter Menu:")
    print("1. View My Compatibility Matches")
    print("2. Reserve a Pet")
    print("3. View My Reserved/Adopted Pets")
    print("4. Cancel a Reservation")
    print("5. Logout")

def viewCompatabilityMatches():
    pass

def reservePet():
    pass

def viewReservedAdoptedPets():
    pass

def cancelReservation():
    pass

def logout():
    system("clear")
    print("Logged out. Returning to main menu...")
    sleep(1.5)
    displayMainMenu()


def checkCompatbility(pet_type, pet_size, pet_energy_level, pet_age, preferred_size, preferred_energy_level, experience, home_type):
    points = 0

    if home_type == "flat" and pet_size == "large": points -= 20
    if home_type == "farm" and pet_type == "dog": points += 15
    if home_type == "flat" and pet_type != "dog": points += 10

    if pet_size == preferred_size: points += 20
    elif preferred_size == "any": points += 10

    if experience == "expert": points += 15
    elif experience == "some": points += 10
    elif pet_energy_level == "high": points -= 15

    if pet_age >= 6: points += 10

    if points >= 50: compatability_rating = "Excellent Match ⭐⭐⭐"
    elif 30 <= points <= 49: compatability_rating = "Good Match ⭐⭐"
    elif 10 <= points <= 29:: compatability_rating = "Possible Match ⭐"
    else: compatability_rating = "Not Recommended"

    return compatability_rating



def askOption(n):
    user_option = int(input(f"\nChoose from options 1-{n}: "))
    return user_option
    

def main():
    displayMainMenu()


main()
