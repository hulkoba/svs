import math

keyLength = [40, 56, 64, 112, 128]

#unit: keys per second
ASICs = 5 * 10 ** 8

money = 1000000

costPerAsic = 50 + 50

maxAsics = float(money / costPerAsic)

#unit: keys per secons
keysPerSecond = ASICs * maxAsics

print("2.1.1 ")
print(str(maxAsics) + " Einheiten koennen mit dem zur Verfuegung stehendem Etat patallel betrieben werden. \n")


print("2.1.2 ")
print("Wie lange dauert die durchschnittliche, die minimale und die maximale Schluesselsuchzeit?")

for length in keyLength:
	print("------------------------------- \n")
	print("Suchzeit bei einer Schluessellaenge von " + str(length) + " bit \n")
	print("Mindestens 1 Versuch.")


	maxTries = float(2 ** length)
	avgTries = float(maxTries / 2)

	maxSeconds = maxTries / float(keysPerSecond)
	avgSeconds = avgTries / float(keysPerSecond)

	print("Durchschnittlich " + str(avgTries) + " Versuche in " + avgSeconds)
	print("Maximal " + str(maxTries) + " Versuche in " + maxSeconds)

	print("\n")


	print("2.2")
	futureMoney = 1000000000
	maxAsics = float(futureMoney / float(costPerAsic))

	#unit: keys per second
	requieredKeysPerSecond = avgTries / float(60*60*24)
	#unit: keys per second
	requieredASICs = requieredKeysPerSecond / maxAsics


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

	#http://www.mathe-paradies.de/mathe/gleichungsloeser/index.htm
	#A = B * 2^X

	requieredYears = math.log(requieredASICs/ASICs) / math.log(2)

	if requieredYears <= 0:
		print("Hamwaschon!")
	else:
		print("In " + str(format(requieredYears, '.2f')) +
			" kann laut Moore's Law eine Maschine gebaut werden, die in 24h einen " + str(length) +
			" bit grossen Schluessel findet.")
