import random as rand

population  = 1000
infection_rate = rand.uniform(0.1, 0.5)
lethality_rate = rand.uniform(0.01, 0.1)
initial_infected = 10

def simulate_disease_spread():
    global initial_infected
    percent_infected = (initial_infected / population) * 100
    print(f"Initial infected percentage: {percent_infected:.2f}%")
    infected = initial_infected + int(infection_rate * population)

simulate_disease_spread()