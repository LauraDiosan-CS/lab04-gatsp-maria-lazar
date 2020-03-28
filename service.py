from random import uniform

import matplotlib.pyplot as plt

from ga import GA


def generate_value(lim1, lim2):
    return int(uniform(lim1, lim2))


class Service:
    def __init__(self, repo):
        self.repository = repo

    # euclidean route distance
    def e_route_distance(self, route):
        dict = self.repository.graph['dict']
        pathDistance = 0
        for i in range(0, len(route) - 1):
            fromCity = dict[route[i]]
            toCity = dict[route[i + 1]]
            pathDistance += fromCity.distance(toCity)
        return pathDistance

    # fitness function for euclidean distance
    def e_fittness(self, route):
        d = float(self.e_route_distance(route))
        return 1 / d

    # graph route distance
    def route_distance(self, route):
        d = 0.0
        mat = self.repository.graph['mat']
        for i in range(len(route) - 1):
            a = mat[route[i]][route[i + 1]]
            d = d + a
        return d

    # fitness function for graph route distance
    def fitness(self, route):
        return 1 / self.route_distance(route)

    def find_tsp_solution(self, e=None):
        if e is None:
            # problem with graph
            problem_param = {'min': 1, 'max': self.repository.graph['num_nodes'], 'function': self.fitness,
                             'dim': self.repository.graph['num_nodes'] + 1, 'noBits': 1}
            dist_function = self.route_distance
        else:
            # problem with coordinates
            problem_param = {'min': 1, 'max': self.repository.graph['num_nodes'], 'function': self.e_fittness,
                             'dim': self.repository.graph['num_nodes'] + 1, 'noBits': 1}
            dist_function = self.e_route_distance
        ga_params = self.repository.get_ga_params()
        ga = GA(ga_params, problem_param)
        ga.initialisation()
        ga.evaluation()
        overall_best = ga.best_chromosome()
        # stores best distance in each generation
        progress = []
        for g in range(ga_params['no_gen']):
            best_chromosome = ga.best_chromosome()
            progress.append(dist_function(best_chromosome.representation))
            # generate next generation
            ga.one_generation_pool()
            best_chromosome = ga.best_chromosome()
            # update overall best chromosome
            if best_chromosome.fitness > overall_best.fitness:
                overall_best = best_chromosome
            print('Best solution in generation ' + str(g) + ' is: x = ' + str(
                best_chromosome.representation) + ' f(x) = ' + str(
                best_chromosome.fitness))
        print [i + 1 for i in overall_best.representation]
        print dist_function(overall_best.representation)
        # save results to file
        self.repository.write_network("data/graph_out.txt", overall_best.representation,
                                      dist_function(overall_best.representation))
        # plot distance progress
        plt.plot(progress)
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.savefig('figure')
        plt.show()
