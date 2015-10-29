import logging, time
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black

class Box():
    '''
    Handles actually drawing of the notched box to a file.  This class passes everything around
    in millimeters until it actually draws it at the low level.  It renders a files like this:
    <pre>
                ----------
                |  w x d |
                ----------
                ----------
                |  w x h |
                |        |
                ----------
     ---------  ----------  ---------
     | d x h |  |  w x d |  | d x h |
     ---------  ----------  ---------
                ----------
                |  w x h |
                |        |
                ----------
    </pre>
    '''

    def __init__(self,width,height,depth,thickness,cut_width,notch_length):
        self._logger = logging.getLogger(__name__)
        self._desired_size = { 'w': float(width), 'h': float(height), 'd': float(depth) }
        self._logger.debug(" desired box size: (w=%.2f, h=%.2f, d=%.2f)" % (self._desired_size['w'],self._desired_size['h'],self._desired_size['d']))
        self._thickness = float(thickness)
        self._cut_width = float(cut_width)
        self._desired_notch_length = float(notch_length)

    def render(self,):
        # set things up
        self._compute_dimensions()
        self._initialize_document("test.pdf")

        # # 1. a W x H side (the back)
        # self._draw_width_by_height_side(self._size['d'] + self._margin*2.0, self._margin)
        # # 2. a D x H side (the left side)
        # self._draw_depth_by_height_side(self._margin,self._size['h'] + self._margin*2.0)
        # # 3. a W X D side (the bottom)
        # self._draw_width_by_depth_side(self._size['d'] + self._margin*2.0, self._size['h'] + self._margin*2.0)
        # # 4. a D x H side (the left side)
        # self._draw_depth_by_height_side(self._size['d'] + self._size['w'] + self._margin*3.0,self._size['h'] + self._margin*2.0)
        # # 5. a W x H side (the front)
        # self._draw_width_by_height_side(self._size['d'] + self._margin*2.0, self._size['h'] + self._size['d'] + self._margin*3.0)        
        # 6. a W X D side (the top)
        self._draw_width_by_depth_side(self._size['d'] + self._margin*2.0, self._size['h']*2.0 + self._size['d'] + self._margin*4.0)
        # and write out the PDF
        self._doc.save()

    def _draw_width_by_depth_side(self,x0,y0):
        self._draw_horizontal_line(x0,y0,
            self._notch_length['w'],self._num_notches['w'],
            self._thickness, -1*self._cut_width/2.0, True, True)
        self._draw_horizontal_line(x0, y0+self._size['d']-self._thickness,
            self._notch_length['w'],self._num_notches['w'],
            self._thickness, -1*self._cut_width/2.0, False, True)
        self._draw_vertical_line(x0,y0,
            self._notch_length['d'], self._num_notches['d'],
            self._thickness, -1*self._cut_width/2.0,True,True)
        self._draw_vertical_line(x0+self._size['w']-self._thickness, y0,
            self._notch_length['d'],self._num_notches['d'],
            self._thickness, -1*self._cut_width/2.0,False,True)

    def _draw_depth_by_height_side(self,x0,y0):
        self._draw_horizontal_line(x0,y0,
            self._notch_length['d'], self._num_notches['d'],
            self._thickness, self._cut_width/2, False, False)
        self._draw_horizontal_line(x0,y0+self._size['h']-self._thickness,
            self._notch_length['d'],self._num_notches['d'],
            self._thickness, self._cut_width/2.0, True, False)
        self._draw_vertical_line(x0,y0,self._notch_length['h'],self._num_notches['h'],
            self._thickness, self._cut_width/2.0, False, False)
        self._draw_vertical_line(x0+self._size['d']-self._thickness, y0,
            self._notch_length['h'],self._num_notches['h'],
            self._thickness,-1*self._cut_width/2.0,False, False)

    def _draw_width_by_height_side(self,x0,y0):
        self._draw_horizontal_line(x0, y0, 
            self._notch_length['w'], self._num_notches['w'],
            self._thickness,self._cut_width/2.0, False, False);
        self._draw_horizontal_line(x0, y0+self._size['h']-self._thickness, 
            self._notch_length['w'], self._num_notches['w'],
            self._thickness,self._cut_width/2.0, True, False);
        self._draw_vertical_line(x0,y0,
            self._notch_length['h'], self._num_notches['h'],
            self._thickness, -1*self._cut_width/2.0, False, False)
        self._draw_vertical_line(x0+self._size['w']-self._thickness,y0,
            self._notch_length['h'], self._num_notches['h'],
            self._thickness, -1*self._cut_width/2.0, False, False)

    def _compute_dimensions(self):
        # first enlarge the box to compensate for cut width
        self._size = { 'w':self._desired_size['w'] + self._cut_width, 
                       'h':self._desired_size['h'] + self._cut_width,
                       'd':self._desired_size['d'] + self._cut_width }
        # figure out how many notches for each side, trying to make notches about the right length.
        self._num_notches = { 'w': self._closest_odd(self._desired_size['w'] / self._desired_notch_length),
                              'h': self._closest_odd(self._desired_size['h'] / self._desired_notch_length),
                              'd': self._closest_odd(self._desired_size['d'] / self._desired_notch_length) }
        self._logger.debug(" notch count: (w=%d, h=%d, d=%d)" % (self._num_notches['w'],self._num_notches['h'],self._num_notches['d']))
        # compute exact notch lengths
        self._notch_length = { 'w': self._size['w'] / self._num_notches['w'],
                               'h': self._size['h'] / self._num_notches['h'],
                               'd': self._size['d'] / self._num_notches['d'] }
        self._logger.debug(" notch length: (w=%.2f, h=%.2f, d=%.2f)" % (self._notch_length['w'],self._notch_length['h'],self._notch_length['d']))
        # and compute the new width based on that (should be a NO-OP)
        self._margin = 10.0 + self._cut_width
        self._logger.debug(" margin: %.2f" % (self._margin))
        self._size = { 'w': self._num_notches['w'] * self._notch_length['w'], 
                       'h': self._num_notches['h'] * self._notch_length['h'], 
                       'd': self._num_notches['d'] * self._notch_length['d'] }
        self._logger.debug(" box size: (w=%.2f, h=%.2f, d=%.2f)" % (self._size['w'],self._size['h'],self._size['d']))
        # compute how big the document will be based on the layout of the pieces
        self._box_pieces_size = { 'w': self._size['d']*2.0 + self._size['w'],
                                  'h': self._size['h']*2.0 + self._size['d']*2.0 }
        self._doc_size = {'w': self._box_pieces_size['w']+self._margin*4,
                          'h': self._box_pieces_size['h']+self._margin*5 }
        # compute a bounding box size, in case we need to render it
        self._bounding_box_size = { 'w': self._box_pieces_size['w']+self._margin*2,
                                    'h': self._box_pieces_size['h']+self._margin*3 }

    def _initialize_document(self, filename, width, height):
        # initialize the pdf file (based on layout of pieces)
        self._doc = canvas.Canvas(filename, width, height)
        self._doc.setPageSize( [width*mm, height*mm] )
        self._doc.setStrokeColor(black)
        self._doc.setLineWidth(0.1)

    def _draw_horizontal_line(self, x0,y0,notch_width,notch_count,notch_height,cut_width,flip,smallside):
        x = x0
        y = y0
        for step in range(0,int(notch_count)):
            y = y0 if (((step%2)==0)^flip) else y0+notch_height
            if step==0: # start first edge in the right place
                if smallside:
                    self._draw_line(x+notch_height,y,x+notch_width+cut_width,y)
                else:
                    self._draw_line(x,y,x+notch_width+cut_width,y)
            elif step==(notch_count-1): # shorter last edge
                self._draw_line(x-cut_width,y,x+notch_width-notch_height,y);
            elif step%2==0:
                self._draw_line(x-cut_width,y,x+notch_width+cut_width,y);
            else:
                self._draw_line(x+cut_width,y,x+notch_width-cut_width,y);
            if step<(notch_count-1):
                if step%2==0:
                    self._draw_line(x+notch_width+cut_width,y0+notch_height,x+notch_width+cut_width,y0);
                else:
                    self._draw_line(x+notch_width-cut_width,y0+notch_height,x+notch_width-cut_width,y0);
            x = x + notch_width;

    def _draw_vertical_line(self, x0,y0,notch_width,notch_count,notch_height,cut_width,flip,smallside):
        x = x0
        y = y0
        for step in range(0,int(notch_count)):
            x = x0 if (((step%2)==0)^flip) else x0+notch_height
            if step==0:
                if smallside:
                    self._draw_line(x, y+notch_height, x, y+notch_width+cut_width)
                else:
                    self._draw_line(x,y,x,y+notch_width+cut_width)
            elif step==(notch_count-1):
                if smallside:
                    self._draw_line(x,y-cut_width,x,y+notch_width-notch_height)
                else:
                    self._draw_line(x,y-cut_width,x,y+notch_width)
            elif step%2==0:
                self._draw_line(x,y-cut_width,x,y+notch_width+cut_width)
            else:
                self._draw_line(x,y+cut_width,x,y+notch_width-cut_width)
            if step<(notch_count-1):
                if step%2==0:
                    self._draw_line(x0+notch_height, y+notch_width+cut_width,x0,y+notch_width+cut_width)
                else:
                    self._draw_line(x0+notch_height, y+notch_width-cut_width,x0,y+notch_width-cut_width)
            y = y+notch_width

    def _draw_line(self, fromX,fromY,toX,toY):
        self._doc.line(fromX*mm,fromY*mm,toX*mm,toY*mm)

    def _draw_circle(self, X, Y, radius):
        self._doc.circle(X*mm, Y*mm, radius*mm)

    def _closest_odd(self, number):
        '''
        Find and return the closest odd number to the one passed in
        '''
        num = int(float(number)+0.5)
        closest_odd = None
        if num % 2 == 0:
            closest_odd = num-1
        else:
            closest_odd = num
        return float(closest_odd)