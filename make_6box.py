import Boxmaker

import json
from reportlab.lib.colors import black
from reportlab.lib.colors import red
from reportlab.lib.colors import blue
from reportlab.lib.colors import green

PLATE_LENGTH = 1530
PLATE_WIDTH = 1000
MATERIAL_THICKNESS = 5

BOX_LENGTH = 270
BOX_WIDTH = 140
BOX_INNER_HEIGHT = 30

CUT_WIDTH = 0.01

SCREEN_POSITION_X = 20
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
marginy = 10

##### preparation (box and field)
box = Boxmaker.Box(BOX_LENGTH, BOX_INNER_HEIGHT + MATERIAL_THICKNESS, BOX_WIDTH, MATERIAL_THICKNESS, CUT_WIDTH, 2.5*MATERIAL_THICKNESS)
box._compute_dimensions()

def drawField(X, Y, width, flip = False):
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

	for curve in preparedCurves:
		x = curve[0]
		y = curve[1]
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
drawField(marginx + BOX_LENGTH - MATERIAL_THICKNESS, marginy + MATERIAL_THICKNESS, (BOX_WIDTH - 2*MATERIAL_THICKNESS)/2)
drawField(marginx + MATERIAL_THICKNESS, marginy + MATERIAL_THICKNESS, (BOX_WIDTH - 2*MATERIAL_THICKNESS)/2, True)


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
# screws
box._doc.setStrokeColor(red)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)


################# render the sides parts
box._doc.setStrokeColor(blue)
box._draw_width_by_height_side(marginx, 3 * marginy + 2 * BOX_WIDTH)
box._draw_width_by_height_side(marginx, 3 * marginy + 2 * BOX_WIDTH + box._size['h'] + marginy)
box._draw_depth_by_height_side(marginx, 3 * marginy + 2 * BOX_WIDTH + box._size['h']*2 + 2*marginy)
# box._draw_depth_by_height_side(5, (5 + box._size['h'])*3 + 5)
box._doc.save()

