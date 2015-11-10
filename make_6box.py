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

BOX_LENGTH = 220
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
boxTop.drawOn(box._doc, 300, 200)

# ################## render the bottom part
# box._doc.setStrokeColor(blue)
# box._draw_width_by_depth_side(marginxBottom, 2 * marginy + BOX_WIDTH)

# # the field
# box.drawField(marginxBottom + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 6)
# box.drawField(marginxBottom + MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, BOX_WIDTH/2, 6, -1)

# def draw_side(x, y, attach_height, fieldnum, fliph = 1, colorout = green, colorin = green):
# 	box._doc.setStrokeColor(colorout)
# 	f = box.drawField(x, y, BOX_WIDTH/2, fieldnum, fliph)
# 	attach_width = 15
# 	etiration = fliph * 1.5
# 	insert_length = fliph * 10
# 	insert_width = 5
# 	l1 = shapes.Line(x, y, x, y + MATERIAL_THICKNESS)
# 	l2 = shapes.Line(x, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS)
# 	l3 = shapes.Line(x - insert_length, y + MATERIAL_THICKNESS, x - insert_length, y + MATERIAL_THICKNESS + insert_width)
# 	l4 = shapes.Line(x, y + MATERIAL_THICKNESS + insert_width, x - insert_length, y + MATERIAL_THICKNESS + insert_width)
	
# 	l5 = shapes.Line(x, y + MATERIAL_THICKNESS + insert_width, x, y + attach_height - attach_width/2)
# 	b = box._draw_bezier(x, y + attach_height - attach_width/2 ,
# 		x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height - attach_width/2 ,
# 		x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*etiration, y + attach_height + attach_width/2 ,
# 		x, y + attach_height + attach_width/2)
	

# 	l6 = shapes.Line(x, y + attach_height + attach_width/2, x,  BOX_WIDTH + y - MATERIAL_THICKNESS - insert_width )
# 	l7 = shapes.Line(x, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width)
# 	l8 = shapes.Line(x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS - insert_width, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS  )
# 	l9 = shapes.Line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x - insert_length, y + BOX_WIDTH - MATERIAL_THICKNESS)
# 	l10 = shapes.Line(x, y + BOX_WIDTH - MATERIAL_THICKNESS, x, y + BOX_WIDTH)
# 	l11 = box._doc.setStrokeColor(colorin)
# 	if fliph == 1:
# 		p1 = box._draw_circle(x - (SCREEN_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
# 		p2 = box._draw_circle(x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X), y + attach_height, RADIUS)
# 	else:
# 		p1 = box._draw_circle(x - (SCREEN_X - MATERIAL_THICKNESS +  SCREEN_TO_SCREW1X)*fliph, y + attach_height, RADIUS)
# 		p2 = box._draw_circle(x - (SCREEN_X + MATERIAL_THICKNESS + SCREEN_WIDTH - SCREEN_TO_SCREW2X)*fliph, y + attach_height, RADIUS)
# 	return shapes.Group(f, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, p1, p2)

# for i in [5 ,4, 3, 2, 1]:
# 	draw_side(marginxBottom + BOX_LENGTH - MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, SCREEN_Y + SCREEN_TO_SCREW1Y, i)
# 	draw_side(marginxBottom  + MATERIAL_THICKNESS, 2 * marginy + BOX_WIDTH, SCREEN_Y + SCREEN_TO_SCREW1Y, i, -1)


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


# # screws
# box._doc.setStrokeColor(red)
# box._draw_circle(marginxBottom + SCREEN_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS)
# box._draw_circle(marginxBottom + SCREEN_X + SCREEN_TO_SCREW1X, 2 * marginy + BOX_WIDTH + SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS)
# box._draw_circle(marginxBottom + SCREEN_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_Y + SCREEN_TO_SCREW1Y, RADIUS)
# box._draw_circle(marginxBottom + SCREEN_X + SCREEN_TO_SCREW2X, 2 * marginy + BOX_WIDTH + SCREEN_Y + SCREEN_TO_SCREW2Y, RADIUS)


# ################# render the sides parts
# box._doc.setStrokeColor(blue)
# www = 2*BOX_WIDTH

# box._draw_width_by_height_side(marginx, 3 * marginy + www)
# box._draw_line(marginx + MATERIAL_THICKNESS, 3 * marginy + www + MATERIAL_THICKNESS, marginx + MATERIAL_THICKNESS, 3 * marginy + www + BOX_INNER_HEIGHT)
# box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + www + MATERIAL_THICKNESS, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 3 * marginy + www + BOX_INNER_HEIGHT)

# box._draw_width_by_height_side(marginx, 4 * marginy + (BOX_INNER_HEIGHT + MATERIAL_THICKNESS) + www)
# box._draw_line(marginx + MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + 2*MATERIAL_THICKNESS + www, marginx + MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + MATERIAL_THICKNESS + www + BOX_INNER_HEIGHT)
# box._draw_line(marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + 2*MATERIAL_THICKNESS + www, marginx + BOX_LENGTH - MATERIAL_THICKNESS, 4 * marginy + BOX_INNER_HEIGHT + MATERIAL_THICKNESS + www + BOX_INNER_HEIGHT)

# box._doc.setStrokeColor(red)
# box._draw_rectangle(marginx + 40, 4 * marginy + (BOX_INNER_HEIGHT + MATERIAL_THICKNESS) + www +  (BOX_INNER_HEIGHT + MATERIAL_THICKNESS)/2 -3, 10, 5)


# ################ sides



box._doc.save()
