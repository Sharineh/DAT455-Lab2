from gamemodel import *
from graphics import *
import math


class GameGraphics:
    def __init__(self, game):
        
        self.game = game

        # open the window
        
        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
        
        # Initlaize a line from (-110,0) to (110,0)
        
        line = Line(Point(-110,0),Point(110,0))
        
        # Line color
        line.setFill('black')
        
        # Line width
        line.setWidth(2) 
        
        # Draw the line
        line.draw(self.win)
        

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None]

    def drawCanon(self,playerNr):
        
        # Get the current player cannon size
        cannon_size = self.game.getCannonSize()
        
        if self.game.getCurrentPlayerNumber() == playerNr:
            
            # Get the current player position
            pos = self.game.getCurrentPlayer().getX()
            
            # Top left corner cooridnates (x,y) of the triangle
            top_left = Point( pos - (cannon_size/2),cannon_size)
            
            # Bottom right corner cooridnates (x,y) of the triangle
            bottom_right = Point( pos + (cannon_size/2),0)
            
            # Initilaize the rectangle
            rect = Rectangle(top_left,bottom_right)
            
            # Use player specific color
            rect.setOutline(self.game.getCurrentPlayer().getColor())
            
            # Fill the rectangle with player specific color
            rect.setFill(self.game.getCurrentPlayer().getColor())
            
            # Draw the rectanlge
            rect.draw(self.win)
            
            
            return rect
        
        elif self.game.getCurrentPlayerNumber() != playerNr:
            
            pos = self.game.getOtherPlayer().getX()
            
            # Top left corner cooridnates (x,y) of the triangle
            top_left = Point( pos - (cannon_size/2),cannon_size)
            
            # Bottom right corner cooridnates (x,y) of the triangle
            bottom_right = Point( pos + (cannon_size/2),0)
            
            # Initilaize the rectangle
            rect = Rectangle(top_left,bottom_right)
            
            # Use player specific color
            rect.setOutline(self.game.getOtherPlayer().getColor())
            
            # Fill the rectangle with player specific color
            rect.setFill(self.game.getOtherPlayer().getColor())
            
            # Draw the rectanlge
            rect.draw(self.win)
            
            return rect
        
        else:
            
            return None

    def drawScore(self,playerNr):
        
        if self.game.getCurrentPlayerNumber() == playerNr:
            
            score = self.game.getCurrentPlayer().getScore()
            
            player_pos = self.game.getCurrentPlayer().getX()
            
            text_pos = Point(player_pos,-5)
            
            text = Text(text_pos,"Score : " + str(score))
            
            text.draw(self.win)
            
            return text
        
        elif self.game.getCurrentPlayerNumber() != playerNr:
            
            score = self.game.getOtherPlayer().getScore()
            
            player_pos = self.game.getOtherPlayer().getX()
            
            text_pos = Point(player_pos,-5)
            
            text = Text(text_pos,"Score : " + str(score))
            
            text.draw(self.win)
            
            return text
        
        else:
            
            return None

    def fire(self, angle, vel):
        
        player = self.game.getCurrentPlayer()
        
        proj = player.fire(angle, vel)

        circle_X = proj.getX()
        
        circle_Y = proj.getY()
        
        circle = Circle(Point(circle_X,circle_Y),self.game.getBallSize())
        
        circle.setFill(player.getColor())
        
        prev_circle = self.draw_projs[self.game.getCurrentPlayerNumber()]
        
        if prev_circle is not None:
            
            prev_circle.undraw()
        
        circle.draw(self.win)
            
        self.draw_projs[self.game.getCurrentPlayerNumber()] = circle
            

        while proj.isMoving():
            
            proj.update(1/50)

            # move is a function in graphics. It moves an object dx units in x direction and dy units in y direction
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            
            circle_Y = proj.getY()

            update(50)

        return proj

    def updateScore(self,playerNr):
        score_text = self.draw_scores[playerNr]
        
        if score_text is not None:
            
            score_text.undraw()
            
        new_score_text =  self.drawScore(playerNr)
        
        self.draw_scores[playerNr] = new_score_text
        
    def drawStar(self, center, radius,color):
        
        num_points = 5
        
        inner_radius = radius /2
        
        # Calculate the angle between each point of the star
        angle = 360 / (2 * num_points)

        # Create a list to store the points of the star
        points = []

        # Calculate the outer points of the star
        for i in range(num_points * 2):
            
            # Alternate between outer and inner radius
            
            r = radius if i % 2 == 0 else inner_radius

            # Calculate the angle in radians
            theta = angle * i * (math.pi / 180)

            # Calculate the x and y coordinates of the point
            x = center.getX() + r * math.cos(theta)
            y = center.getY() - r * math.sin(theta)

            # Create a Point object and add it to the list
            point = Point(x, y)
            
            points.append(point)

        # Create a Polygon object with the list of points
        star = Polygon(*points)
        
        star.setFill(color)
        
        return star
        
        
    def explode(self,playerNr):
        
        radius = self.game.getBallSize()
        
        prev_proj = self.draw_projs[playerNr]
        
        prev_proj.undraw()
        
        for i in range(radius , 2*self.game.getCannonSize()):
            
            x_pos = self.game.getOtherPlayer().getX()
            
            y_pos = self.game.getCannonSize()/2
            
            center = Point(x_pos,y_pos)
            
            star = self.drawStar(center,i,'orange')
            
            star.draw(self.win)

            
            update(40)
            
            star.undraw()
            
            
        
        

    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()

            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind)
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()
            
            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)

            if distance == 0.0:
                player.increaseScore()
                self.explode(self.game.getCurrentPlayerNumber())
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.game.newRound()

            self.game.nextPlayer()


class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()
