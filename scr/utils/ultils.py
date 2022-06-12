import csv

from scr.Graph import Graph


def init_graph(filename: str):
    """
    Khởi tạo graph từ path truyền vào
    :param filename: đường dẫn của file
    :return: graph
    """
    graph = Graph()
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            IATA_org, IATA_des, Name_org, Name_des, Passengers = list(row.values())[0:5]
            graph.add_edge(IATA_org, IATA_des, Name_org, Name_des, Passengers)
    graph.init_pagerank()
    return graph
