import networkx as nx
import matplotlib.pyplot as plt
import json

class Przystanek:

    def __init__(self, nazwa):
        self.nazwa = nazwa

    def __str__(self):
        return self.nazwa

with open('przystanki_0_159.json', 'r') as plik:
    przystanki = json.load(plik)

ogarniete = {klucz: (float(przystanki[klucz]['y'])*(10**6), float(przystanki[klucz]['x'])*(10**6)) for klucz in przystanki}
G = nx.Graph()
#G.add_node('kleparz')
#G.add_node('dworzec')
#G.add_node('bagatela')
#G.add_node('filharmonia')
#G.add_node('wszystkichsw')
#G.add_node('gertrudy')
#G.add_node('poczta')

#jubilat = Przystanek('jubilat')

#G.add_node(jubilat)

#G.add_edge('kleparz', 'dworzec', {'odleglosc': 422})
#G.add_edge('dworzec', 'poczta', {'odleglosc': 615})
#G.add_edge('poczta', 'gertrudy', {'odleglosc': 170})
#G.add_edge('gertrudy', 'wszystkichsw', {'odleglosc': 218})
#G.add_edge('wszystkichsw', 'filharmonia', {'odleglosc': 354})
#G.add_edge('filharmonia', 'bagatela', {'odleglosc': 531})
#G.add_edge('bagatela', 'kleparz', {'odleglosc': 585})
#G.add_edge(jubilat, 'filharmonia', {'odleglosc': 572})

G.add_nodes_from(ogarniete.keys())
for n, p in ogarniete.items():
    G.node[n]['pos'] = p
pos = nx.get_node_attributes(G, 'pos')


offset = {}
for k,v in pos.items():
     offset[k] = (v[0], v[1]-500)

plt.figure(3, figsize=(80,80))
nx.draw(G, pos, font_size=12, node_size=100)
nx.draw_networkx_labels(G, offset, font_family=('ubuntu','arial'))
#nx.draw_networkx_edge_labels(G, pos)
plt.savefig('graph.png', format='png', dpi=75)
plt.show()
