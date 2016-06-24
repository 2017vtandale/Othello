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
def evaluate(string, char):
    numpiece = 0
    corner = 0
    posmove = 0
    for i, j in enumerate(string):
        if i in {0,7,56,63}:
            corner+=1
        if j == char:
            numpiece+=1
    posmove = len(posmoves(string,char))
    if numpiece>44:
        return 3*posmove + 15*corner
    else:
        return 15*corner+numpiece
def maxplay(string, char, currdepth, maxdepth):
    oppchar = 'X'
    if oppchar ==char:
        oppchar = 'O'
    posMove = posmoves(string, char)
    if len(posMove)==0 or currdepth == maxdepth:
        return evaluate(string, char)
    bestscore = 100000
    for move in posMove:
        newstr = playmove(string, char, move)
        score = minplay(newstr, oppchar, currdepth+1, maxdepth)
        if score>bestscore:
            bestscore = score
            best = move
    return bestscore
def minplay(string, char,currdepth, maxdepth):
    oppchar = 'X'
    if oppchar ==char:
        oppchar = 'O'
    #print(string)
    posMove = posmoves(string, char)
    if len(posMove)==0 or currdepth == maxdepth:
        return evaluate(string, char)
    bestscore = 100000
    for move in posMove:
        newstr = playmove(string, char, move)
        score = maxplay(newstr, oppchar, currdepth+1, maxdepth)
        if score<bestscore:
            bestscore = score
            best = move
    return bestscore
def minmax(string, char, maxdepth, posMoves):
    oppchar = 'X'
    if oppchar ==char:
        oppchar = 'O'
    #print(posmoves)
    best = random.choice(list(posMoves))
    bestscore = -10000
    for move in posMoves:
        newstr = playmove(string, char, move)
        #print(newstr)
        score = minplay(newstr,oppchar, 1, maxdepth)
        if score>bestscore:
            bestscore = score
            best = move
    return best
def calcdepth(string):
    tokens = 0
    for i, j in enumerate(string):
        if j == "X" or j=="O":
            tokens+=1
    if tokens<50:
        return 2
    else:
        return int(((tokens+1)-50)/2)+2
def strategy(string, char):
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
    return minmax(string, char, maxdepth,posMoves)
print(str(strategy(sys.argv[1],sys.argv[2])))
