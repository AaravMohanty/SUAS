import math
import tkinter as tk   
from tkinter import *       
from PIL import Image, ImageTk  
import numpy as np
from math import asin, atan2, cos, degrees, radians, sin
import os
                                
class PanZoomCanvas(tk.Frame):
    def __init__(self, master,canvas_w,canvas_h):
        super().__init__(master)
        self.pil_image = None   # Image data to be displayed

        self.zoom_cycle = 0

        self.create_widget(canvas_w,canvas_h) # Create canvas
        
        # Initial affine transformation matrix
        self.reset_transform()
 
    # Define the create_widget method.
    def create_widget(self,width,height):
        # Canvas
        self.canvas = tk.Canvas(self.master, background="black", width = width,height = height)
        self.canvas.pack() 

        # Controls
        self.master.bind("<Button-1>", self.mouse_down_left)                   # MouseDown
        self.master.bind("<B1-Motion>", self.mouse_move_left)                  # MouseDrag
        self.master.bind("<Double-Button-1>", self.mouse_double_click_left)    # MouseDoubleClick
        self.master.bind("<MouseWheel>", self.mouse_wheel)                     # MouseWheel


    def set_image(self, filename):
        '''To open an image file'''
        if not filename:
            return
        # PIL.Image
        self.pil_image = Image.open(filename)
        # Set the affine transformation matrix to display the entire image.
        self.zoom_fit(self.pil_image.width, self.pil_image.height)
        # To display the image
        self.draw_image(self.pil_image)

    # -------------------------------------------------------------------------------
    # Mouse events
    # -------------------------------------------------------------------------------
    def mouse_down_left(self, event):
        self.__old_event = event

    def mouse_move_left(self, event):
        if (self.pil_image == None):
            return
        
        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event


    def get_point_at_distance(self, lat1, lon1, d, bearing, R=6371):
        """
        lat: initial latitude, in degrees
        lon: initial longitude, in degrees
        d: target distance from initial
        bearing: (true) heading in degrees
        R: optional radius of sphere, defaults to mean radius of earth

        Returns new lat/lon coordinate {d}km from initial, in degrees
        """
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        a = radians(bearing)
        lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
        lon2 = lon1 + atan2(
            sin(a) * sin(d/R) * cos(lat1),
            cos(d/R) - sin(lat1) * sin(lat2)
        )
        return (degrees(lat2), degrees(lon2),)

    def mouse_double_click_left(self, event):
        x = event.x
        y = event.y
        #convert canvas coords to image coords test is for random matrix number 
        coordx, coordy, test = self.to_image_point(x, y)
        
        #translate from top left to middle
        coordx -= 2784
        coordy -= 2088
        ##feet per pixel
        coordx = coordx * coord[2] * math.tan(0.80285) / 2784 
        coordy = -coordy * coord[2] * math.tan(0.54978) / 2088
        #convert to r and theta in rads
        coordr = math.sqrt(coordx ** 2 + coordy **2)
        coordtheta = math.atan(coordy / coordx)
        if (coordx < 0):
            coordtheta += math.pi
        elif(coordy < 0):
            coordtheta+= 2 * math.pi
        newlat, newlong = self.get_point_at_distance(coord[1], coord[0],coordr,coordtheta + coord[3])
        CoordLat.set(newlat)
        CoordLong.set(newlong)
        CoordVar.set(f'{newlong},{newlat}')

    def mouse_wheel(self, event):
        if self.pil_image == None:
            return

        if (event.delta < 0):
            if self.zoom_cycle <= 0:
                return
            # Rotate upwards and shrink
            self.scale_at(0.8, event.x, event.y)
            self.zoom_cycle -= 1
        else:
            if self.zoom_cycle >= 9:
                return
            #  Rotate downwards and enlarge
            self.scale_at(1.25, event.x, event.y)
            self.zoom_cycle += 1
    
        self.redraw_image() # Refresh
        
    # -------------------------------------------------------------------------------
    # Affine Transformation for Image Display
    # -------------------------------------------------------------------------------

    def reset_transform(self):
        self.mat_affine = np.eye(3) # 3x3の単位行列

    def translate(self, offset_x, offset_y,zoom = False):
        mat = np.eye(3) # 3x3 identity matrix
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)
        # Get the current canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Get the current scale
        scale = self.mat_affine[0, 0]
        max_y = scale * 3072
        max_x = scale * 4096
        self.mat_affine = np.dot(mat, self.mat_affine)

        if not zoom:
            if abs(self.mat_affine[0,2]) > abs(max_x-canvas_width):
                self.mat_affine[0,2] = -(max_x-canvas_width)
            if abs(self.mat_affine[1,2]) > abs(max_y-canvas_height):
                self.mat_affine[1,2] = -(max_y-canvas_height)

        if self.mat_affine[0, 2] > 0.0:
            self.mat_affine[0, 2] = 0.0
        if self.mat_affine[1,2] > 0.0:
            self.mat_affine[1,2]  = 0.0

    def scale(self, scale:float):
        mat = np.eye(3) # 3x3 identity matrix

        mat[0, 0] = scale
        mat[1, 1] = scale
        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale_at(self, scale:float, cx:float, cy:float):

        # Translate to the origin
        self.translate(-cx, -cy, True)
        # Scale
        self.scale(scale)
        # Restore
        self.translate(cx, cy)

    def zoom_fit(self, image_width, image_height):

        # Update canvas object and get size
        self.master.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if (image_width * image_height <= 0) or (canvas_width * canvas_height <= 0):
            return

        # Initialization of affine transformation
        self.reset_transform()

        scale = 1.0
        offsetx = 0.0
        offsety = 0.0
        if (canvas_width * image_height) > (image_width * canvas_height):
            # The widget is horizontally elongated (resizing the image vertically)
            scale = canvas_height / image_height
            # Align the remaining space to the center by offsetting horizontally
            offsetx = (canvas_width - image_width * scale) / 2
        else:
            # The widget is vertically elongated (resizing the image horizontally)
            scale = canvas_width / image_width
            # Align the remaining space to the center by offsetting vertically
            offsety = (canvas_height - image_height * scale) / 2

        # Scale
        self.scale(scale)
        # Align the remaining space to the center
        self.translate(offsetx, offsety)
        self.zoom_cycle = 0

    def to_image_point(self, x, y):
        '''Convert coordinates from the canvas to the image'''
        if self.pil_image == None:
            return []
        # Convert coordinates from the image to the canvas by taking the inverse of the transformation matrix.
        mat_inv = np.linalg.inv(self.mat_affine)
        image_point = np.dot(mat_inv, (x, y, 1.))
        if  image_point[0] < 0 or image_point[1] < 0 or image_point[0] > self.pil_image.width or image_point[1] > self.pil_image.height:
            return []

        return image_point

    # -------------------------------------------------------------------------------
    # Drawing 
    # -------------------------------------------------------------------------------

    def draw_image(self, pil_image):
        
        if pil_image == None:
            return

        self.pil_image = pil_image

        # Canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the affine transformation matrix from canvas to image data
        # (Calculate the inverse of the display affine transformation matrix)
        mat_inv = np.linalg.inv(self.mat_affine)

        # Convert the numpy array to a tuple for affine transformation
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
        )

        # Apply affine transformation to the PIL image data
        dst = self.pil_image.transform(
            (canvas_width, canvas_height),  # Output size
            Image.AFFINE,   # Affine transformation
            affine_inv,     # Affine transformation matrix (conversion matrix from output to input)
            Image.NEAREST   # Interpolation method, nearest neighbor
        )

        im = ImageTk.PhotoImage(image=dst)

        # Draw the image
        item = self.canvas.create_image(
            0, 0,           # Image display position (top-left coordinate)
            anchor='nw',    # Anchor, top-left is the origin
            image=im        # Display image data
        )
        self.image = im

    def redraw_image(self):
        '''Redraw the image'''
        if self.pil_image == None:
            return
        self.draw_image(self.pil_image)

if __name__ == "__main__":
    imagefile = "/Users/jeffrey/Documents/ImageLabeling"
    def dir_to_photo():
        global images
        after = dict([(f, f) for f in os.listdir(imagefile)])
        added = [f for f in after if not f in images]
        if added:
            for f in added:
                qimage.append(f)
                images = after
    def next_image():
        dir_to_photo()
        if len(qimage) == 1:
            app.set_image("/Users/jeffrey/Documents/Waiting_for_images.jpg")
        else:
            app.set_image(imagefile + "/" + coord_from_image(qimage.pop(1)))
    def coord_from_image(photo):
        global coord
        temp = photo.split("_")
        coord = (int(temp[1]), int(temp[2]), int(temp[3]), int((temp[4])[0: temp[4].rfind('.')]))
        return photo
    
    
    #Root
    root = tk.Tk()
    root.geometry('1200x900')
    frame2 = tk.Frame(root)
    
    #Zoom App
    app = PanZoomCanvas(master=root,canvas_w = 1024,canvas_h = 768) # 1024, 768
    app.canvas.config(bg = 'grey')
    ##change picture to variable once testing 
    app.set_image("/Users/jeffrey/Documents/Waiting_for_images.jpg")
    
    #coord label
    CoordVar = StringVar() 
    CoordVar.set('Coordinates') 
    CoordLat = DoubleVar()
    CoordLong = DoubleVar()
    l = Label(frame2, textvariable = CoordVar)
    l.grid(column = 0, row = 0) 
    coord = (1, 1, 100, 0) ##(long, Lat, Alt, degree from north where 0 is true north and clockwise)
    
    #image queue
    images = dict([(f, f) for f in os.listdir(imagefile)])
    qimage = [f for f in os.listdir(imagefile)]
    
    #switch image
    nextImgBtn = Button(frame2, text = 'Next Img', bd = '5', command = lambda : next_image())
    nextImgBtn.grid(column = 1, row = 0)
    
    # Drop Down Menu
    ColorShapeList = []

    # Change the label text 
    def MakeList(): 
        #label.config( text = clicked.get() ) 
        ColorElement = color.get()
        ShapeElement = shape.get()
        ColorShapeCoordQ = [ColorElement, ShapeElement, CoordLong.get(), CoordLat.get()] 
        print(ColorShapeCoordQ[0], ColorShapeCoordQ[1], ColorShapeCoordQ[2], ColorShapeCoordQ[3])
        ColorShapeList.append(ColorShapeCoordQ)
        print(ColorShapeList)
        #label.config( text = ColorShapeList ) 
    
    # Dropdown menu options 
    colors = [ 
        "White", 
        "Black", 
        "Red", 
        "Blue", 
        "Green", 
        "Purple", 
        "Brown",
        "Orange"
    ]

    shapes = [
        "Circle", 
        "Semicircle", 
        "Quarter Circle", 
        "Triange", 
        "Rectangle", 
        "Pentagon", 
        "Star",
        "Cross"
    ]


    
    # datatype of menu text 
    color = StringVar() 
    shape = StringVar()
    
    # initial menu text 
    color.set("White")
    shape.set("Circle")
    
    # Create Dropdown menu 
    colordrop = OptionMenu(frame2 , color , *colors) 
    colordrop.grid(column = 0, row = 1) 
    shapedrop = OptionMenu(frame2 ,shape, *shapes)
    shapedrop.grid(column = 1, row = 1)
    
    color_shape = ""
    # Create button, it will change label text 
    addList = Button(frame2 , text = "add to list" , command = MakeList ).grid(column = 2, row = 1)
    
    def submit():
        root.destroy()
        return(ColorShapeList)
    
    submit_button = Button(frame2, text = "END", command = submit).grid(column = 2, row = 0)
    
    frame2.pack()
    app.mainloop()
    
    
    ##long  x = cos alt     92  1.6057 radians 0.80285
    ##lat y = sin           63  1.09956 radians 0.54978
    ## 5568 × 4176
    # Folder where files are added
    