import time

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import plotly.express as px
import geopandas as gpd
import contextily as cx


class Vertex:
    def __init__(self, name="", latitude=0, longitude=0, country="", size=2):
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.country = country
        self.adjacency_list = {}
        self.size = size
        self.g = float(0)
        self.h = float(0)
        self.f = float(0)
        self.parent = ""


    def get_neighbours(self):
        return self.adjacency_list.keys()

    def new_path(self, target):
        self.adjacency_list[target.name] = heuristic(self, target)

    def del_path(self, target):
        del self.adjacency_list[target]


def heuristic(vertex, target):
    dx = target.longitude - vertex.longitude
    dy = target.latitude - vertex.latitude
    h = (dx*dx + dy*dy)**0.5
    return h


def new_path(vertex, target):
    vertex.new_path(target)
    target.new_path(vertex)


if __name__ == "__main__":
    graph = {}
    with open("book2.csv", 'r', encoding="utf-8-sig") as f:
        for line in f:
            line = line.split(",")
            if int(line[0]) > -5:
                graph[line[1]] = Vertex(name=line[1], longitude=line[4].strip("\n"),
                                        latitude=line[3], country=line[2], size=int(line[0]))


for city in graph:
    for target_city in graph:
        if target_city == city:
            pass
        elif heuristic(graph[city], graph[target_city]) < 1:
            new_path(graph[city], graph[target_city])
        elif ((graph[city].size > 6) and (graph[target_city].size > 6)):
            new_path(graph[city], graph[target_city])

for city in graph:
    if len(graph[city].adjacency_list.keys()) == 0:
        min = 99999999
        closest = "null"
        for target_city in graph:
            if target_city == city:
                pass
            else:
                h = heuristic(graph[city], graph[target_city])
                if h < min:
                    min = h
                    closest = target_city
                else:
                    pass
        new_path(graph[city], graph[closest])


df = pd.read_csv("book2 - Copy.csv")
df_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(
    df.longitude, df.latitude
))
fig, ax = plt.subplots(figsize=(8, 8))
padding = 1
plt.ylim(df_geo['latitude'].min() - padding, df_geo['latitude'].max() + padding)
plt.xlim(df_geo['longitude'].min() - padding, df_geo['longitude'].max() + padding)


for city in graph:
    plt.annotate(city, [graph[city].longitude, graph[city].latitude], fontsize=7, color="white",
                 path_effects=[pe.withStroke(linewidth=1, foreground="grey")])

for city in graph:
    for neighbour in graph[city].get_neighbours():
        x1 = graph[neighbour].longitude
        x2 = graph[city].longitude
        y1 = graph[neighbour].latitude
        y2 = graph[city].latitude
        plt.plot([x1, x2], [y1, y2], color="blue", linewidth=1)

df_geo.plot(ax=ax, alpha=1, color="red", marker='o', markersize=2)
cx.add_basemap(ax, crs="epsg:4326", source=cx.providers.NASAGIBS.BlueMarble, zoom=5)



def astar(graph, start="Plymouth", end="Tralee"):
    """Initialize both open and closed list
let the openList equal empty list of nodes
let the closedList equal empty list of nodes"""
    start = start
    end = end
    open_list = []
    closed_list = []
    current_node = start

    #add the start node. put the startnode on the openlist (leave its f at zero)
    open_list.append(start)
    #loop until you find the end. while the openlist is not empty.
    count = 0
    while len(open_list) > 0:

        #print(f"count {count} ____________")
        # find the lowest total cost and make that the current node
        current_node = open_list[0]
        current_index = 0

        for index, item in enumerate(open_list):
            count += 1
            #print(current_node, graph[item].f, graph[current_node].f)
            if graph[item].f < graph[current_node].f:
                current_node = item
                current_index = index
        #print("___current node____", current_node)

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        #open_list is where we currently are. If we try to open something on the closed menu,
        #we know the current way isn't the best way to get to that node.

        #closed list is where we have been before
        closed_list.append(current_node)
        #print("post append", current_node, open_list, closed_list)
        # Found the goal
        path = [end]
        if current_node == end:
            print("END FOUND")
            current_node = end
            print(graph[end].f)
            while current_node != start:
                count += 1
                f = 999

                city = ""
                #time.sleep(1)
                #print(f"\n {current_node}")
                #print(closed_list)
                #print(open_list)

                for neighbour in graph[current_node].get_neighbours():
                    count += 1
                    #print(neighbour, graph[neighbour].f)
                    if neighbour not in path:
                        if neighbour in closed_list:
                            if graph[neighbour].f < f:
                                city = neighbour
                                f = graph[neighbour].f
                                path.append(city)
                                current_node = city
                #print(path)

            return path

        # Loop through children
        for child in graph[current_node].get_neighbours():
            count += 1
            #print("_______")
            # continue if Child is on the closed list
            if child in closed_list:
                continue

            # if open or not yet seen
            # Create the f, g, and h values

            new_g = graph[current_node].g + heuristic(graph[child], graph[current_node])
            new_h = heuristic(graph[child], graph[end])
            new_f = new_g + new_h

            #print("calc", current_node, child, "total", graph[child].f, "start-curr", graph[child].g, "start-end", graph[child].h)

            # Child is open
            if child in open_list:
                #print("location match", child, open_list)
                if graph[child].g > new_g:
                    print("better route to that city found", current_node, child, new_g, graph[child].g)
                    #TODO update previous path steps as well as just the first city
                    graph[child].g = new_g
                    graph[child].h = new_h
                    graph[child].f = new_f

                else:
                    #print("superior route not found", child, new_g, graph[child].g)
                    continue
            else:
                graph[child].g = new_g
                graph[child].h = new_h
                graph[child].f = new_f



            # Add the child to the open list
            open_list.append(child)
            #print(open_list)
    print(count)

path = astar(graph)

print(path)

for city in graph:
    for neighbour in graph[city].get_neighbours():
        x1 = graph[neighbour].longitude
        x2 = graph[city].longitude
        y1 = graph[neighbour].latitude
        y2 = graph[city].latitude
        plt.plot([x1, x2], [y1, y2], color="blue", linewidth=1)

for road in range(len(path)-1):
    x1 = graph[path[road]].longitude
    y1 = graph[path[road]].latitude
    x2 = graph[path[road+1]].longitude
    y2 = graph[path[road+1]].latitude
    plt.plot([x1, x2], [y1, y2], color="green", linewidth=2)

plt.show()

""" REFERENCES
https://www.youtube.com/watch?v=5G-1k4CNChI
https://xyzservices.readthedocs.io/en/stable/gallery.html
https://epsg.io/?q=3857
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
https://plainenglish.io/blog/a-algorithm-in-python
"""
