import threading,time,os
import Commands as commands
from MatrixObjects import *

global ledsize,spacing,matrix
ledsize = 7
spacing = 16
grid = 40,14


pygame.font.init()
ledText = pygame.font.SysFont("Ubuntu Mono", 10)

screen = pygame.display.set_mode((spacing*grid[0],spacing*grid[1]))

matrix = ledmatrix((grid[0],grid[1]),(0,255,0),(20,20,20),(0,0,0))
led.containters = matrix
matrix.createLEDs()
print(matrix.on)

def commandLine(matrix):
    global split,command
    while 1:
        command = input(">")
        split = list(command.split(" "))
        split[0] = split[0].lower()
        if type(split) != list:
            split = (matrix,command,"")
            
            
        if split[0] == "print":
            if len(split) == 2:
                commands.dump(matrix,split[1])
            else:
                commands.dump(matrix)
        elif split[0] == "set":
            commands.setValue(matrix,(int(split[1]),int(split[2])),int(split[3]))
        elif split[0] == "scroll":
            if len(split) >= 4:
                if "." in split[1]:
                    speed = float(split[1])
                else:
                    speed = int(split[1])
                commands.scroll(matrix,speed,int(split[2])," ".join(split[3:]))
            else:
                print("Command requires 3 elements")
        elif split[0] == "scroll2":
            if len(split) >= 4:
                commands.scroll(matrix,int(split[-2]),int(split[-1])," ".join(split[1:-2]))
            else:
                print("Command requires 3 elements")
        elif split[0] == "letter":
            if len(split) == 4:
                commands.letter(matrix,split[1],split[2],split[3])
            elif len(split) in (2,3):
                commands.letter(matrix,split[1])
        elif split[0] == "store":
            commands.store(matrix)
        elif split[0] == "shift":
            commands.shift(matrix)
        elif split[0] == "write":
            if len(split) >= 4:
                if split[-1].isdecimal() and split[len(split)].isdecimal():
                    commands.write(matrix," ".join(split[1:-1]),int(split[-1]),int(split[len(split)]))
                    continue
            commands.write(matrix," ".join(split[1:]))
        elif split[0] == "charset":
            commands.charset(matrix,split[1])
        elif split[0] == "repeat":
            print("Press S to stop")
        elif split[0] == "test":
            commands.test(matrix)
        elif split[0] in ["exit","quit"]:
            os._exit(0)
        else:
            print("Unrecognised command '"+split[0]+"'")
commandsThread = threading.Thread(group=None, target=commandLine, name = "Commands", kwargs = {"matrix":matrix})
commandsThread.start()



while 1:
#     if not commandsThread.is_alive():
#         del(commandsThread)
#         commandsThread = threading.Thread(group=None, target=commandLine, name = "Commands", kwargs = {"matrix":matrix})
#         commandsThread.start()
    start = time.time()
    screen.fill((0,0,0))
    matrix.draw(screen)
    pygame.display.flip()
    pygame.event.pump()
    if pygame.event.peek(pygame.QUIT):
        os._exit(0)
    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
        pos = event.pos
        x,y = pos[0]//spacing,pos[1]//spacing
        matrix.set((x,y),-1)
    pygame.event.clear()
    wait = 1/30-(time.time()-start)
    if wait < 0:
        print(wait)
        continue
    else:
        time.sleep(wait)     