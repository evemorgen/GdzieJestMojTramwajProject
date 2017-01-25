# Usage

## PRZENIESIONE WEWNĄTRZ APKI

```
python3 przystanki.py OD DO

(ENV) [mapping_stops] python przystanki.py 50 100
[50/100] Przystanek: Os.Piastów, [x,y]
```

# Algorytm postępowania
### Przykład przeprowadzony na przystnaku np. 50 - Os. Piastów
1. Szukamy przystanku na jak dojadę
    ![img](http://i.imgur.com/ajJrcCy.png)
2. Ogarniamy gdzie znajduje się dany przystanek
    ![img](https://i.imgur.com/hG5hYfo.png)
3. Szukamy tej samej okolicy na Google Maps i zaznaczamy interesujący nas punkt
    ![img](http://i.imgur.com/xRqXloe.jpg)
4. Kopiujemy współrzędne tak jak na obrazku
    ![img](http://i.imgur.com/AA47T9b.png)
5. Wklejamy współrzędne w skrypt i naduszamy enter
    ![img](http://i.imgur.com/l9sNSbk.png)
6. Operacje powtarzamy aż do zakończenia działania skryptu, wynikiem będzie plik "przystanki_OD_DO.json" w naszym przypadku "przystanki_50_100.json"
    ![img](http://i.imgur.com/7HLnzGx.png)
