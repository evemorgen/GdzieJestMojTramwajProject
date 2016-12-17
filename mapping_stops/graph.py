import networkx as nx
import matplotlib.pyplot as plt


class Przystanek:

    def __init__(self, nazwa):
        self.nazwa = nazwa

    def __str__(self):
        return self.nazwa

G = nx.Graph()
G.add_node('kleparz')
G.add_node('dworzec')
G.add_node('bagatela')
G.add_node('filharmonia')
G.add_node('wszystkichsw')
G.add_node('gertrudy')
G.add_node('poczta')

jubilat = Przystanek('jubilat')

G.add_node(jubilat)

G.add_edge('kleparz', 'dworzec', {'odleglosc': 422})
G.add_edge('dworzec', 'poczta', {'odleglosc': 615})
G.add_edge('poczta', 'gertrudy', {'odleglosc': 170})
G.add_edge('gertrudy', 'wszystkichsw', {'odleglosc': 218})
G.add_edge('wszystkichsw', 'filharmonia', {'odleglosc': 354})
G.add_edge('filharmonia', 'bagatela', {'odleglosc': 531})
G.add_edge('bagatela', 'kleparz', {'odleglosc': 585})
G.add_edge(jubilat, 'filharmonia', {'odleglosc': 572})
pos = nx.spring_layout(G)

nx.draw(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos)
plt.show()
