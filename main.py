from repository import Repository
from service import Service

repository = Repository("data/berlin.txt", True)
service = Service(repository)
service.find_tsp_solution(True)
