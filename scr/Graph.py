class Graph:
    def __init__(self):
        self.nodes = {}

    # khởi tạo giá trị pagerank ban đầu cho từng node sau khi khởi tạo graph
    def init_pagerank(self):
        """
        Khởi tạo giá trị pagerank ban đầu cho từng node là 1/n sau khi tạo liên kết
        :return: none
        """
        count_node = len(self.nodes)
        for node in self.nodes.values():
            node.pagerank = node.pagerank / count_node
            node.weight_pagerank = node.weight_pagerank / count_node

    # hàm tìm kiếm và trả về node đã tồn tại trong dict nodes. Nếu chưa có thì tạo node mới, thêm vào dict nodes và trả về node mới đó
    def find(self, IATA, name):
        """
        Tìm kiếm và trả về node đã tồn tại trong dict nodes. Nếu chưa có thì tạo node mới
        :param IATA: Mã IATA của sân bay
        :param name: Tên của sân bay
        :return: node
        """
        if IATA not in self.nodes:
            newnode = Node(IATA)
            newnode.name = name
            self.nodes[IATA] = newnode
            return newnode
        else:
            return self.nodes[IATA]

    def add_edge(self, parent, child, parent_name, child_name, passengers: int = 1):
        """
        Thêm cạnh trọng số từ sân bay nguồn tới sân bay đích, nếu sân bay chưa có trong graph thi tiến hành khỏi tạo.
        :param parent: Mã IATA sân bay nguồn
        :param child: Mã IATA sân bay đích
        :param parent_name: Tên sân bay nguồn
        :param child_name: Tên sân ay đích
        :param passengers: Số lượng hành khách trên đường bay này
        :return: none
        """
        parent_node = self.find(parent, parent_name)
        child_node = self.find(child, child_name)
        passengers = int(passengers)
        parent_node.link_child(child_node, passengers)
        child_node.link_parent(parent_node, passengers)

    def sum_of_pagerank(self):
        """
        Tính tổng pagerank của graph
        :return: tổng pagerank của graph
        """
        return sum(node.pagerank for node in self.nodes.values())

    def sum_of_weight_pagerank(self):
        """
        Tính tổng pagerank trọng số của graph
        :return: tổng pagerank trọng số của graph
        """
        return sum(node.weight_pagerank for node in self.nodes.values())

    def dangling_node_handle(self):
        """
        Tính tổng tổng phân phối pagerank của các nút cụt
        :return: tổng phân phối pagerank của nút cụt
        """
        dangling_sum = 0
        count_node = len(self.nodes)
        for node in self.nodes.values():
            if len(node.children) == 0:
                dangling_sum += node.pagerank / count_node
        return dangling_sum

    def dangling_node_weight_handle(self):
        """
        Tính tổng tổng phân phối pagerank của các nút cụt
        :return: tổng phân phối pagerank của nút cụt
        """
        dangling_sum = 0
        count_node = len(self.nodes)
        for node in self.nodes.values():
            if len(node.children) == 0:
                dangling_sum += node.weight_pagerank / count_node
        return dangling_sum

    def display(self):
        """
        Xuất ra console dồ thị
        :return: none
        """
        for IATA, node in self.nodes.items():
            for parent, weight in node.parents.items():
                print(f'{parent.IATA}->{weight} {IATA}')

    def get_weight_pagerank_list(self):
        """
        Lấy danh sách thông tin pagerank trọng số của đồ thị
        :return:
        """
        arr = []
        for IATA, node in self.nodes.items():
            arr.append([IATA, node.name, node.weight_pagerank])
        return arr

    def get_airport_weight_rank_list(self):
        """
        Lấy danh sách xếp hạng sân bay theo trọng số
        :return: danh sách xếp hạng của sân bay
        """
        arr = self.get_weight_pagerank_list()
        arr = sorted(arr, key=lambda x: x[2], reverse=True)
        count = 1
        for i in arr:
            i.append(count)
            count += 1
        return arr

    def get_pagerank_list(self):
        """
        Lấy danh sách pagerank của sân bay
        :return: danh sách pagrank của sân bay
        """
        arr = []
        for IATA, node in self.nodes.items():
            arr.append([IATA, node.name, node.pagerank])
        return arr

    def get_airport_rank_list(self):
        """
        Lấy danh sách xếp hạng sân bay theo pagerank
        :return:
        """
        arr = self.get_pagerank_list()
        arr = sorted(arr, key=lambda x: x[2], reverse=True)
        count = 1
        for i in arr:
            i.append(count)
            count += 1
        return arr

    def get_weight_in_airport(self):
        return {IATA: sum(list(node.parents.values())) for IATA, node in self.nodes.items()}

    def get_weight_out_airport(self):
        return {IATA: node.out_passengers for IATA, node in self.nodes.items()}

    def get_test_list(self):
        """
        Lấy danh sách cho test case
        :return:
        """
        arr = []
        for IATA, node in self.nodes.items():
            arr.append([IATA, node.pagerank, node.weight_pagerank])
        return sorted(arr, key=lambda x: x[0])

    # ["#", "IATA", "In Passenger", "Out passenger", "Inlink", "Outlink"]
    def get_graph_info(self):
        info = []
        count_node = 1
        for node in self.nodes.values():
            info.append(
                [count_node, node.IATA, node.get_in_passenger(), node.out_passengers, len(node.parents),
                 len(node.children)])
            count_node += 1
        return info


class Node:
    def __init__(self, IATA):
        self.IATA = IATA
        self.name = ""
        self.out_passengers = 0
        self.parents = {}
        self.children = set()
        self.pagerank = 1
        self.new_pagerank = 1
        self.weight_pagerank = 1
        self.new_weight_pagerank = 1

    def get_in_passenger(self):
        return sum(self.parents.values())

    def link_child(self, child, passengers):
        """
        Khởi tạo đường bay từ Node hiện tại với Node con
        :param child: Node con
        :param passengers: Số lượng hành khách từ Node hiện tại ra các Node khác
        :return: none
        """
        self.children.add(child)
        self.out_passengers += passengers

    def link_parent(self, parent, passengers):
        """
        Liên kết Node hiện tại tới Node cha của nó
        :param parent: Node cha
        :param passengers: số lượng hành khách từ Node cha tới Node hiện tại
        :return: none
        """
        if parent not in self.parents:
            self.parents[parent] = passengers
        else:
            self.parents[parent] += passengers

    def update_weight_pagerank(self):
        """
        Cập nhật giá trị pagerank trọng số của node
        :return: none
        """
        self.weight_pagerank = self.new_weight_pagerank

    def update_new_weight_pagerank(self, d, dangling_sum, n):
        """
        Tính pagerank trọng số của Node hiện tại
        :param d: Damping factor
        :param dangling_sum: Phân phối pagerank của nút cụt
        :param n: số lượng nút trong graph
        :return: none
        """
        in_neighbors = self.parents
        pagerank_sum = sum((node.weight_pagerank * passengers / node.out_passengers) for node, passengers in
                           in_neighbors.items())
        random_jumping = (1 - d) / n
        self.new_weight_pagerank = random_jumping + d * (pagerank_sum + dangling_sum)

    def update_pagerank(self):
        """
        Cập nhật pagerank cho node hiện tại
        :return: none
        """
        self.pagerank = self.new_pagerank

    def update_new_pagerank(self, d, dangling_sum, n):
        """
        Tính pagerank mới cho node hiện tại
        :param d: damping factor
        :param dangling_sum: Tổng phân phối pagerank của node cụt
        :param n: Số lượng graph trong dồ thị
        :return: none
        """
        in_neighbors = self.parents
        pagerank_sum = sum((node.pagerank / len(node.children)) for node in in_neighbors.keys())
        random_jumping = (1 - d) / n
        self.new_pagerank = random_jumping + d * (pagerank_sum + dangling_sum)
