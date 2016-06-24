import sys, string, random

def showboard(string):
    string = (" ".join(string)+" ")
    print(" ------------------")
    for i in range(0,len(string),16):
        print(str(int((i/16)))+str("|")+""+string[i:i+16]+"|"+str(int((i/16))))
    print(" ------------------")
    print("  0 1 2 3 4 5 6 7")
def diffstr(str1, str2, char):
    one = 0
    two = 0
    for i, j in enumerate(str1):
        if j == char:
            one+=1
    for i, j in enumerate(str2):
        if j == char:
            two+=1
    return two-one
def playmove(string, char, pos, neighhors):
    posdirections ={}
    flip = set([pos])
    Temp = set([])
    for mov in neighhors[pos]:
        if not string[mov]==char and not string[mov]==".":
            posdirections[mov-pos] = mov
            #print(mov)
    for diff in posdirections.keys():
        mov = posdirections[diff]
        while -1<mov<64 and not string[mov]==char and not string[mov]=="." :
            Temp.add(mov)
            mov = mov+diff
        if -1<mov<64 and string[mov]==char:
            flip = flip|Temp
        else:
            Temp = set([])
    for mov in flip:
        string=string[0:mov]+char+string[mov+1:len(string)]
    return string
def calcstable(string, char):
    maxcount = 0
    neighbors = getneighbors()
    poschar = set([])
    corners = set([])
    stable = set([])
    status = True
    diff = {"hor":{1,-1},"vert":{8,-8},"rdiag":{7,-7},"ldiag":{-9,9}}
    test = {"hor":False, "vert":False, "rdiag":False, "ldiag":False}
    Stest = test
    for corner in {0,7,56,63}:
        if string[corner]==char:
            #count+=1
            stable.add(corner)
            #poschar.add(corner)
            maxcount = len(stable)
            while len(stable)>0:
                Temp = stable.pop()
                for stat in diff:
                    for difference in diff[stat]:
                        if Temp+difference<64:
                            test[stat]=test[stat]|(string[(Temp+difference)]==char)
                for stat in test:
                    status = status&test[stat]
                test = Stest
                if status:
                    stable.add(Temp)
                    if maxcount<len(stable):
                        maxcount = len(stable)
                status = True
    return maxcount
def calcbadmoves(string, char):
    neighbhors = getneighbors()
    corners = {0,7,56,63}
    badmoves = set([])
    for corner in corners:
        if string[corner]==char:
            badmoves = badmoves|neighbhors[corner]
    return badmoves
def evaluate(string, char):
    numpiece = 0
    numopppiece=  0
    edges = 0
    edgesopp = 0
    oppchar = 'X'
    badpiece=0
    if oppchar ==char:
        oppchar = 'O'
    for i, j in enumerate(string):
        if j == char:
            numpiece+=1
        if j == oppchar:
            numopppiece+=1
        if j== char and i in calcbadmoves(string, char):
            badpiece+=1
        if j ==char and (i%8 ==0 or i%8==7 or int(i/8)==7 or int(i/8)==0):
            edges +=1
        if j ==oppchar and (i%8 ==0 or i%8==7 or int(i/8)==7 or int(i/8)==0):
            edgesopp +=1
    posMove = posmoves(string,char)
    posoppMove = posmoves(string,oppchar)
    posmove = len(posMove)-len(posoppMove)
    stable = calcstable(string, char)
    oppstable = calcstable(string, oppchar)
    if (len(posMove)==0 and len(posoppMove)==0) or (not "." in string):
        if numpiece>numopppiece:
            return 10000
        else:
            return -10000
    if numpiece<30:
        return 30*posmove + 30*(stable-oppstable)-(15*(numpiece-numopppiece))-30*badpiece
    if numopppiece<40:
        return 20*posmove+40*(stable-oppstable)+15*(numpiece-numopppiece) - 30*badpiece
    if numpiece<59:
        return 10*posmove + 50*(stable-oppstable)+30*(numpiece-numopppiece)-30*badpiece
    else:
        return 10*(stable-stableopp)+30*(numpiece-numopppiece)+2*posmove

def maxplay(string, char, oppchar, maxdepth, alpha, beta):
    posMove = posmoves(string, char)
    if len(posMove)==0 or maxdepth==0:
        return evaluate(string, char)
    bestscore = 100000
    for move in posMove:
        if not move in calcbadmoves(string, char):
            newstr = playmove(string, char, move,getneighbors())
            score = minplay(newstr, char, oppchar, maxdepth-1, alpha,beta)
            if score>bestscore:
                bestscore = score
                best = move
            if alpha<score:
                alpha = score
            if beta<=alpha:
                return -100000
    return bestscore
def minplay(string, char, oppchar, maxdepth, alpha, beta):
    #print(string)
    corner = set([])
    posMove = posmoves(string, oppchar)
    for pos in {0,7,56,63}:
        if pos in posMove:
            corner.add(pos)
    if len(corner)>0:
        return -100000

    if len(posMove)==0 or maxdepth==0:
        return evaluate(string, char)
    bestscore = 100000
    for move in posMove:
        if move not in {0,7,56,63}:
            newstr = playmove(string, oppchar, move,getneighbors())
            score = maxplay(newstr, char, oppchar, maxdepth-1,alpha,beta)
            if score<bestscore:
                bestscore = score
                best = move
            if beta>score:
                beta = score
            if beta<=alpha:
                return 100000
    return bestscore
def minmax(string, char,oppchar, maxdepth, posMoves):
    #print(posmoves)
    alpha = -10000
    beta = 10000
    best = random.choice(list(posMoves))
    bestscore = -10000
    corners = 0
    for move in posMoves:
        newstr = playmove(string, char, move,getneighbors())
        if move not in calcbadmoves(string, char):
            #print(str(move))
            score = minplay(newstr,char,oppchar,maxdepth-1,alpha,beta)
            if score>bestscore:
                bestscore = score
                best = move
    '''if bestscore == -1000:
        for move in posMoves:
            newstr = playmove(string, char, move)
        score = minplay(newstr,char,oppchar,maxdepth-1,alpha,beta)
        if score>bestscore:
            bestscore = score
            best = move
    '''
    return best
def calcdepth(string):
    tokens = 0
    for i, j in enumerate(string):
        if j == "X" or j=="O":
            tokens+=1
    if tokens<30:
        return 2
    if tokens<40:
        return 3
    if tokens<50:
        return 4

    else:
        return int(((tokens)-45)/2)+2

def strategy(string, char):
    #showboard(string)
    oppchar = 'X'

    if oppchar ==char:
        oppchar = 'O'

    maxdepth = calcdepth(string)
    corner = set([])
    posMoves = posmoves(string, char)

    #print(str(posMoves))
    for pos in {0,7,56,63}:
        if pos in posMoves:
            corner.add(pos)
    #print(str(posMoves))

    if len(corner)>0:
        posMoves = corner

    #print(str(posMoves))
    return minmax(string, char, oppchar, maxdepth,posMoves)
def getequivalency():
    pos={}
    for i in range(8):
        pos[i] = {}
        for x in range(8):
            pos[i][x]=(i*8)+x
    flipd = {}
    flipo = {}
    RR = {}
    R2 = {}
    RL = {}
    flipx = {}
    flipy={}
    for i in range(8):
        flipo[i] ={}
        flipd[i] = {}
        RR[i] = {}
        R2[i] = {}
        RL[i] = {}
        flipx[i] = {}
        flipy[i]= {}
        for x in range(8):
            flipd[i][x]=pos[7-x][7-i]
            flipo[i][x] = pos[x][i]
            RR[i][x] = pos[x][7-i]
            R2[i][x] = pos[7-i][7-x]
            RL[i][x]=pos[7-x][7-(7-i)]
            flipx[i][x] = pos[i][7-x]
            flipy[i][x] = pos[7-i][x]
    return {"RL":RR,"R2":R2,"RR":RL,"FD":flipd,"FO":flipo, "FY":flipx,"FX":flipy, "I":pos}

def getneighbors():
    neighbors = {}
    for pos in range(64):
        neighbors[pos] = set([])
        neighbors[pos].add(pos+1)
        neighbors[pos].add(pos-1)
        neighbors[pos].add(pos-8)
        neighbors[pos].add(pos+8)
        neighbors[pos].add(pos+9)
        neighbors[pos].add(pos+7)
        neighbors[pos].add(pos-9)
        neighbors[pos].add(pos-7)
        neighbors[pos]=neighbors[pos]-set(range(64,100))-set(range(-10,0))
        if pos%8==7:
            neighbors[pos] = neighbors[pos]-set(range(0,64,8))
        elif pos%8==0:
            neighbors[pos] = neighbors[pos]-set(range(7,64,8))
    return neighbors

def posmoves(string, char):
    dictposmoves = set([])
    poschar = set([])
    for i, j in enumerate(string):
        if j == char:
            poschar.add(i)
    posneighbors = getneighbors()
    Tempposstep = {}
    #print(str(poschar))
    #print(string)
    for pos in poschar:
        for mov in posneighbors[pos]:
            if not string[mov] =="." and not string[mov]==char:
                if (mov-pos)in Tempposstep:
                    Tempposstep[mov-pos].add(mov)
                else:
                    Tempposstep[mov-pos] = set([mov])
    #print(str(Tempposstep))
    for diff in Tempposstep.keys():
        for pos in Tempposstep[diff]:
            Temppos = pos
            while not string[Temppos]==char and not string[Temppos]==".":
                if Temppos+diff in posneighbors[Temppos]:
                    Temppos+=diff
                else:
                    break
            if string[Temppos] =='.':
                dictposmoves.add(Temppos)
    #print(str(dictposmoves))
    return dictposmoves

def endgame(string):
    players = ["O","X"]
    counts = [set([]),set([])]
    for player in range(2):
        for i, j in enumerate(string):
            if j == players[player]:
                counts[player].add(i)

    if len(counts[0])==len(counts[1]):
        print("Tie "+str(len(counts[0]))+"-"+str(len(counts[1])))
    else:
        if len(counts[0])>len(counts[1]):
            winner = 0
        else:
            winner = 1
        return players[winner]

def transform(string, operation):
    Temp = ""
    for i in range(8):
        for x in range(8):
            Temp+=string[operation[i][x]]
    return Temp

def playgame(string, play):#random vs strategy
    neighhors = getneighbors()
    print(str(neighhors))
    currentgame = string
    players = ["O","X"]
    currplayer = 1
    check = True
    equivalnce = getequivalency()
    while "." in string:
        showboard(string)
        posmov = posmoves(string, players[currplayer])
        #print(str(posmov))
        if len(posmov)>0:
            check = True
            print(players[currplayer]+"'s turn\tRow Col")
            if currplayer == 1:
                Temp = set([])
                for i in {0,7,56,63}:
                    if i in posmov:
                        Temp.add(i)
                if len(Temp)>0:
                    posmov = Temp
                pos = strategy(string, players[currplayer])
            else:
                pos = random.choice(list(posmov))
            print(str(pos))
            string = playmove(string, players[currplayer],pos, neighhors)
            currplayer = 1-currplayer
        else:
            if check:
                print("No Possible moves for "+players[currplayer]+" They Pass")
                check = False
                currplayer = 1-currplayer
            else:
                print()
                return endgame(string)
    #print(string)
    showboard(string)
    endgame(string)

if len(sys.argv)>2:
    play = [sys.argv[1],sys.argv[2]]
else:
    play = ["p","p"]
print(str(play))
playgame("...........................OX......XO...........................", play)

'''play =["c","c"]
onewin = 0
twowin = 0
for i in range(100):
    if playgame("...........................OX......XO...........................", play) =="X":
        onewin+=1
    else:
        twowin+=1
    print("Strategy won "+str(twowin)+" times")
'''
