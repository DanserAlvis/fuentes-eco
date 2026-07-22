"""Build ECO Sumiha Beta, an original low-coverage humanist text face.

The design is generated from an original continuous-stroke skeleton. It does
not contain ink-saving holes or outlines copied from another typeface.
"""
from math import cos, pi, sin
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / "_deps"))

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.removeOverlaps import removeOverlaps

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
UPM = 1000
ADVANCE = 600
STROKE = 69


def polygon(pen, points):
    pen.moveTo(points[0])
    for point in points[1:]:
        pen.lineTo(point)
    pen.closePath()


def round_node(pen, point, diameter, sides=16):
    radius = diameter / 2
    x, y = point
    polygon(pen, [(round(x + radius*cos(-2*pi*i/sides)),
                   round(y + radius*sin(-2*pi*i/sides))) for i in range(sides)])


def segment(pen, a, b, width=STROKE):
    x1, y1 = a
    x2, y2 = b
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5 or 1
    # Humanist contrast: horizontal strokes are lighter than verticals.
    effective_width = width * (0.77 + 0.23 * abs(dy) / length)
    nx, ny = -dy / length * effective_width / 2, dx / length * effective_width / 2
    polygon(pen, [(round(x1 + nx), round(y1 + ny)),
                  (round(x2 + nx), round(y2 + ny)),
                  (round(x2 - nx), round(y2 - ny)),
                  (round(x1 - nx), round(y1 - ny))])


def stroked(paths, width=STROKE):
    pen = TTGlyphPen(None)
    for path in paths:
        for a, b in zip(path, path[1:]):
            segment(pen, a, b, width)
        for index, point in enumerate(path):
            # Full caps belong at terminals and sharp extrema such as A/V.
            # Smooth sampled curves and right-angle corners use compact joins,
            # avoiding the beads previously visible on E, F and numerals.
            sharp_aligned_extreme = False
            if 0 < index < len(path) - 1 and point[1] in (DESC, 0, XH, CAP):
                previous, following = path[index - 1], path[index + 1]
                strict_extreme = ((point[1] > previous[1] and point[1] > following[1]) or
                                  (point[1] < previous[1] and point[1] < following[1]))
                va = (previous[0] - point[0], previous[1] - point[1])
                vb = (following[0] - point[0], following[1] - point[1])
                la = (va[0] ** 2 + va[1] ** 2) ** 0.5 or 1
                lb = (vb[0] ** 2 + vb[1] ** 2) ** 0.5 or 1
                corner_cosine = (va[0] * vb[0] + va[1] * vb[1]) / (la * lb)
                sharp_aligned_extreme = strict_extreme and corner_cosine > -0.8
            diameter = width if index in (0, len(path) - 1) or sharp_aligned_extreme else width * 0.78
            round_node(pen, point, diameter)
    return pen.glyph()


def dot(x, y, size=STROKE):
    pen = TTGlyphPen(None)
    round_node(pen, (x, y), size)
    return pen.glyph()


def arc(cx, cy, rx, ry, start, end, steps=9):
    steps = max(steps, 24)
    return [(round(cx + rx*cos((start+(end-start)*i/steps)*pi/180)),
             round(cy + ry*sin((start+(end-start)*i/steps)*pi/180))) for i in range(steps+1)]


def cubic(p0, p1, p2, p3, steps=12):
    points = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        points.append((round(u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]),
                       round(u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])))
    return points


L, C, R = 90, 300, 510
CAP, XH, DESC = 700, 500, -180


UPPER = {
    'A': [[(L,0),(C,CAP),(R,0)],[(160,260),(440,260)]],
    'B': [[(L,0),(L,CAP)],cubic((L,CAP),(390,CAP),(500,650),(485,520),12)+cubic((485,520),(475,405),(390,360),(L,360),10)[1:],cubic((L,360),(410,360),(510,285),(500,155),12)+cubic((500,155),(490,35),(390,0),(L,0),10)[1:]],
    'C': [arc(305,350,220,357,45,315,12)],
    'D': [[(L,0),(L,CAP)],cubic((L,CAP),(390,CAP),(510,575),(510,350),14)+cubic((510,350),(510,125),(390,0),(L,0),14)[1:]],
    'E': [[(R,CAP),(L,CAP),(L,0),(R,0)],[(L,350),(430,350)]],
    'F': [[(L,0),(L,CAP),(R,CAP)],[(L,350),(430,350)]],
    'G': [arc(305,350,220,357,30,330,14),[(496,172),(496,300),(360,300)]],
    'H': [[(L,0),(L,CAP)],[(R,0),(R,CAP)],[(L,350),(R,350)]],
    'I': [[(70,CAP),(370,CAP)],[(220,CAP),(220,0)],[(70,0),(370,0)]],
    'J': [[(120,CAP),(R,CAP)],cubic((R,CAP),(R,170),(500,25),(310,0),15)+cubic((310,0),(210,-5),(135,35),(105,120),8)[1:]],
    'K': [[(L,0),(L,CAP)],[(R,CAP),(L,315),(R,0)]],
    'L': [[(L,CAP),(L,0),(R,0)]],
    'M': [[(L,0),(L,CAP),(C,330),(R,CAP),(R,0)]],
    'N': [[(L,0),(L,CAP),(R,0),(R,CAP)]],
    'O': [arc(C,350,220,357,0,360,16)],
    'P': [[(L,0),(L,CAP)],cubic((L,CAP),(405,CAP),(510,625),(500,515),12)+cubic((500,515),(490,390),(385,350),(L,350),12)[1:]],
    'Q': [arc(C,350,220,357,0,360,16),[(350,150),(530,-40)]],
    'R': [[(L,0),(L,CAP)],cubic((L,CAP),(405,CAP),(510,625),(500,515),12)+cubic((500,515),(490,390),(385,350),(L,350),12)[1:],[(330,350),(R,0)]],
    'S': [cubic((500,610),(430,735),(150,730),(95,575),10)+cubic((95,575),(45,405),(520,350),(500,145),12)[1:]+cubic((500,145),(480,-25),(180,-35),(80,90),10)[1:]],
    'T': [[(L,CAP),(R,CAP)],[(C,CAP),(C,0)]],
    'U': [[(L,CAP),(L,170)]+cubic((L,170),(L,45),(185,0),(300,0),10)[1:]+cubic((300,0),(430,0),(R,55),(R,170),10)[1:]+[(R,CAP)]],
    'V': [[(L,CAP),(C,0),(R,CAP)]],
    'W': [[(60,CAP),(155,0),(300,390),(445,0),(540,CAP)]],
    'X': [[(L,CAP),(R,0)],[(R,CAP),(L,0)]],
    'Y': [[(L,CAP),(C,370),(R,CAP)],[(C,370),(C,0)]],
    'Z': [[(L,CAP),(R,CAP),(L,0),(R,0)]],
}


LOWER = {
    'a': [arc(280,240,175,240,0,360,14),cubic((455,0),(455,160),(455,340),(455,500),8)],
    'b': [[(110,0),(110,700)],cubic((110,360),(205,520),(390,525),(470,390),10)+cubic((470,390),(540,260),(485,60),(350,10),12)[1:]+cubic((350,10),(230,-25),(145,60),(110,155),9)[1:]],
    'c': [arc(300,250,190,256,42,318,11)],
    'd': [[(470,0),(470,700)],cubic((470,360),(390,520),(205,525),(125,390),10)+cubic((125,390),(55,260),(110,60),(245,10),12)[1:]+cubic((245,10),(365,-25),(445,60),(470,155),9)[1:]],
    'e': [[(120,260),(455,260)]
          +cubic((455,260),(455,420),(385,500),(300,500),9)[1:]
          +cubic((300,500),(175,500),(105,400),(105,250),10)[1:]
          +cubic((105,250),(105,100),(200,0),(300,0),10)[1:]
          +cubic((300,0),(390,0),(455,50),(480,110),7)[1:]],
    'f': [[(235,0),(235,555)]+cubic((235,555),(235,665),(325,725),(440,690),10)[1:],[(100,480),(375,480)]],
    'g': [arc(280,250,175,256,0,360,14),[(455,500),(455,-65)]+cubic((455,-65),(455,-175),(335,-215),(215,-180),10)[1:]+cubic((215,-180),(150,-165),(105,-125),(100,-80),7)[1:]],
    'h': [[(110,0),(110,700)],cubic((110,330),(175,465),(275,515),(365,490),9)+cubic((365,490),(450,465),(470,390),(470,300),8)[1:]+[(470,0)]],
    'i': [[(170,0),(170,500)],[(170,605),(170,610)]],
    'j': [[(245,500),(245,-70)]+cubic((245,-70),(245,-165),(170,-205),(90,-180),8)[1:]+cubic((90,-180),(45,-165),(20,-130),(25,-95),5)[1:],[(245,605),(245,610)]],
    'k': [[(110,0),(110,700)],[(470,500),(110,205),(480,0)]],
    'l': [[(170,700),(170,80)]+cubic((170,80),(170,25),(195,0),(235,0),6)[1:]],
    'm': [[(70,0),(70,500)],cubic((70,340),(125,475),(210,515),(270,450),8)+cubic((270,450),(300,415),(300,350),(300,280),6)[1:]+[(300,0)],cubic((300,340),(355,475),(445,515),(505,450),8)+cubic((505,450),(535,415),(535,350),(535,280),6)[1:]+[(535,0)]],
    'n': [[(110,0),(110,500)],cubic((110,335),(175,470),(275,515),(365,490),9)+cubic((365,490),(450,465),(470,390),(470,300),8)[1:]+[(470,0)]],
    'o': [arc(300,250,190,256,0,360,14)],
    'p': [[(110,-180),(110,500)],arc(285,250,175,256,-90,270,14)],
    'q': [[(470,-180),(470,500)],arc(295,250,175,256,-270,90,14)],
    'r': [[(130,0),(130,500)],cubic((130,335),(195,465),(300,520),(430,445),10)],
    's': [cubic((475,420),(410,520),(170,530),(100,410),9)+cubic((100,410),(45,285),(500,245),(475,80),10)[1:]+cubic((475,80),(450,-20),(180,-25),(95,70),9)[1:]],
    't': [[(285,650),(285,105)]+cubic((285,105),(285,30),(340,0),(435,0),7)[1:],[(125,480),(405,480)]],
    'u': [[(110,500),(110,155)]+cubic((110,155),(110,45),(195,0),(300,0),9)[1:]+cubic((300,0),(405,0),(470,70),(470,165),9)[1:]+[(470,500)],[(470,0),(470,500)]],
    'v': [[(100,500),(300,0),(500,500)]],
    'w': [[(60,500),(155,0),(300,315),(445,0),(540,500)]],
    'x': [[(110,500),(490,0)],[(490,500),(110,0)]],
    'y': [[(100,500),(300,0)],[(500,500),(300,0)]+cubic((300,0),(260,-105),(220,-175),(115,-185),9)[1:]],
    'z': [[(110,500),(490,500),(110,0),(490,0)]],
}


DIGITS = {
    '0': [arc(C,350,180,357,0,360,16)],
    '1': [[(180,570),(300,CAP),(300,0)],[(160,0),(450,0)]],
    '2': [cubic((100,570),(125,690),(225,720),(340,720),9)
          +cubic((340,720),(465,720),(520,645),(495,550),8)[1:]
          +cubic((495,550),(465,445),(330,315),(100,0),12)[1:]+[(510,0)]],
    '3': [cubic((105,610),(165,725),(390,750),(485,620),10)
          +cubic((485,620),(520,505),(430,395),(330,350),9)[1:]
          +cubic((330,350),(450,325),(515,225),(490,110),9)[1:]
          +cubic((490,110),(445,-20),(180,-30),(95,85),10)[1:]],
    '4': [[(430,0),(430,CAP),(80,220),(520,220)]],
    '5': [[(490,CAP),(130,CAP),(105,390)]
          +cubic((105,390),(220,425),(395,430),(480,320),9)[1:]
          +cubic((480,320),(560,205),(500,55),(390,5),9)[1:]
          +cubic((390,5),(270,-35),(145,-5),(90,80),8)[1:]],
    '6': [cubic((470,620),(405,725),(220,735),(125,570),10)
          +cubic((125,570),(65,455),(80,190),(120,130),10)[1:]
          +cubic((120,130),(175,-20),(420,-35),(490,120),11)[1:]
          +cubic((490,120),(540,280),(430,405),(290,400),10)[1:]
          +cubic((290,400),(190,400),(125,350),(105,300),8)[1:]],
    '7': [[(80,CAP),(520,CAP),(230,0)]],
    '8': [arc(C,525,180,182,0,360,12),arc(C,175,200,182,0,360,12)],
    '9': [arc(300,480,190,220,0,360,14),
          cubic((490,500),(505,310),(480,120),(390,25),10)
          +cubic((390,25),(325,-30),(205,-20),(135,65),8)[1:]],
}


PUNCT = {
    '-': [[(170,250),(430,250)]], '_': [[(70,-80),(530,-80)]],
    '+': [[(130,300),(470,300)],[(300,130),(300,470)]],
    '=': [[(140,360),(460,360)],[(140,210),(460,210)]],
    '/': [[(100,-60),(500,700)]], '\\': [[(100,700),(500,-60)]],
    '|': [[(300,-100),(300,700)]], '<': [[(450,520),(150,300),(450,80)]],
    '>': [[(150,520),(450,300),(150,80)]],
    '[': [[(390,700),(200,700),(200,-150),(390,-150)]],
    ']': [[(210,700),(400,700),(400,-150),(210,-150)]],
    '(': [arc(400,275,190,430,110,250,10)], ')': [arc(200,275,190,430,-70,70,10)],
    '{': [[(410,700),(300,660),(270,480),(190,390),(270,300),(300,50),(410,0)]],
    '}': [[(190,700),(300,660),(330,480),(410,390),(330,300),(300,50),(190,0)]],
    '?': [cubic((110,585),(135,720),(390,755),(485,625),10)
          +cubic((485,625),(535,500),(430,400),(300,330),9)[1:]+[(300,225)],
          [(300,75),(300,80)]],
    '!': [[(300,700),(300,185)],[(300,75),(300,80)]],
    ':': [], ';': [], '.': [], ',': [], '"': [[(220,700),(200,560)],[(380,700),(360,560)]],
    "'": [[(300,700),(280,560)]],
    '#': [[(200,0),(260,700)],[(350,0),(410,700)],[(100,470),(500,470)],[(80,220),(480,220)]],
    '%': [[(100,0),(500,700)],arc(170,580,75,90,0,360,8),arc(430,120,75,90,0,360,8),
    ], '&': [[(500,0),(170,420),(150,570),(240,700),(380,650),(390,520),(100,210),(110,80),(200,0),(350,0),(500,170)]],
    '*': [[(300,600),(300,250)],[(150,520),(450,330)],[(450,520),(150,330)]],
    '–': [[(130,250),(470,250)]], '—': [[(50,250),(550,250)]],
    '·': [], '•': [], '…': [],
    '“': [[(220,620),(245,740)],[(380,620),(405,740)]],
    '”': [[(220,700),(195,580)],[(380,700),(355,580)]],
    '‘': [[(300,620),(325,740)]], '’': [[(300,700),(275,580)]],
    '@': [arc(300,330,230,310,20,340,14),arc(305,340,120,150,0,360,10),[(425,490),(425,210),(500,210)]],
    '$': [[(300,760),(300,-70)],[(480,610),(405,700),(190,700),(100,590),(130,440),(455,270),(485,100),(400,0),(175,0),(90,80)]],
    '€': [arc(330,350,210,350,45,315,12),[(80,420),(390,420)],[(70,270),(360,270)]],
    '£': [[(440,620),(380,700),(230,700),(150,610),(180,0),(500,0)],[(100,350),(390,350)]],
    '¥': [[(90,700),(300,390),(510,700)],[(300,390),(300,0)],[(130,280),(470,280)],[(130,160),(470,160)]],
    '°': [arc(300,600,95,100,0,360,10)], '×': [[(140,500),(460,100)],[(460,500),(140,100)]],
}


def base_glyphs():
    glyphs = {'.notdef': stroked([[(80,0),(80,700),(520,700),(520,0),(80,0)],[(160,100),(440,600)],[(160,600),(440,100)]])}
    for char, paths in {**UPPER, **LOWER, **DIGITS, **PUNCT}.items():
        glyphs[f'u{ord(char):04X}'] = stroked(paths)
    glyphs['space'] = TTGlyphPen(None).glyph()
    glyphs['u002E'] = dot(150, 25)
    glyphs['u002C'] = stroked([[(170,30),(110,-120)]])
    glyphs['u003A'] = TTGlyphPen(None).glyph()
    pen = TTGlyphPen(None); round_node(pen,(150,440),50); round_node(pen,(150,60),50); glyphs['u003A'] = pen.glyph()
    pen = TTGlyphPen(None); round_node(pen,(150,440),50); segment(pen,(170,50),(110,-100)); glyphs['u003B'] = pen.glyph()
    glyphs['u00B7'] = dot(300, 280)
    glyphs['u2022'] = dot(300, 280, 72)
    pen = TTGlyphPen(None)
    for x in (155,300,445): polygon(pen, [(x-18,7),(x+18,7),(x+18,43),(x-18,43)])
    glyphs['u2026'] = pen.glyph()
    glyphs['dotlessi'] = stroked([[(170,0),(170,500)]])
    glyphs['acute.cap'] = stroked([[(230,775),(375,855)]], 42)
    glyphs['acute.low'] = stroked([[(230,585),(365,665)]], 42)
    glyphs['acute.i.cap'] = stroked([[(115,775),(245,855)]], 42)
    glyphs['acute.i.low'] = stroked([[(105,585),(230,665)]], 42)
    glyphs['tilde.cap'] = stroked([cubic((155,810),(225,880),(310,755),(445,830),12)], 44)
    glyphs['tilde.low'] = stroked([cubic((155,610),(225,680),(310,555),(445,630),12)], 44)
    pen = TTGlyphPen(None); round_node(pen, (210,805), 48, 16); round_node(pen, (390,805), 48, 16); glyphs['dieresis.cap'] = pen.glyph()
    pen = TTGlyphPen(None); round_node(pen, (210,610), 48, 16); round_node(pen, (390,610), 48, 16); glyphs['dieresis.low'] = pen.glyph()
    return glyphs


def composite(glyphs, base, mark):
    pen = TTGlyphPen(glyphs)
    pen.addComponent(base, (1,0,0,1,0,0))
    pen.addComponent(mark, (1,0,0,1,0,0))
    return pen.glyph()


def main():
    glyphs = base_glyphs()
    cmap = {32:'space'}
    for char in list(UPPER) + list(LOWER) + list(DIGITS) + list(PUNCT):
        cmap[ord(char)] = f'u{ord(char):04X}'
    accents = {
        'Á':('A','acute.cap'),'É':('E','acute.cap'),'Í':('I','acute.i.cap'),'Ó':('O','acute.cap'),'Ú':('U','acute.cap'),
        'á':('a','acute.low'),'é':('e','acute.low'),'í':(None,'acute.i.low'),'ó':('o','acute.low'),'ú':('u','acute.low'),
        'Ñ':('N','tilde.cap'),'ñ':('n','tilde.low'),'Ü':('U','dieresis.cap'),'ü':('u','dieresis.low'),
    }
    for char,(base,mark) in accents.items():
        name=f'u{ord(char):04X}'
        base_name='dotlessi' if char=='í' else f'u{ord(base):04X}'
        glyphs[name]=composite(glyphs,base_name,mark); cmap[ord(char)]=name
    # Spanish inverted punctuation.
    glyphs['u00A1']=stroked([[(300,515),(300,0)],[(300,620),(300,625)]]); cmap[0xA1]='u00A1'
    glyphs['u00BF']=stroked([[(300,475),(300,365)]
                              +cubic((300,365),(175,300),(80,215),(105,105),9)[1:]
                              +cubic((105,105),(135,-25),(400,-30),(485,105),10)[1:],
                              [(300,585),(300,590)]]); cmap[0xBF]='u00BF'
    for name in ('u002E','u002C','u003A','u003B'):
        cmap[int(name[1:],16)]=name
    order=list(glyphs)
    # Derive proportional advances from the actual outline bounds. The glyph
    # coordinates already include their intended left space, so mirroring it
    # on the right produces optically centered, internally consistent metrics.
    metrics = {}
    for name, glyph in glyphs.items():
        coordinates = getattr(glyph, 'coordinates', None)
        if coordinates:
            xs = [point[0] for point in coordinates]
            x_min, x_max = min(xs), max(xs)
            metrics[name] = (max(200, round(x_max + x_min)), round(x_min))
        else:
            metrics[name] = (600, 0)
    metrics['space'] = (275, 0)
    for char, (base, _mark) in accents.items():
        base_name = 'dotlessi' if char == 'í' else f'u{ord(base):04X}'
        metrics[f'u{ord(char):04X}'] = metrics[base_name]
    fb=FontBuilder(UPM,isTTF=True)
    fb.setupGlyphOrder(order); fb.setupCharacterMap(cmap); fb.setupGlyf(glyphs); fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900,descent=-220,lineGap=80)
    fb.setupNameTable({'familyName':'ECO Sumiha Beta','styleName':'Regular','uniqueFontIdentifier':'ShiroLabs; ECO Sumiha Beta Regular; 0.500','fullName':'ECO Sumiha Beta Regular','psName':'ECOSumihaBeta-Regular','version':'Version 0.500','copyright':'Copyright 2026 Shiro Labs. All rights reserved.','licenseDescription':'Licensed under the Shiro Labs ECO Sumiha Free Beta License 1.0. Free for personal, academic and internal evaluation use only. Commercial production, redistribution, modification and embedding require written permission.','licenseInfoURL':'https://github.com/DanserAlvis/fuentes-eco/blob/main/LICENSES/ECO-SUMIHA-BETA-LICENSE.txt'})
    fb.setupOS2(sTypoAscender=900,sTypoDescender=-220,sTypoLineGap=80,usWinAscent=900,usWinDescent=220,usWeightClass=300,usWidthClass=5,fsType=2)
    fb.setupPost(underlinePosition=-120,underlineThickness=45); fb.setupMaxp()
    removeOverlaps(fb.font, removeHinting=True, ignoreErrors=False)
    OUT.mkdir(exist_ok=True)
    path=OUT/'ECO-Sumiha-Beta-Regular.ttf'; fb.save(path); print(path)


if __name__=='__main__': main()
