class Adopter:
    def __init__(self, name, home_type, experience_level, preferred_size, preferred_energy):
        self.name = name
        self.home_type = home_type
        self.experience_level = experience_level
        self.preferred_size = preferred_size
        self.preferred_energy = preferred_energy

        self.id = self.create_id()
        self.adopted_pets = None