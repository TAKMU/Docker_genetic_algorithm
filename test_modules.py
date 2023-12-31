import pandas as pd
import numpy as np
import random
import math
import db_access

PRODUCTS = pd.DataFrame({
    'Names' : ["Dubalin", "Chocolate", "Sabritas", "Gansitos", "Bubaloo", "Panditas", "Kranky"],
    'Weight' : [.6, .5, .1, .6, 2, .2, .3],
    'Buy_Price': [60, 30, 80, 66, 34, 76, 33],
    'Sale_Price' : [70, 80, 140, 100, 170, 76, 124]
    })

n_product = len(PRODUCTS.index)
n_pop = 500
n_generations = 1000
max_value = 7
min_value = 1
p_mutate = 0.9
per_selection = 0.90

def init_population(n):
    """Return a population of n random solutions. Each solution is 
    a 4x3 list, with each element being a selection of 3 distinct
    random barrels.
    """
    global n_product
    new_population = np.random.randint(low=min_value, high=max_value, size=(n, n_product))
    return new_population

def fitness(candidate):
    """Give the score of the 
    """
    result_weight = (PRODUCTS['Weight'] * candidate).sum()
    result_buy = (PRODUCTS['Buy_Price'] * candidate).sum()
    result_sale = (PRODUCTS['Sale_Price'] * candidate).sum()
    if result_weight > 15:
        return (15 - result_weight) * 66.67
    if result_buy > 1000:
        return 1000 - result_buy
    return result_sale - result_buy

def evaluation(population):
    """Return a population sorted by fitness."""
    return sorted(population, key= lambda x:fitness(x), reverse= True)

def selection(population, percentage_selection):
    """Return top half of population."""
    n_parents = math.ceil(len(population) * percentage_selection / 2) * 2
    n_parents = int(n_parents)
    return population[:n_parents]

def crossover(parents : np.array):
    """Return a new population, generated by pairing best solution with second best, and so forth. 
    """
    children = np.empty((len(parents), n_product), dtype=int)
    n_children = len(parents)
    for i in range(n_children): # Cross N times
        if i % 2 == 0:
            parent1, parent2 = parents[i], parents[i+1]
            child1 = np.empty(n_product)
            child2 = np.empty(n_product)
            child1[:int(n_product / 2)] = parent1[:int(n_product / 2)]
            child1[int(n_product / 2):] = parent2[int((n_product / 2)):]
            child2[:int(n_product / 2)] = parent2[:int(n_product / 2)]
            child2[int(n_product / 2):] = parent1[int(n_product / 2):]
            children[i] = child1
            children[i+1] = child2
    return children

def mutation(population):
    """Return a mutated population (out-of-place). For each
    candidate, mutate with probability p_mutate.
    If mutate:
        Select random slot.
        Select a randon integer to change the value excluding the preceding value.
    Else:
        The candidate is not affected.
    Return new (partially mutated) population.
    """
    mutated_population = population.copy()
    for index in range(population.shape[0]):
        if random.random() < p_mutate:
            # Mutate
            # Choose random slot
            o = random.randrange(n_product)
            mutated_population[index][o] = random.choice([x for x in range(min_value, max_value+1) if x != mutated_population[index][o]])
    return mutated_population



def testing():
    for i in range(10):    
        pop = init_population(n_pop)
        ranking = evaluation(pop)

        for i in range(n_generations):
            parents = selection(ranking, per_selection)
            children = crossover(parents)
            children = mutation(children)
            new_pop = np.empty((n_pop, n_product), dtype=int)
            new_pop[:children.shape[0]] = children
            new_pop[children.shape[0]:] = pop[:(n_pop-children.shape[0])]
            pop = evaluation(new_pop)


        solution = evaluation(pop)[0]
        print(solution)
        print(fitness(solution))

testing()