from datetime import date
class Person:
    def __init__(self, name, birth_year, birth_month, birth_day):
        self.name = name
        self.birth_date = date(birth_year, birth_month, birth_day)

    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def get_details(self):
        return f"Name: {self.name}, Birth Date: {self.birth_date}, Age: {self.get_age()}"
    

# Example usage:
person = Person("Huzaifa", 2005, 1, 6)
print(person.get_details())