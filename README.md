# Intellicrop
## Create intelligent thumbnails

Long gone are the days where you generate thumbnails for people's photos by cropping the pic from center. Use intellicrop to automatically detect faces and generate thumbnails around the face. If no faces are detected, it automatically does old school center crop.

Intellicrop uses OpenCV and supports all image types supported by it.

### Examples
![Example 1](https://i.imgur.com/AtItPRf.png "Example 1")
![Example 2](https://i.imgur.com/fQipZol.png "Example 2")
![Spacing](https://i.imgur.com/lY3lhR5.jpg "Example 3")
*Image credits:* [Brooke Cagle](https://unsplash.com/@brookecagle)

### Requirements
- Python3
- OpenCV
- Dlib

### Install
- Install Requirements using `pip install -r requirements.txt`
- Add intellicrop to your path

### Available functions
#### intellicrop(img [,size [,spacing='m']])
Takes an OpenCV image and an optional size (full size image will be returned if not specified) and does cropping. Control the spacing around the face with spacing parameter. Spacing takes a `str` as argument. Acceptable values are 's', 'm', 'l' for small, medium and large.

**Return**
A dict containing:
- `found`: [bool] True is face is found
- `img`: Cropped Image
- `bounds`: [dict] Boundary of crop box in original image
    - `pt1`: (x,y) top-left coordinates
    - `pt2`: (x,y) bottom-right coordinates
    - `w`: Width of crop area
    - `h`: Height of crop area
- `relative_bounds`: ((x1, y1), (x2, y2)) Relative boundary on a scale of 0 to 1 of crop box in original image

#### resize(img, size_x [, size_y])
Takes an OpenCV image and size (if size_y is not specified, size_y=size_x) and returns an image with the largest dimension equalling the specified size

#### get_sub_image(img, relative_bounds)
Takes an image that is proportional to the actual image whose relative bounds are provided and returns a cropped image

#### relative_to_absolute(img, rel_pt1, rel_pt2)
Returns the absolute coordinates ((x1, y1), (x2, y2)) for an image that is proportional to the actual image whose relative points are provided


### Usage
``` python
import cv2
from intellicrop import intellicrop, resize

img = cv2.imread('test.jpg')
cropped = intellicrop(img, spacing='l')
cropped_300 = resize(cropped['img'], 300)

cv2.imwrite('full.jpg', cropped['img'])
cv2.imwrite('s300x300.jpg', cropped_300)

```

### TODO
- Add support to rectangle crop
- Add support to Haar Classifiers when dlib cannot be installed/loaded
- Consider multiple nearby faces and do group cropping

