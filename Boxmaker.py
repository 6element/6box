import logging, time, json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics import shapes
from reportlab.lib.colors import blue

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


    def _draw_width_by_depth_side(self, x0, y0, color = blue):
        g = shapes.Group()
        g.add(self._draw_horizontal_line(x0,y0,
            self._notch_length['w'],self._num_notches['w'],
            self._thickness, -1*self._cut_width/2.0, False, True, color))
        g.add(self._draw_horizontal_line(x0, y0+self._size['d']-self._thickness,
            self._notch_length['w'],self._num_notches['w'],
            self._thickness, -1*self._cut_width/2.0, True, True, color))
        return g

    def _draw_width_by_height_side(self, x0, y0, color = blue):
        g = shapes.Group()
        g.add(self._draw_horizontal_line(x0, y0, 
            self._notch_length['w'], self._num_notches['w'],
            self._thickness,self._cut_width/2.0, True, True, color))
        g.add(self._draw_horizontal_line(x0, y0+self._size['h']-self._thickness, 
            self._notch_length['w'], self._num_notches['w'],
            self._thickness,self._cut_width/2.0, False, True, color))
        return g

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

    def _initialize_document(self, filename, width, height, strokeWidth):
        # initialize the pdf file (based on layout of pieces)
        self._doc = canvas.Canvas(filename, width, height)
        self._doc.setPageSize( [width*mm, height*mm] )
        self._doc.setLineWidth(strokeWidth)
        self.strokeWidth = strokeWidth

    def _draw_horizontal_line(self, x0,y0,notch_width,notch_count,notch_height,cut_width,flip,smallside, color):
        x = x0
        y = y0
        g = shapes.Group()
        for step in range(0,int(notch_count)):
            y = y0 if (((step%2)==0)^flip) else y0+notch_height
            if step==0: # start first edge in the right place
                if smallside:
                    l = self._draw_line(x+notch_height,y,x+notch_width+cut_width,y, color)
                    l.strokeWidth = self.strokeWidth
                    g.add(l)
                else:
                    l = self._draw_line(x,y,x+notch_width+cut_width,y, color)
                    l.strokeWidth = self.strokeWidth
                    g.add(l)
            elif step==(notch_count-1): # shorter last edge
                l = self._draw_line(x-cut_width,y,x+notch_width-notch_height,y, color)
                l.strokeWidth = self.strokeWidth
                g.add(l)
            elif step%2==0:
                l = self._draw_line(x-cut_width,y,x+notch_width+cut_width,y, color)
                l.strokeWidth = self.strokeWidth
                g.add(l)
            else:
                l = self._draw_line(x+cut_width,y,x+notch_width-cut_width,y, color)
                l.strokeWidth = self.strokeWidth
                g.add(l)
            if step<(notch_count-1):
                if step%2==0:
                    l = self._draw_line(x+notch_width+cut_width,y0+notch_height,x+notch_width+cut_width,y0, color)
                    l.strokeWidth = self.strokeWidth
                    g.add(l)
                else:
                    l = self._draw_line(x+notch_width-cut_width,y0+notch_height,x+notch_width-cut_width,y0, color)
                    l.strokeWidth = self.strokeWidth
                    g.add(l)
            x = x + notch_width
        return g

    def drawField(self, X, Y, width, lineNum, flip = 1, color = blue):
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

        xp = preparedCurves[lineNum][0]
        yp = preparedCurves[lineNum][1]
        coords = []
        for x,y in zip(xp, yp):
            coords += [x*mm, y*mm]
        p = shapes.PolyLine(coords)
        p.strokeColor = color
        p.strokeWidth = self.strokeWidth
        return p

    def _draw_polyline(self, coords, color = blue):
        mmcoords = map(lambda x: x*mm, coords)
        p = shapes.PolyLine(mmcoords)
        p.strokeColor = color
        p.strokeWidth = self.strokeWidth
        return p

    def _draw_line(self, fromX, fromY, toX, toY, color = blue):
        l = shapes.Line(fromX*mm,fromY*mm,toX*mm,toY*mm)
        l.strokeColor = color
        l.strokeWidth = self.strokeWidth
        return l

    def _draw_circle(self, X, Y, radius, color=blue):
        c = shapes.Circle(X*mm, Y*mm, radius*mm)
        c.fillColor = None
        c.strokeColor = color
        c.strokeWidth = self.strokeWidth
        return c

    def _draw_rectangle(self, X, Y, w, h, color = blue):
        r = shapes.Rect(X*mm, Y*mm, w*mm, h*mm)
        r.fillColor = None
        r.strokeColor = color
        r.strokeWidth = self.strokeWidth
        return r

    def _draw_bezier(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self._doc.bezier(x1*mm, y1*mm, x2*mm, y2*mm, x3*mm, y3*mm, x4*mm, y4*mm)

    def _place_logo(self, logo, X, Y, W, H):
        self._doc.drawImage(logo, X*mm, Y*mm, W*mm, H*mm, mask='auto')

    def _write(self, X, Y, text):
        self._doc.drawString(X*mm, Y*mm, text)

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