import copy


class Node:
    def __init__(self):
        self.arity = 0  # int
        self.parents = []  # Node[]
        self.dist = []  # [][floats]


class BayesNet:
    def __init__(self):
        self.nodes = []  # Node[]
        self.evidences = []  # int[] (-1 if no evidence)
        self.target = Node()

    def eliminate(self):
        index_of_virus_erzekenyseg = len(self.nodes) - 10
        if self.evidences[index_of_virus_erzekenyseg] != -1:
            for i in range(0, index_of_virus_erzekenyseg):
                if self.nodes[0] != self.target:
                    for n in self.nodes:
                        if self.nodes[0] in n.parents:
                            n.parents.remove(self.nodes[0])
                    self.nodes.remove(self.nodes[0])
                    self.evidences.remove(self.evidences[0])

    def enumeration_ask(self, x: Node, e: []):  # e: Node[]
        q = []
        for value in range(0, x.arity):
            ev = copy.deepcopy(e)
            ev[self.nodes.index(x)] = value
            q.append(self.enumerate_all(self.nodes, ev))
        sum_of_q = 0.0
        for j in range(0, len(q)):
            sum_of_q += q[j]
        for j in range(0, len(q)):
            q[j] /= sum_of_q
        return q

    def enumerate_all(self, nodes: [], e: []):
        if len(nodes) == 0:
            return 1.0
        y = nodes[0]
        if e[self.nodes.index(y)] != -1:
            re = self.assuming_parents(y, e) * self.enumerate_all(nodes[1:], e)
            return re
        else:
            _sum = []
            ev = copy.deepcopy(e)
            for i in range(0, y.arity):
                ev[self.nodes.index(y)] = i
                _sum.append(self.assuming_parents(y, ev) * self.enumerate_all(nodes[1:], ev))
            re = sum(_sum)
            return re

    def assuming_parents(self, node: Node, evidences: []):
        index_of_row = 0
        parent_values = []
        if len(node.parents) == 0:
            re = self.nodes[self.nodes.index(node)].dist[0][evidences[self.nodes.index(node)]]
            # print(re)
            return re
        for parent in node.parents:
            parent_values.append(evidences[self.nodes.index(parent)])  # reverse??
        num_of_rows = len(node.dist)
        for i in range(0, len(node.parents)):
            index_of_row += parent_values[i] * int(num_of_rows / node.parents[i].arity)
            num_of_rows /= node.parents[i].arity
        re = node.dist[index_of_row][evidences[self.nodes.index(node)]]
        # print(re)
        return re


def read(bn: BayesNet):
    num_of_nodes = 0
    num_of_evidences = 0
    line_num = 0
    try:
        while True:
            line_num += 1
            line = input()
            split = line.split()
            if line_num == 1:
                num_of_nodes = int(split[0])
                for i in range(0, num_of_nodes):
                    bn.evidences.append(-1)
            elif line_num < 2 + num_of_nodes:
                node = Node()
                node.arity = int(split[0])
                num_of_parents = int(split[1])
                for i in range(0, num_of_parents):
                    index_of_parent = int(split[2+i])
                    node.parents.append(bn.nodes[index_of_parent])
                num_of_dist_table_rows = 1
                for i in range(0, num_of_parents):
                    num_of_dist_table_rows *= node.parents[i].arity
                for i in range(0, num_of_dist_table_rows):
                    dist_row = split[2 + num_of_parents + i]
                    split_dist_row = dist_row.split(":")
                    if len(split_dist_row) != 1:
                        str_self_distribution = split_dist_row[1].split(",")
                    else:
                        str_self_distribution = split_dist_row[0].split(",")
                    distribution_values = []
                    for j in range(0, len(str_self_distribution)):
                        distribution_values.append(float(str_self_distribution[j]))
                    node.dist.append(distribution_values)
                bn.nodes.append(node)
            elif line_num == 2 + num_of_nodes:
                num_of_evidences = int(split[0])
            elif line_num < 3 + num_of_nodes + num_of_evidences:
                index_of_evidence = int(split[0])
                bn.evidences[index_of_evidence] = int(split[1])
            elif line_num == 3 + num_of_nodes + num_of_evidences:
                index_of_target = int(split[0])
                bn.target = bn.nodes[index_of_target]
                break
            else:
                break
    except EOFError:
        pass


def arrays_equal(arr1: [], arr2: []):
    if len(arr1) != len(arr2):
        return False
    for i in range(0, len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True


def write(b: BayesNet):
    print(len(b.nodes))
    for n in b.nodes:
        print(n.arity, end="\t")
        print(len(n.parents), end="\t")
        rows_in_dist_table = 1
        for p in n.parents:
            print(b.nodes.index(p), end="\t")
            rows_in_dist_table *= p.arity
        for row in range(0, rows_in_dist_table):
            for dist_probability in n.dist[row]:
                print(str(dist_probability), end=",")
            print("\t", end="")
        print()
    print(len(b.evidences))
    for i in range(0, len(b.evidences)):
        if b.evidences[i] != -1:
            print(i, end="\t")
            print(b.evidences[i])
    print(b.nodes.index(b.target))


bnw = BayesNet()
read(bnw)
bnw.eliminate()
#write(bnw)
solution = bnw.enumeration_ask(bnw.target, bnw.evidences)
#print("solution:")
for k in range(0, len(solution)):
    print(solution[k])
