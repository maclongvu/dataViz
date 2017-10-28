import csv
import json

def parsedatafile(filename):
    idscore = {}
    linkList = []
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)

        count = 0
        for row in csvreader:
            # skip 2000 earlier data
            if count < 35350:
                count = count + 1
                continue

            fromNode = row[0]
            toNode = row[1]
            score = int(row[2])

            linkList.append((fromNode, toNode, score))

            if toNode in idscore:
                idscore[toNode] = idscore[toNode] + score
            else:
                idscore[toNode] = score

            if fromNode not in idscore:
                idscore[fromNode] = 0

            count = count + 1

    return (idscore, linkList)

(idScore, dirList) = parsedatafile('soc-sign-bitcoinotc.csv')


# print (idScore)
# print (len(dirList))
# print (len(idScore))
# print ('Max Score ', max(idScore.values()))
# print ('Min Score ', min(idScore.values()))

maxval = max(idScore.values())
minval = min(idScore.values())
scaleval = max(maxval, abs(minval))
# print (maxval, minval, scaleval)

ascale = (minval + scaleval) / (scaleval * 2)
# print (ascale)
nodeList = []
for key in idScore:
    scoreScale = (idScore[key] + scaleval) / (scaleval * 2)
    nodeList.append({ "id" : key, "score" : scoreScale })

linkList = []

for lnk in dirList:
    value = int((lnk[2] + 10) / 2) + 1
    linkList.append({ "source" : lnk[0], "target" : lnk[1], "value" : value })

graphData = { "nodes" : nodeList, "links" : linkList }

jsonstring = json.dumps(graphData, indent=2)

with open('bitcoin_graph.js', 'w') as jsfile:
    jsfile.write('var graph = ')
    jsfile.write(jsonstring)
