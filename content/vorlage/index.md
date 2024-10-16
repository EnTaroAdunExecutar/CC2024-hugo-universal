+++
# Dies ist ein Kommentar innerhalb der +++ Sektion die von Hugo interpretiert wird - hier steht kein Text der nachher Kontent ist

title = 'Titel eines Artiekls welcher in der Übersicht angezeigt wird'
# Zeitstempel für den Artiekl --> Vorsicht - falls dieser in der Zukunft liegt wird der Artiekl nicht beim Build-Prozess berücksichtigt. Im Konkreten Fall --> 15.07.2024
date = "2024-07-15T03:23:19+02:00"
summary = "Zusammenfassung des Artikels"
# daraus wird ein Link erzeugt der auf eine dedizierte Seite zeigt wo wir Infos über einen Autor haben können
authors = ["Pasi Echner"]
# rechts neben dem Artikel werden alle Tags aller Artiekl angezeigt - das kann man als Suche verwenden um z.B. alle Artiekel mit dem U-Boot 17 oder zum Stadtradeln 2024 zu finden --> hier sollten wir nicht zu viele Tags einführen und uns eine gewisse Struktur gönnen
tags = ["Stadtradeln-2024"]

# Bild welches unter den "Aktuellen Artikeln" angezeigt wird. Das Bild muss allerdings unter /static/Bilder/<<bild>> existieren
banner = "Bilder/logo-stadtradeln.png"
# bei draft = true wird der Build-Prozess die Datei nicht berücksichtigen
draft = false

+++

Ab hier wird der Text wirklich angezeigt. Ich verwende den Text zur Erklärung bzw. um eine Art Spickzettel für Markdown zu erzeugen.

Wieso Markdown? Markdown ist eine Auszeichnungssprache, soll heißen im Vergleich zu Word welches proprietär Spezialzeichen verwendet um z.B. einen Text Fett zu machen -> was im Kontext einer Homepage erst übersetzt werden muss, macht man es mit Markdown explizit, siehe Beispiele unten. Dies hat den Vorteil das man unabhängig von einem Hersteller ist "fast" beliebige Software verwenden kann. Das Tooling welches ich für die HP verwende nutzt ebenfalls markdown als Input.

Wie habe ich versucht etwas Struktur in die Artiekl zu bekommen?  
Prinzipiell liegen alle Artikel im Ordner "posts" - in welchem ich einen Unterordner "2024" angelegt habe - nächstes Jahre dann "2025" usw... Wir können gerne diskutieren ob wir weitere Strukturen wie Monate oder Quartale benötigen.

Vorgehen:

1. Neuen Unterordner anlegen -> /content/posts/2024/<<neuer_ordner>>
2. /vorlage/<<index.md>> in den /content/posts/2024/<<neuen ordner>> kopieren
3. Bilder ebenfalls in /content/posts/2024/<<neuen ordner>> kopieren
4. neuer_ordner/<<index.md>> editieren wie man möchte und Bilder verlinken
5. (lokal testen mit vscode und hugo z.B.?)
6. Auf Github pushen (speichern) damit es nach erfolgreichem Build-Prozess live ist

Normaler Text wird so dargestellt wie eingegeben.

Eine Leerzeile erzeugt einen Absatz.

Zwei oder mehr Leerzeichen am Ende der Zeile  
erzeugen einen Zeilenumbruch.

## Dies ist eine Überschrift --> Level 2 - bisher hab ich das als Top-Level Überschrift verwendet

### Dies ist ebenfalls eine Überschrift --> Level 3 - hab ich bisher in einem Artiekl zur Gruppierung verwendet

Dies ist normaler Text.
Ein normaler Umbruch sort nicht dafür das eine neue Zeile begonnen wird, dafür muss eine dedizierte Zeile eingefügt werden. 

siehe hier!

So kann ein Bild eingefügt werden --> das Bild muss im gleichen Verzeichnis liegen wie die markdown-Datei selbst. Bei diesem Script (ähnlich zu einem Excel-Makro) muss man den Bildname - hier "Picture2.jpg", die Bildgröße - hier "resize 600x" mit einer breite von 600 Pixeln, und einen Text der im Fehlerfall wenn das Bild nicht angezeigt werden kann angezeigt wird. Zusätzlich entfernt der Script alle EXIF metainformationen.

{{< imgprocess "Picture2.jpg" "resize 600x" "Gipfel" >}}

> Diese spezielle Formatierung nutze ich als Unterschrift für Bilder

**So kann man fette Schrift erzeugen**

*So kann man kursive Schrift erzeugen*

~~durchgestrichener Text~~

Dies ist eine Bullet-Punkt-liste:

- Bullet-Punkt abc
- Bullet-Punkt xyz
  - Unterpunkt von xyz
    - Jetzt wird es aber crazy
  - Noch ein Unterpunkt von xyz
- Bullet-Punkt hugo

Dies ist eine Aufzählung:

1. Punkt 1
2. Punkt 2
3. Punkt 3

`So kann ich Code anzeigen lassen`

Dies ist ein Satz mit Fußnote. [^1]

So kann ich einen Link in Text integrieren --> der folgende Link soll auf Ecosia.de zeigen [Ecosia.de](https://www.ecosia.de) - die nachhaltige Google-Alternative.

So kann ich eine Mail integrieren [info@irgendwas.de](mailto:info@irgendwas.de)

So kann ich einen anruf integrieren [anrufen](tel:+490151123456789)

==> in beiden Fällen mail und telefon wär ich eher vorsichtig - es gibt genug Leute die Homepages mit scripten scannen und man dann Spam ohne Ende hat. 

[^1]: Dies ist die Fußnote

Dies ist eine To-Do-Liste:

- [x] Tour planen
- [ ] Tour durchführen
- [ ] krassen Artiekl schreiben
