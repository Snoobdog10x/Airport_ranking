import csv

from main import output_PageRank
from scr.utils.ultils import init_graph
import os


def read_testcase(filename: str):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        test_list = []
        for row in csv_reader:
            test_list.append(list(row.values()))
        return sorted(test_list, key=lambda x: x[0])

def testcase_checker(output_list: [], testcase_list: []):
    print(output_list)
    print(testcase_list)
    mean_pagerank_percent = 0
    pagerank_percent = {}
    for i in range(len(output_list)):
        percent = output_list[i][1] * 100 / float(testcase_list[i][1])
        pagerank_percent[output_list[i][0]] = percent
        mean_pagerank_percent += percent
    mean_pagerank_percent /= len(pagerank_percent)
    mean_pagerank_weight_percent = 0
    weight_pagerank_percent = {}
    for i in range(len(output_list)):
        percent = output_list[i][2] * 100 / float(testcase_list[i][2])
        weight_pagerank_percent[output_list[i][0]] = percent
        mean_pagerank_weight_percent += percent
    mean_pagerank_weight_percent /= len(weight_pagerank_percent)
    print(f"Pagerank percent: {mean_pagerank_percent}")
    print(pagerank_percent)
    print(f"Pagerank weight percent: {mean_pagerank_weight_percent}")
    print(weight_pagerank_percent)


iteration = 15
damping_factor = 0.85
dataset_path = 'dataset'
testcase_path = 'testcase'
result_dir = 'result'
for filename in os.listdir(dataset_path):
    if filename != "Airports2.csv" and filename != "Airports2_clean_scr_des.csv" and filename != "Airports2_top5_clean_scr_des.csv":
        print(filename)
        file_path = dataset_path + "/" + filename
        fname = file_path.split('/')[-1].split('.')[0]
        filetest_path = testcase_path + "/" + filename
        graph = init_graph(file_path)
        output_PageRank(iteration, graph, damping_factor, result_dir, fname)
        output_list = graph.get_test_list()
        testcase_list = read_testcase(filetest_path)
        testcase_checker(output_list, testcase_list)
