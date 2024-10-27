class Graph:
    def __init__(self, size: int, directed: bool = False) -> None:
        self._out: list[list[int | None]] = [
            [None for i in range(size)] for j in range(size)
        ]

        self._directed = directed

    """ PROTECTED """

    def __str__(self):
        return str(self._out)

    def __len__(self) -> int:
        return len(self._out)

    @property
    def directed(self):
        return self._directed

    def __getitem__(self, item: int) -> list[int | None]:
        return self._out[item]

    def insert_edge(self, start: int, end: int, weight: int = 1) -> None:
        if weight == 0:
            return  # no weight

        self[start][end] = weight
        if not self.directed:
            self[end][start] = self[start][end]

    """ COUNT """

    def degree(self, vertex: int) -> int:
        deg = 0
        for u in self[vertex]:
            if self[vertex][u] is not None:
                deg += 1

        return deg

    """ ITERATE """

    def get_vertex(self):
        for v in range(len(self)):
            yield v

    def get_incident_edge(self, start: int = 0):
        for end in range(len(self)):
            if self[start][end] is not None:
                yield self[start][end]

    def get_adjacent_vertex(self, start: int = 0):
        for end in range(len(self[start])):
            if self[start][end] is not None:
                yield end

    """ TRAVERSAL """

    def DFS_ordered(self, start: int) -> list[int]:
        stack = [start]
        path = list()

        while stack:
            v = stack.pop(-1)

            if v not in path:
                path.append(v)

                next_level = [
                    u for u in self.get_adjacent_vertex(v) if u not in path]
                next_level.sort()
                stack += next_level

        return path

    def BFS_ordered(self, start: int) -> list[int]:
        path = list()

        queue = [start]
        while queue:
            v = queue.pop(0)

            if v not in path:
                path.append(v)

                next_level = [
                    u for u in self.get_adjacent_vertex(v) if u not in path]
                next_level.sort()

                queue += next_level

        return path

    """ SHORTEST PATH """

    def shortest_distance_djikstra(self, start: int = 0) -> list[float]:
        dist = [float("inf") for i in range(len(self._out))]
        dist[start] = 0

        # vertices is the index
        # so that we can get the index as vertices
        min_list = [i for i in range(len(self))]  # list of vertices
        while min_list:
            v = min(min_list, key=lambda v: dist[v])
            min_list.remove(v)

            for u in self.get_adjacent_vertex(v):
                if u in min_list and dist[u] > dist[v] + self[v][u]:
                    dist[u] = dist[v] + self[v][u]

        return dist

    # instead of musing two list: min_vertex and distance to
    # which fform a key_value pair, should use a
    # dict from vertex to distance, and a
    # shortest path list map index as vertex to distance
    def MST_prim(self, start: int = 0) -> list[float]:  # list of vertex
        dist = [float("inf") for i in range(len(self))]
        dist[start] = 0

        min_vertex = [i for i in range(len(self))]  # list of vertices
        while min_vertex:
            v = min(min_vertex, key=lambda v: dist[v])
            min_vertex.remove(v)

            for u in self.get_adjacent_vertex(v):
                e = self[v][u]  # get edge

                if u in min_vertex and e is not None and e < dist[u]:
                    dist[u] = e

        return dist

    """ ONE-TIME PATH """

    def floywarshall_shortest_distance(self):
        dist = [[float("inf") for i in range(len(self))]
                for j in range(len(self))]
        for v in self.get_vertex():
            for u in self.get_vertex():
                dist[u][v] = self[u][v]

        for v in self.get_vertex():
            dist[v][v] = 0

        for k in range(len(self)):
            for i in range(len(self)):
                for j in range(len(self)):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def floywarshall_path_reconstruction(self):
        dist = [[float("inf") for i in range(len(self))]
                for j in range(len(self))]
        prev = [[None for i in range(len(self))] for j in range(len(self))]

        for v in self.get_vertex():
            for u in self.get_vertex():
                dist[u][v] = self[u][v]
                prev[u][v] = u

        for v in self.get_vertex():
            dist[v][v] = 0

        for k in range(len(self)):
            for i in range(len(self)):
                for j in range(len(self)):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def djiasktra_path_reconstruction(self, start: int = 0) -> dict[int:int]:
        dist = [float("inf") for i in range(len(self))]
        dist[start] = 0
        prev: dict[int:int] = dict()
        for v in self.get_vertex():
            prev[v] = None

        min_vertex = [i for i in range(len(self))]  # list of vertices
        while min_vertex:
            v = min(min_vertex, key=lambda v: dist[v])
            min_vertex.remove(v)

            for u in self.get_adjacent_vertex(v):
                e = self[v][u]  # get edge

                if u in min_vertex and e is not None and e < dist[u]:
                    dist[u] = e + dist[v]
                    prev[u] = v

        return prev

    def eulerian_cycle(self, start: int = 0) -> dict[int:int]:
        stack = [(start, None)]
        path = dict()

        while stack:
            v, used_e = stack.pop(-1)
            for u in self.get_adjacent_vertex(v):
                e = self[v][u]
                if e not in path.values():
                    stack.append((u, e))
                    path[u] = e

        return path

    """ PUBLIC """

    def get_shortest_path(self, start: int, end: int) -> list[int | None]:
        prev = self.djiasktra_path_reconstruction(start)
        if prev[end] is None:
            return [None]

        path: list[int:int] = [end]  # start from end = prev[end]
        while end := prev[end] is not None:
            path.append(prev[end])

        path.reverse()
        return path

    def get_isolated_vertex(self):
        isolated_vertecies = list()
        for i in range(len(self._out)):
            for e in self._out[i]:
                if e is not None:
                    break

            else:
                isolated_vertecies.append(i)

        return isolated_vertecies

    def isolated_vertex_print(self):
        isolated_vertices = self.get_isolated_vertex()
        if isolated_vertices:
            return str(isolated_vertices)[1:-1]
        else:
            return "There is a connected graph"

    def graph_coloring(self, start: int = 0) -> list[set[int]]:
        color_list: list[set[int]] = [None, None]

        color_list[0] = set(v for v in self.get_adjacent_vertex(start))
        color_list[1] = set(v for v in self.get_vertex()
                            if v not in color_list[0])

        i = -1  # loop start from 0
        while (i := i + 1) < len(color_list):
            color = color_list[i]
            for v in color:
                for u in self.get_adjacent_vertex(v):
                    if u in color:  # u is adjacent and same color
                        if color is color_list[-1]:  # if last color
                            color_list.append(set())

                        color_list[i + 1].add(u)  # push to the next colors

        return color_list

    def is_cut_vertex(self, vertex: int) -> bool:
        """THIS WILL AFFECT THE GRAPH, PLEASE COPY
        BEFORE USING THIS"""

        # delete the edges
        for u in self.get_adjacent_vertex(vertex):
            self[vertex][u] = None
            self[u][vertex] = None

        start: int = int()  # make sure start is not vertex
        for v in self.get_vertex():
            if v != vertex:
                start = v
                break
        else:
            return True

        closure = self.DFS_ordered(start)
        print(closure)
        if len(closure) + 1 != len(self):
            return True
        return False
