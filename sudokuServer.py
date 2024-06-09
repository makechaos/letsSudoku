import os, sys
import datetime, json

dateTimeEnts = {}

sudokuDir = '/home/makechaos/letsSudoku/'

def loadDateEnts(force=False):
    global dateTimeEnts

    if len(dateTimeEnts)==0 or force:
        dateTimeEnts = json.load(open(sudokuDir+'sudoku.json','r'))

def fresh(inp):
    global dateTimeEnts
    with open(sudokuDir + 'sudokuMain.html','r') as f:
        r = f.read()
    loadDateEnts(True)

    optxt = ''
    for a in dateTimeEnts:
        optxt += '<option value="%s">%s</option>'%(a,a)
    r= r.replace('dateOptions',optxt);
    return r

def specificEntry(dt):
    global dateTimeEnts

    loadDateEnts(True)
    if dt not in dateTimeEnts:
        with open(sudokuDir + 'sudokuNoEntry.html','r') as f:
            r = f.read()
        r = r.replace('{{dateEntry}}', dt)
        return r

    with open(sudokuDir + 'sudokuMain.html','r') as f:
        r = f.read()
    optxt = ''
    for a in dateTimeEnts:
        opt = ''
        if a==dt:
            opt = 'selected'
        optxt += '<option value="%s" %s>%s</option>'%(a,opt,a)
    r= r.replace('dateOptions',optxt);
    return r

def update(jsonStr):
    global dateTimeEnts

    jsonData = json.loads(jsonStr)
    curDate = jsonData['date']

    curDate = getDate(curDate)
    # if curDate=='today':
    #     curDate = datetime.datetime.now().strftime('%Y-%m-%d')

    if 'entries' in jsonStr:
        if curDate not in dateTimeEnts:
            dateTimeEnts[curDate] = []
        dateTimeEnts[curDate] += jsonData['entries']
        json.dump(dateTimeEnts, open(sudokuDir+'sudoku.json','w'), indent=2)
        return json.dumps(dateTimeEnts[curDate])
    else:
        dateTimeEnts[curDate] = jsonStr

    json.dump(dateTimeEnts, open(sudokuDir+'sudoku.json','w'), indent=2)
    return dateTimeEnts[curDate]

def getDate(curDate):
    if curDate=="today":
        curDate = datetime.datetime.now().strftime('%Y-%m-%d')
    return curDate

def clear(dt):
    global dateTimeEnts
    dt = getDate(dt)
    dateTimeEnts[dt] = ""
    json.dump(dateTimeEnts, open(sudokuDir+'sudoku.json','w'), indent=2)
    return "cl-"+dt

def poll(curDate):
    global dateTimeEnts

    loadDateEnts()
    if curDate.find('{')>=0 or curDate.find('[')>=0:
        jdata = json.loads(curDate)
        loadDateEnts()
        curDate = getDate(jdata['date'])
        indx = 0 if 'lastN' not in jdata else jdata['lastN']
        if curDate in dateTimeEnts:
            if type(dateTimeEnts[curDate]) is list:
                return json.dumps(dateTimeEnts[curDate][indx:])
            else:
                return 'wrongD'
        return "no data"

    # OLD way
    curDate = getDate(curDate)
    if curDate in dateTimeEnts:
        return dateTimeEnts[curDate]
    else:
        return "no-data"