from random import randint, uniform, random, shuffle
import numpy.random as npr
from numpy import interp

from chromosome import Chromosome


def generate_value(lim1, lim2):
    return int(uniform(lim1, lim2))


class GA:
    def __init__(self, param=None, probl_param=None):
        self.__param = param
        self.__prob_param = probl_param
        self.__population = []
        self.__mating_pool = []
        self.__selection_probabilities = []

    @property
    def population(self):
        return self.__population

    # random
    def initialisation(self):
        for _ in range(0, self.__param['pop_size']):
            r = [i for i in range(1, self.__prob_param['max'])]
            shuffle(r)
            r = [0] + r
            r.append(0)
            cr = Chromosome(self.__prob_param)
            cr.set_representation(r)
            self.__population.append(cr)

    def evaluation(self):
        for c in self.__population:
            c.set_fitness(self.__prob_param['function'](c.representation))
        self.__population.sort(key=lambda x: x.fitness)

    def best_chromosome(self):
        return self.population[len(self.population) - 1]

    # roulette wheel selection
    def selectOne(self):
        return npr.choice(self.__population, p=self.__selection_probabilities)

    def selection_probabilities(self):
        max = sum([c.fitness for c in self.__population])
        self.__selection_probabilities = [c.fitness / max for c in self.__population]

    def one_generation_pool(self):
        self.selection_probabilities()
        new_population = []
        # best elite number of chromosomes are passed to the next generation
        elite = self.__param['elite']
        for i in range(len(self.population) - elite, len(self.population)):
            new_population.append(self.__population[i])
        # generate rest
        for i in range(self.__param['pop_size'] - elite):
            p1 = self.selectOne()
            p2 = self.selectOne()
            off = p1.crossover(p2)
            off.mutation(self.__param['rate'])
            new_population.append(off)
        self.__population = new_population
        self.evaluation()
