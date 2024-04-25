from PIL import Image, ImageFilter, ImageDraw

gradient = [
    (10, 20, 40),       # Дно
    (11, 25, 50),       # Придонные воды
    (12, 30, 60),       # Очень глубокая вода
    (13, 40, 71),       # Глубокая вода
    (14, 50, 85),       # Средняя вода
    (15, 60, 103),      # Неглубокая вода
    (16, 72, 120),      # Малая вода
    (17, 85, 140),      # Прибрежная вода
    (18, 100, 145),     # Лагуна
    (20, 119, 147),     # Вода около пляжа
    (23, 126, 152),     # Вода на пляжу
    (164, 154, 90),     # Пляж
    (151, 143, 80),     # Вершина пляжа
    (126, 175, 50),     # Растительность около пляжа
    (100, 200, 45),     # Небольшие заросли
    (115, 193, 64),     # Кусты
    (110, 186, 76),     # Тёпмлый лес
    (100, 170, 80),     # Обычный лес
    (103, 157, 90),     # Лесная чаща
    (115, 176, 100),    # Густой лес
    (87, 161, 97),      # Прохладный лес
    (80, 150, 90),      # Холодный лес
    (150, 170, 150),    # замшелые скалы
    (220, 220, 220),    # Скалы
    (247, 247, 247),    # Заснеженые вершины
    (255, 255, 255),    # Снежная шапка
    ]
im_list = "qwertyuiopasdfghjklzxcvbnm"
for im in im_list:
    try:
        print(im + ".png")
        original = Image.open(im + ".png")
        pix = original.load()
        grayscale = original.convert('RGB')
        draw = ImageDraw.Draw(grayscale)
        for x in range(grayscale.size[0]):
            if not x % 1000:
                print(x)
            for y in range(grayscale.size[1]):
                try:
                    draw.point((x, y), (gradient[pix[x, y]//10]))
                except:
                    print(pix[x, y]//10)
                
        grayscale.save(im + " color.png")
    except: continue











            
