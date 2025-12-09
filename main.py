from os import system
from time import sleep
import pandas as pd
import re


class AdopterManager:
    @staticmethod
    def register_as_new_adopter():
        system("clear")
        print("Register Page:\n")
        print("Fill out the following to register:")

        string_pattern = re.compile(r"^[a-zA-Z\s]+$")
        valid_home_types = ["Flat", "House", "Farm"]
        valid_experiences = ["None", "Some", "Expert"]
        valid_sizes = ["Small", "Medium", "Large", "Any"]
        valid_energy_levels = ["Low", "Medium", "High", "Any"]

        name = input("1. Full name (must be at least 2 words): ").strip().title()
        if not re.search(string_pattern, name):
            print("Invalid input")
            return False

        home_type = input("2. Home type (Flat, House, or Farm): ").strip().title()
        if home_type not in valid_home_types:
            print("Invalid input")
            return False

        experience = input("3. Experience level (None, Some, or Expert): ").strip().title()
        if experience not in valid_experiences:
            print("Invalid input")
            return False

        preferred_size = input("4. Preferred pet size (Small, Medium, Large, or Any): ").strip().title()
        if preferred_size not in valid_sizes:
            print("Invalid input")
            return False

        preferred_energy_level = input("5. Preferred energy level (Low, Medium, High, or Any): ").strip().title()
        if preferred_energy_level not in valid_energy_levels:
            print("Invalid input")
            return False

        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        last_id = adopter_df.index[-1]
        last_num = int(last_id[1::])
        new_adopter_id = f"P{1+last_num:03d}"

        new_adopter = {
            "AdopterID": new_adopter_id,
            "Name": name,
            "HomeType": home_type,
            "Experience": experience,
            "PreferredSize": preferred_size,
            "PreferredEnergy": preferred_size,
            "Adopted/ReservedPets": "None",
        }
    
        # TODO: fix why new_adopter_df isn't being added to the adopters.csv
        new_adopter_df = pd.DataFrame([new_adopter])
        new_adopter_df.to_csv("adopters.csv", mode="a", index=False, header=False)
        
        print("\nThank you for signing up.")
        print(f"Your unique adopter ID is: {new_adopter_id}")
        return

    
    @staticmethod
    def login():
        system("clear")
        print("Adopter Login:\n")
        
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        adopter_ids = adopter_df.index
        entered_id = input("Enter your adopter ID: ")
        id_pattern = re.compile(r"^[a-zA-Z\s\d]+$")

        if len(entered_id) != 4:
            print("Invalid ID. Returning to main menu...")
            sleep(1.5)
            display_main_menu()
            return
        if not re.search(id_pattern, entered_id):
            print("Invalid ID. Returning to main menu...")
            sleep(1.5)
            display_main_menu()
            return
        if entered_id not in adopter_ids:
            print("ID not found. Returning to main menu...")
            sleep(1.5)
            display_main_menu()
            return

        display_adopter_menu()
    
    @staticmethod
    def logout():
        system("clear")
        print("Logged out. Returning to main menu...")
        sleep(1.5)
        display_main_menu()
        


    # TODO: fix this code to work for adopter_id and pet_id
    @classmethod
    def calculate_compatability(pet_id, adopter_id):
        pets_df = pd.read_csv("pets.csv", index_col="PetID")

        points = 0
        if adopter.home_type == "flat" and self.size == "large": points -= 20
        if adopter.home_type == "farm" and self.type == "dog": points += 15
        if adopter.home_type == "flat" and self.type != "dog": points += 10

        if adopter.preferred_size == self.size: points += 20
        elif adopter.preferred_size == "any": points += 10

        if adopter.experience_level == "expert": points += 15
        elif adopter.experience_level == "some": points += 10
        elif self.energy_level == "high": points -= 15

        if self.age >= 6: points += 10

        if points >= 50: compatability_rating = "Excellent Match ⭐⭐⭐"
        elif 30 <= points <= 49: compatability_rating = "Good Match ⭐⭐"
        elif 10 <= points <= 29: compatability_rating = "Possible Match ⭐"
        else: compatability_rating = "Not Recommended"

        return compatability_rating


    def view_compatabilities():
        pass

    def calculate_fee(pet, adopter_id):
        pass



class PetManager:
    @staticmethod
    def add_pet():
        system("clear")
        print("Add Pet:\n")
        print("Fill out the following to add a pet:")

        # TODO: use dictionary to handle vaildation
        string_pattern = re.compile(r"^[a-zA-Z\s]+$")
        int_pattern = re.compile(r"^[\d]+$")
        valid_types = ["Dog", "Cat", "Rabbit", "Hamster"]
        valid_sizes = ["Small", "Medium", "Large"]
        valid_energy_levels = ["Low", "Medium", "High"]

        name = input("1. Name: ").strip().title()
        if not re.search(string_pattern, name):
            print("Invalid input")
            return False

        type = input("2. Type (Dog, Cat, Rabbit, Hamster): ").strip().title()
        if type not in valid_types:
            print("Invalid input")
            return False

        size = input("4. Pet size (Small, Medium or Large): ").strip().title()
        if size not in valid_sizes:
            print("Invalid input")
            return False

        energy_level = input("5. Energy level (Low, Medium or High): ").strip().title()
        if energy_level not in valid_energy_levels:
            print("Invalid input")
            return False

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        last_id = pets_df.index[-1]
        last_num = int(last_id[1::])
        new_pet_id = f"P{1+last_num:03d}"

        new_pet = {
            "PetID": new_pet_id,
            "Name": name,
            "Type": type,
            "Size": size,
            "Energy": size,
        }
    
        new_pet_df = pd.DataFrame([new_pet])
        new_pet_df.to_csv("pets.csv", mode="a", index=False, header=False)
        
        print("\nPet has been added to database.")
        

    @staticmethod
    def remove_pet():
        pass

    @staticmethod
    def view_statistics():
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        pets_df = pets_df[pets_df["Status"] == "Available"]

        # TODO: fix this
        num_dogs = len(pets_df[pets_df["Type"] == "Dog"])
        num_cats = len(pets_df[pets_df["Type"] == "Cat"])
        num_rabbits = len(pets_df[pets_df["Type"] == "Hamster"])
        num_hamsters = len(pets_df[pets_df["Type"] == "Rabbit"])
        type_mode = pets_df[pets_df["Type"]].mode()

        

    @staticmethod
    def view_available_pets():
        system("clear")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        available_pets = (pets_df[pets_df["Status"] == "Available"]).sort_values(by="DaysInCentre", ascending=False).drop(columns="Status")
        mean = f"{pets_df["DaysInCentre"].mean():.1f}"
        print(available_pets)
        print(mean)
    
    @staticmethod
    def view_all_pets():
        system("clear")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        pets_df = pets_df.sort_values(by="DaysInCentre", ascending=False)
        mean = f"{pets_df["DaysInCentre"].mean():.1f}"
        print(pets_df)
        print(mean)



def display_main_menu():
    system("clear")
    print("Main Menu:\n")
    print("1. View Available Pets")
    print("2. Register as New Adopter")
    print("3. Adopter Login")
    print("4. Staff Menu")
    print("5. Quit")

    pages = [AdopterManager.view_available_pets, AdopterManager.register_as_new_adopter, AdopterManager.login, display_staff_menu, quit_site]
    options = len(pages)
    user_choice = askOption(options)
    if 1 <= user_choice <= options:
        pages[user_choice - 1]()
    else:
        print("Invalid option, reloading page...")
        sleep(1.5)
        display_main_menu()


def display_adopter_menu(adopter_id):
    system("clear")
    name = None
    print(f"Welcome, {name}\n")
    print("Adopter Menu:")
    print("1. View My Compatibility Matches")
    print("2. Reserve a Pet")
    print("3. View My Reserved/Adopted Pets")
    print("4. Cancel a Reservation")
    print("5. Logout")

    pages = [AdopterManager.view_compatabilities, AdopterManager.reserve_pet, AdopterManager.logout]
    options = len(pages)
    user_choice = askOption(options)
    if 1 <= user_choice <= options:
        pages[user_choice - 1]()
    else:
        print("Invalid option, reloading page...")
        sleep(1.5)
        display_main_menu()


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
    PetManager.view_statistics()

main()
