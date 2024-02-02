from copy import deepcopy
from heap_piorityqueue import HeapPriorityQueueAdaptive
from parition_disjoint_set import Parition


class Graph:
    class _Vertex:
        __slot__ = "_key"

        def __init__(self, key) -> None:
            self._key = key

        def get_key(self):
            return self._key

        def __str__(self) -> str:
            return f"{self._key}"

        def __hash__(self) -> int:
            return hash(id(self))

    class _Edge:
        __slot__ = "_origin", "_destination", "_key"

        def __init__(self, origin, des, key) -> None:
            """Do not call constructor directly. Use Graph s insert edge(u,v,x)."""
            self._origin = origin
            self._destination = des
            self._key = key

        def endpoints(self):
            return (self._origin, self._destination)

        def oposite(self, origin):
            if origin is self._origin:
                return self._destination
            else:
                return self._origin

        def get_key(self):
            return self._key

        def __lt__(self, __other: object):
            if type(self._key) is not type(__other._key):
                raise TypeError(
                    f"'<' not supported between instances of {type(self._key)} and '{type(__other._key)}'")
            return self._key < __other._key

        def __str__(self) -> str:
            return f"({self._origin}, {self._destination}): {self._key} "

        def __hash__(self) -> int:
            return hash(id(self._origin, self._destination))

    def __init__(self, directed=False) -> None:
        self._out = dict()
        self._in_ = dict() if directed else self._out

    """ ULILITY """

    def is_directed(self):
        return self._out is self._in_

    def vertex_count(self):
        return len(self._out)

    def get_vertices(self):
        return self._out.keys()

    def edge_counts(self):
        total = sum(len(self._out[v]) for v in self._out)
        return total if self.is_directed() else total // 2

    def get_edges(self):
        edges = set()

        for secondary_map in self._out.values():
            edges.update(secondary_map.value())

        return edges

    def get_edges_frompair(self, u, v):
        return self._out[u].get(v)

    def get_degree(self, v, outgoing=True):
        adj = self._out if outgoing else self._in_
        return len(adj[v])

    def get_incident_edges(self, v, outgoing=True):
        adj = self._out if outgoing else self._in_
        for e in adj[v].values():
            yield e

    """ INSERT """

    def insert_vertex(self, key=None):
        v = self._Vertex(key)

        self._out[v] = dict()
        if not self.is_directed():
            self._in_[v] = dict()

        return v

    def insert_edge(self, start, end, key=None):
        e = self._Edge(start, end, key)
        self._out[start][end] = e
        self._in_[end][start] = e

        return e

    """ TRAVERSAL """

    def DFS(self, start, visited: dict):
        """Deapth First Search

            NOTE: USE VISITED ARGUMENT ALSO AS THE RESULT
        Args:
            g (Graph): 
            start (Graph.Vertex):
            visited (dict): pair of vertex, edged used to walk
        """
        for e in self.get_incident_edges(start):
            # Get its path the collorative vertexes.
            # For each vertex, add it into visited dictionary if it is not there.
            # We use visited list as a dictionary
            # for saving the edges along its endpoint vertexes
            next_v = e.oposite(start)
            if next_v not in visited:
                visited[next_v] = e
                # print(next_v._key, visited[next_v]._key)
                self.DFS(next_v, visited)

    def construct_path(self, start, end, all_path):  # i can not remove self argument
        """Get path from start to end

        Args:
            start (Graph.Vertex): 
            end (Graph.Vertex): 
            visited (dict): DFS result fron start node, i.e All possible route from the start
        """

        path = list()
        if end in all_path:
            path.append(end)
            walk = end
            while walk is not start:
                walk = all_path[walk].oposite(walk)
                path.append(walk)

            path.reverse()

        return path

    def DFS_complete(self):
        forest = dict()
        for v in self.get_vertices():
            if v not in forest:
                forest[v] = None  # start as a root
                self.DFS(v, forest)

        return forest

    def BFS(self, start, visited: dict):
        level = list(start)

        while len(level) > 0:
            next_level = list()
            for s in level:
                for e in self.get_incident_edges(s):
                    v = e.oposite(s)
                    if v not in visited:
                        next_level.append(v)
                        visited[v] = e

            level = next_level

        return visited

    """ SHOARTEST PATH OF CLOSURE"""

    def dijkstra(self, start, end):
        q = HeapPriorityQueueAdaptive()
        q_pointer = dict()
        dist = dict()

        visited = dict()

        # initialize
        for v in self.get_vertices():
            dist[v] = 0 if v is start else float("inf")

            q_pointer[v] = q.add(v, dist[v])

        while not q.is_empty():
            vertex, _ = q.remove_min()
            del (q_pointer[vertex])

            for e in self.get_incident_edges(vertex):
                u = e.oposite(vertex)

                if u in q_pointer and e._key + dist[vertex] < dist[u]:
                    dist[u] = dist[vertex] + e._key
                    visited[u] = dist[u]

                    q.update(q_pointer[u], u, dist[u])

        return visited

    def shortest_path_tree(self, start, min_dist: dict):
        tree = dict()
        for v in min_dist:
            if v is not start:
                # incoming edges, because we backtrack
                for e in self.get_incident_edges(v, False):
                    u = e.oposite(v)

                    if min_dist[v] == min_dist[u] + e._key:
                        tree[v] = e
                        continue

        return tree

    def floyd_warshall(self):
        """Return a new graph that is the transitive closure of graph"""
        closure = deepcopy(self)  # imported from copy module
        vertecies = list(self.get_vertices)  # make indexable list
        leng = len(vertecies)

        for i in range(leng):
            for ii in range(leng):
                # verify that edge (i,ii) exists in the partial closure
                if i != ii and closure.get_edges_frompair(vertecies[i], vertecies[ii]) is not None:
                    for iii in range(leng):
                        # verify that edge (ii,iii) exists in the partial closure
                        if i != iii and ii != iii and closure.get_edges_frompair(vertecies[ii], vertecies[iii]) is not None:
                            # if (i,j) not yet included, add it to the closure
                            if closure.get_edges_frompair(vertecies[i], vertecies[iii]) is None:
                                closure.insert_edge(
                                    vertecies[i], vertecies[iii])

        return closure

    """ SHOREST SPANNING TREE """

    def MST_prim(self):
        """Compute a minimum spanning tree of a graph using Kruskal s algorithm. 
        Return a dictionary of vertices with used edges that comprise the MST. 

        The elements of the graph s edges are assumed to be weights.
        """
        root = None
        dist = dict()
        prev = dict()
        # piority queue
        Q = HeapPriorityQueueAdaptive()
        locator = dict()

        for v in self.get_vertices():
            if root is None:
                root = v

            dist[v] = 0 if v is root else float("inf")
            locator[v] = Q.add(v, dist[v])
            prev[v] = None

        while not Q.is_empty():
            v, _ = Q.remove_min()
            del (locator[v])

            for e in self.get_incident_edges(v):
                u = e.oposite(v)
                if u in locator and e._key < dist[u]:
                    dist[u] = e._key
                    prev[u] = e

                    Q.update(locator[u], u, dist[u])

        return prev

    class Partition:
        ...

    def MST_krusal(self):
        """Compute a minimum spanning tree of a graph using Kruskal s algorithm. 
        Return a list of edges that comprise the MST. 

        The elements of the graph s edges are assumed to be weights."""

        tree = list()  # list of edges in spanning tree
        Q = HeapPriorityQueueAdaptive()  # entries are edges in G, with weights as key
        forest = self.Partition()  # keeps track of forest clusters
        position = dict()  # map each node to its Partition entry

        for v in self.get_vertices():
            position[v] = forest.make_group(v)

        for e in self.get_edges():
            Q.add(e, e._key)

        n_vertex = self.vertex_count()
        while len(tree) != n_vertex and not Q.is_empty():
            # tree not spanning and unprocessed edges remain
            e, _ = Q.remove_min()
            u, v = e.endpoints()

            a = forest.find(u)
            b = forest.find(v)
            if a != b:
                tree.append(e)
                forest.union(a, b)

        return tree

    """ TOPOLICICAL ORDER, ACYLIC TREE """

    def topological_sort(self):
        topo_order = list()
        zero_deg = list()

        in_deg = dict()
        for v in self.get_vertices():  # get incoming degree
            in_deg[v] = self.get_degree(v, outgoing=False)
            if in_deg[v] == 0:
                zero_deg.append(v)
                topo_order.append(v)

        while zero_deg:
            v = zero_deg.pop(0)
            for e in self.get_incident_edges(v):
                u = e.oposite(v)
                in_deg[u] -= 1

                if in_deg[u] == 0:
                    topo_order.append(u)
                    zero_deg.append(u)

        return topo_order

    """ CLOSURE TOUR """

    def is_eulerian(self):
        ...

    def eulerian_path(self):
        ...


""" ultility """

if __name__ == "__main__":

    g = Graph()
    vertex_list = [None] * 7
    for i in range(1, 7):
        vertex_list[i] = g.insert_vertex(f"v{i}")

    e23 = g.insert_edge(vertex_list[2], vertex_list[3], 1)
    e24 = g.insert_edge(vertex_list[2], vertex_list[4], 3)
    e25 = g.insert_edge(vertex_list[2], vertex_list[5], 4)
    e34 = g.insert_edge(vertex_list[4], vertex_list[3], 3)
    e13 = g.insert_edge(vertex_list[1], vertex_list[3], 2)
    e12 = g.insert_edge(vertex_list[1], vertex_list[2], 2)
    e16 = g.insert_edge(vertex_list[1], vertex_list[6], 3)
    e45 = g.insert_edge(vertex_list[4], vertex_list[5], 2)
    e46 = g.insert_edge(vertex_list[4], vertex_list[6], 7)

    directed_g = Graph(directed=False)

    vertex_list = [None] * 12
    for i in [5, 7, 3, 11, 8, 2, 9, 10]:
        vertex_list[i] = directed_g.insert_vertex(f"v{i}")

    e511 = directed_g.insert_edge(vertex_list[5], vertex_list[11], "e5_11")

    e711 = directed_g.insert_edge(vertex_list[7], vertex_list[11], "e7_11")
    e78 = directed_g.insert_edge(vertex_list[7], vertex_list[8], "e7_8")

    e38 = directed_g.insert_edge(vertex_list[3], vertex_list[8], "e3_8")
    e310 = directed_g.insert_edge(vertex_list[3], vertex_list[10], "e3_10")

    e112 = directed_g.insert_edge(vertex_list[11], vertex_list[2], "e11_2")
    e119 = directed_g.insert_edge(vertex_list[11], vertex_list[9], "e11_9")
    e1110 = directed_g.insert_edge(vertex_list[11], vertex_list[10], "e11_10")

    e89 = directed_g.insert_edge(vertex_list[8], vertex_list[9], "e8_9")

    tree = g.prim()
    for k, v in tree.items():
        ...
        print(k, v)

    # -----
