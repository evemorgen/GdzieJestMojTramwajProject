import os
import logging
import networkx as nx
import matplotlib.pyplot as plt
import json
from geopy.distance import vincenty
from collections import deque

from db import MpkDb as DbApi
from utils import Config


def czy_skrzyzowanie(przystanek, skrzyzowania, wariant, punkty):
    for skrzyzowanie in skrzyzowania:
        if przystanek in punkty[skrzyzowanie]['between'] and wariant[1][wariant[1].index(przystanek) + 1] in punkty[skrzyzowanie]['between']:
            return skrzyzowanie
    return None


def generate_graph():
    config = Config()
    dbapi = DbApi()
    #test = Przystanki()
    linie = [str(linia) for linia in config['lines']]

    logging.info(test.petle)

    dokladne_linie = {klucz: [] for klucz in linie}
    for linia in linie:
        warianty = dbapi.get_variants_for_line(linia)
        for wariant in warianty:
            przystanki = dbapi.get_stops_for_variant(wariant)
            tupla = tuple([wariant, przystanki])
            dokladne_linie[linia].append(tupla)

    with open(os.environ['TRAM_ROOT'] + '/data/przystanki_0_159.json', 'r') as plik:
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
                ze_skrzyzowaniem = czy_skrzyzowanie(przystanek, skrzyzowania, wariant, punkty)
                if ze_skrzyzowaniem is not None:
                    kraw1 = tuple([przystanek, ze_skrzyzowaniem])
                    if kraw1 in edges:
                        edges[kraw1].append(linia)
                    else:
                        edges[kraw1] = [linia]
                else:
                    kraw = tuple([przystanek, wariant[1][wariant[1].index(przystanek) + 1]])
                    if kraw in edges:
                        edges[kraw].append(linia)
                    else:
                        edges[kraw] = [linia]

    for edge, label in edges.items():
        first = (punkty[edge[0]]['x'], punkty[edge[0]]['y'])
        second = (punkty[edge[1]]['x'], punkty[edge[1]]['y'])
        logging.info('%s - %s: %s', edge[0], edge[1], vincenty(first, second).meters)
        G.add_edge(edge[0], edge[1], linie=label, kolejka_L=deque(), kolejka_R=deque(), odleglosc=vincenty(first, second).meters)
    nx.draw_networkx_edges(G, pos)
    # nx.draw_networkx_edge_labels(G, pos)

    plt.savefig(os.environ['TRAM_ROOT'] + '/data/graph.png', format='png', dpi=75)
    nx.write_yaml(G, os.environ['TRAM_ROOT'] + '/data/graph.yaml')
