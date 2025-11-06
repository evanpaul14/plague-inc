import random
import time
import requests

# Fetch all country codes from IPQualityScore API
def get_country_code():
    try:
        response = requests.get("https://www.ipqualityscore.com/api/json/country/list")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                countries = data['countries']
                return [(code, name) for code, name in countries.items()]
            else:
                print(f"API Error: {data.get('message')}")
    except Exception as e:
        print(f"Error getting countries data: {e}")
    return []

# Get population data from REST Countries API
def get_population_data(country_code):
    response = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
    data = response.json()
    population = data[0]['population']
    population = round(population/100)
    return data[0]['population']
 

class Disease:
    def __init__(self, country_code):
        self.country = country_code
        self.population = get_population_data(country_code)
        self.infectivity = random.uniform(0.05, 1.00)  # Infection rate
        self.lethality = random.uniform(0.01, 1.00)     # Lethality rate
        self.recovery_rate = random.uniform(0.05, 0.15)  # Recovery rate
        self.current_infected = 10
        self.current_dead = 0
        self.current_susceptible = self.population - self.current_infected

    def update(self):
        if self.current_dead < self.population and self.current_infected > 0:
            # Calculate new infections and deaths
            susceptible = self.current_susceptible
            new_infected = int(self.infectivity * self.current_infected * (susceptible / self.population))
            new_deaths = int(self.current_infected * self.lethality)
            new_recovered = int(self.current_infected * self.recovery_rate)
            
            # Update counts
            self.current_infected += new_infected - new_recovered - new_deaths
            self.current_dead += new_deaths
            self.current_susceptible -= new_infected
            
            # Ensure no negative values and respect population limits
            self.current_infected = max(0, min(self.current_infected, self.population - self.current_dead))
            self.current_dead = min(self.current_dead, self.population)
            self.current_susceptible = max(0, min(self.current_susceptible, self.population - self.current_dead - self.current_infected))
            
            # Print the current status
            print(f"Country: {self.country}, Population: {self.population}, "
                  f"Susceptible: {int(self.current_susceptible)}, Infected: {int(self.current_infected)}, Dead: {int(self.current_dead)}")
            
            return False  # Continue simulation
        else:
            print(f"The entire population of {self.country} is either dead or infected.")
            return True  # End simulation

def main():
    countries = get_country_code()  # Get all countries and their codes
    if not countries:
        print("No data.")
        return

    # Choose a random country
    starting_country_code, starting_country_name = random.choice(countries)
    disease = Disease(starting_country_code)
    
    print(f"Starting Disease in {starting_country_name} ({starting_country_code}) with infectivity: {disease.infectivity:.2f}, lethality: {disease.lethality:.2f}")
    
    # Simulation loop until the population is dead or fully infected
    while True:
        if disease.update():
            break
        time.sleep(0.5)   #Pause for a second before the next update

if __name__ == "__main__":
    main()

