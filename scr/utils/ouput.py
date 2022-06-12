import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


# def graph_to_img(graph, result_dir, fname):
#     """
#     Chuyển graph thành ảnh
#     :param graph:
#     :param result_dir:
#     :param fname:
#     :return:
#     """
#     pagerank_fname = '_Graph.png'
#     path = os.path.join(result_dir, fname)
#     os.makedirs(path, exist_ok=True)
#     file_path = os.path.join(path, fname + pagerank_fname)
#     G = nx.DiGraph()
#     for from_node in graph.nodes.values():
#         for to_node in from_node.children:
#             G.add_edge(from_node.IATA, to_node.IATA, weight=to_node.parents[from_node])
#     pos = nx.circular_layout(G)
#     nx.draw_circular(G, node_size=700,
#                      with_labels=True, font_weight=10)
#     edge_labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
#     plt.savefig(file_path)
#     plt.clf()

def graph_to_img(graph, result_dir, fname):
    """
    Chuyển graph thành ảnh
    :param graph:
    :param result_dir:
    :param fname:
    :return:
    """
    pagerank_fname = '_Graph.png'
    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, fname + pagerank_fname)
    G = nx.DiGraph()
    for from_node in graph.nodes.values():
        for to_node in from_node.children:
            G.add_edge(from_node.IATA, to_node.IATA, weight=to_node.parents[from_node])
    pos = nx.circular_layout(G)
    nx.draw(G, pos, node_size=700,
            with_labels=True, font_weight=10, connectionstyle='arc3, rad = 0.1')
    plt.savefig(file_path)
    plt.clf()


def graph_info(graph, result_dir, folder_name, file_name):
    header_list = ["#", "IATA", "In Passenger", "Out passenger", "Inlink", "Outlink"]
    list = graph.get_graph_info()
    file_name += ".csv"
    path = os.path.join(result_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, folder_name + file_name)
    with open(file_path, newline='', mode='w') as csv_write_file:
        fieldnames = header_list
        writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in list:
            row = {}
            count = 0
            for j in header_list:
                row[j] = i[count]
                count += 1
            writer.writerow(row)


def output_file(list, header_list, result_dir, folder_name, file_name):
    """
    xuất file csv
    :param list: danh sách cần xuất
    :param header_list: header của các cột
    :param result_dir: đường dẫn thư mục kết quả
    :param folder_name: tên folder
    :param file_name: file name
    :return: none
    """
    file_name += ".csv"
    path = os.path.join(result_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, folder_name + file_name)
    with open(file_path, newline='', mode='w') as csv_write_file:
        fieldnames = header_list
        writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in list:
            row = {}
            count = 0
            for j in header_list:
                row[j] = i[count]
                count += 1
            writer.writerow(row)


def plot_pagerank_iteration(pagerank, weight_pagerank, limit, iteration, result_dir, fname):
    pagerank = dict(sorted(pagerank.items(), key=lambda item: item[1][-1], reverse=True))
    weight_pagerank = dict(sorted(weight_pagerank.items(), key=lambda item: item[1][-1], reverse=True))
    pagerank_fname = '_pagerank_chart.png'
    weightpagerank_fname = '_weight_pagerank_chart.png'
    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)
    pagerank_path = os.path.join(path, fname + pagerank_fname)
    weightpagerank_path = os.path.join(path, fname + weightpagerank_fname)
    iter = [i for i in range(iteration)]
    count = 0
    plt.title("PageRank")
    plt.xlim(0, iteration)
    for IATA, pagerank in pagerank.items():
        plt.plot(iter, pagerank, label=IATA)
        # naming the x axis
        plt.xlabel('Iteration')
        # naming the y axis
        plt.ylabel('PageRank')
        count += 1
        if count == limit:
            break
    plt.xticks(iter)
    plt.legend(loc='upper right')
    plt.savefig(pagerank_path)
    plt.clf()
    count = 0
    plt.title("Weight PageRank")
    plt.xlim(0, iteration)
    for IATA, pagerank in weight_pagerank.items():
        plt.plot(iter, pagerank, label=IATA)
        # naming the x axis
        plt.xlabel('Iteration')
        # naming the y axis
        plt.ylabel('Weight PageRank')
        count += 1
        if count == limit:
            break
    plt.xticks(iter)
    plt.legend(loc='upper right')
    plt.savefig(weightpagerank_path)
    plt.clf()


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha='center',
                 Bbox=dict(facecolor='white', alpha=.5))


def plot_weight_airport(weight_in, weight_out, limit, result_dir, fname):
    weight_in = dict(sorted(weight_in.items(), key=lambda item: item[1], reverse=True))
    weight_fname = '_in_passenger_chart.png'
    path = os.path.join(result_dir, fname)
    os.makedirs(path, exist_ok=True)
    weight_path = os.path.join(path, fname + weight_fname)
    lable = list(weight_in.keys())[0:limit]
    X_axis = np.arange(len(lable))
    weight_in = list(weight_in.values())[0:limit]
    weight_outt = list()
    for IATA in lable:
        weight_outt.append(weight_out[IATA])
    plt.bar(X_axis - 0.2, weight_in, 0.4, label='in passenger')
    plt.bar(X_axis + 0.2, weight_outt, 0.4, label='out passenger')
    plt.xticks(X_axis, lable)
    # plot title
    plt.legend()
    plt.savefig(weight_path)
    plt.clf()


def write_speed(list: {}, result_dir, folder_name, file_name):
    """
        xuất file csv
        :param list: danh sách cần xuất
        :param header_list: header của các cột
        :param result_dir: đường dẫn thư mục kết quả
        :param folder_name: tên folder
        :param file_name: file name
        :return: none
        """
    file_name += ".csv"
    path = os.path.join(result_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, folder_name + file_name)
    with open(file_path, newline='', mode='w') as csv_write_file:
        fieldnames = list.keys()
        writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(list)
