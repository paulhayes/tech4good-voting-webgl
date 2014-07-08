"""
Colors to filter (as given by GIMP):
pink: 255, 42, 255
yellow: 255, 255, 0

We have a few Camvoters, using various filters. CamVoterHSV seems likely to get the best results, using the pixel value as a threshold. This corresponds pretty well to brightness, picking up the glowsticks (and fluorescent monitors, lights etc.).

We should normalize on a fixed background - just fix the camera and create a mask with averaged pixels over time.
"""
import SimpleCV as scv
import math
import cv2
import numpy as np
import argparse


VOTING_COLORS = [scv.Color.YELLOW]
BLOB_FILTER_DEFAULTS = {
    'dilate':2,
    'stretch_min':200,
    'stretch_max':255,
    'angle': 70,
    'area_max': 400,
    'area_min': 20,
    'thresh_V':220,
    'draw_color':scv.Color.PUCE,
    'draw_color_filtered':scv.Color.RED,
    'colors': VOTING_COLORS
    }


class CamVoter(object):

    def __init__(self, image=None, **kw):
        self.image = image
        if self.image:
            self.image_HSV = image.toHSV()
        self.__dict__.update(BLOB_FILTER_DEFAULTS)
        self.__dict__.update(**kw)

    def set_image(self, img):
        self.image = img
        self.image_HSV = img.toHSV()

    def get_vote_count(self):
        self.get_blobs()
        self.filter_blobs()
        return self.filtered_blobs.count()
        
    def filter_blobs(self):
        self.filtered_blobs = self.all_blobs and self.all_blobs.filter([(math.fabs(b.angle()) > self.angle) and (b.area() > self.area_min) and (b.area() < self.area_max) for b in self.all_blobs]) or scv.FeatureSet()
        return self.filtered_blobs

    def show_blobs(self):
        
        for b in self.all_blobs:
            self.image.drawCircle((b.x, b.y), 5, self.draw_color)
        for b in self.filtered_blobs:
            self.image.drawCircle((b.x, b.y), 5, self.draw_color_filtered)
            
        while True:
            self.image.show()
        
            
class CamVoterCol(CamVoter):
    
    def get_blobs(self):
        self.colored_blobs = []
        self.all_blobs = scv.FeatureSet()
        for col in self.colors:
            dist = self.image.colorDistance(col).dilate(1)
            segmented = dist.stretch(self.stretch_min, self.stretch_max)
            blobs = segmented.findBlobs()
            self.colored_blobs.append({'blobs':blobs, 'dist':dist})
            if blobs:
                self.all_blobs += blobs
                 

class CamVoterCol2(CamVoter):
    
    def get_blobs(self):
        self.colored_blobs = []
        self.all_blobs = scv.FeatureSet()
        for col in self.colors:
            dist = self.image.colorDistance(col).invert()
            blobs = dist.findBlobs()
            self.colored_blobs.append({'blobs':blobs, 'dist':dist})
            if blobs:
                self.all_blobs += blobs

            
class CamVoterHSV(CamVoter):

    def get_blobs(self):
        
        self.image_hot = cv2.inRange(self.image_HSV.getNumpyCv2(), np.array([0, 0, self.thresh_V]), np.array([179, 255, 255]))
        # and back to scv <sigh>
        self.image_hot = scv.Image(self.image_hot, cv2image = True).dilate(self.dilate)
        self.all_blobs = self.image_hot.findBlobs() 
         
    def show_blobs(self):
        
        for b in self.all_blobs:
            b.draw(color=self.draw_color, width=2)
        for b in self.filtered_blobs:
            b.draw(color=self.draw_color_filtered, width=2)
            
        while True:
            self.image.sideBySide(self.image_hot.applyLayers()).show()
            # self.all_blobs.show()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Locate voting glowsticks (orientation approx. vertical) in image.')

    parser.add_argument('--fname', help='file to process',
                    default='images/2470_800.jpg')
    args = parser.parse_args()
    cv = CamVoterHSV(scv.Image(args.fname))
    count = cv.get_vote_count()
    print 'Number of estimated votes: ' + str(count)
    cv.show_blobs()
