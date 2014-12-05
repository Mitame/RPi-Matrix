import pygame,time
import pygame.gfxdraw

ledsize = 7
spacing = 16


class led(pygame.sprite.Sprite):
    def __init__(self,pos,value,onMatrix):
        self.containers = onMatrix
        pygame.sprite.Sprite.__init__(self,self.containters)
        self.Matrix = onMatrix
        self.pos = pos
        self.value = value
        self.image = pygame.surface.Surface((spacing,spacing))
        if self.value == 1:
            self.image.blit(onMatrix.on,(0,0))
        else:
            self.image.blit(onMatrix.off,(0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]*spacing,pos[1]*spacing)
    def update(self):
        if self.value == 1:
            self.image.blit(self.Matrix.on,(0,0))
        else:
            self.image.blit(self.Matrix.off,(0,0))
            
class ledmatrix(pygame.sprite.Group):
    leds = []
    def __init__(self,size,onColour,offColour,bgColour,charset="5x7"):
        self.size = size
        pygame.sprite.Group.__init__(self)
        pos = spacing // 2
        
        self.on = pygame.surface.Surface((spacing,spacing))
        self.on.fill(bgColour)
        pygame.gfxdraw.aacircle(self.on, pos, pos, ledsize, onColour)
        pygame.gfxdraw.filled_circle(self.on, pos, pos, ledsize, onColour)
        self.on.convert()
        self.off = pygame.surface.Surface((spacing,spacing))
        self.off.fill(bgColour)
        pygame.gfxdraw.aacircle(self.off, pos, pos, ledsize, offColour)
        pygame.gfxdraw.filled_circle(self.off, pos, pos, ledsize, offColour)
        self.off.convert()
        self.bgColour = bgColour
        
        try:
            self.letters = {}
            print("letters "+charset+".txt")
            letterstr = open("letters "+charset+".txt","r")
            split = letterstr.read().split("\n\n")
            for item in split:
                split2 = item.split(" ")
                self.letters[split2[0]] = split2[1].strip("\n")
            del split,letterstr,split2
            self.letters[" "] = """000"""
        except:
            print(split2)
        
    def createLEDs(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.makeLed((x,y))
                
    def set(self,pos,value):
        try:
            if value == -1:
                self.leds[self.size[0]*pos[1]+pos[0]].value = int(not self.leds[self.size[0]*pos[1]+pos[0]].value)
            elif value:
                self.leds[self.size[0]*pos[1]+pos[0]].value = 1
            else:
                self.leds[self.size[0]*pos[1]+pos[0]].value = 0
            self.leds[self.size[0]*pos[1]+pos[0]].update()
        except:
            print(pos,value)
            return 1
        
    def makeLed(self,pos):
        temp = led(pos,0,self)
        self.leds.append(temp)
        
    def getValues(self):
        string = ""
        count = 0
        for sprite in self.leds:
            count += 1
            string += str(sprite.value)
            if count % self.size[0] == 0:
                string += "\n"
        return string
    
    def scroll(self,text,speed,endblank):
        for letter in text:
            layout = self.letters[letter]
            layout2 = layout.replace("\n","")
            for column in range(len(layout.split("\n")[0])):
                self.shift("left",1)
                for line in range(len(layout.split("\n"))):
                    if layout2[line*5+column].isdecimal():
                        self.set((self.size[0]-1,line),int(layout2[line*5+column]))
                    else:
                        print("Invalid value'",(layout2[line*5+column],""),"' at",line,column)
                time.sleep(speed)
            self.shift("left",1)
            time.sleep(speed)
        if endblank:
            for a in range(self.size[0]):
                self.shift("left",1)
                time.sleep(speed)
                
    def batchSet(self,values,pos = (0,0)):
        split = values.split("\n")
        for line in range(len(split)):
            for column in range(len(split[line])):
                self.set((column+pos[0],line+pos[1]), int(split[line][column]))
                
    def shift(self,direction,ammount):
        for a in range(ammount):
            values = self.getValues()
            newValues = ""
            split = values.split("\n")
            for line in split:
                for column in range(len(line)):
                    if column != 0:
                        newValues += line[column]
                newValues += "0\n"
            self.batchSet(newValues[:-3])
    def __str__(self):
        return "LEDMatrix"+str(self.size)+"  "+str(len(self.sprites()))+" LEDs Total"