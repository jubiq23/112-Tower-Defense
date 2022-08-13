from cmu_112_graphics import *
import random
from random import choices
import decimal

def makeVerteces(app):
### USE THIS FUNCTION TO DETERMINE HOW COMPLEX MAP SHOULD BE!###
# Lower number = less verteces, and vice versa
    app.verteces = 8

def checkForDivZero(y1,y2,x2,x1):
    try:
        slope = ((y1-y2)/(x2-x1))
        return False
    except:
        return True

#from 112 notes!
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

towersOut = []
#pathNodes = [(0,0),(150,250),(250,250),(400,400),(500,450),(600,450)]
#pathNodes = [(0,0),(0,300),(200,300),(200,100),(400,100),(400,400),(600,400)]
pathNodes = []


def randomGrabber(total, splits):
    remainder = total
    result = []
    for split in range(splits):
        if range(splits)[split] == splits-1:
            result.append(remainder)
        else:
            currVal = random.randint(0,remainder)
            result.append(currVal)
            remainder -= currVal
    random.shuffle(result)
    return result


class Player(object):
    def __init__(self, cash, health):
        self.cash = cash
        self.health = health
        self.level = 1
        self.secondsLeft = 25
        self.timer = 250

player = Player(100, 50)

class Balloon(object):
    def __init__(self, strength,x,y, currNode, nextNode):
        self.strength = strength
        self.x = x ; self.y = y
        self.currNode = currNode
        self.nextNode = nextNode
        if self.strength == 1:
            self.color = "magenta"
            self.speed = 8
            self.health = 3
        elif self.strength == 2:
            self.color = "sky blue"
            self.speed = 10
            self.health = 9
        elif self.strength == 3:
            self.color = "light green"
            self.speed = 16
            self.health = 10
        elif self.strength == 4:
            self.color = "yellow"
            self.speed = 25
            self.health = 30
        elif self.strength == 5:
            self.color = "black"
            self.speed = 40
            self.health = 200

    def __repr__(self):
        return self.color

    def move(self, currPoint, nextPoint):
        currPointX = currPoint[0]
        currPointY = currPoint[1]
        nextPointX = nextPoint[0]
        nextPointY = nextPoint[1]
        newX = currPointX
        newY = currPointY
        if checkForDivZero(currPointY,nextPointY,nextPointX,currPointX):
            if nextPointY > currPointY:
                while newY < nextPointY:
                    newY += 1
            elif (currPointY > nextPointY):
                while newY > nextPointY:
                    newY -= 1
        else:
            slope = (nextPointY-currPointY)/(nextPointX-currPointX)
            if nextPointX > currPointX:
                while newX < nextPointX:
                    newX +=1
                    newY += slope
            if currPointX > nextPointX:
                while newX > nextPointX:
                    newX -= 1
                    newY += slope
        self.x = newX
        self.y = newY
            
class Tower(object):
    def __init__(self, x, y, type):
        self.type = type
        self.x = x
        self.y = y
        self.ammoX = x
        self.ammoY = y
        self.ballsInRange = []
        self.rangeShow = True
        #self.image = Here, i'm going to insert the sprites
        if type == 'normal':
            self.color = 'brown'
            self.text = "D"
            self.range = 75
            self.speed = 2
            self.cost = 100
            self.damage = 3
        #getting a tack shooter might be hard... i'll
        #keep this here for now but its not likely ill
        #include it in the final game
        elif type == 'tack':
            self.color = 'pink'
            self.text = "TS"
            self.range = 60
            self.speed = 1
            self.cost = 200
            self.damage = 1
        elif type == 'cannon':
            self.color = 'gray'
            self.text = "C"
            self.range = 100
            self.speed = 3
            self.cost = 300
            self.damage = 10
        elif type == 'super':
            self.color = 'red'
            self.text = "SUP"
            self.range = 200
            self.speed = 1
            self.cost = 2000
            self.damage = 100
        elif type == 'Taylor':
            self.color = 'green'
            self.text = 'Taylor'
            self.range = 400
            self.speed = 0.5
            self.cost = 5000
            self.damage = 500
        self.timer = self.speed*3
    def __repr__(self):
        return self.type
    def shoot(self, score):
        return score

def legalRandom(dataset, currPoint):
    try:
        tester = random.choice([ele for ele in dataset if ele != currPoint])
        return True
    except:
        return False

#This function is extremely long but shortening it was tough.
def finalizeBoard(app, start,turns):
    dir = random.choice(['x','y'])
    currPoint = start
    while turns > 0:
        #check if a blacklisted point is in another list and remove it
        for item in app.blacklist:
            if item in app.row1:
                app.row1.pop(app.row1.index(item))
            if item in app.row2:
                app.row2.pop(app.row2.index(item))
            if item in app.row3:
                app.row3.pop(app.row3.index(item))
            if item in app.row4:
                app.row4.pop(app.row4.index(item))
            if item in app.row5:
                app.row5.pop(app.row5.index(item))
            if item in app.row6:
                app.row6.pop(app.row6.index(item))
            if item in app.col1:
                app.col1.pop(app.col1.index(item))
            if item in app.col2:
                app.col2.pop(app.col2.index(item))
            if item in app.col3:
                app.col3.pop(app.col3.index(item))
            if item in app.col4:
                app.col4.pop(app.col4.index(item))
            if item in app.col5:
                app.col5.pop(app.col5.index(item))
            if item in app.col6:
                app.col6.pop(app.col6.index(item))
        if dir == 'x':
            if currPoint[1] == 0:
                #Below makes sure that there isn't an indexing error, if so
                #it cuts off the map early
                if legalRandom(app.row1, currPoint):
                    nextPoint = random.choice([ele for ele in app.row1 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row1.index(currPoint),app.row1.index(nextPoint)):
                            app.blacklist.add(app.row1[val])
                        del app.row1[app.row1.index(currPoint):app.row1.index(nextPoint)]
                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row1.index(nextPoint)+1,app.row1.index(currPoint)+1):
                            app.blacklist.add(app.row1[val])
                        del app.row1[app.row1.index(currPoint)+1:app.row1.index(nextPoint)+1]
            elif currPoint[1] == 100:
                if legalRandom(app.row2, currPoint):
                    nextPoint = random.choice([ele for ele in app.row2 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row2.index(currPoint),app.row2.index(nextPoint)):
                            app.blacklist.add(app.row2[val])
                        del app.row2[app.row2.index(currPoint):app.row2.index(nextPoint)]
                        
                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row2.index(nextPoint)+1,app.row2.index(currPoint)+1):
                            app.blacklist.add(app.row2[val])
                        del app.row2[app.row2.index(currPoint)+1:app.row2.index(nextPoint)+1]
                        
            elif currPoint[1] == 200:
                if legalRandom(app.row3, currPoint):
                    nextPoint = random.choice([ele for ele in app.row3 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row3.index(currPoint),app.row3.index(nextPoint)):
                            app.blacklist.add(app.row3[val])
                        del app.row3[app.row3.index(currPoint):app.row3.index(nextPoint)]
                        

                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row3.index(nextPoint)+1,app.row3.index(currPoint)+1):
                            app.blacklist.add(app.row3[val])
                        del app.row3[app.row3.index(currPoint)+1:app.row3.index(nextPoint)+1]
                        
            elif currPoint[1] == 300:
                if legalRandom(app.row4, currPoint):
                    nextPoint = random.choice([ele for ele in app.row4 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row4.index(currPoint),app.row4.index(nextPoint)):
                            app.blacklist.add(app.row4[val])
                        del app.row4[app.row4.index(currPoint):app.row4.index(nextPoint)]
                        
                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row4.index(nextPoint)+1,app.row4.index(currPoint)+1):
                            app.blacklist.add(app.row4[val])
                        del app.row4[app.row4.index(currPoint)+1:app.row4.index(nextPoint)+1]
                        
            elif currPoint[1] == 400:
                if legalRandom(app.row5, currPoint):
                    nextPoint = random.choice([ele for ele in app.row5 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row5.index(currPoint),app.row5.index(nextPoint)):
                            app.blacklist.add(app.row5[val])
                        del app.row5[app.row5.index(currPoint):app.row5.index(nextPoint)]
                        
                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row5.index(nextPoint)+1,app.row5.index(currPoint)+1):
                            app.blacklist.add(app.row5[val])
                        del app.row5[app.row5.index(currPoint)+1:app.row5.index(nextPoint)+1]

            elif currPoint[1] == 500:
                if legalRandom(app.row6, currPoint):
                    nextPoint = random.choice([ele for ele in app.row6 if ele != currPoint])
                    if nextPoint[0] > currPoint[0]:
                        for val in range(app.row6.index(currPoint),app.row6.index(nextPoint)):
                            app.blacklist.add(app.row6[val])
                        del app.row6[app.row6.index(currPoint):app.row6.index(nextPoint)]

                    elif currPoint[0] > nextPoint[0]:
                        for val in range(app.row6.index(nextPoint)+1,app.row6.index(currPoint)+1):
                            app.blacklist.add(app.row6[val])
                        del app.row6[app.row6.index(currPoint)+1:app.row6.index(nextPoint)+1]
                        

            turns -=1
        else:
            if currPoint[0] == 0:
                if legalRandom(app.col1, currPoint):
                    nextPoint = random.choice([ele for ele in app.col1 if ele != currPoint])
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col1.index(currPoint),app.col1.index(nextPoint)):
                            app.blacklist.add(app.col1[val])
                        del app.col1[app.col1.index(currPoint):app.col1.index(nextPoint)]
                        
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col1.index(nextPoint)+1,app.col1.index(currPoint)+1):
                            app.blacklist.add(app.col1[val])
                        del app.col1[app.col1.index(currPoint)+1:app.col1.index(nextPoint)+1]
                        

            elif currPoint[0] == 120:
                if legalRandom(app.col2, currPoint):
                    nextPoint = random.choice([ele for ele in app.col2 if ele != currPoint])
                    #print ("curr?", currPoint, "next?", nextPoint)
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col2.index(currPoint),app.col2.index(nextPoint)):
                            app.blacklist.add(app.col2[val])
                        del app.col2[app.col2.index(currPoint):app.col2.index(nextPoint)]
                        
                            #print (val, app.col2)
                            #app.col2.pop(val)
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col2.index(nextPoint)+1,app.col2.index(currPoint)+1):
                            app.blacklist.add(app.col2[val])
                        del app.col2[app.col2.index(currPoint)+1:app.col2.index(nextPoint)+1]
                        
                            #app.col2.pop(val)
                    #print ("COL2", app.col2)
            elif currPoint[0] == 240:
                if legalRandom(app.col3, currPoint):
                    nextPoint = random.choice([ele for ele in app.col3 if ele != currPoint])
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col3.index(currPoint),app.col3.index(nextPoint)):
                            app.blacklist.add(app.col3[val])
                        del app.col3[app.col3.index(currPoint):app.col3.index(nextPoint)]
                        
                            #app.col3.pop(val)
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col3.index(nextPoint)+1,app.col3.index(currPoint)+1):
                            app.blacklist.add(app.col3[val])
                        del app.col3[app.col3.index(currPoint)+1:app.col3.index(nextPoint)+1]
                        
                            #app.col3.pop(val)
                    #print ("COL3", app.col3)
            elif currPoint[0] == 360:
                if legalRandom(app.col4, currPoint):
                    nextPoint = random.choice([ele for ele in app.col4 if ele != currPoint])
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col4.index(currPoint),app.col4.index(nextPoint)):
                            app.blacklist.add(app.col4[val])
                        del app.col4[app.col4.index(currPoint):app.col4.index(nextPoint)]
                        
                            #app.col4.pop(val)
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col4.index(nextPoint)+1,app.col4.index(currPoint)+1):
                            app.blacklist.add(app.col4[val])
                        del app.col4[app.col4.index(currPoint)+1:app.col4.index(nextPoint)+1]
                        
                            #app.col4.pop(val)
                    #print ("COL4", app.col4)
            elif currPoint[0] == 480:
                if legalRandom(app.col5, currPoint):
                    nextPoint = random.choice([ele for ele in app.col5 if ele != currPoint])
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col5.index(currPoint),app.col5.index(nextPoint)):
                            app.blacklist.add(app.col5[val])
                        del app.col5[app.col5.index(currPoint):app.col5.index(nextPoint)]
                        
                            #app.col5.pop(val)
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col5.index(nextPoint)+1,app.col5.index(currPoint)+1):
                            app.blacklist.add(app.col5[val])
                        del app.col5[app.col5.index(currPoint)+1:app.col5.index(nextPoint)+1]
                        
                            #app.col5.pop(val)
                    #print ("COL5", app.col5)
            elif currPoint[0] == 600:
                if legalRandom(app.col6, currPoint):
                    nextPoint = random.choice([ele for ele in app.col6 if ele != currPoint])
                    if nextPoint[1] > currPoint[1]:
                        for val in range(app.col6.index(currPoint),app.col6.index(nextPoint)):
                            app.blacklist.add(app.col6[val])
                        del app.col6[app.col6.index(currPoint):app.col6.index(nextPoint)]
                        
                            #app.col6.pop(val)
                    elif currPoint[1] > nextPoint[1]:
                        for val in range(app.col6.index(nextPoint)+1,app.col6.index(currPoint)+1):
                            app.blacklist.add(app.col6[val])
                        del app.col6[app.col6.index(currPoint)+1:app.col6.index(nextPoint)+1]
                        
                            #app.col6.pop(val)
            turns -=1
        if currPoint != nextPoint:
            currPoint = nextPoint
            pathNodes.append(currPoint)
        else:
            break
        if dir == 'x':
            dir = 'y'
        else: dir = 'x'



#inspired by https://www.geeksforgeeks.org/building-an-undirected-graph-and-finding-shortest-path-using-dictionaries-in-python/
def buildBoard(app, start, points):
    pathNodes.append(start)
    #hardcoded grid
    a = (0,0);   b = (120,0); c= (240,0);   d = (360,0); e = (480,0); f =(600,0)
    g = (0,100); h=(120,100); i=  (240,100);j= (360,100);k= (480,100);l=(600,100)
    m = (0,200); n=(120,200); o=  (240,200);p= (360,200);q= (480,200);r=(600,200)
    s = (0,300); t=(120,300); u=  (240,300);v= (360,300);w= (480,300);x=(600,300)
    y = (0,400); z=(120,400); ap= (240,400);bp=(360,400);cp=(480,400);dp=(600,400)
    ep = (0,500);fp=(120,500);gp=(240,500); hp=(360,500);ip=(480,500);jp=(600,500)

    app.blacklist = set()

    app.row1 = [a,b,c,d,e,f]
    app.row2 = [g,h,i,j,k,l]
    app.row3 = [m,n,o,p,q,r]
    app.row4 = [s,t,u,v,w,x]
    app.row5 = [y,z,ap,bp,cp,dp]
    app.row6 = [ep,fp,gp,hp,ip,jp]

    app.col1 = [a,g,m,s,y,ep]
    app.col2 = [b,h,n,t,z,fp]
    app.col3 = [c,i,o,u,ap,gp]
    app.col4 = [d,j,p,v,bp,hp]
    app.col5 = [e,k,q,w,cp,ip]
    app.col6 = [f,l,r,x,dp,jp]
    finalizeBoard(app,start, points)

def appStarted(app):
    makeVerteces(app)
    buildBoard(app, (0,0), app.verteces)
    #https://www.kosbie.net/cmu/
    app.kosbie = app.loadImage('kosbie.png')
    #https://scsdean.cs.cmu.edu/new-faculty/2020.html 
    app.taylor = app.loadImage('taylor.png')
    #https://media.istockphoto.com/photos/evergreen-grass-texture-background-picture-id182232364
    app.grass = app.loadImage('grass.jpg')
    app.randomBall = 1
    app.ballOptions = [1,2,3,4]
    app.ballWeight = [0.5,0.3,0.15,0.05]
    app.ballWeight10 = [0.47,0.3,0.15,0.05,0.03]
    app.turrCounter = False
    app.gameOver = False
    app.timerDelay = 50
    app.MoneyCounter = 6
    app.overLapCounter = 6
    app.balloonList = []
    app.currBalloon = -1
    app.mouseX = 0
    app.mouseY = 0
    app.moneyError = False
    app.overlapError = False

def randomBallGen(app):
    app.randomBall = choices(app.ballOptions,app.ballWeight)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app, event):
    for tower in towersOut:
        if (app.mouseX > (tower.x-20)) and (app.mouseX < (tower.x+20)):
            if (app.mouseY > (tower.y-20)) and (app.mouseY < (tower.y+20)):
                tower.rangeShow = True
        else:
            tower.rangeShow = False
    
def isPointLegal(app, point):
    try:
        pathNodes[point]
        return True
    except:
        return False

# from https://www.geeksforgeeks.org/check-two-given-circles-touch-intersect/
#this tells if the circles are overlapping or not! useful
def circleOverlap(x1, y1, x2, y2, r1, r2):
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);
    radSumSq = (r1 + r2) * (r1 + r2);
    if (distSq == radSumSq):
        return True
    elif (distSq > radSumSq):
        return False
    else:
        return True
  




def pathCalc(app):
    for tupleNum in range(len(pathNodes)):
        point1 = tupleNum
        point2 = tupleNum+1
        if isPointLegal(app, point2):
            if checkForDivZero(pathNodes[point1][1],pathNodes[point2][1],
            pathNodes[point2][0],pathNodes[point1][0]):
                p1X = pathNodes[point1][0]
                p1Y = pathNodes[point1][1]
                p2Y = pathNodes[point2][1]
                deltaY = abs(pathNodes[point2][1]-pathNodes[point1][1])
                if p1Y > p2Y:
                    for yVal in range(deltaY):
                        if circleOverlap(app.mouseX,app.mouseY,p1X,p2Y+yVal, 
                        20, 20):
                            return True
                if p2Y > p1Y:
                    for yVal in range(deltaY):
                        if circleOverlap(app.mouseX,app.mouseY,p1X,p1Y+yVal, 
                        20, 20):
                            return True
            else:
                slope = ((pathNodes[point1][1]-pathNodes[point2][1])/
                (pathNodes[point2][0]-pathNodes[point1][0]))
                deltaX = (pathNodes[point2][0]-pathNodes[point1][0])
                newY = pathNodes[point1][1]
                for xVal in range(deltaX):
                    newY -= slope
                    if circleOverlap(app.mouseX, app.mouseY, pathNodes[point1][0]+xVal, 
                    newY, 20, 20):
                        return True
    return False

def towerPlace(app):
    if towersOut == []:
        if pathCalc(app):
            return False
    for tower in towersOut:
        if (app.mouseX+20 > tower.x-20) and (app.mouseX-20 < tower.x+20):
            if (app.mouseY+20 > tower.y-20) and (app.mouseY-20 < tower.y+20):
                return False
        if pathCalc(app):
            return False
    
    return True

def createTower(app, type):
    towersOut.append(Tower(app.mouseX,app.mouseY, type))

    

def keyPressed(app, event):
    if event.key == '1':
        if player.cash >= 100:
            if towerPlace(app):

                player.cash-=100
                createTower(app,'normal')
            else:
                app.overlapError = True
        else:
            app.moneyError = True
    if event.key == '2':
        if player.cash >= 200:
            if towerPlace(app):
                player.cash-=200
                createTower(app,'tack')
            else:
                app.overlapError = True
        else:
            app.moneyError = True
            #towersOut.append(Tower(event.x,event.y, 'tack'))
    if event.key == '3':
        if player.cash >= 400:
            if towerPlace(app):
                player.cash-=400
                createTower(app,'cannon')
            else:
                app.overlapError = True
        else:
            app.moneyError = True
    if player.level >= 10:
        if event.key == '4':
            if player.cash >= 2000:
                if towerPlace(app):
                    player.cash-=2000
                    createTower(app,'super')
                else:
                    app.overlapError = True
            else:
                app.moneyError = True
    if player.level >= 13:
        if event.key == '5':
            if player.cash >= 5000:
                if towerPlace(app):
                    player.cash-=5000
                    createTower(app,'Taylor')
                else:
                    app.overlapError = True
            else:
                app.moneyError = True
    # if event.key == 'l':
    #     app.currBalloon +=1
    #     app.balloonList.append(Balloon(1,pathNodes[0][0], pathNodes[0][1],pathNodes[0],pathNodes[1]))
    # if event.key == 'k':
    #     app.currBalloon +=1
    #     app.balloonList.append(Balloon(2,pathNodes[0][0], pathNodes[0][1],pathNodes[0],pathNodes[1]))
    # if event.key == 'o':
    #     app.currBalloon +=1
    #     app.balloonList.append(Balloon(3,pathNodes[0][0], pathNodes[0][1],pathNodes[0],pathNodes[1]))
    #print ("Balloons:", app.balloonList)
    #print ("Turrets:", towersOut)
        
def balloonNodeChecker(app, currNode, nextNode):
    for num in range(len(pathNodes)):
            point1 = num
            point2 = num+1
            if isPointLegal(app, point2):
                if nextNode == pathNodes[point1]:
                    currNode = pathNodes[point1]
                    nextNode = pathNodes[point2]
                    return (currNode, nextNode)
            else:
                currNode = pathNodes[-1]
                return (currNode, nextNode)

def turretsAttack(app, balloon,turret):
    if circleOverlap(balloon.x, balloon.y, turret.x, turret.y, 10, turret.range):
        app.turrCounter = True
        if turret.speed == 3:
            balloon.health -= 1
    else:
        app.turrCounter = False

def balloonStillExists(app, dataList, balloon):
    try:
        dataList[dataList.index(balloon)]
        return True
    except:
        return False



def timerFired(app):
    if player.timer > 0:
        player.timer -= 1
    else:
        if app.gameOver == False:
            player.level += 1; player.secondsLeft = 25; player.timer = 250
    
    if (player.timer != 250) and (player.timer % 10 == 0):
        player.secondsLeft -= 1
    if (player.timer < 200) and (player.level < 10) and (player.timer % (10-player.level) == 0):
        if player.level > 3:
            ballNum = choices(app.ballOptions, app.ballWeight)[0]
        else: ballNum = 1
        app.balloonList.append(Balloon(ballNum,pathNodes[0][0], pathNodes[0][1],pathNodes[0],pathNodes[1]))
    if (player.timer < 200) and (player.level >= 10) and (player.timer % (1) == 0):
        ballNum = choices(app.ballOptions+[5], app.ballWeight10)[0]
        app.balloonList.append(Balloon(ballNum,pathNodes[0][0], pathNodes[0][1],pathNodes[0],pathNodes[1]))

    #print (app.balloonList)
    for balloon in app.balloonList:
        #print (balloon.health)
        if balloon.health <= 0:
            app.balloonList.pop(app.balloonList.index(balloon))
            if balloon.strength == 1:
                player.cash += 5
            elif balloon.strength == 2:
                player.cash+=10
            elif balloon.strength == 3:
                player.cash += 15
            elif balloon.strength == 4:
                player.cash += 25
            elif balloon.strength == 5:
                player.cash += 100
            for turret in towersOut:
                if balloon in turret.ballsInRange:
                    turret.ballsInRange.pop(turret.ballsInRange.index(balloon))
        #print (balloon, balloon.currNode,balloon.nextNode)
        if checkForDivZero(balloon.currNode[1],balloon.nextNode[1],
        balloon.nextNode[0], balloon.currNode[0]):
            if balloon.nextNode[1] > balloon.currNode[1]:
                if balloon.y < balloon.nextNode[1]:
                    balloon.y += balloon.speed
                else:
                    (balloon.currNode, balloon.nextNode) =balloonNodeChecker(
                        app, balloon.currNode, balloon.nextNode)
                #all of these else cases need to set currNode to nextNode and 
                #nextNode to nextNode+1
            elif balloon.nextNode[1] < balloon.currNode[1]:
                if balloon.y > balloon.nextNode[1]:
                    balloon.y -= balloon.speed
                else:
                    (balloon.currNode, balloon.nextNode) =balloonNodeChecker(
                        app, balloon.currNode, balloon.nextNode)
        else:
            slope = (balloon.nextNode[1]-
            balloon.currNode[1])/(balloon.nextNode[0]-balloon.currNode[0])
            if balloon.nextNode[0] > balloon.currNode[0]:
                if balloon.x < balloon.nextNode[0]:
                    balloon.x += balloon.speed
                    balloon.y += (balloon.speed)*slope
                else:
                    (balloon.currNode, balloon.nextNode) =balloonNodeChecker(
                        app, balloon.currNode, balloon.nextNode)
            elif balloon.nextNode[0] < balloon.currNode[0]:
                if balloon.x > balloon.nextNode[0]:
                    balloon.x -= balloon.speed
                    balloon.y += (balloon.speed)*slope
                else:
                    (balloon.currNode, balloon.nextNode) =balloonNodeChecker(
                        app, balloon.currNode, balloon.nextNode)
        if balloon.currNode == pathNodes[-1]:
            if balloonStillExists(app, app.balloonList, balloon):
                app.balloonList.pop(app.balloonList.index(balloon))
                player.health -= balloon.strength
                for turret in towersOut:
                    if balloon in turret.ballsInRange:
                        turret.ballsInRange.pop(turret.ballsInRange.index(balloon))

    for turret in towersOut:
        #print (turret.type,turret.ballsInRange)
        for balloon in app.balloonList:
                if circleOverlap(balloon.x, balloon.y, turret.x, turret.y, 10, turret.range):
                    if balloon not in turret.ballsInRange:
                        turret.ballsInRange.append(balloon)
                elif (balloon in turret.ballsInRange):
                    turret.ballsInRange.pop(turret.ballsInRange.index(balloon))


    
    for turret in towersOut:
        if turret.timer == turret.speed*3:
            if turret.ballsInRange != []:
                attacking = turret.ballsInRange[0]
            #for balloon in app.balloonList:
                if circleOverlap(attacking.x, attacking.y, turret.x, turret.y, 10, turret.range):
                        attacking.health -= turret.damage
                        if attacking.x < turret.ammoX:
                            deltaXVal = turret.ammoX - attacking.x
                            turret.ammoX -= (deltaXVal)
                        else:
                            deltaXVal = attacking.x - turret.ammoX
                            turret.ammoX += (deltaXVal)
                        deltaYVal = abs(turret.ammoY - attacking.y)
                        if attacking.y < turret.ammoY:
                            turret.ammoY -= deltaYVal
                        else:
                            turret.ammoY += deltaYVal
                        turret.timer = turret.speed*3
                        if (attacking.health <= 0):
                            turret.ballsInRange.pop(turret.ballsInRange.index(attacking))
                        turret.timer -= 1
        else:
            turret.timer -= 1
            
            if turret.timer <= 0:
                turret.timer = turret.speed*3
                turret.ammoX = turret.x; turret.ammoY = turret.y
                
                
    if app.overlapError:
        app.overLapCounter -= 1
        if app.overLapCounter < 1:
            app.overlapError = False
            app.overLapCounter = 6
    if app.moneyError:
        app.MoneyCounter -= 1
        if app.MoneyCounter < 1:
            app.moneyError = False
            app.MoneyCounter = 6
    if player.health <= 0:
        app.gameOver = True

def drawAmmo(app, canvas, turret):
    canvas.create_oval(turret.ammoX-2,turret.ammoY-2,turret.ammoX+2,turret.ammoY+2,fill='black')

        
def drawHouse(app, canvas):
    x = pathNodes[-1][0]
    y= pathNodes[-1][1]
    canvas.create_rectangle(x-20,y-30,x+30,y+30,fill='brown')
    canvas.create_oval(x,y-2,x+4,y+2)

def drawIcons(app,canvas):
    canvas.create_oval(670,190,710,230, fill='brown')
    canvas.create_text(690,210,text="$100")
    canvas.create_text(690,240,text='Press 1')
    canvas.create_oval(740,190,780,230, fill='pink')
    canvas.create_text(760,210,text="$200")
    canvas.create_text(760,240,text='Press 2')
    canvas.create_oval(670,260,710,300, fill='grey')
    canvas.create_text(690,280,text="$400")
    canvas.create_text(690,310,text='Press 3')
    if player.level < 10:
        canvas.create_oval(740,260,780,300, fill='black')
        canvas.create_text(760,310,text='?')
    else:
        canvas.create_oval(740,260,780,300, fill='red')
        canvas.create_text(760,280,text="$2000", font = 'size 10')
        canvas.create_text(760,310,text='Press 4')
    if player.level < 13:
        canvas.create_oval(705,330,745,370, fill='black')
        canvas.create_text(725,380,text='?')
    else:
        canvas.create_oval(705,330,745,370, fill='green')
        canvas.create_text(725,350,text="$5000", font = 'size 10')
        canvas.create_text(725,380,text='Taylor')
        canvas.create_text(725,400,text='Press 5')

def redrawAll(app, canvas):
    if app.gameOver == False:
        canvas.create_image(400,225,image=ImageTk.PhotoImage(app.grass))
        for tupleNum in range(len(pathNodes)):
            point1 = tupleNum
            point2 = tupleNum+1
            if isPointLegal(app, point2):
                canvas.create_line(pathNodes[point1][0],pathNodes[point1][1],
                pathNodes[point2][0],pathNodes[point2][1])
        for tupleNum in range(len(pathNodes)):
            point1 = tupleNum
            point2 = tupleNum+1
            if isPointLegal(app, point2):
                if checkForDivZero(pathNodes[point1][1],pathNodes[point2][1],
                pathNodes[point2][0],pathNodes[point1][0]):
                    p1X = pathNodes[point1][0]
                    p1Y = pathNodes[point1][1]
                    p2Y = pathNodes[point2][1]
                    deltaY = abs(pathNodes[point2][1]-pathNodes[point1][1])
                    if p1Y > p2Y:
                        newY = p2Y
                        while newY < p1Y:
                            newY += 1
                            canvas.create_oval(p1X-20,newY-20,p1X+20,newY+20,
                        fill='beige', outline = 'beige')
                    if p2Y > p1Y:
                        newY = p1Y
                        while newY < p2Y:
                            newY += 1
                            canvas.create_oval(p1X-20,newY-20,p1X+20,newY+20,
                        fill='beige', outline = 'beige')
                else:
                    slope = ((pathNodes[point1][1]-pathNodes[point2][1])/
                    (pathNodes[point2][0]-pathNodes[point1][0]))
                    if pathNodes[point2][0] > pathNodes[point1][0]:
                        deltaX = (pathNodes[point2][0]-pathNodes[point1][0])
                        newY = pathNodes[point1][1]
                        for xVal in range(deltaX):
                            newX = pathNodes[point1][0]+xVal
                            newY -= slope
                            canvas.create_oval(newX-20,newY-20,newX+20,newY+20,
                            fill='beige', outline = 'beige')
                    else:
                        deltaX = (pathNodes[point1][0]-pathNodes[point2][0])
                        newY = pathNodes[point2][1]
                        for xVal in range(deltaX):
                            newX = pathNodes[point2][0]+xVal
                            newY -= slope
                            canvas.create_oval(newX-20,newY-20,newX+20,newY+20,
                            fill='beige', outline = 'beige')
        for balloon in app.balloonList:
            if balloon.strength != 5:
                canvas.create_oval(balloon.x-10,balloon.y-10,balloon.x+10,balloon.y+10, fill=balloon.color)
            else:
                canvas.create_image(balloon.x,balloon.y,image=ImageTk.PhotoImage(app.kosbie))
        for tower in towersOut:
            drawAmmo(app, canvas, tower)
            if tower.rangeShow:
                canvas.create_oval(tower.x-tower.range, tower.y-tower.range,
                tower.x+tower.range,tower.y+tower.range)
            if tower.type != "Taylor":
                canvas.create_oval(tower.x-20,tower.y-20,tower.x+20,tower.y+20, 
                fill=tower.color)
                canvas.create_text(tower.x,tower.y,text=f"{tower.text}")
            else:
                canvas.create_image(tower.x,tower.y,image=ImageTk.PhotoImage(app.taylor))

        drawHouse(app, canvas)
        if app.overlapError:
            canvas.create_text(300,450,text=
            "Illegal location! Try again somewhere else",font='size 25')
        if app.moneyError:
            canvas.create_text(200,400,text="Insufficient funds!",font='size 30')
        canvas.create_rectangle(650,0,800,550,fill='turquoise')
        canvas.create_text(705,20,text=f"Cash:${player.cash}", font='size 20')
        canvas.create_text(700,45,text=f"Health:{player.health}",font='size 20')
        canvas.create_text(720,80,text=f"Wave {player.level}",font='size 27')
        canvas.create_text(760,120,text=f"{player.secondsLeft}",font='size 36')
        canvas.create_text(720,150,text="secs left in this wave")
        drawIcons(app,canvas)
    else:
        canvas.create_text(360,225,text="GAME OVER!",font='size 100')
        canvas.create_text(360,320,text=f'You made it to wave {player.level}',font='size 30')

#use list indexing to figure out each tower!
#so, run through each index in the list, check self.type:
#if self.type = dart, vs tack vs cannon

runApp(width=800, height=550)