# rijmparen.py

import rijmwoord
from collections import defaultdict

def list_to_dict(lst):
    frequency_dict = defaultdict(int)
    for item in lst:
        frequency_dict[item] += 1
    return dict(frequency_dict)


def last_word(line):
    if not len(line.split()): return ""
    return ("".join((char if char.isalpha() else "") for char in line.split()[-1])).lower()

def begin_gedicht(line):
    return (line[-3:]=='xml')

def end_gedicht(line):
    return (line[:2]=='--')

def gedichten(text):
    gedichten = []
    gedicht = []
    gaande = False
    for line in text:
        line = line.strip()
        if begin_gedicht(line): 
            gedicht = []
            gaande = True
        elif end_gedicht(line):
            if (gaande):
                gedichten.append(gedicht)
                gaande = False
        else: 
            if (gaande) and line != '':
                gedicht.append(line)
    gedichten.append(gedicht)
    return gedichten

def geef_rijmen(gedicht):
    rijmen = []
    for line in gedicht:
        lw = last_word(line)
        if lw in rijmwoord.hulprijmwoordenboek:
            rijmen.append((lw,rijmwoord.hulprijmwoordenboek[lw]))
        else:
            rijmen.append(())
    return rijmen

def maak_rijmvormen(gedichten):
    rijmvormen = []
    for gedicht in gedichten:
        rijmvormen.append(geef_rijmen(gedicht)) 
    return rijmvormen

def maak_rijmwb(rijmvormen):
    woordenboek = {}
    for gedicht in rijmvormen:
        for line in gedicht:
            if len(line) > 1:
                if line[1] in woordenboek:
                    woordenboek[line[1]].append(line[0])
                else: woordenboek[line[1]] = [line[0]]
    for klank in woordenboek:
        woordenboek[klank] = list_to_dict(woordenboek[klank])
    return woordenboek

def maak_rijmparen (rijmvormen, rijmwb):
    def voeg_toe(rd):
        lijst = []
        for r in rd:
            if len(rd[r]) > 2:
                for i in range(len(rd[r])-1):
                    lijst.append(rd[r][i:i+2])
            elif len(rd[r]) == 2:
                lijst.append(rd[r])
        return lijst
    rijmfrequentie = {}
    rijmparen = []
    for r in rijmwb:
        for item in rijmwb[r]:
            rijmfrequentie [item] = rijmwb[r][item]
    for rv in rijmvormen:
        rd = {}
        for r in rv:
            if len (r) > 1:
                entry = rijmfrequentie[r[0]]
                if r[1] in rd:
                    rd[r[1]].append (entry)
                else: rd[r[1]] = [entry]
        rijmparen += voeg_toe(rd)
    return rijmparen

def verdeel(rijmparen):
    stijgend, gelijk, dalend = 0, 0, 0
    for rp in rijmparen:
        if rp[0] < rp[1]:
            stijgend += 1
        elif rp[0] > rp[1]:
            dalend += 1
        else: gelijk += 1
    return stijgend, gelijk, dalend

def verschil(rijmparen):
    totaal = 0
    i = 0
    for rp in rijmparen:
        i += 1
        totaal += rp[0]-rp[1]
    return i, totaal

with open("gedichten.txt", "r") as book:
    text = book.readlines() # verzameling regels
    gedichten = gedichten(text) # de tekst opgedeeld in gedichten, die ieder een lijst van regels zijn
    rijmvormen = maak_rijmvormen(gedichten) # in ieder van de gedichten geven we alleen het laatste woord van een regel en de rijmklank, als we die kunnen vinden
    rijmwb = maak_rijmwb(rijmvormen)
    rijmparen = maak_rijmparen(rijmvormen, rijmwb)
    stijgend, gelijk, dalend = verdeel(rijmparen)
    totaal = stijgend + gelijk + dalend
    print (stijgend / totaal, gelijk / totaal, dalend / totaal)
