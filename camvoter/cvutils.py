import SimpleCV as scv
import math


def get_blobs_by_color(img, col=scv.Color.YELLOW):
    dist = img.colorDistance(col).invert()
    blobs = dist.findBlobs()
    return dist, blobs


def get_blobs_by_color2(img, col=scv.Color.YELLOW, stretch_thresh=200):
    dist = img.colorDistance(col).dilate(2)
    segmented = dist.stretch(stretch_thresh, 255)
    blobs = segmented.findBlobs()
    return blobs


def show_blobs(img, dist):
    img_blobs = img.copy()
    img_blobs.addDrawingLayer(dist.dl())
    res = img.sideBySide(img_blobs.applyLayers())
    res.show()
    return img_blobs


def filter_blobs(blobs, angle=70, area_max=200, area_min=0):
    filtered_blobs = blobs.filter([(math.fabs(b.angle()) > angle) and (b.area() > area_min) and (b.area() < area_max) for b in blobs])
    return filtered_blobs

            
def draw_blobs(blobs, col=scv.Color.PUCE):
    for b in blobs:
        b.draw(col)

def get_blob_votes(img, col=scv.Color.YELLOW, **kw):
    dist, blobs = get_blobs_by_color(img, col)
    filtered_blobs = filter_blobs(blobs, **kw)
    draw_blobs(filtered_blobs)
    show_blobs(img, dist)
    return filtered_blobs
    
    
if __name__ == '__main__':
    img = scv.Image('images/t4gimages/800/re_DSC_2470.jpg')
    while 1:
        votes = get_blob_votes(img)
        print 'Number of votes: ' + str(len(votes))
