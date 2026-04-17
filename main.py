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
        if not re.search(string_pattern, name) or len(name.split()) < 2:
            return AdopterManager.register_as_new_adopter()

        home_type = input("2. Home type (Flat, House, or Farm): ").strip().title()
        if home_type not in valid_home_types:
            return AdopterManager.register_as_new_adopter()

        experience = input("3. Experience level (None, Some, or Expert): ").strip().title()
        if experience not in valid_experiences:
            return AdopterManager.register_as_new_adopter()

        preferred_size = input("4. Preferred pet size (Small, Medium, Large, or Any): ").strip().title()
        if preferred_size not in valid_sizes:
            return AdopterManager.register_as_new_adopter()

        preferred_energy_level = input("5. Preferred energy level (Low, Medium, High, or Any): ").strip().title()
        if preferred_energy_level not in valid_energy_levels:
            return AdopterManager.register_as_new_adopter()

        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        last_id = adopter_df.index[-1]
        last_num = int(last_id[1::])
        new_adopter_id = f"A{1+last_num:03d}"

        new_adopter = {
            "AdopterID": new_adopter_id,
            "Name": name,
            "HomeType": home_type,
            "Experience": experience,
            "PreferredSize": preferred_size,
            "PreferredEnergy": preferred_energy_level,
            "Adopted/ReservedPets": "none",
        }
    
        new_adopter_df = pd.DataFrame([new_adopter])
        new_adopter_df.to_csv("adopters.csv", mode="a", index=False, header=False)
        
        print("\nThank you for signing up.")
        print(f"Your unique adopter ID is: {new_adopter_id}")
        input("\nEnter any character to enter adopter menu: ")
        return display_adopter_menu(new_adopter_id)

    @staticmethod
    def login():
        system("clear")
        print("Adopter Login:\n")
        
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        adopter_ids = adopter_df.index
        entered_id = input("Enter your adopter ID: ").title()
        id_pattern = re.compile(r"^[a-zA-Z\s\d]+$")

        if not re.search(id_pattern, entered_id) or len(entered_id) != 4:
            return AdopterManager.login()

        if entered_id not in adopter_ids:
            print("ID not found. Returning to main menu...")
            sleep(1.5)
            return display_main_menu()

        display_adopter_menu(entered_id)
    
    @staticmethod
    def logout(*args):
        system("clear")
        print("Logged out. Returning to main menu...")
        sleep(1.5)
        display_main_menu()

    @staticmethod
    def reserve_pet(adopter_id):
        system("clear")
        print("Reserve a Pet:\n")

        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        reserved_pets = adopter_df.loc[adopter_id]["Adopted/ReservedPets"]

        if reserved_pets != "None":
            for pet_id in reserved_pets.split(";"):
                if pets_df.loc[pet_id]["Status"] == "Reserved":
                    print("You already have a reservation. Please complete or cancel it first.")
                    input("\nEnter any character to return to adopter menu: ")
                    return display_adopter_menu(adopter_id)

        available_pets = pets_df[pets_df["Status"] == "Available"]
        if len(available_pets) == 0:
            print("There are no available pets to reserve.")
            input("\nEnter any character to return to adopter menu: ")
            return display_adopter_menu(adopter_id)

        results = []
        for pet_id in available_pets.index:
            points, rating = AdopterManager.calculate_compatibility(adopter_id, pet_id)
            pet = available_pets.loc[pet_id]
            results.append((pet_id, pet["Name"], pet["Type"], pet["Size"], pet["Energy"], pet["Age"], points, rating))

        results.sort(key=lambda x: x[6], reverse=True)

        for pet_id, name, pet_type, size, energy, age, points, rating in results:
            print(f"{pet_id} - {name} ({pet_type}, {size}, {energy} energy, age {age})")
            print(f"         {rating} - Score: {points}/80")
            print()

        chosen_id = input("Enter Pet ID to reserve: ").strip().upper()

        if chosen_id not in pets_df.index:
            print("Pet ID not found.")
            sleep(1.5)
            return AdopterManager.reserve_pet(adopter_id)

        if pets_df.loc[chosen_id]["Status"] != "Available":
            print("That pet is not available.")
            sleep(1.5)
            return AdopterManager.reserve_pet(adopter_id)

        points, rating = AdopterManager.calculate_compatibility(adopter_id, chosen_id)
        if points < 10:
            confirm = input(f"Warning: This pet's compatibility score is low. Are you sure? (Yes/No): ").strip().title()
            if confirm != "Yes":
                return display_adopter_menu(adopter_id)

        # - update pets.csv -
        pets_df.loc[chosen_id, "Status"] = "Reserved"
        pets_df.to_csv("pets.csv")

        # - update adopters.csv -
        current_pets = adopter_df.loc[adopter_id]["Adopted/ReservedPets"]
        if current_pets == "None":
            adopter_df.loc[adopter_id, "Adopted/ReservedPets"] = chosen_id
        else:
            adopter_df.loc[adopter_id, "Adopted/ReservedPets"] = current_pets + ";" + chosen_id
        adopter_df.to_csv("adopters.csv")

        fee = AdopterManager.calculate_fee(chosen_id, adopter_id)
        pet_name = pets_df.loc[chosen_id]["Name"]
        print(f"\n{pet_name} has been reserved successfully!")
        print(f"Your adoption fee will be: £{fee}")
        input("\nEnter any character to return to adopter menu: ")
        return display_adopter_menu(adopter_id)
    
    @staticmethod
    def calculate_compatibility(adopter_id, pet_id):
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")

        adopter = adopter_df.loc[adopter_id]
        pet = pets_df.loc[pet_id]

        home_type = adopter["HomeType"]
        experience = adopter["Experience"]
        preferred_size = adopter["PreferredSize"]
        preferred_energy = adopter["PreferredEnergy"]

        pet_type = pet["Type"]
        pet_size = pet["Size"]
        pet_energy = pet["Energy"]
        pet_age = int(pet["Age"])

        points = 0

        if pet_size == "Large" and pet_type == "Dog" and home_type == "Flat":
            points -= 20
        if pet_type == "Dog" and home_type == "Farm":
            points += 15
        if pet_type != "Dog" and home_type == "Flat":
            points += 10

        if preferred_size == pet_size:
            points += 20
        elif preferred_size == "Any":
            points += 10

        if preferred_energy == pet_energy:
            points += 20
        elif preferred_energy == "Any":
            points += 10

        if experience == "Expert":
            points += 15
        elif experience == "Some":
            points += 10
        elif pet_energy == "High" and experience == "None":
            points -= 15

        if pet_age >= 6:
            points += 10

        if points >= 50:
            rating = "Excellent Match ⭐⭐⭐"
        elif 30 <= points <= 49:
            rating = "Good Match ⭐⭐"
        elif 10 <= points <= 29:
            rating = "Possible Match ⭐"
        else:
            rating = "Not Recommended"

        return points, rating

    @staticmethod
    def view_compatibilities(adopter_id):
        system("clear")
        print("Your Compatibility Matches:\n")

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        available_pets = pets_df[pets_df["Status"] == "Available"]

        if len(available_pets) == 0:
            print("There are no available pets to match with.")
            input("\nEnter any character to return to adopter menu: ")
            return display_adopter_menu(adopter_id)

        results = []
        for pet_id in available_pets.index:
            points, rating = AdopterManager.calculate_compatibility(adopter_id, pet_id)
            pet = available_pets.loc[pet_id]
            results.append({
                "PetID": pet_id,
                "Name": pet["Name"],
                "Type": pet["Type"],
                "Age": pet["Age"],
                "Size": pet["Size"],
                "Energy": pet["Energy"],
                "Score": points,
                "Rating": rating,
            })

        results.sort(key=lambda x: x["Score"], reverse=True)

        for r in results:
            print(f"{r['PetID']} - {r['Name']} ({r['Type']}, {r['Size']}, {r['Energy']} energy, age {r['Age']})")
            print(f"       {r['Rating']} - Score: {r['Score']}/80\n")

        input("Enter any character to return to adopter menu: ")
        return display_adopter_menu(adopter_id)

    @staticmethod
    def calculate_fee(pet_id, adopter_id):
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")

        pet = pets_df.loc[pet_id]
        adopter = adopter_df.loc[adopter_id]

        fee = float(pet["Fee"])
        days = int(pet["DaysInCentre"])
        age = int(pet["Age"])
        experience = adopter["Experience"]

        if days >= 60:
            fee -= fee * 0.30
        elif days >= 30:
            fee -= fee * 0.20

        if age >= 6:
            fee -= 15

        if experience == "Expert":
            fee -= fee * 0.10

        if fee < 20:
            fee = 20

        return round(fee, 2)

    @staticmethod
    def view_my_pets(adopter_id):
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        reserved_pets = adopter_df.loc[adopter_id]["Adopted/ReservedPets"]
        if reserved_pets != "none":
            reserved_pets = reserved_pets.split(";")
            for pet_id in reserved_pets:
                print("\n")
                PetManager.show_reserved_pet_info(pet_id)
            
        else:
            print("\nYou haven't reserved or adopted any pets yet.")
            
        input("\nEnter any character to return to adopter menu: ")
        return display_adopter_menu(adopter_id)

    @staticmethod
    def cancel_reservation(adopter_id):
        system("clear")
        print("Cancel a Reservation:\n")

        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")

        pets_listed = adopter_df.loc[adopter_id]["Adopted/ReservedPets"]

        if pets_listed == "None":
            print("You have no reservations to cancel.")
            input("\nEnter any character to return to adopter menu: ")
            return display_adopter_menu(adopter_id)

        reserved = [pid for pid in pets_listed.split(";") if pets_df.loc[pid]["Status"] == "Reserved"]

        if len(reserved) == 0:
            print("You have no reservations to cancel.")
            input("\nEnter any character to return to adopter menu: ")
            return display_adopter_menu(adopter_id)

        print("Your current reservations:\n")
        for pet_id in reserved:
            pet = pets_df.loc[pet_id]
            print(f"{pet_id} - {pet['Name']} ({pet['Type']}, age {pet['Age']})")

        chosen_id = input("\nEnter Pet ID to cancel: ").strip().upper()

        if chosen_id not in reserved:
            print("Invalid Pet ID. Must be one of your reserved pets.")
            sleep(1.5)
            return AdopterManager.cancel_reservation(adopter_id)

        pets_df.loc[chosen_id, "Status"] = "Available"
        pets_df.to_csv("pets.csv")

        all_pets = pets_listed.split(";")
        all_pets.remove(chosen_id)
        new_pets = ";".join(all_pets) if len(all_pets) > 0 else "None"
        adopter_df.loc[adopter_id, "Adopted/ReservedPets"] = new_pets
        adopter_df.to_csv("adopters.csv")

        pet_name = pets_df.loc[chosen_id]["Name"]
        print(f"\nReservation for {pet_name} has been cancelled.")
        input("\nEnter any character to return to adopter menu: ")
        return display_adopter_menu(adopter_id)

    @staticmethod
    def complete_an_adoption():
        system("clear")
        print("Complete an Adoption:\n")

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")

        reserved_pets = pets_df[pets_df["Status"] == "Reserved"]
        if len(reserved_pets) == 0:
            print("There are no reserved pets.")
            sleep(1.5)
            return display_staff_menu()

        print(reserved_pets)

        pet_id = input("\nEnter Pet ID to finalise: (or enter 'Cancel' to cancel): ").strip().upper()

        if pet_id == "CANCEL":
            return display_staff_menu()

        if pet_id not in pets_df.index:
            print("Pet ID not found.")
            sleep(1.5)
            return AdopterManager.complete_an_adoption()

        if pets_df.loc[pet_id]["Status"] != "Reserved":
            print("That pet is not reserved.")
            sleep(1.5)
            return AdopterManager.complete_an_adoption()

        adopter_id = None
        for aid in adopter_df.index:
            pets_listed = adopter_df.loc[aid]["Adopted/ReservedPets"]
            if pets_listed != "None" and pet_id in pets_listed.split(";"):
                adopter_id = aid
                break

        if adopter_id is None:
            print("Error: no adopter found for this reservation.")
            sleep(1.5)
            return display_staff_menu()

        pet = pets_df.loc[pet_id]
        adopter = adopter_df.loc[adopter_id]
        fee = AdopterManager.calculate_fee(pet_id, adopter_id)

        print(f"\nPet: {pet['Name']} (Type: {pet['Type']}, Age: {pet['Age']})")
        print(f"Adopter: {adopter['Name']} (AdopterID: {adopter_id})")
        print(f"Adoption fee: £{fee}")

        confirm = input("\nConfirm adoption completion? (Yes/No): ").strip().title()

        if confirm == "Yes":
            pets_df.loc[pet_id, "Status"] = "Adopted"
            pets_df.loc[pet_id, "DaysInCentre"] = 0
            pets_df.to_csv("pets.csv")
            print(f"\nAdoption completed! {pet['Name']} has found a forever home with {adopter['Name']}!")
            sleep(2)

        return display_staff_menu()



class PetManager:
    @staticmethod
    def add_pet():
        system("clear")
        print("Add Pet:\n")
        print("Fill out the following to add a pet:")

        string_pattern = re.compile(r"^[a-zA-Z\s]+$")
        valid_types = ["Dog", "Cat", "Rabbit", "Hamster"]
        valid_sizes = ["Small", "Medium", "Large"]
        valid_energy_levels = ["Low", "Medium", "High"]

        name = input("1. Name: ").strip().title()
        if not re.search(string_pattern, name):
            print("Invalid input")
            return PetManager.add_pet()

        pet_type = input("2. Type (Dog, Cat, Rabbit, Hamster): ").strip().title()
        if pet_type not in valid_types:
            print("Invalid input")
            return PetManager.add_pet()

        age = input("3. Age (0-20): ").strip()
        if not age.isdigit() or not (0 <= int(age) <= 20):
            print("Invalid input")
            return PetManager.add_pet()
        age = int(age)

        size = input("4. Pet size (Small, Medium or Large): ").strip().title()
        if size not in valid_sizes:
            print("Invalid input")
            return PetManager.add_pet()

        energy_level = input("5. Energy level (Low, Medium or High): ").strip().title()
        if energy_level not in valid_energy_levels:
            print("Invalid input")
            return PetManager.add_pet()

        fee = input("6. Adoption fee (£20-£300): £").strip()
        if not fee.isdigit() or not (20 <= int(fee) <= 300):
            print("Invalid input")
            return PetManager.add_pet()
        fee = int(fee)

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        last_id = pets_df.index[-1]
        last_num = int(last_id[1:])
        new_pet_id = f"P{1 + last_num:03d}"

        new_pet = {
            "PetID": new_pet_id,
            "Name": name,
            "Type": pet_type,
            "Age": age,
            "Size": size,
            "Energy": energy_level,
            "Fee": fee,
            "Status": "Available",
            "DaysInCentre": 0,
        }

        new_pet_df = pd.DataFrame([new_pet])
        new_pet_df.to_csv("pets.csv", mode="a", index=False, header=False)

        print(f"\nPet has been added to the database.")
        print(f"Assigned Pet ID: {new_pet_id}")
        input("\nEnter any character to return to staff menu: ")
        return display_staff_menu()
        
    @staticmethod
    def complete_adoption():
        pass

    @staticmethod
    def remove_pet():
        system("clear")
        print("Remove a Pet: \n")

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        available_pets = pets_df[pets_df["Status"] == "Available"]

        if len(available_pets) == 0:
            print("There are no available pets to remove.")
            sleep(1.5)
            return display_staff_menu
        
        print(available_pets)

        pet_id = input("\nEnter Pet ID to remove (or enter 'Cancel' to cancel): ").strip().upper()
        
        if pet_id == "CANCEL":
            return display_staff_menu()

        if pet_id not in pets_df.index:
            print("Pet ID not found.")
            sleep(1.5)
            return PetManager.remove_pet()
        
        if pets_df.loc[pet_id]["Status"] != "Available":
            print("You can only remove available pets, not reserved or adopted ones.")
            sleep(1.5)
            return PetManager.remove_pet()
        
        pet_name = pets_df.loc[pet_id]["Name"]
        confirm = input(f"Are you sure you want to remove {pet_name}? (Yes/No): ").lower()

        if confirm == "yes":
            pets_df = pets_df.drop(pet_id)
            pets_df.to_csv("pets.csv")
            print(f"{pet_name} has been removed from the database.")
            sleep(1.5)

        return display_staff_menu()

    @staticmethod
    def view_statistics():
        system("clear")
        print("Statistics: \n")

        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        available_df = pets_df[pets_df["Status"] == "Available"]

        adopters_df = pd.read_csv("adopters.csv", index_col="AdopterID")
        adopted_df = pets_df[pets_df["Status"] == "Adopted"]

        print("Available pets by type:")
        num_pets = {
            "Dog": len(available_df[available_df["Type"] == "Dog"]),
            "Cat": len(available_df[available_df["Type"] == "Cat"]),
            "Rabbit": len(available_df[available_df["Type"] == "Rabbit"]),
            "Hamster": len(available_df[available_df["Type"] == "Hamster"])
        }

        for pet_type, count in num_pets.items():
            print(f"{pet_type}: {count}")
        
        most_common = max(num_pets, key=num_pets.get)
        print(f"Most common available pet type: {most_common}")

        print("\nAdoption success:")
        print(f"Total completed adoptions: {len(adopted_df)}")

        if len(adopted_df) > 0:
            avg_days = adopted_df["DaysInCentre"].mean()
            print(f"Average days in centre before adoption: {avg_days:.1f}")
        else:
            print(f"Average days in centre before adoption: N/A")

        if len(available_df) > 0:
            longest_waiting = available_df["DaysInCentre"].idxmax()
            longest_name = available_df.loc[longest_waiting]["Name"]
            longest_days = available_df.loc[longest_waiting]["DaysInCentre"]
            print(f"Longest waiting pet: {longest_name} ({longest_days} days)")
        else:
            print("Longest waiting pet: N/A")

        print("\nFinancial information:")
        total_income = available_df["Fee"].sum()
        avg_fee = pets_df["Fee"].mean()
        print(f"Total potential income from available pets: £{total_income:.2f}")
        print(f"Average adoption fee across all pets: £{avg_fee:.2f}")

        print("\nAdopter Information:")
        total_adopters = len(adopted_df)
        adopters_with_pets = len(adopters_df[adopters_df["Adopted/ReservedPets"] != "none"])
        print(f"Total registered adopters: {total_adopters}")
        print(f"Adopters with completed adoptions: {adopters_with_pets}")

        experience_counts = adopters_df["Experience"].value_counts()
        for level in ["None", "Some", "Expert"]:
            count = experience_counts.get(level, 0)
            print(f"{level} experience adopters: {count}")

        input("\nEnter any charatcer to return to staff menu: ")
        return display_staff_menu()

    @staticmethod
    def view_available_pets():
        system("clear")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        available_pets = (pets_df[pets_df["Status"] == "Available"]).sort_values(by="DaysInCentre", ascending=False).drop(columns="Status")
        mean = f"{pets_df["DaysInCentre"].mean():.1f}"
        print(available_pets)
        print(mean)
        input("Enter any charater to return to main menu: ")
        display_main_menu()

    @staticmethod
    def show_reserved_pet_info(pet_id):
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        print(f"Pet ID: {pet_id}")
        print(f"Name: {pets_df.loc[pet_id]["Name"]}")
        print(f"Type: {pets_df.loc[pet_id]["Type"]}")
        print(f"Age: {pets_df.loc[pet_id]["Age"]}")
        status = pets_df.loc[pet_id]["Status"]
        print(f"Status: {status}")
        if status == "Reserved":
            print("Ready to finalize adoption")   
    
    @staticmethod
    def view_all_pets():
        system("clear")
        pets_df = pd.read_csv("pets.csv", index_col="PetID")
        pets_df = pets_df.sort_values(by="DaysInCentre", ascending=False)
        mean = f"{pets_df["DaysInCentre"].mean():.1f}"
        print(pets_df)
        print(f"Mean days spent in centre: {mean}")
        input("Enter any character to return to staff menu: ")
        display_staff_menu()



def display_main_menu():
    system("clear")
    print("Main Menu:\n")
    print("1. View Available Pets")
    print("2. Register as New Adopter")
    print("3. Adopter Login")
    print("4. Staff Menu")
    print("5. Quit")

    pages = [PetManager.view_available_pets, AdopterManager.register_as_new_adopter, AdopterManager.login, check_staff_password, quit_site]
    user_choice = askOption(len(pages))
    pages[user_choice - 1]()


def display_adopter_menu(adopter_id):
    system("clear")
    adopter_df = pd.read_csv("adopters.csv", index_col="AdopterID")
    name = adopter_df.loc[adopter_id]["Name"]
    print(f"Welcome, {name}\n")
    print("Adopter Menu:")
    print("1. View My Compatibility Matches")
    print("2. Reserve a Pet")
    print("3. View My Reserved/Adopted Pets")
    print("4. Cancel a Reservation")
    print("5. Logout")

    pages = [AdopterManager.view_compatibilities, AdopterManager.reserve_pet, AdopterManager.view_my_pets, AdopterManager.cancel_reservation, AdopterManager.logout]
    user_choice = askOption(len(pages))
    pages[user_choice - 1](adopter_id)


def display_staff_menu():
        system("clear")
        print("Staff Menu:\n")
        print("1. Add New Pet")
        print("2. Complete an Adoption")
        print("3. View All pets")
        print("4. View Statistics")
        print("5. Remove a pet")
        print("6. Logout")

        pages = [PetManager.add_pet, AdopterManager.complete_an_adoption, PetManager.view_all_pets, PetManager.view_statistics, PetManager.remove_pet, AdopterManager.logout]
        user_choice = askOption(len(pages))
        pages[user_choice - 1]()


def check_staff_password():
    
    system("clear")
    password = "admin123"
    for i in range(3):
        entered_password = input("Enter staff password: ")
        if entered_password == password:
            return display_staff_menu()
        else:
            print(f"Incorrect password. Attempts remaining: {2 - i}\n")
    print("Too many incorrect attempts. Returning to main menu...")
    sleep(1.5)
    return display_main_menu()


def askOption(n):
    user_option = input(f"\nChoose from options 1-{n}: ")

    if user_option in [str(num+1) for num in range(n)]:
        return int(user_option)
    print("Invalid option. Enter again: ")
    return askOption(n)



def quit_site():
    system("clear")
    print("Thanks for visiting, come again!")
    quit()



display_main_menu()
