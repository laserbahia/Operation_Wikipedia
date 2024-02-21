# Operation_Wikipedia
Wikipedia Graph Project by Levi Weber and Cedric Kaufmann

Disclaimer bevore using the programm: 
You might receive the error, that the files you need to load aren't findable (the directory you trying to open is not existent). If this error occurs to you, you need to either remove all the main/ statements from where the files get loaded in or add the main/ statement into every file path that gets loaded in. 
For example:
with io.open("main/txt_files/article_to_be_searched.txt", "r") as f1: 
If the error occurs in this state, you need to change it to the following: 
with io.open("txt_files/article_to_be_searched.txt", "r") as f1.
and the other way around.

The following lines indicate where to find the loading lines of code in the corresponding file:
Main.py : 
- lines: 73, 85, 91, 95

gui_v5.py:
- lines: 17, 25, 27, 30, 33, 92


Programmiert wird ein kleines Python Tool, welches folgende Anforderungen erfüllt:
a)	Der Benutzer kann einen Wikipedia-Artikel eingeben (im Code) ✅

b)	Das Tool sucht nach den verlinkten Artikel dieses Artikels ✅

c)	Man kann im Code festlegen, wie gross der Graph sein soll – d.h. wie viele «hops» Distanz ✅

d)	Die Verwebungen der gefundenen Artikel untereinander werden dabei auch angezeigt ✅

e)	Graphische Darstellung dieses Graphen ✅

f)	Begrenzung in der Anzahl verlinkter Artikel ✅

Zusätzliche Funktionalitäten

g)	Suchfeld für dynamische Suche nach neuen Artikeln (ohne es im Code anzupassen) ✅

h)	Verbunden Artikel wieder untereinander verbinden ? ✅

i)	Speicherung als Bild (SVG?) ✅

Unspezifische Grundanforderungen 

j)	Fehlerhafte Eingaben werden abgefangen und der Benutzer wird aufgefordert, sich zu korrigieren («Ungültige Eingabe, bitte Eingabe nochmals wiederholen») ✅

k)	Das Tool führt das Spiel aus, und kehrt dann wieder zum Menü zurück ✅

l)	Man muss nach der Benutzung des Programms entweder weiterfahren können oder aufhören (z.B. wenn «q» gedrückt wird, endet das Programm) ✅

m)	Beim Beenden des Programms verabschiedet sich dieses und zeigt an, wie lange das Programm benutzt wurde und wie oft welche Funktion verwendet wurde. Finde heraus wie man das mit Python macht. Tip: import time() Funktion time.time(). 😔 nicht geschafft
 
Code Qualität

n)	Verwendet für euren Code Variablennamen, welche jeweils dasjenige bezeichnen was sie beinhalten. Dadurch wird euer Code einfacher zu lesen sein. 

o)	Verwendet wo möglich Schleifen, um repetitiven Code zu vermeiden – so lässt sich der Code einfacher lesen und abändern

p)	Verwendet wo möglich Funktionen, um repetitiven Code zu vermeiden.

q)	Achtet auf korrekte Einrückung

r)	Strukturiert euren Code und fügt jeweils Kommentare hinzu, um das Lesen des Codes zu erleichtern. Nicht jede einzelne Zeile muss einen Kommentar haben, aber sicher dort wo etwas «neues» gemacht wird.



