import Boxmaker

import json
from reportlab.lib.colors import black
from reportlab.lib.colors import red
from reportlab.lib.colors import blue
from reportlab.lib.colors import green
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

PLATE_LENGTH = 1000
PLATE_WIDTH = 500
MATERIAL_THICKNESS = 5

BOX_LENGTH = 220
BOX_WIDTH = 140
BOX_INNER_HEIGHT = 5 * MATERIAL_THICKNESS 

CUT_WIDTH = 0.01

SCREEN_POSITION_X = 8
SCREEN_POSITION_Y = 15
SCREEN_WIDTH = 194
SCREEN_HEIGHT = 111
SCREEN_TO_SCREW1X = 36
SCREEN_TO_SCREW2X = 162
SCREEN_TO_SCREW1Y = 22
SCREEN_TO_SCREW2Y = 87.5
RADIUS = 1.5

SCREEN_TO_METALX1 = 14
SCREEN_TO_METALX2 = 184
SCREEN_TO_METALY1 = 6
SCREEN_TO_METALY2 = 108

marginxTop = 20
marginxBottom = 62
marginx = 70
marginy = 10

##### preparation (box and field)
box = Boxmaker.Box(BOX_LENGTH, BOX_INNER_HEIGHT + MATERIAL_THICKNESS, BOX_WIDTH, MATERIAL_THICKNESS, CUT_WIDTH, 2.5*MATERIAL_THICKNESS)
box._compute_dimensions()

def drawField(X, Y, width, lineNum, flip = 1):
	with open("field.json", "r") as inputfile:
		iso = json.loads(inputfile.read())
	preparedCurves = []
	for curve in iso:
		x = curve[0]
		y = curve[1]
		scale = width/(y[-1]-y[0])
		xp = x[::-1] + x
		yp = map(lambda x: -x, y[::-1]) + y
		x0 = xp[0]
		y0 = yp[0]
		xpp = map(lambda x: flip * scale*(x - x0) + X, xp)
		ypp = map(lambda x: scale*(x - y0) + Y, yp)
		preparedCurves += [[xpp, ypp]]

	x = preparedCurves[lineNum][0]
	y = preparedCurves[lineNum][1]
	xprev = x[0]
	yprev = y[0]
	for x,y in zip(x[1:],y[1:]):
		box._draw_line(xprev, yprev, x, y)
		xprev = x
		yprev = y


################# render the top part
box._initialize_document("6box_wood.pdf", PLATE_LENGTH, PLATE_WIDTH)
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(marginxTop, marginy)

# the field
drawField(marginxTop + BOX_LENGTH - MATERIAL_THICKNESS, marginy, BOX_WIDTH/2, 0)
drawField(marginxTop + MATERIAL_THICKNESS, marginy, BOX_WIDTH/2, 0, -1)

# text and logo
# pdfmetrics.registerFont(TTFont('remington', 'Remington-Noiseless.ttf'))
# pdfmetrics.registerFont(TTFont('raleway', 'Raleway-Medium.ttf'))
# box._doc.setFont('remington', 18)
# box._write(marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH + 3 , marginy + 90, "6element")
# box._doc.setFont('raleway', 9)
# box._write(marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH + 15, marginy + 80, "par")
# logo = svg2rlg.readFile("logo.svg")
# width = 18
# box._place_logo(logo, marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH + 8, marginy + 53, width, width*180/156)
# box._doc.setFont('raleway', 4)
# box._write(marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH + 4, marginy + 45, "En cas de soucis :")
# box._write(marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH + 4, marginy + 40, "http://ants.builders/support")

# draw the screen
box._doc.setStrokeColor(green)
box._draw_line(marginxTop + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y)
box._draw_line(marginxTop + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT, marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginxTop + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginxTop + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y, marginxTop + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
# screws
box._draw_circle(marginxTop + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginxTop + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginxTop + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginxTop + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)

#draw to metal part
box._doc.setStrokeColor(red)
box._draw_line(marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginxTop + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1)
box._draw_line(marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2, marginxTop + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginxTop + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)



################## render the bottom part
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(marginxBottom, 2 * marginy + BOX_WIDTH)

# the field
drawField(marginxBottom + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 6)
drawField(marginxBottom + MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 6, -1)

def draw_side(x, y, attach_height, fieldnum, fliph = 1, colorout = green, colorin = green):
	box._doc.setStrokeColor(colorout)
	drawField(x, y, BOX_WIDTH/2, fieldnum, fliph)
	attach_width = 15
	etiration = fliph * 1.5
	insert_length = fliph * 10
	insert_width = 5
	box._draw_line(x, y, x, y + MATERIAL_THICKNESS)
	box._draw_line(x, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS)
	box._draw_line(x - insert_length, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS + insert_width)
	box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x - insert_length, y + MATERIAL_THICKNESS + insert_width)
	
	box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x, y + attach_height - attach_width/2)
	box._draw_bezier(x, y + attach_height - attach_width/2 ,
		x - (SCREEN_POSITION_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height - attach_width/2 ,
		x - (SCREEN_POSITION_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height + attach_width/2 ,
		x, y + attach_height + attach_width/2)
	

	box._draw_line(x, y + attach_height + attach_width/2, x,  BOX_WIDTH + y - MATERIAL_THICKNESS - insert_width )
	box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width)
	box._draw_line(x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS  )
	box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS)
	box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x, y + BOX_WIDTH)
	box._doc.setStrokeColor(colorin)
	if fliph == 1:
		box._draw_circle(x - (SCREEN_POSITION_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
		box._draw_circle(x - (SCREEN_POSITION_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X), y + attach_height, RADIUS)
	else:
		box._draw_circle(x - (SCREEN_POSITION_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
		box._draw_circle(x - (SCREEN_POSITION_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*fliph, y + attach_height, RADIUS)

for i in [5 ,4, 3, 2, 1]:
	draw_side(marginxBottom + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, i)
	draw_side(marginxBottom  + MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, i, -1)


draw_side(marginxBottom + 285, marginy, BOX_WIDTH - (SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y), 1)
draw_side(marginxBottom  + 230, marginy, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, 1, -1)
draw_side(marginxBottom + 417, marginy, BOX_WIDTH - (SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y), 4)
draw_side(marginxBottom  + 365, marginy, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, 4, -1)
draw_side(marginxBottom + 375, marginy + BOX_WIDTH, BOX_WIDTH - (SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y), 2)
draw_side(marginxBottom  + 320, marginy + BOX_WIDTH, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, 2, -1)
draw_side(marginxBottom + 360, marginy + 2*BOX_WIDTH, BOX_WIDTH - (SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y), 3)
draw_side(marginxBottom  + 300, marginy + 2*BOX_WIDTH, SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, 3, -1)


# screws
box._doc.setStrokeColor(red)
box._draw_circle(marginxBottom + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginxBottom + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginxBottom + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginxBottom + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)


################# render the sides parts
box._doc.setStrokeColor(blue)
www = 2*BOX_WIDTH

box._draw_width_by_height_side(marginx, 3 * marginy + www)
box._draw_line(marginx + MATERIAL_THICKNESS, 3 * marginy + www + MATERIAL_THICKNESS, marginx + MATERIAL_THICKNESS, 3 * marginy + www + BOX_INNER_HEIGHT)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + www + MATERIAL_THICKNESS, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + www + BOX_INNER_HEIGHT)

box._draw_width_by_height_side(marginx, 4 * marginy + (BOX_INNER_HEIGHT + MATERIAL_THICKNESS) + www)
box._draw_line(marginx + MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + 2*MATERIAL_THICKNESS + www, marginx + MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + MATERIAL_THICKNESS + www + BOX_INNER_HEIGHT)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + 2*MATERIAL_THICKNESS + www, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + MATERIAL_THICKNESS + www + BOX_INNER_HEIGHT)

box._doc.setStrokeColor(red)
box._draw_rectangle(marginx + 40, 4 * marginy + (BOX_INNER_HEIGHT + MATERIAL_THICKNESS) + www +  (BOX_INNER_HEIGHT + MATERIAL_THICKNESS)/2 -3, 10, 5)


################ sides



box._doc.save()
