
from os import system
from time import sleep
import pandas as pd

class AdopterManager:
    def __init__(self):
        self.adopter_df = None


    def register_as_new_adopter():
        system("clear")
        print("Register Page:\n")
        print("Fill out the following to register:")

        # TODO: validate these inputs
        entered_name = input("1. Full name (must be at least 2 words): ")
        entered_home_type = input("2. Home type (Flat, House, or Farm only): ")
        entered_experience_level = input("3. Experience level (None, Some, or Expert): ")
        entered_preferred_pet_size = input("4. Preferred pet size (Small, Medium, Large, or Any): ")
        entered_preferred_energy_level = input("5. Preferred energy level (Low, Medium, High, or Any): ")

        new_adopter = {
            name = name
            home_type = home_type
            experience_level = experience_level
            preferred_size = preferred_size
            preferred_energy = preferred_energy
            id = manager.create_id()
            adopted_pets = None
        }
        
        print('Thank you for signing up.')
        print(f"Your unique adopter ID is: {new_adopter.id}")
        # TODO: add to adopter.csv

    
    
    def generate_adopter_id():
        pass
    

    def login():
        system("clear")
        print("Adopter Login:\n")
        
        # TODO: validate adopter ID
        # TODO: check if adoper ID exists
        entered_id = input("Enter your adopter ID: ")
    

    def logout():
        system("clear")
        print("Logged out. Returning to main menu...")
        sleep(1.5)



    def validate_adopter_id():
        pass
