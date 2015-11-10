import Boxmaker


from reportlab.lib.colors import black
from reportlab.lib.colors import red
from reportlab.lib.colors import blue
from reportlab.lib.colors import green
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics import shapes
from reportlab.lib.units import mm

PLATE_LENGTH = 1000
PLATE_WIDTH = 500
MATERIAL_THICKNESS = 5

BOX_LENGTH = 245
BOX_WIDTH = 140
BOX_INNER_HEIGHT = 5 * MATERIAL_THICKNESS 

CUT_WIDTH = 0.01

SCREEN_X = 8
SCREEN_Y = 15
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
box._initialize_document("6box_wood.pdf", PLATE_LENGTH, PLATE_WIDTH)


# ################## render the bottom part
boxBottom = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)

boxBottom.add(box._draw_width_by_depth_side(0, 0))

# the field
boxBottom.add(box.drawField(BOX_LENGTH - MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 6))
boxBottom.add(box.drawField(MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 6, -1))


def draw_side(x, y, attach_height, fieldnum, fliph = 1, colorout = green, colorin = green):
	f = box.drawField(x, y, BOX_WIDTH/2, fieldnum, fliph, colorout)
	attach_width = 15
	etiration = fliph * 1.1
	insert_length = fliph * 10
	insert_width = 5
	l1 = box._draw_line(x, y, x, y + MATERIAL_THICKNESS, colorout)
	l2 = box._draw_line(x, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS, colorout)
	l3 = box._draw_line(x - insert_length, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS + insert_width, colorout)
	l4 = box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x - insert_length, y + MATERIAL_THICKNESS + insert_width, colorout)
	
	l5 = box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x, y + attach_height - attach_width/2, colorout)
	b = box._draw_polyline([
		x, y + attach_height - attach_width/2,
		x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height - attach_width/2 ,
		x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height + attach_width/2 ,
		x, y + attach_height + attach_width/2], colorout)
	l6 = box._draw_line(x, y + attach_height + attach_width/2, x,  BOX_WIDTH + y - MATERIAL_THICKNESS - insert_width , colorout)
	
	l7 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, colorout)
	l8 = box._draw_line(x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS  , colorout)
	l9 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS, colorout)
	l10 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x, y + BOX_WIDTH, colorout)
	if fliph == 1:
		p1 = box._draw_circle(x - (SCREEN_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
		p2 = box._draw_circle(x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X), y + attach_height, RADIUS)
	else:
		p1 = box._draw_circle(x - (SCREEN_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
		p2 = box._draw_circle(x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*fliph, y + attach_height, RADIUS)
	return shapes.Group(f, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, p1, p2, b)

for i in [5 ,4, 3, 2, 1]:
	boxBottom.add(draw_side(BOX_LENGTH - MATERIAL_THICKNESS, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, i))
	boxBottom.add(draw_side(MATERIAL_THICKNESS, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, i, -1))


# draw_side(marginxBottom + 285, marginy, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), 1)
# draw_side(marginxBottom  + 230, marginy, SCREEN_Y + SCREEN_TO_SCREW1Y, 1, -1)
# draw_side(marginxBottom + 417, marginy, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), 4)
# draw_side(marginxBottom  + 365, marginy, SCREEN_Y + SCREEN_TO_SCREW1Y, 4, -1)
# draw_side(marginxBottom + 375, marginy + BOX_WIDTH, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), 2)
# draw_side(marginxBottom  + 320, marginy + BOX_WIDTH, SCREEN_Y + SCREEN_TO_SCREW1Y, 2, -1)
# draw_side(marginxBottom + 360, marginy + 2*BOX_WIDTH, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), 3)
# draw_side(marginxBottom  + 300, marginy + 2*BOX_WIDTH, SCREEN_Y + SCREEN_TO_SCREW1Y, 3, -1)

# g1 = draw_side(200, marginy + 2*BOX_WIDTH, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), 5)
# g1.rotate(90)

# draw_side(250, marginy + 2*BOX_WIDTH, SCREEN_Y + SCREEN_TO_SCREW1Y, 5, -1)


# screws
boxBottom.add(shapes.Group(
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW1X, SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS, red),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW1X, SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS, red),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW2X, SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS, red),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW2X, SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS, red)
))


boxBottom.drawOn(box._doc, 65*mm, 15*mm)


################# render the top part
boxTop = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)

boxTop.add(box._draw_width_by_depth_side(0, 0))

# the field
boxTop.add(box.drawField(BOX_LENGTH - MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 0))
boxTop.add(box.drawField(MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 0, -1))

# the screen
boxTop.add(box._draw_rectangle(SCREEN_X, SCREEN_Y, SCREEN_WIDTH, SCREEN_HEIGHT, green))

# screws
boxTop.add(shapes.Group(
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW1X, SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS, green),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW1X, SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS, green),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW2X, SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS, green),
	box._draw_circle(SCREEN_X + SCREEN_TO_SCREW2X, SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS, green)
))

# the metal part
boxTop.add(box._draw_rectangle(SCREEN_X + SCREEN_TO_METALX1, SCREEN_Y + SCREEN_TO_METALY1, SCREEN_TO_METALX2 - SCREEN_TO_METALX1, SCREEN_TO_METALY2 - SCREEN_TO_METALY1))

boxTop.drawOn(box._doc, 20*mm, (BOX_WIDTH + 27) * mm)

################# render the sides parts
boxSides = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)

boxSides.add(box._draw_width_by_height_side(0, 0))
boxSides.add(box._draw_line(MATERIAL_THICKNESS, MATERIAL_THICKNESS, MATERIAL_THICKNESS, BOX_INNER_HEIGHT))
boxSides.add(box._draw_line(BOX_LENGTH - MATERIAL_THICKNESS, MATERIAL_THICKNESS, BOX_LENGTH - MATERIAL_THICKNESS, BOX_INNER_HEIGHT))

g = shapes.Group()
g.add(box._draw_width_by_height_side(0, 0))
g.add(box._draw_line(MATERIAL_THICKNESS, MATERIAL_THICKNESS, MATERIAL_THICKNESS, BOX_INNER_HEIGHT))
g.add(box._draw_line(BOX_LENGTH - MATERIAL_THICKNESS, MATERIAL_THICKNESS, BOX_LENGTH - MATERIAL_THICKNESS, BOX_INNER_HEIGHT))
g.translate(box._notch_length['w']*mm, BOX_INNER_HEIGHT*mm)
boxSides.add(g)


boxSides.drawOn(box._doc, 20*mm , (2*BOX_WIDTH + 27 - MATERIAL_THICKNESS) * mm)



box._doc.save()
