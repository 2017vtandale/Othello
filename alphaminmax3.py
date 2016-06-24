import sys, string, random
def showboard(string):
    string = (" ".join(string)+" ")
    print(" ------------------")
    for i in range(0,len(string),16):
        print(str(int((i/16)))+str("|")+""+string[i:i+16]+"|"+str(int((i/16))))
    print(" ------------------")
    print("  0 1 2 3 4 5 6 7")
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
    #showboard(string)
    #print("***************posmoves debugging**********************")
    dictposmoves = set([])
    poschar = set([])
    for i, j in enumerate(string):
        if j == char:
            poschar.add(i)
    #print("Index of all char"+str(poschar))
    posneighbors = getneighbors()
    Tempposstep = {}
    #print(str(poschar))
    #print(string)
    for pos in poschar:
        #print(str(pos)+"'s neighbors "+str(posneighbors[pos]))
        for mov in posneighbors[pos]:
            #print(str(mov))
            if not string[mov] =="." and not string[mov]==char:
                #print(str(pos)+" neighbor "+str(mov))
                if (mov-pos)in Tempposstep:
                    Tempposstep[mov-pos].add(mov)
                else:
                    Tempposstep[mov-pos] = set([mov])
    #print(str(Tempposstep))
    #print(str(Tempposstep))
    #print(str(Tempposstep.keys()))
    for diff in Tempposstep.keys():
        #print(str(diff))
        for pos in Tempposstep[diff]:
            #print(Tempposstep[diff])
            Temppos = pos
            while not string[Temppos]==char and not string[Temppos]==".":
                if Temppos+diff in posneighbors[Temppos]:
                    Temppos+=diff
                else:
                    break
            if string[Temppos] =='.':
                dictposmoves.add(Temppos)
    return dictposmoves
def playmove(string, char, pos):
    neighhors = getneighbors()
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
    #showboard(string)
    maxcount = 0
    neighbors = getneighbors()
    poschar = set([])
    corners = set([])
    stable = set([])
    status = True
    diff = {"hor":{1,-1},"vert":{8,-8},"rdiag":{7,-7},"ldiag":{-9,9}}
    test = {"hor":False, "vert":False, "rdiag":False, "ldiag":False}
    Stest = test
    checked = set([])
    for corner in {0,7,56,63}:
        if string[corner]==char:
            #count+=1
            stable= stable|neighbors[corner]
            #poschar.add(corner)
            maxcount = len(stable)
            while len(stable)>0:
                #print(str(stable))
                Temp = stable.pop()
                #print(str(stable))
                if Temp not in checked:
                    checked.add(Temp)
                    #print(str(stable))
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
    badpiece=0
    oppchar = 'X'
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
            newstr = playmove(string, char, move)
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
            newstr = playmove(string, oppchar, move)
            score = maxplay(newstr, char, oppchar, maxdepth-1,alpha,beta)
            if score<bestscore:
                bestscore = score
                best = move
            if beta>score:
                beta = score
            if beta<=alpha:
                return 100000
    return bestscore
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

def strategy1(string, char, posmoves, neighors):
    dictbestmove = {}
    max = 0
    for pos in posmoves:
        newstr = playmove(string, char, pos)
        #print(newstr)
        change = diffstr(string, newstr, char)
        print(str(change))
        if change in dictbestmove:
            dictbestmove[change].add(pos)
            if change>max:
                max = change
        else:
            dictbestmove[change] = set([pos])
            if change>max:
                max=change
    return random.choice(list(dictbestmove[max]))
def minmax(string, char,oppchar, maxdepth, posMoves):
    #print(posmoves)
    alpha = -10000
    beta = 10000
    best = random.choice(list(posMoves))
    #print(strategy1(string, char, posMoves, getneighbors()))
    bestscore = -10000
    corners = 0
    for move in posMoves:
        newstr = playmove(string, char, move)
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

print(str(strategy(sys.argv[1],sys.argv[2])))
