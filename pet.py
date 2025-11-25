from os import system
from time import sleep
import pandas as pd
class  PetManager: pass

manager = PetManager()
class Pet:
    def __init__(self, name, type, age, size, energy_level, fee, status, days_in_centre):
        self.name = name
        self.type = type
        self.age = age
        self.size = size
        self.energy_level = energy_level
        self.fee = fee
        self.status = status
        self.days_in_centre = days_in_centre

        self.is_reserved = False
        self.is_adopted = False
        self.pet_id = self.create_id()

    
    def calculate_fee(self, adopter):
        fee = self.fee
        # TODO: calculate fee
        
        return fee


    def calculate_compatability(self, adopter):
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
    
class PetManager:
    def __init__(self):
        pass

    def generate_pet_id():
        pass
    
    def add_pet():
        pass

    def remove_pet():
        pass

    def view_statistics():
        pass

    def view_available_pets():
        pass
    
    def view_all_pets():
        pass
