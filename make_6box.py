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
boxBottom.add(box.drawField(BOX_LENGTH - MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 5))
boxBottom.add(box.drawField(MATERIAL_THICKNESS, 0, BOX_WIDTH/2, 5, -1))

def draw_side(x, y, attach_height, hole_dist_x, fieldnum, fliph = 1, colorout = green, colorin = green):
	f = box.drawField(x, y, BOX_WIDTH/2, fieldnum, fliph, colorout)
	attach_width = 12
	insert_length = fliph * 10
	insert_width = 15
	margin_hole = 5
	l1 = box._draw_line(x, y, x, y + MATERIAL_THICKNESS, colorout)
	l2 = box._draw_line(x, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS, colorout)
	l3 = box._draw_line(x - insert_length, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS + insert_width, colorout)
	l4 = box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x - insert_length, y + MATERIAL_THICKNESS + insert_width, colorout)
	
	l5 = box._draw_line(x, y + MATERIAL_THICKNESS + insert_width, x, y + attach_height - attach_width/2, colorout)
	b = box._draw_polyline([
		x, y + attach_height - attach_width/2,
		x - (hole_dist_x + margin_hole) * fliph, y + attach_height - attach_width/2 ,
		x - (hole_dist_x + margin_hole) * fliph, y + attach_height + attach_width/2 ,
		x, y + attach_height + attach_width/2], colorout)
	l6 = box._draw_line(x, y + attach_height + attach_width/2, x,  BOX_WIDTH + y - MATERIAL_THICKNESS - insert_width , colorout)
	
	l7 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, colorout)
	l8 = box._draw_line(x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS  , colorout)
	l9 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS, colorout)
	l10 = box._draw_line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x, y + BOX_WIDTH, colorout)
	if fliph == 1:
		p = box._draw_circle(x - hole_dist_x * fliph, y + attach_height, RADIUS, colorin)
	else:
		p = box._draw_circle(x - hole_dist_x * fliph, y + attach_height, RADIUS, colorin)
		# p = box._draw_circle(x - (SCREEN_X + SCREEN_TO_SCREW1X - MATERIAL_THICKNESS)*fliph, y + attach_height, RADIUS, colorin)
	return shapes.Group(f, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, p, b)

for i in [4, 3, 2, 1]:
	boxBottom.add(draw_side(BOX_LENGTH - MATERIAL_THICKNESS, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, BOX_LENGTH - SCREEN_X - SCREEN_TO_SCREW2X - MATERIAL_THICKNESS, i))
	boxBottom.add(draw_side(MATERIAL_THICKNESS, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, SCREEN_TO_SCREW1X - MATERIAL_THICKNESS + SCREEN_X, i, -1))

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
boxTop.add(box._draw_rectangle(SCREEN_X + SCREEN_TO_METALX1, SCREEN_Y + SCREEN_TO_METALY1, SCREEN_TO_METALX2 - SCREEN_TO_METALX1, SCREEN_TO_METALY2 - SCREEN_TO_METALY1, red))

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
c = box._draw_circle(MATERIAL_THICKNESS + 50.5*mm, MATERIAL_THICKNESS + 2*BOX_INNER_HEIGHT - MATERIAL_THICKNESS, 5, red)
boxSides.add(c)

boxSides.drawOn(box._doc, 20*mm , (2*BOX_WIDTH + 27 - MATERIAL_THICKNESS) * mm)

################# the sides
d = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)
d.add(draw_side(0, 0, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), BOX_LENGTH - SCREEN_X - SCREEN_TO_SCREW2X - MATERIAL_THICKNESS, 1, -1, blue, red))
d.add(draw_side(51, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, SCREEN_TO_SCREW1X - MATERIAL_THICKNESS + SCREEN_X, 1, 1, blue, red))
d.drawOn(box._doc, (BOX_LENGTH + 155)*mm ,  5* mm)

d = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)
d.add(draw_side(0, 0, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), BOX_LENGTH - SCREEN_X - SCREEN_TO_SCREW2X - MATERIAL_THICKNESS, 2, -1, blue, red))
d.add(draw_side(55, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, SCREEN_TO_SCREW1X - MATERIAL_THICKNESS + SCREEN_X, 2, 1, blue, red))
d.drawOn(box._doc, (BOX_LENGTH + 75)*mm ,  (BOX_WIDTH + 30)* mm)

d = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)
g = shapes.Group()
s = draw_side(0, 0, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), BOX_LENGTH - SCREEN_X - SCREEN_TO_SCREW2X - MATERIAL_THICKNESS, 3, -1, blue, red)
s.rotate(90)
g.add(s)
s = draw_side(55, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, SCREEN_TO_SCREW1X - MATERIAL_THICKNESS + SCREEN_X, 3, 1, blue, red)
s.rotate(90)
s.translate(-40*mm, -50*mm)
g.add(s)
d.add(g)
d.drawOn(box._doc, (BOX_WIDTH + 20)*mm ,  3*BOX_WIDTH* mm)

d = shapes.Drawing(PLATE_LENGTH, PLATE_WIDTH)
g = shapes.Group()
s = draw_side(0, 0, BOX_WIDTH - (SCREEN_Y + SCREEN_TO_SCREW1Y), BOX_LENGTH - SCREEN_X - SCREEN_TO_SCREW2X - MATERIAL_THICKNESS, 4, -1, blue, red)
s.rotate(90)
g.add(s)
s = draw_side(55, 0, SCREEN_Y + SCREEN_TO_SCREW1Y, SCREEN_TO_SCREW1X - MATERIAL_THICKNESS + SCREEN_X, 4, 1, blue, red)
# s.rotate(90)
s.translate(-50*mm, -100*mm)
g.add(s)
d.add(g)
d.drawOn(box._doc, (BOX_WIDTH + 210)*mm ,  3*BOX_WIDTH* mm)



box._doc.save()
