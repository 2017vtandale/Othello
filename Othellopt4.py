import sys, string, random

def showboard(string):
    string = (" ".join(string)+" ")
    print(" ------------------")
    for i in range(0,len(string),16):
        print(str(int((i/16)))+str("|")+""+string[i:i+16]+"|"+str(int((i/16))))
    print(" ------------------")
    print("  0 1 2 3 4 5 6 7")
def getequivalency():
    pos={}
    for i in range(8):
        pos[i] = {}
        for x in range(8):
            pos[i][x]=x
    flipx = {}
    flip1x = {}
    RR = {}
    R2 = {}
    RL = {}
    for i in range(8):
        flip1x[i] ={}
        flipx[i] = {}
        RR[i] = {}
        R2[i] = {}
        RL[i] = {}
        for x in range(8):
            flipx[i][x]=pos[7-x][7-i]
            flip1x[i][x] = pos[x][i]
            RR[i][x] = pos[x][7-i]
            R2[i][x] = pos[7-i][7-x]
            RL[i][x]=pos[7-x][7-(7-i)]
    return {"RR":RR,"R2":R2,"RL":RL,"FX":flipx,"F1X":flip1x}

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
    print(str(dictposmoves))
    return dictposmoves
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
        print(players[winner]+" wins "+str(len(counts[winner]))+"-"+str(len(counts[1-winner])))

def transform(string, operation):
    Temp = ""
    for i in range(8):
        for x in range(8):
            Temp+=string[operation[i][x]]
    return Temp
def playgame(string, play):
    neighhors = getneighbors()
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
            if play[1-currplayer]=="p":
                Temp = input()
                if Temp in equivalnce:
                    newstr = string
                    while not Temp=="PL":
                        newstr = transform(newstr,equivalnce[Temp])
                        showboard(newstr)
                        Temp = input()
                Temp = Temp.split()
                pos = -1
                if len(Temp)==1 and len(Temp[0])==1 and int(Temp[0])<7:
                    pos = Temp[0]
                    print(str(pos))
                elif "," in Temp[0]:
                    row = int(Temp[0][0])
                    if len(Temp)>1:
                        col = int(Temp[1])
                    else:
                        col = int(Temp[0][2])
                elif int(Temp[0])>7:
                    pos = int(Temp[0])
                else:
                    row = int(Temp[0])
                    col = int(Temp[1])
                if pos==-1:
                    pos = (row*8)+col
                #print(str(pos
                print(str(pos))
                print(str(posmov))
                if pos in posmov:
                    #print(string)
                    string = playmove(string, players[currplayer], pos, neighhors)
                    currplayer = 1-currplayer
                else:
                    print("Not a valid move")
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
                endgame(string)
                return
    #print(string)
    showboard(string)
    endgame(string)

if len(sys.argv)>2:
    play = [sys.argv[1],sys.argv[2]]
else:
    play = ["p","p"]
print(str(play))
playgame("...........................OX......XO...........................", play)
