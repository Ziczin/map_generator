import random
import numpy as np
import time
import os
import json
from PIL import Image, ImageDraw

def rotate(x_, y_, alpha):
    alpha = np.pi*alpha
    x = x_* np.cos(alpha) - y_* np.sin(alpha)
    y = x_* np.sin(alpha) + y_* np.cos(alpha)
    return x, y

def coolRandom(massive):
    summ = 0
    for elem in massive:
        summ += elem[0]
    count = random.random()
    point = 0
    for elem in massive:
        point += elem[0]/summ
        if point >= count:
            return elem[1]

def modify(x, y, size):
    global new_map
    if 0 == x or size[0]-1 == x: return
    if 0 == y or size[1]-1 == y: return
    if random.random() > 0.5: return
    try:
        if random.random > 0.5:
            new_coords = coolRandom((
                (1/(abs(new_map[x,   y]-127)+1),    (x,     y)),
                (1/(abs(new_map[x,   y+1]-127)+1),  (x,     y+1)),
                (1/(abs(new_map[x,   y-1]-127)+1),  (x,     y-1)),
                (1/(abs(new_map[x+1, y]-127)+1),    (x+1,   y)),
                (1/(abs(new_map[x+1, y+1]-127)+1),  (x+1,   y+1)),
                (1/(abs(new_map[x+1, y-1]-127)+1),  (x+1,   y-1)),
                (1/(abs(new_map[x-1, y]-127)+1),    (x-1,   y)),
                (1/(abs(new_map[x-1, y+1]-127)+1),  (x-1,   y+1)),
                (1/(abs(new_map[x-1, y-1]-127)+1),  (x-1,   y-1))))
        else: raise ValueError
    except:
        return
    if new_map[new_coords] == new_map[x, y]:
        new_map[new_coords] += random.choice((-1, 0, 1))
    else:
        new_map[new_coords] += new_map[x, y] - new_map[new_coords]
    return
    if new_map[new_coords] < 0:
        new_map[new_coords] = 0
    if new_map[new_coords] > 255:
        new_map[new_coords] = 255

list_to_gen = [
    "16 Empty.png",
    "32 Empty.png",
    "64 Empty.png",
    "128 Empty.png",
    "256 Empty.png",
    "512 Empty.png",
    "1024 Empty.png",
    "2048 Empty.png",
    "4096 Empty.png",
    "8192 Empty.png"
    ]

if True:
    list_to_gen = list_to_gen[6]
    pass






iteration = 100
quality = 16
isNeedBetter = True
loadSinFile = False
sinFile = "sinParams.json"
power = 36

doLocal = False
localRange = (1024*16, 1024*16)
localCoordsList = [(0,0)]#[(i, i) for i in range(0, 5001, 16)]





sin_list = [{
    "scale":    random.random() / (10 + i**0.667),
    "rotate":   random.random() / 2,
    "volume":   random.random() * (3 + i**0.333),
    "param":    1 if random.random() > 0.25 else 1
    } for i in range(iteration)]

def time_format(t):
    time_to_return = ""
    if t // 3600 > 0:
        time_to_return += str(int(t // 3600)) + "h "
        t %= 3600
    if t // 60 > 0:
        time_to_return += str(int(t // 60)) + "m "
        t %= 60
    return time_to_return + str(int(t)) + "s"

def getSinValue(x, y):
    global sin_list
    value = 0
    for layer in sin_list:
        coeff = rotate(x, y, layer["rotate"])
        local = coeff[1] * layer["scale"]
        local = (1 + np.sin(local))*(-1)**layer["param"]
        local *= power*layer["volume"]
        value -= local/iteration
    return value

def timeCounter(line, new_map, current_time, start_time):
    global iteration
    ifParam = int(max(1, (iteration**0.5) * (2048/len(new_map))))
    if not line % ifParam:
        this_time = time.time()
        lastString = f"Total time: {time_format(this_time - start_time)}/ ~" +\
        f"{time_format(len(new_map)*(this_time - current_time)/ifParam)}"
        print(
            "-"*len(lastString),
            f"Layer: {line}/{len(new_map)}",
            f"Time: {round(this_time - current_time, 2)}",
            lastString,
            sep="\n")
        return time.time()
    return current_time

    
if not type(list_to_gen) in (tuple, list, dict, set, frozenset): list_to_gen = [list_to_gen]

directory = f"{time.ctime()}".replace(":", "-")
os.mkdir(directory)

if loadSinFile:
    with open(sinFile, 'r+') as f:
        sin_list = json.load(f)
with open(f'{directory}/Sin params.json', 'w+') as f:
    json.dump(sin_list, f)

def work():
    global list_to_gen, doLocal, localCoords
    for empty_file in list_to_gen:
        genName = f"===== Генерация {empty_file} ====="
        print("", "="*len(genName), genName, "="*len(genName), "", sep="\n")
        current_time = time.time()
        start_time = time.time()
        if doLocal:
            new_map = np.zeros(localRange)
            Xshift = localCoords[0]
            Yshift = localCoords[1]
        else:
            empty = Image.open(f"empty/{empty_file}")
            new_map = np.zeros(empty.size)
            Xshift = 0
            Yshift = 0
        for line in range(len(new_map)):
            for elem in range(len(new_map[line])):
                new_map[line, elem] = getSinValue(line + Xshift, elem + Yshift)
            current_time = timeCounter(line, new_map, current_time, start_time)

        print("-"*len(genName))
        if isNeedBetter and not doLocal:
            this_time = time.time()
            print(f"\n>>> Обработка {empty_file}:")
            for i in range(quality):
                if time.time() > this_time + 1:
                    print(f">>> Quality: {i}/{quality}")
                    this_time = time.time()
                for x in range(len(new_map)):
                    for y in range(len(new_map[x])):
                        modify(x, y, empty.size)
            print(f">>> Quality: {quality}/{quality}")
        #new_map -= np.min(new_map)
        #new_map *= 255/np.max(new_map)
        new_map_img = Image.fromarray(new_map)

        name = f"{directory}/" +\
               f"Size_{empty_file if doLocal else empty_file.split()[0]} " +\
               f"Iter_{iteration}"
        new_map_img = new_map_img.convert('L')
        new_map_img.save(name + ".png")

if doLocal:
    list_to_gen = []
    for localCoords in localCoordsList:
        list_to_gen = [f"{localRange}_at_{localCoords}"]
        work()
else:
    work()

    
