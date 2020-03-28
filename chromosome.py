from random import randint, uniform, random


def generate_value(lim1, lim2):
    return int(uniform(lim1, lim2))


class Chromosome:
    def __init__(self, problParam=None):
        self.__prob_param = problParam
        self.__representation = []
        self.__fitness = 0.0

    def set_representation(self, r):
        self.__representation = r

    @property
    def representation(self):
        return self.__representation

    @property
    def fitness(self):
        return self.__fitness

    def set_fitness(self, fit):
        self.__fitness = fit

    def invert(self, i, j):
        if i > j:
            i, j = j, i

        while i < j:
            self.__representation[i], self.__representation[j] = self.__representation[j], \
                                                                        self.__representation[i]
            i = i + 1
            j = j - 1

    #Order Crossover
    def crossover(self, c):
        childP1 = []
        childP2 = []
        gene1 = generate_value(1, self.__prob_param['dim'] - 1)
        gene2 = generate_value(1, self.__prob_param['dim'] - 1)
        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)
        for i in range(start_gene, end_gene):
            childP1.append(self.__representation[i])
        childP2 = [item for item in c.__representation if item not in childP1]
        childP2[start_gene:start_gene] = childP1
        if childP2[len(childP2) - 1] != 0:
            childP2.append(0)
        ch = Chromosome(self.__prob_param)
        ch.set_representation(childP2)
        return ch

    # Reverse Sequence Mutation
    def mutation(self, rate):
        for gene in range(1, len(self.__representation) - 1):
            rand = random()
            if rand < rate:
                gene2 = generate_value(1, len(self.__representation) - 1)
                self.invert(gene, gene2)
                # # gene2 = (gene + 1)
                # self.__representation[gene], self.__representation[gene2] = self.__representation[gene2], \
                #                                                             self.__representation[gene]

    def __cmp__(self, other):
        return self.fitness < other.fitness
    def __str__(self):
        return '\nChromo: ' + str(self.__representation) + ' has fit: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__representation == c.__representation and self.__fitness == c.__fitness

