import boxmaker

from reportlab.lib.colors import black
from reportlab.lib.colors import red
from reportlab.lib.colors import blue
from reportlab.lib.colors import green

BOX_LENGTH = 230
BOX_WIDTH = 135
BOX_INNER_HEIGHT = 30

MATERIAL_THICKNESS = 7.1
CUT_WIDTH = 0.01

PLATE_WIDTH = 240
PLATE_HEIGHT = 145

SCREEN_POSITION_X = 8
SCREEN_POSITION_Y = 13
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

box = boxmaker.Box(BOX_LENGTH, BOX_INNER_HEIGHT + MATERIAL_THICKNESS, BOX_WIDTH, MATERIAL_THICKNESS, CUT_WIDTH, 2.5*MATERIAL_THICKNESS)
box._compute_dimensions()


################# render the top part
box._initialize_document("top.pdf", PLATE_WIDTH, PLATE_HEIGHT)
marginx = 5
marginy = 5
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(marginx, marginy)
# draw the screen
box._doc.setStrokeColor(green)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y, marginx + SCREEN_POSITION_X + SCREEN_WIDTH, marginy + SCREEN_POSITION_Y + SCREEN_HEIGHT)

#draw to metal part
box._doc.setStrokeColor(red)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2, marginx + SCREEN_POSITION_X  + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X + SCREEN_TO_METALX1, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)
box._draw_line(marginx + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY1, marginx + SCREEN_POSITION_X + SCREEN_TO_METALX2, marginy + SCREEN_POSITION_Y + SCREEN_TO_METALY2)

box._doc.save()

################## render the bottom part
box._initialize_document("bottom.pdf", PLATE_WIDTH, PLATE_HEIGHT)
box._doc.setStrokeColor(blue)
box._draw_width_by_depth_side(5, 5)
# screws
box._doc.setStrokeColor(red)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW1X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW1Y, RADIUS)
box._draw_circle(marginx + SCREEN_POSITION_X + SCREEN_TO_SCREW2X, marginy + SCREEN_POSITION_Y + SCREEN_TO_SCREW2Y, RADIUS)

box._doc.save()

################# render the sides parts
box._initialize_document("sides.pdf", PLATE_WIDTH, PLATE_HEIGHT)
box._doc.setStrokeColor(blue)
box._draw_width_by_height_side(5, 5)
box._draw_width_by_height_side(5, 5 + box._size['h'] + 5)
box._draw_depth_by_height_side(5, (5 + box._size['h'])*2 + 5)
# box._draw_depth_by_height_side(5, (5 + box._size['h'])*3 + 5)
box._doc.save()

