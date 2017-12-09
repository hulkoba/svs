## Public-key Kryptographie

### Aufgabe 3.1: Diffie-Hellmann Schlüsselaustausch (DHKE)
Der Diffie-Hellmann Schlüsselaustausch erlaubt es, zwei Kommunikationsparteien, über einen unsicheren Kanal, einen gemeinsamen geheimen Schlüssel zu vereinbaren.
Berechnen Sie für die folgenden Beispiele die beiden öffentlichen und den mittels DHKE vereinbarten gemeinsamen geheimen Schlüssel. Verwenden Sie in allen Fällen die öffentlichen Parameter **p = 467** und **g = 2**

```
- I. 		a = 2, b = 5
- II.		a = 400, b = 134
- III.		a = 228, b = 57
```

### Aufgabe 3.2 RSA
Verschlüsseln Sie zunächst die Nachricht m = 9 mit den RSA-Parametern
p = 5, q = 11, e = 3
und berechnen Sie anschließend den zugehörigen privaten Schlüssel um die Nachricht wieder zu entschlüsseln.

### Aufgabe 3.3 RSA-Exponenten
Gegeben seien die Primzahlen *p = 41 und q = 17*.

- Welche der Zahlen *e1 = 32 und e2 = 39* ist als öffentlicher RSA-Exponent geeignet?
- Berechnen Sie den privaten Exponenten mit Hilfe des erweiterten euklidischen Algorithmus

### Aufgabe 3.4 Schlüsselaustausch Protokoll
Programmieren Sie ein (Python-)Script mit dem Namen `naive_dh`, welches einen generischen Diffie-Hellmann Schlüsselaustausch mittels Base64 kodierter E-Mails implementiert. Der vereinbarte gemeinsame Schlüssel soll anschließend verwendet werden können, um Nachrichten auszutauschen die mittels XTEA im CFB-Mode verschlüsselt wurden.

*Senden:*
```
naive_dh.py -s -k xtea_password -m my_friend@mail.de "Hey, wie geht es dir?"
```

*Empfangen:*
```
naive_dh.py -r -k xtea_passwortd
```

Ausgabe (Wiederhergestellter Originaltext): 
``` 
my_other_friend@mail:   Hey, wie geht es dir? 
```

*Hinweise:*
- Die E-Mails und E-Mail-Konten dürfen mit Hilfe von einfachen TextDateien und einer simplen Ordnerstruktur auf ihrem lokalen Dateisystem simuliert werden.
- Der Schlüsselaustausch sollte pro Partei nur einmal erfolgen. Alle folgenden Nachrichten sollten das selbe initial ausgemacht Passwort verwenden.
- Die Base-64 Kodierung sollten Sie nur auf die Daten anwenden die Sie schlussendlich per E-Mail versenden. Die ganzen Berechnungen müssen Sie weiterhin auf Bit bzw. Byte-Ebene durchführen. D.h. sie müssen beim Einlesen der E-Mails die Informationen auch wieder zurückkonvertieren. Das ermöglicht es den Inhalt der Nachrichten anfangs auch per Copy&Paste in die Kommandozeile einzufügen und zu verhindern, dass unsichtbare, nicht menschenlesbare Zeichen in den E-Mails enthalten sind. Dies gilt sowohl für die Nachrichten des Schlüsselaustausches, als auch für die verschlüsselten Nachrichten.
