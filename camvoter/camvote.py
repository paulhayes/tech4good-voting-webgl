'''
A light-stick voting system, with vertically aligned sticks counting as positive.
'''
print __doc__
import SimpleCV as scv
import cvutils
from camvoter import CamVoterHSV, CamVoterCol

display = scv.Display()
cam = scv.Camera()
normaldisplay = True
camv = CamVoterHSV()

while display.isNotDone():

	# if display.mouseRight:
	# 	normaldisplay = not(normaldisplay)
	# 	print "Display Mode:", "Normal" if normaldisplay else "Segmented" 
	
	camv.set_image(cam.getImage().flipHorizontal())
        votes = camv.get_vote_count()
        print 'We have %d votes'%votes
        print camv.filtered_blobs
	if votes:
            for b in camv.filtered_blobs:
                camv.image.drawCircle((b.x, b.y), 5, scv.Color.RED)

	# if normaldisplay:
	# 	camv.image.show()
	# else:
        camv.image.show()
		



