import json
import sys

przystanki = ['Fabryczna', 'Cystersów', 'Norymberska', 'Politechnika', 'Dworcowa', 'Smolki', 'Prokocim Szpital', 'Kopiec Wandy', 'Stradom', 'Teatr Bagatela', 'Dworzec Główny Tunel', 'Cmentarz Podgórski', 'DH Wanda', 'Bieżanowska', 'Plac Centralny im. R.Reagana', 'TAURON Arena Kraków Wieczysta', 'Limanowskiego', 'Uniwersytet Jagielloński', 'Os.Złotego Wieku', 'Ofiar Dąbia', 'Filharmonia', 'Rondo Grzegórzeckie', 'Brama nr 4', 'Nowy Bieżanów', 'Kurdwanów', 'Korona', 'Rzemieślnicza', 'Os.Zgody', 'Biprostal', 'Plaza', 'Reymana', 'Rondo Matecznego', 'Batorego', 'Komorowskiego', 'Kleeberga', 'Jeżynowa', 'Borek Fałęcki', 'Lipińskiego', 'Bratysławska', 'Solvay', 'Plac Wszystkich Świętych', 'Mały Płaszów', 'Wiadukty', 'Centrum Kongresowe ICE', 'Jubilat', 'Szwedzka', 'Stary Kleparz', 'Kampus UJ', 'Powstańców Wielkopolskich', 'Agencja Kraków Wschód', 'Os.Piastów', 'Łagiewniki ZUS', 'Głowackiego', 'Salwator', 'Rondo Kocmyrzowskie im. Ks. Gorzelanego', 'Kapelanka', 'M1 Al. Pokoju', 'Rondo Czyżyńskie', 'Bieńczycka', 'Lipska', 'Koksochemia', 'Gromadzka', 'Teatr Variété', 'Rzebika', 'Cracovia', 'Teatr Ludowy', 'Suche Stawy', 'Czyżyny', 'Pleszów', 'Kobierzyńska', 'Sanktuarium Bożego Miłosierdzia', 'Miśnieńska', 'Plac Wolnica', 'Łagiewniki', 'Orzeszkowej', 'Borsucza', 'Brama nr 5', 'Piaski Nowe', 'Meksyk', 'Lubicz', 'Św.Gertrudy', 'Wawel', 'Kuklińskiego', 'Os.Na Skarpie', 'Wańkowicza', 'Stella-Sawickiego', 'Dauna', 'Hala Targowa', 'Elektromontaż', 'Rondo Piastowskie', 'Mrozowa', 'Rondo 308. Dywizjonu', 'Mistrzejowice', 'Cienista', 'Oleandry', 'Bronowice', 'Cmentarz Rakowicki', 'Chmieleniec', 'Krowodrza Górka', 'Nowy Kleparz', 'Uniwersytet Pedagogiczny', 'Borek Fałęcki I', 'Centralna', 'Dworzec Główny Zachód', 'Białucha', 'Klasztorna', 'Cichy Kącik', 'Bardosa', 'Darwina', 'Klimeckiego', 'Pędzichów', 'Grota-Roweckiego', 'Park Jordana', 'Wesele', 'Dworzec Płaszów Estakada', 'Św.Wawrzyńca', 'Dunikowskiego', 'Dworzec Towarowy', 'Teligi', 'Brożka', 'Urzędnicza', 'Nowy Prokocim', 'Ćwiklińskiej', 'Nowosądecka', 'Bronowice Małe', 'Piasta Kołodzieja', 'Starowiślna', 'Os.Kolorowe', 'Balicka Wiadukt', 'Ruczaj', 'Walcownia', 'Muzeum Lotnictwa', 'AWF', 'Dworzec Główny', 'Plac Bohaterów Getta', 'Słomiana', 'Uniwersytet Ekonomiczny', 'Rondo Mogilskie', 'Plac Inwalidów', 'Rondo Hipokratesa', 'TAURON Arena Kraków Al. Pokoju', 'Struga', 'Dąbie', 'Prokocim', 'Miodowa', 'Zabłocie', 'Czerwone Maki P+R', 'Szpital Narutowicza', 'Zajezdnia Nowa Huta', 'Blokowa', 'Francesco Nullo', 'Poczta Główna', 'Rakowicka', 'Wlotowa', 'Wzgórza Krzesławickie', 'Jarzębiny', 'Kabel', 'Kombinat', 'Witosa']

linie = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
"16", "18", "19", "20", "21", "22", "23", "24", "50", "52", "62", "64", "69"
}
przystanki = list(przystanki)
przystanki = przystanki[int(sys.argv[1]):int(sys.argv[2])]

przystanki_dict = dict()

i = int(sys.argv[1])
maxa = int(sys.argv[2])

for przy in przystanki:
    combined = input('[%s/%s] Przystanek: %s, [x,y] ' % (i,maxa,przy))
    x = combined.split(',')[0]
    y = combined.split(',')[1]
    przystanki_dict[przy] = {'x': x, 'y': y, 'on_demand': False}
    i += 1

with open('przystanki_%s_%s.json' % (sys.argv[1], sys.argv[2]), 'w') as plik:
    json.dump(przystanki_dict, plik)
