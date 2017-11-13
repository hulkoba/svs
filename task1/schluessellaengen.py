import math

keyLength = [40, 56, 64, 112, 128] # bit

#unit: check 5*10 keys per second
ASICs = 5 * 10 ** 8

# 1 mio per year
money = 1000000

# 50 euro per asic, 50 euro per integration
costPerAsic = 50 + 50


maxAsics = money / costPerAsic
#unit: keys per secons
# 5 * 10^8 * (1 mio / 100)
keysPerSecond = ASICs * maxAsics

print("2.1.1 ")
print(str(maxAsics) + " Einheiten koennen mit dem zur Verfuegung stehendem Etat parallel betrieben werden. \n")
print

print("2.1.2 ")
print("Wie lange dauert die durchschnittliche, die minimale und die maximale Schluesselsuchzeit?")

for length in keyLength:
    print("------------------------------- \n")
    print("Suchzeit bei einer Schluessellaenge von " + str(length) + " bit \n")

    maxTries = float(2 ** length)
    avgTries = float(maxTries / 2)

    maxSeconds = maxTries / float(keysPerSecond)
    avgSeconds = avgTries / float(keysPerSecond)
    minSeconds = float(1 / float(keysPerSecond))

    print "Minimal: \n    1 Versuch."
    print "    " + '{:.10f}'.format(minSeconds) + "(= einem Bruchteil einer Sekunde)  Sekunden. \n"

    print "Durchschnittlich: \n    " + '{:.0f}'.format(avgTries) + " Versuche"
    print "in  " + '{:.0f}'.format(avgSeconds) + " Sekunden."
    print "in  " + '{:.0f}'.format(avgSeconds / 60) + " Minuten."
    print "in  " + '{:.0f}'.format(avgSeconds / 60 / 60) + " Stunden."
    print "in  " + '{:.0f}'.format(avgSeconds / 60 / 60  24) + " Tagen. \n"

    print "Maximal: \n    " + '{:.0f}'.format(maxTries) + " Versuche"
    print "in  " + '{:.0f}'.format(maxSeconds) + " Sekunden."
    print "in  " + '{:.0f}'.format(maxSeconds * 60) + " Minuten."
    print "in  " + '{:.0f}'.format(maxSeconds * 60 * 60) + " Stunden."
    print "in  " + '{:.0f}'.format(maxSeconds * 60 * 60 * 24) + " Tagen. \n"

    print("2.2 (ausgehend von einmaliger Investition (1 Mrd)")
    # Das mooresche Gesetz besagt,
    # dass sich die Komplexitaet integrierter Schaltkreise mit minimalen Komponentenkosten
    # regelmaessig verdoppelt;
    # je nach Quelle werden 12 bis 24 Monate als Zeitraum genannt.
    # meistens 18 Monate

    # N(t): power after years
    # N0:   start power
    # t:    years
    # N(t) = N0 * 2^t
    # t= ln(  N(t) / N0  )  /  ln(2)

    # http://www.mathe-paradies.de/mathe/gleichungsloeser/index.htm
    # A = B * 2^X

    futureMoney = 1000000000

    # 1 Mrd / (50 + 50)
    maxAsics = float(futureMoney / costPerAsic)

    keysPerDay = ASICs * maxAsics * float(60 * 60 * 24)

    # unit: keys per second
    days = avgTries / keysPerDay  # 24h

    print("days=" + str(days))
    print("keysPerDay=" + str(keysPerDay))

    years = 0

    asictmp = ASICs
    while days > 1:
        years = years + 1.5
        asictmp = asictmp * 2
        keysPerDay = asictmp * maxAsics * float(60 * 60 * 24)
        days = avgTries / keysPerDay

    print("years=" + str(years))

    # unit: keys per second
    #requieredASICs = requieredKeysPerSecond / maxAsics

    #requieredYears = math.log(requieredASICs / ASICs) / math.log(2)

    #if requieredYears <= 0:
    #    print "hamwaschon"
    #else:
    #    print("In " + str(format(requieredYears, '.2f')) +
    #          " Jahren kann laut Moore's Law eine Maschine gebaut werden, die in 24h einen " + str(length) +
    #          " bit grossen Schluessel findet.")
