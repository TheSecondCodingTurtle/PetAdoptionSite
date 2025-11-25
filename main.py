from os import system
from time import sleep
from adopter import *
from pet import *

adopter_manager = AdopterManager()
pet_manager = PetManager()


def display_main_menu():
    system("clear")
    print("Main Menu:\n")
    print("1. View Available Pets")
    print("2. Register as New Adopter")
    print("3. Adopter Login")
    print("4. Staff Menu")
    print("5. Quit")

    pages = [adopter_manager.view_available_pets, adopter_manager.register_as_new_adopter, adopter_manager.login, display_staff_menu, quit_site]
    options = len(pages)
    user_choice = askOption(options)
    if 1 <= user_choice <= options:
        pages[user_choice - 1]()
    else:
        print("Invalid option, reloading page...")
        sleep(1.5)
        display_main_menu()


def display_adopter_menu():
    system("clear")
    print("Adopter Menu:")
    print("1. View My Compatibility Matches")
    print("2. Reserve a Pet")
    print("3. View My Reserved/Adopted Pets")
    print("4. Cancel a Reservation")
    print("5. Logout")



def display_staff_menu():
    system("clear")
    if not check_staff_password(): 
        display_main_menu()
    else:
        system("clear")
        print("Staff Menu:\n")
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
    print("Too many incorrect attempts. Returning to main menu...")
    sleep(1.5)
    return False


def askOption(n):
    user_option = int(input(f"\nChoose from options 1-{n}: "))
    return user_option


def quit_site():
    system("clear")
    print("Thanks for visiting, come again!")
    quit()


def main():
    # TODO: make each pet and adopter in csv files an object
    display_main_menu()


main()