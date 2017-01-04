import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
import sqlite3

db_connection = sqlite3.connect('/Users/evemorgen/Dropbox/projekty/GdzieJestTenCholernyTramwajProject/backend/schedule_worker/data/baza.ready.zip')
cursor = db_connection.cursor()

linie = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "16", "18", "19", "20", "21", "22", "23", "24", "50", "52", "62", "64", "69" ]

dokladne_linie = {klucz: [] for klucz in linie}
for linia in linie:
    query = """
            select id
            from Variants
            where SheduleId = (
                select ID
                from Shedules
                where LineName = %s
                order by LastUpdate DESC
                limit 1
            ) and "Default" = 1
            """
    cursor.execute(query % linia)
    warianty = [tupel[0] for tupel in cursor.fetchall()]
    for wariant in warianty:
        query = """
                select No, StopName
                from routes
                where VariantId = %s
                """
        cursor.execute(query % wariant)
        przystanki = [tupel[1] for tupel in cursor.fetchall()]
        tupla = tuple([wariant, przystanki])
        dokladne_linie[linia].append(tupla)


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
nx.draw_networkx_nodes(G, pos, nodelist=przystanki, node_color='b', node_size=150)
nx.draw_networkx_nodes(G, pos, nodelist=skrzyzowania, node_color='g', node_size=100)
nx.draw_networkx_nodes(G, pos, nodelist=petle, node_color='r', node_size=200)
nx.draw_networkx_labels(G, offset, font_size=12, font_family=('ubuntu', 'arial'))

edges = {}
for linia in linie:
    for wariant in dokladne_linie[linia]:
        for przystanek in wariant[1][:-1]:
            kraw = tuple([przystanek, wariant[1][wariant[1].index(przystanek)+1]])
            if kraw in edges:
                edges[kraw].append(linia)
            else:
                edges[kraw] = [linia]

for edge, label in edges.items():
    G.add_edge(edge[0], edge[1], linie=label)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos)

plt.savefig('graph.png', format='png', dpi=75)
plt.show()

with open('graph.json', 'w') as plik:
    json.dump(json_graph.node_link_data(G), plik)
