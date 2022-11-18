import time
import matplotlib.pyplot as plt
import numpy as np


class AntColony:
    ITERATION_LIMIT = 100
    ANTS_AMOUNT = 50
    ELITE_ANTS_AMOUNT = 5
    WILD_ANTS_AMOUNT = 1
    EVAPORATION_RATE = 0.2
    ALPHA = 1
    BETA = 3
    L_MIN = 1500
    EARLY_STOPPING_COUNT = round(ITERATION_LIMIT * 0.7)
    START_FROM_DIFFERENT_POINTS = True

    def __init__(self):
        # internal representations
        self.pheromone_matrix = None
        self.visibility_matrix = None
        self.probability_matrix = None
        self.map = None
        self.available_nodes = None
        self.fit_time = None
        self.stopped_early = False

        # internal stats
        self.best_score = float('inf')
        self.best_path = None
        self.all_best_scores = []

    def initialize(self):
        """Initializes the model by creating the various matrices and generating the list of available nodes"""
        num_nodes = self.map.shape[0]
        self.available_nodes = list(range(num_nodes))
        self.pheromone_matrix = np.zeros((num_nodes, num_nodes))
        # remove the diagonal since there is no pheromone from node i to itself
        self.pheromone_matrix[np.eye(num_nodes) == 0] = 0.1
        self.visibility_matrix = 1 / self.map
        self.probability_matrix = np.zeros((num_nodes, num_nodes))
        self.get_probabilities()

    def get_probabilities(self):
        """Obtaining a matrix of transition probabilities to a neighboring vertex"""
        num_nodes = self.map.shape[0]
        for i in range(num_nodes):
            for j in range(num_nodes):
                numerator = self.pheromone_matrix[i][j] ** self.ALPHA * self.visibility_matrix[i][j] ** self.BETA
                denominator = 0
                for k in range(num_nodes):
                    denominator += self.pheromone_matrix[i][k] ** self.ALPHA * self.visibility_matrix[i][k] ** self.BETA
                self.probability_matrix[i][j] = numerator / denominator

    def choose_next_node(self, from_node, ant_type="default"):
        """Chooses the next node based on probabilities
        :param ant_type: type of ant, can be elite or default
        :param from_node: the node the ant is coming from
        :return: index of the node the ant is going to"""
        probabilities = self.probability_matrix[from_node, self.available_nodes]
        if ant_type == "default":
            probabilities /= sum(probabilities)
            next_node = np.random.choice(range(len(probabilities)), p=probabilities)
        else:
            next_node = np.random.choice(range(len(probabilities)))
        return next_node

    def evaluate_distance(self, paths):
        """Evaluates the solutions of the ants by adding up the distances between nodes.
        :param paths: solutions from the ants
        :return: x and y coordinates of the best path as a tuple, the best path, and the best score"""
        best = float('inf')
        scores = np.zeros(len(paths))
        for index, path in enumerate(paths):
            score = 0
            for i in range(len(path) - 1):
                score += self.map[path[i], path[i + 1]]
            scores[index] = score
            best = np.argmin(scores)
        return paths[best], scores[best], scores

    def evaporation(self):
        """Evaporate some pheromone as the inverse of the evaporation rate."""
        self.pheromone_matrix *= (1 - self.EVAPORATION_RATE)

    def intensify(self, scores, paths):
        """Increase the pheromone on traveled paths, and on a better path if elite ants are present.
        :param paths: all the paths taken by the ants
        :param scores: all costs of traveled paths"""
        i = self.best_path[:-1]
        j = self.best_path[1:]
        self.pheromone_matrix[i, j] += self.ELITE_ANTS_AMOUNT * (self.L_MIN / self.best_score)
        for index, score in enumerate(scores):
            i = paths[index][:-1]
            j = paths[index][1:]
            self.pheromone_matrix[i, j] += self.L_MIN / score

    def fit(self, map_matrix):
        """Fits the ACO to a specific map.
        :param map_matrix: Distance matrix or some other matrix with similar properties"""
        print("Beginning ACO Optimization with {} iterations...".format(self.ITERATION_LIMIT))
        self.map = map_matrix
        start = time.time()
        self.initialize()
        num_equal = 0
        for i in range(self.ITERATION_LIMIT):
            start_iter = time.time()
            all_paths = []
            ant_type = "default"
            for ant in range(self.ANTS_AMOUNT + self.WILD_ANTS_AMOUNT):
                if ant >= self.ANTS_AMOUNT:
                    ant_type = "wild"
                path = []
                if self.START_FROM_DIFFERENT_POINTS:
                    current_node = self.available_nodes[np.random.randint(0, len(self.available_nodes))]
                else:
                    current_node = self.available_nodes[0]
                start_node = current_node
                while True:
                    path.append(current_node)
                    self.available_nodes.remove(current_node)
                    if len(self.available_nodes) != 0:
                        current_node_index = self.choose_next_node(current_node, ant_type)
                        current_node = self.available_nodes[current_node_index]
                    else:
                        break

                path.append(start_node)  # go back to start
                self.available_nodes = list(range(self.map.shape[0]))
                all_paths.append(path)

            best_path, best_score, all_scores = self.evaluate_distance(all_paths)

            if i == 0:
                self.best_score = best_score
                self.best_path = best_path
            else:
                if best_score < self.best_score:
                    self.best_score = best_score
                    self.best_path = best_path
            if best_score == self.best_score:
                num_equal += 1
            else:
                num_equal = 0
            self.all_best_scores.append(best_score)
            self.evaporation()
            self.intensify(all_scores, all_paths)
            self.get_probabilities()

            print("Best score at iteration {}: {}; overall: {} ({:.2f}s)".format(i, best_score,
                                                                                 self.best_score,
                                                                                 time.time() - start_iter))

            if best_score == self.best_score and num_equal == self.EARLY_STOPPING_COUNT:
                self.stopped_early = True
                print("Stopping early due to {} iterations of the same score.".format(self.EARLY_STOPPING_COUNT))
                print(self.best_path)
                break

        self.fit_time = (time.time() - start)
        print("ACO fitted.  Time taken: {} seconds.  Best score: {}. \nBest path{}".format(round(self.fit_time, 2),
                                                                                           self.best_score,
                                                                                           self.best_path))
        return self.best_score

    def plot(self):
        """
        Plots the score over time after the model has been fitted.
        :return: None if the model isn't fitted yet
        """
        fig, ax = plt.subplots(figsize=(20, 15))
        ax.plot(self.all_best_scores, label="Best Run")
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Performance")
        ax.text(.8, .6,
                'Default ants: {}\nElite ants: {}\nWild ants: {}\nEvap Rate: {}\nAlpha: {}\nBeta: {}\n\nFit Time: {}s'.format(
                    self.ANTS_AMOUNT, self.ELITE_ANTS_AMOUNT, self.WILD_ANTS_AMOUNT, self.EVAPORATION_RATE, self.ALPHA,
                    self.BETA, round(self.fit_time, 2), ["\nStopped Early!" if self.stopped_early else ""][0]),
                bbox={'facecolor': 'gray', 'alpha': 0.8, 'pad': 10}, transform=ax.transAxes)
        ax.legend()
        plt.title("Ant Colony Optimization Results (best: {})".format(self.best_score))
        plt.show()


problem = np.random.randint(1, 500, size=(50, 50))
optimizer = AntColony()

best = optimizer.fit(problem)
optimizer.plot()

# np.array([[float('inf'), 1, 7, 3, 14], [3, float('inf'), 6, 9, 1], [6, 14, float('inf'), 3, 7],
#                     [2, 3, 5, float('inf'), 9], [15, 7, 11, 2, float('inf')]])

# np.array(           [[float('inf'), 3, 5, 6, 8, 1, 2, 2, 8, 3], [1, float('inf'), 3, 5, 7, 9, 4, 3, 8, 1],
#                     [3, 5, float('inf'), 8, 6, 9, 6, 3, 2, 3], [6, 8, 1, float('inf'), 2, 4, 6, 2, 4, 6],
#                     [5, 2, 1, 3, float('inf'), 5, 6, 8, 1, 4], [1, 4, 5, 6, 3, float('inf'), 6, 3, 7, 7],
#                     [1, 2, 4, 8, 6, 4, float('inf'), 6, 2, 4], [1, 5, 8, 2, 8, 6, 4, float('inf'), 1, 2],
#                     [2, 4, 6, 8, 1, 7, 4, 6, float('inf'), 5], [1, 2, 4, 1, 4, 5, 2, 4, 7, float('inf')]]

# np.random.randint(1, 50, size=(30, 30))
