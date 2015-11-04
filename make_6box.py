import Boxmaker

import json
from reportlab.lib.colors import black
from reportlab.lib.colors import red
from reportlab.lib.colors import blue
from reportlab.lib.colors import green
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

PLATE_LENGTH = 1530
PLATE_WIDTH = 1000
MATERIAL_THICKNESS = 5

BOX_LENGTH = 220
BOX_WIDTH = 140
BOX_INNER_HEIGHT = 18

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

marginx = 100
marginy = 20

##### preparation (box and field)
box = Boxmaker.Box(BOX_LENGTH, BOX_INNER_HEIGHT + MATERIAL_THICKNESS, BOX_WIDTH, MATERIAL_THICKNESS, CUT_WIDTH, 2.5*MATERIAL_THICKNESS)
box._compute_dimensions()

def drawField(X, Y, width, lineNum, flip = False):
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
		if flip:
			xpp = map(lambda x: -scale*(x - x0) + X, xp)
		else:
			xpp = map(lambda x: scale*(x - x0) + X, xp)
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
box._initialize_document("all.pdf", PLATE_LENGTH, PLATE_WIDTH)
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(marginx, marginy)

# the field
drawField(marginx + BOX_LENGTH - MATERIAL_THICKNESS, marginy, BOX_WIDTH/2, 1)
drawField(marginx + MATERIAL_THICKNESS, marginy, BOX_WIDTH/2, 0, True)

# text and logo
pdfmetrics.registerFont(TTFont('remington', 'Remington-Noiseless.ttf'))
pdfmetrics.registerFont(TTFont('raleway', 'Raleway-Medium.ttf'))
box._doc.setFont('remington', 18)
box._write(marginx + SCREEN_POSITION_X + SCREEN_WIDTH + 3 , marginy + 90, "6element")
box._doc.setFont('raleway', 9)
box._write(marginx + SCREEN_POSITION_X + SCREEN_WIDTH + 15, marginy + 80, "par")
logo = ImageReader('logo.png')
width = 18
box._place_logo(logo, marginx + SCREEN_POSITION_X + SCREEN_WIDTH + 8, marginy + 53, width, width*180/156)
box._doc.setFont('raleway', 6)
box._write(marginx + SCREEN_POSITION_X + SCREEN_WIDTH + 3, marginy + 45, "En cas de soucis :")
box._write(marginx + SCREEN_POSITION_X + SCREEN_WIDTH + 3, marginy + 40, "http://ants.builders/support")

# draw the screen
box._doc.setStrokeColor(green)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
# screws
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)

#draw to metal part
box._doc.setStrokeColor(red)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2, marginx + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)



################## render the bottom part
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(marginx, 2 * marginy + BOX_WIDTH)

# the field
drawField(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 7)
drawField(marginx + MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 7, True)


box._doc.setStrokeColor(green)
drawField(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 6)
attach_width = 15
etiration=2.2
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y - attach_width/2)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y + attach_width/2, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y - attach_width/2)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y + attach_width/2, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + 2*BOX_WIDTH)
box._draw_bezier(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y - attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS - (SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y - attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS - (SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y + attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y + attach_width/2)
box._draw_bezier(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y - attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS - (SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y - attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS - (SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y + attach_width/2 ,
	marginx + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y + attach_width/2)
# screws
box._doc.setStrokeColor(red)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)


################# render the sides parts
box._doc.setStrokeColor(blue)
box._draw_width_by_height_side(marginx, 3 * marginy + 2 * BOX_WIDTH)
box._draw_line(marginx + MATERIAL_THICKNESS, 3 * marginy + 2 * BOX_WIDTH + MATERIAL_THICKNESS, marginx + MATERIAL_THICKNESS, 3 * marginy + 2 * BOX_WIDTH +  BOX_INNER_HEIGHT)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + 2 * BOX_WIDTH + MATERIAL_THICKNESS, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + 2 * BOX_WIDTH +  BOX_INNER_HEIGHT)
box._draw_width_by_height_side(marginx, 3 * marginy + 2 * BOX_WIDTH + box._size['h'] + marginy)
box._draw_line(marginx + MATERIAL_THICKNESS, 4 * marginy + 2 * BOX_WIDTH + box._size['h'] + MATERIAL_THICKNESS, marginx + MATERIAL_THICKNESS, 4 * marginy + 2 * BOX_WIDTH + box._size['h'] +  BOX_INNER_HEIGHT)
box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + 2 * BOX_WIDTH + box._size['h'] + MATERIAL_THICKNESS, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + 2 * BOX_WIDTH + box._size['h'] +  BOX_INNER_HEIGHT)

box._doc.save()

