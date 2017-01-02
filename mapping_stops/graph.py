import networkx as nx
import matplotlib.pyplot as plt
import json


with open('przystanki_0_159.json', 'r') as plik:
    punkty = json.load(plik)

ogarniete = {klucz: (float(punkty[klucz]['y']) * (10**6), float(punkty[klucz]['x']) * (10**6)) for klucz in punkty}
petle = {k: v for k, v in ogarniete.items() if punkty[k]['petla'] is True}
skrzyzowania = {k: v for k, v in ogarniete.items() if punkty[k]['skrzyzowanie'] is True}
przystanki = {k: v for k, v in ogarniete.items() if punkty[k]['przystanek'] is True}

G = nx.Graph()

G.add_nodes_from(ogarniete.keys())
for n, p in ogarniete.items():
    G.node[n]['pos'] = p
pos = nx.get_node_attributes(G, 'pos')


offset = {}
for k, v in pos.items():
    offset[k] = (v[0], v[1] - 500)

plt.figure(3, figsize=(80, 80))
nx.draw_networkx_nodes(G, pos, nodelist=petle, node_color='r', node_size=200)
nx.draw_networkx_nodes(G, pos, nodelist=przystanki, node_color='b', node_size=150)
nx.draw_networkx_nodes(G, pos, nodelist=skrzyzowania, node_color='g', node_size=100)
nx.draw_networkx_labels(G, offset, font_size=12, font_family=('ubuntu', 'arial'))
plt.savefig('graph.png', format='png', dpi=75)
plt.show()
