import networkx as nx
import random

def Q(offspring):
    global G
    m = G.number_of_edges()
    Q_value = 0
    A = nx.to_numpy_array(G)
    communities = {}

    for node, label in enumerate(offspring):
        if label not in communities:
            communities[label] = []
        communities[label].append(node)

    for community in communities.values():
        for i in community:
            for j in community:
                A_ij = A[i, j]
                k_i = sum(A[i])
                k_j = sum(A[j])
                expected_edge = (k_i * k_j) / (2 * m)
                Q_value += (A_ij - expected_edge)

    Q_value /= (2 * m)
    return Q_value

def SHC(offspring):
    idx = random.randrange(len(offspring))
    neighbor = offspring[:]
    current_modularity = Q(offspring)
    change = []

    for label in range(NUM_LABEL):
        neighbor[idx] = label
        delta_modularity = Q(neighbor) - current_modularity
        change.append(delta_modularity)

    max_change = max(change)
    max_idx = change.index(max_change)
    offspring[idx] = max_idx
    return offspring

def repair(offspring):
    while True:
        labels_in_offspring = set(offspring)
        missing_labels = set(range(NUM_LABEL)) - labels_in_offspring
        if not missing_labels:
            break
        for i in range(len(missing_labels)):
            idx = random.randrange(len(offspring))
            offspring[idx] = missing_labels.pop()
    return offspring

def selection(population):
    selected = random.sample(population, TOURNAMENT_SIZE)
    selected.sort(key=lambda individual: individual[0], reverse=True)
    return selected[0]

def crossover(parent1, parent2):
    offspring = []
    for i in range(len(parent1[1])):
        offspring.append(parent1[1][i] if random.random() > 0.5 else parent2[1][i])
    return offspring

def mutation(offspring):
    idx = random.randrange(len(offspring))
    offspring[idx] = random.randint(0, NUM_LABEL - 1)
    return offspring

def genetic_algorithm(chromosomes_size, population_size, num_generations, num_label):
    population = [[0, [random.randint(0, num_label - 1) for _ in range(chromosomes_size)]] for _ in
                  range(population_size)]

    for index in range(population_size):
        print(index)
        population[index][0] = Q(population[index][1])

    for generation in range(num_generations):
        for i in range(population_size):
            print(i)
            parent1 = selection(population)
            parent2 = selection(population)

            offspring = crossover(parent1, parent2)
            offspring = mutation(offspring)
            offspring = repair(offspring)
            offspring = SHC(offspring)

            population.append([Q(offspring), offspring])
        population.sort(key=lambda individual: individual[0], reverse=True)
        population = population[:population_size]
        print(generation, population[0][0], population[1][0], population[2][0])

    best_individual = max(population, key=lambda individual: individual[0])
    return best_individual

G = nx.read_gml('polbooks.gml')
CHROMOSOMES_SIZE = len(G.nodes())
POPULATION_SIZE = 50
NUM_GENERATIONS = 200
NUM_LABEL = 3
TOURNAMENT_SIZE = 3

best_solution = genetic_algorithm(
    chromosomes_size=CHROMOSOMES_SIZE,
    population_size=POPULATION_SIZE,
    num_generations=NUM_GENERATIONS,
    num_label=NUM_LABEL
)

print("Best Solution:", best_solution)
