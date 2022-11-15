from random import random
from random import randint
from copy import copy


class Genetic:
    BACKPACK_CAPACITY = 150
    NUMBER_OF_ITEMS = 100
    ITERATION_LIMIT = 1000
    PATH_TO_FILE = "output.txt"
    weight = [randint(1, 5) for _ in range(NUMBER_OF_ITEMS)]
    value = [randint(2, 10) for _ in range(NUMBER_OF_ITEMS)]
    population = []
    probabilities = []
    mutation_probability = 0.05
    best = None
    best_ = None

    # the initial population is 100 solutions each with 1 different item
    def initialPopulation(self):
        for i in range(self.NUMBER_OF_ITEMS):
            init = [0] * self.NUMBER_OF_ITEMS
            init[i] = 1
            self.population.append((init, self.fitness(init)))
        return True

    # the fitness function is the total value of item in the bag now
    # once the weight beyond the bag's capacity, the result of fitness function will be 0
    def fitness(self, chromosome):
        sum_of_weights = 0
        sum_of_values = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                sum_of_weights += self.weight[i]
                sum_of_values += self.value[i]
        if sum_of_weights > self.BACKPACK_CAPACITY:
            return 0
        else:
            return sum_of_values

    # calculating the possibility of every individual chromosome to be selected based on their fitness result
    def getPossibility(self):
        self.probabilities = []
        total_sum = 0
        for chromosome in self.population:
            total_sum += chromosome[1]
        probability_sum = 0
        for chromosome in self.population:
            if total_sum == 0:
                probability_sum = 0
            else:
                probability_sum += float(chromosome[1] / total_sum)
            self.probabilities.append(probability_sum)

    # local chromosome improvement: changing a random gene from 0 to 1
    def local_improvement(self, chromosome):
        improved_chromosome = chromosome.copy()
        while True:
            i = randint(0, self.NUMBER_OF_ITEMS - 1)
            if improved_chromosome[i] == 0:
                improved_chromosome[i] = 1
                break
        # print("Old value: ", self.fitness(chromosome), "New value: ", self.fitness(improved_chromosome))
        return improved_chromosome

    # using crossover, mutation and local improvement to generate a new generation
    def nextGeneration(self):
        # fitness proportionate parents selection
        parent_1 = 0
        parent_2 = -1
        r = random()
        for parent in range(len(self.probabilities)):
            if r < self.probabilities[parent]:
                parent_1 = parent
                break

        r = random()
        for parent in range(len(self.probabilities)):
            if r < self.probabilities[parent]:
                parent_2 = parent
                break

        child_chromosome = self.crossover(self.population[parent_1][0], self.population[parent_2][0])
        r = random()
        if r < self.mutation_probability:
            mutated_chromosome = self.mutation(child_chromosome)
            final_chromosome = self.local_improvement(mutated_chromosome)
        else:
            final_chromosome = self.local_improvement(child_chromosome)
        self.population.append((final_chromosome, self.fitness(final_chromosome)))
        self.population.sort(key=lambda x: x[-1])
        self.population.pop(0)

    # using mutation to generate a new chromosome.
    @staticmethod
    def mutation(chromosome):
        mutated_chromosome = copy(chromosome)
        i1 = randint(0, len(chromosome) - 1)
        i2 = randint(0, len(chromosome) - 1)
        mutated_chromosome[i1], mutated_chromosome[i2] = mutated_chromosome[i2], mutated_chromosome[i1]
        return mutated_chromosome

    # use uniform crossover operator to generate a new population.
    @staticmethod
    def crossover(parent_1, parent_2):
        child_chromosome = []
        for i in range(len(parent_1)):
            if parent_1[i] != parent_2[i]:
                new_gene = randint(0, 1)
                child_chromosome.append(new_gene)
            else:
                child_chromosome.append(parent_1[i])
        return child_chromosome

    def write_info_to_file(self, graph_data):
        final_weight = 0
        result = 'Values are written in this format "item number: (item weight, item value)"\n'
        for i in range(self.NUMBER_OF_ITEMS):
            result += f"item {i + 1}: ({self.weight[i]}, {self.value[i]})\n"
        result += "---------------------------------\n\n"
        result += "Final decision:\n"
        for i in range(self.NUMBER_OF_ITEMS):
            if self.population[-1][0][i] == 1:
                result += f"item {i + 1}: ({self.weight[i]}, {self.value[i]})\n"
                final_weight += self.weight[i]
        result += "---------------------------------\n\n"
        result += "Data for plotting a graph (iteration number, fitness function):\n"
        result += graph_data
        with open(self.PATH_TO_FILE, "wt") as text_to_file:
            text_to_file.write(result)

    def run(self):
        graph_data = ""
        print("There are %d item and %d iterations." % (len(self.weight), self.ITERATION_LIMIT))
        print("---------------------------------")
        self.initialPopulation()
        for i in range(self.ITERATION_LIMIT):
            if (i + 1) % 20 == 0:
                graph_data += f"({i + 1}, {self.population[-1][-1]})\n"
            self.getPossibility()
            self.nextGeneration()

        weight = 0
        for i in range(self.NUMBER_OF_ITEMS):
            if self.population[-1][0][i] == 1:
                weight += self.weight[i]
        print("Total weight is: ", weight)
        print("Total value is: ", self.population[-1][-1])
        self.write_info_to_file(graph_data)


g = Genetic()
g.run()
