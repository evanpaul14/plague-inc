import random
import time
import requests

# Function to fetch all country codes from IPQualityScore API
def fetch_all_country_codes():
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
        print(f"Error fetching countries data: {e}")
    return []

# Function to get population data from REST Countries API
def get_population_data(country_code):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
        if response.status_code == 200:
            data = response.json()
            return data[0]['population']
    except Exception as e:
        print(f"Error fetching data for {country_code}: {e}")
    return 1000000  # Fallback population

class Disease:
    def __init__(self, country_code):
        self.country = country_code
        self.population = get_population_data(country_code)
        self.infectivity = random.uniform(0.05, 0.15)  # Infection rate as a percent
        self.lethality = random.uniform(0.01, 0.05)  # Lethality rate as a percent
        self.spread_rate = 0.1  # Spread factor
        self.current_infected = 10  # Start with 1 initial infection
        self.current_dead = 0

    def update(self):
            # Check if the disease has contaminated the entire population
            if self.current_infected + self.current_dead < self.population:
                susceptible = self.population - self.current_infected - self.current_dead
                # Exponential spread: infectivity * infected * (susceptible/population)
                new_infections = int(self.infectivity * self.current_infected * (susceptible / self.population))
                deaths = int(self.current_infected * self.lethality)

                # Update counts while ensuring they do not exceed the population
                self.current_infected += new_infections
                self.current_infected = min(self.current_infected, self.population - self.current_dead)
                self.current_dead += deaths
                self.current_dead = min(self.current_dead, self.population)

                # Print the current status
                print(f"Country: {self.country}, Population: {self.population}, "
                      f"Infected: {self.current_infected}, Dead: {self.current_dead}")

            else:
                print(f"The entire population of {self.country} is dead or infected.")
                return True  # Indicates the end of the simulation

def main():
    countries = fetch_all_country_codes()  # Get all countries and their codes
    if not countries:
        print("Failed to retrieve countries data.")
        return

    # Choose a random country
    starting_country_code, starting_country_name = random.choice(countries)
    disease = Disease(starting_country_code)
    
    print(f"Starting Disease in {starting_country_name} ({starting_country_code}) with infectivity: {disease.infectivity:.2f}, lethality: {disease.lethality:.2f}")

    # Simulation loop until the population is dead or fully infected
    while True:
        if disease.update():
            break
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    main()
