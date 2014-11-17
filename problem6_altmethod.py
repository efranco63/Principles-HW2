import sys
import csv
csvData = csv.DictReader(open(sys.argv[1]))
agencyDict = {}
for t in csvData:
    if t['Agency'] != '' and t['Incident Zip'] != '':
        if t['Agency'] in agencyDict.keys():
            agencyDict[t['Agency']].append(t['Incident Zip'])
        else:
            agencyDict[t['Agency']] = [t['Incident Zip']]
agencyList = agencyDict.keys()
agencyList.sort()