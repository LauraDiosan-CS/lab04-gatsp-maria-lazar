from city import City


class Repository:
    def __init__(self, file_name, e=False):
        self.__graph = {}
        self.__ga_params = {}
        if e == False:
            # problem with graph
            self.load_from_file(file_name)
        else:
            # problem with coordinates
            self.load_from_file_e(file_name)

    # from txt file
    def load_from_file(self, file_name):
        f = open(file_name, "r")
        n = int(f.readline())
        self.__graph['num_nodes'] = n
        mat = []
        for i in range(n):
            mat.append([])
            line = f.readline()
            elements = line.split(",")
            for j in range(n):
                mat[-1].append(int(elements[j]))
        self.__graph["mat"] = mat
        size = int(f.readline())
        gen = int(f.readline())
        rate = float(f.readline())
        elite = int(f.readline())
        self.__ga_params = {'pop_size': size, 'no_gen': gen, 'rate': rate, 'elite': elite}
        f.close()

    @property
    def graph(self):
        return self.__graph

    def write_network(self, file_name, solution, distance):
        f = open(file_name, "w")
        result = ''
        result += str(distance) + "\n"
        for i in solution:
            result += str(i + 1) + " "
        f.writelines(result)
        f.close()

    def get_ga_params(self):
        return self.__ga_params

    def load_from_file_e(self, file_name):
        f = open(file_name, "r")
        n = int(f.readline())
        self.__graph['num_nodes'] = n
        # dictionary with key index city and value city
        dict = {}
        for i in range(n):
            line = f.readline()
            elements = line.split(" ")
            dict[int(elements[0]) - 1] = City(float(elements[1]), float(elements[2]))
        self.__graph["dict"] = dict
        size = int(f.readline())
        gen = int(f.readline())
        rate = float(f.readline())
        elite = int(f.readline())
        self.__ga_params = {'pop_size': size, 'no_gen': gen, 'rate': rate, 'elite': elite}
        f.close()
