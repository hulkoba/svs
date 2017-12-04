## Public-key Kryptographie

### Aufgabe 3.1: Diffie-Hellmann Schlüsselaustausch (DHKE)
Der Diffie-Hellmann Schlüsselaustausch erlaubt es, zwei Kommunikationsparteien, über einen unsicheren Kanal, einen gemeinsamen geheimen Schlüssel zu vereinbaren.
Berechnen Sie für die folgenden Beispiele die beiden öffentlichen und den mittels DHKE vereinbarten gemeinsamen geheimen Schlüssel. Verwenden Sie in allen Fällen die öffentlichen Parameter **p = 467** und **g = 2**

```
- I. 		a = 2, b = 5
- II.		a = 400, b = 134
- III.	a = 228, b = 57
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
Programmieren Sie ein `naive_dh` Programm, welches einen generischen Diffie-Hellmann Schlüsselaustausch mittels `Bade64` kodierte E-Mails implementiert.
Der so erzeugte gemeinsame geheime Schlüssel soll anschließend verwendet werden können, um verschlüsselte Nachrichten auszutauschen. Diese sollen mit Hilfe des XTEA-Algorithmus im CBC-Modus verschlüsselt werden.
Die E-Mail-Konten dürfen mit Hilfe von Dateien in einfachen Ordnern auf ihrem lokalen Dateisystem simuliert werden.