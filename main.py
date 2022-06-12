from scr.utils.ultils import init_graph
from optparse import OptionParser
from scr.Graph import Graph
import scr.utils.ouput as op
import time


def weight_pagerank_one_iter(graph: Graph, d: float):
    node_list = graph.nodes.values()
    dangling_sum_weight = graph.dangling_node_weight_handle()
    leng_node = len(graph.nodes)
    for node in node_list:
        node.update_new_weight_pagerank(d, dangling_sum_weight, leng_node)
    for node in node_list:
        node.update_weight_pagerank()


def weight_pagerank(graph: Graph, d: float = 0.85, iteration: int = 50):
    plot_weight_pagerank = {}
    for i in range(iteration):
        weight_pagerank_list = graph.get_weight_pagerank_list()
        for IATA, name, pagerank in weight_pagerank_list:
            if IATA not in plot_weight_pagerank:
                plot_weight_pagerank[IATA] = []
                plot_weight_pagerank[IATA].append(pagerank)
            else:
                plot_weight_pagerank[IATA].append(pagerank)
        weight_pagerank_one_iter(graph, d)
    return plot_weight_pagerank


def PageRank_one_iter(graph: Graph, d: float):
    """
    Tính pagerank 1 lần lặp
    :param graph: Đồ thị sân bay truyền vào
    :param d: damping factor
    :return: none
    """
    node_list = graph.nodes.values()
    dangling_sum = graph.dangling_node_handle()
    leng_node = len(graph.nodes)
    for node in node_list:
        node.update_new_pagerank(d, dangling_sum, leng_node)
    for node in node_list:
        node.update_pagerank()


def PageRank(graph: Graph, d: float = 0.85, iteration: int = 50):
    """
    Tính pagerank iteration lần lặp
    :param graph: đồ thị
    :param d: damping factor
    :param iteration: số lần lặp
    :return: none
    """
    plot_pagerank = {}
    for i in range(iteration):
        pagerank_list = graph.get_pagerank_list()
        for IATA, name, pagerank in pagerank_list:
            if IATA not in plot_pagerank:
                plot_pagerank[IATA] = []
                plot_pagerank[IATA].append(pagerank)
            else:
                plot_pagerank[IATA].append(pagerank)
        PageRank_one_iter(graph, d)
    return plot_pagerank


def output_PageRank(iteration, graph, damping_factor, result_dir, fname):
    """
    xuất file, tính thời gian và xuất ảnh pagerank
    :param iteration: số lần lặp
    :param graph: dồ thị sân bay
    :param damping_factor: damping factor
    :param result_dir: đường dẫn của thư mục kết quả
    :param fname: tên file
    :return: none
    """
    speed = {}
    start_time = time.time()
    plot_pagerank = PageRank(graph, damping_factor, iteration)
    pagerank_time = time.time()
    speed['pagerank'] = pagerank_time - start_time
    plot_weight_pagerank = weight_pagerank(graph, damping_factor, iteration)
    weight_pagerank_time = time.time()
    speed['weight_pagerank'] = weight_pagerank_time - pagerank_time
    op.plot_pagerank_iteration(plot_pagerank, plot_weight_pagerank, 5, iteration, result_dir, fname, )
    airport_rank_list = graph.get_airport_rank_list()
    pagerank_list = graph.get_pagerank_list()
    airport_weight_rank_list = graph.get_airport_weight_rank_list()
    weight_pagerank_list = graph.get_weight_pagerank_list()
    weight_in_airport = graph.get_weight_in_airport()
    weight_out_airport = graph.get_weight_out_airport()
    op.plot_weight_airport(weight_in_airport, weight_out_airport, 5, result_dir, fname)
    op.output_file(pagerank_list, ["IATA", "City", "Pagerank"], result_dir, fname, "_Airport_pagerank")
    op.output_file(airport_rank_list, ["IATA", "City", "Pagerank", "Rank"], result_dir, fname, "_Airport_rank")
    op.output_file(weight_pagerank_list, ["IATA", "City", "Weight pagerank"], result_dir, fname,
                   "_Airport_weight_pagerank")
    op.output_file(airport_weight_rank_list, ["IATA", "City", "Weight Pagerank", "Rank"], result_dir, fname,
                   "_Airport_Weight_rank")
    op.graph_info(graph,result_dir, fname,"_graph_info")
    file_time = time.time()
    speed['file'] = file_time - weight_pagerank_time
    op.graph_to_img(graph, result_dir, fname)
    image_time = time.time()
    speed['image'] = image_time - file_time
    return speed


if __name__ == '__main__':
    optparser = OptionParser()
    optparser.add_option('-f', '--input_file',
                         dest='input_file',
                         help='CSV filename',
                         default='dataset/Airports2_clean_scr_des.csv')
    # testcase6.csv
    # Airports2_clean_scr_des.csv
    # Dangling_node_case.txt
    # Airports2_top5_clean_scr_des.csv
    optparser.add_option('--damping_factor',
                         dest='damping_factor',
                         help='Damping factor (float)',
                         default=0.7,
                         type='float')
    optparser.add_option('--iteration',
                         dest='iteration',
                         help='Iteration (int)',
                         default=15,
                         type='int')
    (options, args) = optparser.parse_args()
    file_path = options.input_file
    iteration = options.iteration
    damping_factor = options.damping_factor
    result_dir = 'result'
    fname = file_path.split('/')[-1].split('.')[0]
    start_time = time.time()
    graph = init_graph(file_path)
    init_graph_time = time.time()
    speed = output_PageRank(iteration, graph, damping_factor, result_dir, fname)
    end_time = time.time()
    speed['init_graph'] = init_graph_time - start_time
    speed['total'] = end_time - start_time
    op.write_speed(speed, result_dir, fname, "_speed")
    print(graph.get_graph_info())
