import time

def dump(matrix,pos=False):
    print(matrix,"\n"+matrix.getValues())
    try:
        if pos:
            string = ""
            count = 0
            for sprite in matrix:
                count += 1
                string += str(sprite.value)
                if count % matrix.size[0] == 0:
                    string += "\n"
    except:
        pass
    
def setValue(matrix,x,y,value):
    try:
        matrix.set((x,y),value)
    except:
        print("""SYNTAX: SET X Y VALUE
        EXAMPLE: SET 2 5 0
        EXAMPLE: SET 5 3 True""")

def scroll(matrix,speed,endblank,text,x=0,y=0):
    try:
        matrix.scroll(text,1-(speed/10),endblank)
    except KeyboardInterrupt: 
        pass
    except:
        print("""SYNTAX: SCROLL SPEED ENDBLANK TEXT
        EXAMPLE: SCROLL 7 1 "Hello, World!\"""")
def letter(matrix,text,x=0,y=0):
#     try:
    if len(text) > 1:
        for char in text:
            try:
                matrix.batchSet(matrix.letters[char],(int(x),int(y)))
            except KeyError:
                print("No character'"+char+"'")
            time.sleep(1)
    elif len(text) == 1:
        matrix.batchSet(matrix.letters[text],(int(x),int(y)))
#     except:
#         print("SYNTAX: LETTER CHAR [X] [Y]")

def store(matrix,char,file):
    print("Storing in file under '"+char+"'")
    file = open("letters "+file+".txt","a")
    file.write(char+" \n")
    file.write(matrix.getValues())
    file.write("\n")
    file.close()

def shift(matrix,direction,ammount):
    try:
        matrix.shift(direction,ammount)
    except:
        print("SYNTAX: SHIFT DIRECTION AMMOUNT")
        
def write(matrix,text,x=0,y=0):
    if len(text) > matrix.size[0]//6:
        print("Text is too long for the display. Showing as much as possible.")
        limit = matrix.size[0]//6
    else:
        limit = len(text)
    for char in range(limit):
        if char == 0:
            matrix.batchSet(matrix.letters[text[char]],(5*char,0))
        else:
            matrix.batchSet(matrix.letters[text[char]],(5*char+char,0))

def charset(matrix,charset,options=""):
    try:
        if "a" not in options:
            matrix.letters = {}
        print("letters "+charset+".txt")
        letterstr = open("letters "+charset+".txt","r")
        split = letterstr.read().split("\n\n")
        for item in split:
            split2 = item.split(" ")
            matrix.letters[split2[0]] = split2[1].strip("\n")
        del split,letterstr,split2
        matrix.letters[" "] = """00000
        00000
        00000
        00000
        00000"""
    except:
        pass
def test(matrix):
    
    scroll(matrix,9.5,1,"Hello, World! This is a test message!"+"     "+"".join(sorted(matrix.letters)))
        
        
        
        
        