import SimpleCV as scv
import math
import cv2
import numpy as np
import argparse

MOVEMENT_FILTER_DEFAULTS = {
	'threshold' : 25,
	'multiplier': 1000,
	'mask_file': 'images/mask-2015.png'
}

class MovementVoter:
	def __init__(self,**kw):
		self.last_image = None
		self.current_image = None
		self.vote = 0
		self.__dict__.update( MOVEMENT_FILTER_DEFAULTS )
		self.mask = scv.Image(self.mask_file).flipHorizontal()
		print( "{0} {1}".format(self.mask.width, self.mask.height) )

	def set_image(self,img):

		self.current_image = img.grayscale() - self.mask

		if( self.last_image != None ): 
			self.comparison_image = ( self.last_image - self.current_image ).binarize(self.threshold)
			
			self.vote = 1.0 * self.multiplier * self.comparison_image.histogram(2)[0] / ( img.width * img.height );
			if self.vote == 1000.0:
				( self.last_image - self.current_image ).save('err-image1.jpg')

		self.last_image = self.current_image

	def get_vote_count(self):
		return self.vote

	def get_params(self):
		return MOVEMENT_FILTER_DEFAULTS.keys()

	def clear_votes(self):
		print("clearing votes"	)
		self.last_image = None
		if self.current_image : 
			self.current_image.save('images/image.jpg')

if __name__ == '__main__':
	print("run as main")
	images = [scv.Image('images/cam8.jpg'),scv.Image('images/cam9.jpg')]
	movement_voter = MovementVoter()
	movement_voter.set_image(images[0])
	movement_voter.set_image(images[1])
	print( movement_voter.get_vote_count() )
	movement_voter.comparison_image.show()
	str = input("Show image")

