from collections import deque

from mesh import Mesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
FPS = 500
AXIS_SHOW = 'off'


# hold_on之后不允许进行图像的修改，
def hold_on():
    plt.show()


class Graph(Mesh):
    def __init__(self):
        super().__init__()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        plt.axis(AXIS_SHOW)
        self.ax.view_init(elev=-87, azim=-95)

    def read_file(self, file_path):
        super(Graph, self).read_file(file_path)
        self.edges_init()
        self.net_init()

    def draw_by_steps(self, faces):
        faces_portion = []
        for index in range(len(faces)):
            faces_portion.append(faces[index].location)
            if index % FPS == 0:
                self.add_face(faces_portion, edge_color='g')
                faces_portion = []
                plt.pause(0.0001)

    def draw(self, vertices):
        faces = []
        appended = {}
        for vertex in vertices:
            related_face = [face for face in vertex.related_faces]
            for face in related_face:
                try:
                    appended[face]
                    continue
                except:
                    faces.append(face)
                    appended[face] = True
        # print(len(faces))
        self.draw_by_steps(faces)

    def add_face(self, faces, edge_color, face_color='b', alpha=1):
        collection = Poly3DCollection(faces, linewidths=1)
        collection.set_edgecolor(edge_color)
        collection.set_facecolor(face_color)
        collection.set_alpha(alpha=alpha)
        self.ax.add_collection3d(collection)

    def draw_by_one_step(self):
        faces_location = [face.location for face in self.faces]
        self.add_face(faces_location, edge_color='g')

    def draw_edge(self, point, color='r'):
        vertex = self.get_vertex(vertex_id=point)
        print(vertex)
        faces = [face.location for face in vertex.related_faces]
        print(faces)
        # face_index = self.vertices_index[point]
        # # debugging
        # print(face_index)
        # faces = [self.faces[index] for index in face_index]
        self.add_face(faces, edge_color=color, alpha=1, face_color='g')
        pass

    def draw_neighbors(self, point):
        first_neighbors = self.vertices[point].get_first_neighbors()
        for neighbor in first_neighbors:
            self.draw_edge(neighbor.get_vertex_id())

    def get_adjacent_point(self, point):
        face_index = self.vertices_index[point]
        vertices = [self.faces_index[index] for index in face_index]
        vertices = list(map(lambda x: x.pop(x.index(point)), vertices))

        print(vertices)

    def add_comment(self, point, text='·', color='r'):
        assistant_points = [
            [x, y, z]
            for x in range(2)
            for y in range(2)
            for z in range(2)
        ]
        location = self.vertices[point].axis
        px, py, pz = location
        print(location)
        # self.ax.scatter(location[0], location[1], location[2])
        self.ax.text(px, py, pz, text, color=color)
        for assistant_point in assistant_points:
            xs, ys, zs = list(zip(assistant_point, location))
            print(xs)
            self.ax.plot(xs, ys, zs, color='r')
        # self.ax.text(location[0], location[1], location[2], text,color)
        # self.ax.plot([beg[0], end[0]], [beg[1], end[1]], [beg[2], end[2]], color='r', linewidth=10.0)

        # plt.show()
        # colors = ['w'] * len(faces)
        # collection.set_edgecolor(colors)
        # collection.set_facecolor('white')

        # def update(frame):
        #     colors[frame] = 'r'
        #     collection.set_edgecolor(colors)
        #     return collection,

        # anim = FuncAnimation(self.fig, update, frames=len(faces), blit=False, interval=100)
        # anim.save("a.gif")
    # 改变边的颜色并显示动画
    #     for i in range(len(faces)):  # 设置所有边为黑色
    #         colors[i] = 'r'  # 更改特定边的颜色为红色
    #         collection.set_edgecolor(colors)
    #         plt.pause(0.01)  # 显示0.5秒的间隔

    def iterative_dfs(self, start_id):
        # self.find_all_first_neighbors()
        visited = [False] * self.vertices_count
        stack = []
        dfs_sequence = []

        stack.append(self.get_vertex(start_id))

        while stack:
            node = stack.pop()
            node_id = node.get_vertex_id()

            if not node.get_first_neighbors():
                self.find_first_neighbors(node_id)
            if not visited[node_id]:
                visited[node_id] = True
                dfs_sequence.append(node)

            for neighbor in node.get_first_neighbors():
                if not visited[neighbor.get_vertex_id()]:
                    stack.append(neighbor)

        return dfs_sequence

    def bfs(self, start_id):
        visited = [False] * self.vertices_count
        queue = deque()
        bfs_sequence = []

        queue.append(self.get_vertex(start_id))
        visited[start_id] = True

        while queue:
            node = queue.popleft()
            bfs_sequence.append(node)

            if not node.get_first_neighbors():
                self.find_first_neighbors(node.get_vertex_id())

            for neighbor in node.get_first_neighbors():
                neighbor_id = neighbor.get_vertex_id()
                if not visited[neighbor_id]:
                    queue.append(neighbor)
                    visited[neighbor_id] = True

        return bfs_sequence
