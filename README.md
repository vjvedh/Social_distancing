Social Distancing App

> In the first step, focal length 'f' of the camera was calculated by taking a reference object of width 'w' and at a distance of 'd'.
     f = ( (Pixcel_width of the object in image) * d ) / w
  For my camera; w = 17cm, d = 30cm, Pixcel_widht = 200px, f = 400
  
  Hence, for detection of distance from camera = (f * w) / Pixcel_width

> In the second step, the face was captured and a bounding box was put over the face using Haar Cascade Frontal-face Model.
  Also, the distance of person from camera was put in the bounding box of the faces and different ID was assigned to each face.
  Using the coordinates of the bonding box, centroid of the face was measured using mid-point formula and was stored in a variable for future calculation of distane between multiple faces.
  
> In the thid step, using the centroids of multiple faces each distance was calculated using Euclidean Distance. Then centroid distance that is in pixcels were mapped to distance in cm.

