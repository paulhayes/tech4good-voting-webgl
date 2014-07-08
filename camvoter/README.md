## Intro
We have a few CamVoterX filters, using color-RGB distance or HSV values thresholding. Lots of tweaking to be done. Angle and size of the minimal bounding-box for blobs used to locate voting sticks. A number of factors, like image dilation, have been hand-tweaked. Minimum size of relevant blobs etc., will all be resolution and scene dependent. With a fixed camera almost all the light pollution from monitors, fluorescent bulbs and the like can be removed.

### camvoter
To test CamVoter:

$ python camvoter.py --fname <image-file>

### camvote
Very noisy in natural scene but should work well under controlled (dark) conditions. Lots of tweaking to be done.

$ python camvote.py

### socket-solution
First install the python requirements:

$ pip install -r requirements.txt

If no pip then easy_install pip should do it.

- set the server running

$ python server.py

- fire up web browser at localhost:5000
