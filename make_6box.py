import boxmaker

BOX_LENGTH = 230
BOX_WIDTH = 135
BOX_HEIGHT = 30

MATERIAL_THICKNESS = 7.1
CUT_WIDTH = 0

PLATE_WIDTH = 240
PLATE_HEIGHT = 145

box = boxmaker.Box(BOX_LENGTH, BOX_HEIGHT, BOX_WIDTH, MATERIAL_THICKNESS, CUT_WIDTH, 2.5*MATERIAL_THICKNESS)
box._compute_dimensions()


# render the top part
box._initialize_document("top.pdf", PLATE_WIDTH, PLATE_HEIGHT)
box._draw_width_by_depth_side(5, 5)
box._doc.save()

# render the bottom part
box._initialize_document("bottom.pdf", PLATE_WIDTH, PLATE_HEIGHT)
box._draw_width_by_depth_side(5, 5)
box._doc.save()

# render the sides parts
box._initialize_document("sides.pdf", PLATE_WIDTH, PLATE_HEIGHT)
box._draw_width_by_height_side(5, 5)
box._draw_width_by_height_side(5, 5 + box._size['h'] + 5)
box._draw_depth_by_height_side(5, (5 + box._size['h'])*2 + 5)
box._draw_depth_by_height_side(5, (5 + box._size['h'])*3 + 5)
box._doc.save()

