# Intellicrop
## Create intelligent thumbnails

Long gone are the days where you generate thumbnails for people's photos by cropping the pic from center. Use intellicrop to automatically detect faces and generate thumbnails around the face. If no faces are detected, it automatically does old school center crop.

Intellicrop uses OpenCV and supports all image types supported by it.

### Examples
![Example 1](https://i.imgur.com/AtItPRf.png "Example 1")
![Example 2](https://i.imgur.com/fQipZol.png "Example 2")
![Example 3](https://i.imgur.com/6UdN3oH.png "Example 3")
*Image credits:* <a style="background-color:black;color:white;text-decoration:none;padding:4px 6px;font-family:-apple-system, BlinkMacSystemFont, &quot;San Francisco&quot;, &quot;Helvetica Neue&quot;, Helvetica, Ubuntu, Roboto, Noto, &quot;Segoe UI&quot;, Arial, sans-serif;font-size:12px;font-weight:bold;line-height:1.2;display:inline-block;border-radius:3px" href="https://unsplash.com/@brookecagle?utm_medium=referral&amp;utm_campaign=photographer-credit&amp;utm_content=creditBadge" target="_blank" rel="noopener noreferrer" title="Download free do whatever you want high-resolution photos from Brooke Cagle"><span style="display:inline-block;padding:2px 3px"><svg xmlns="http://www.w3.org/2000/svg" style="height:12px;width:auto;position:relative;vertical-align:middle;top:-1px;fill:white" viewBox="0 0 32 32"><title>unsplash-logo</title><path d="M20.8 18.1c0 2.7-2.2 4.8-4.8 4.8s-4.8-2.1-4.8-4.8c0-2.7 2.2-4.8 4.8-4.8 2.7.1 4.8 2.2 4.8 4.8zm11.2-7.4v14.9c0 2.3-1.9 4.3-4.3 4.3h-23.4c-2.4 0-4.3-1.9-4.3-4.3v-15c0-2.3 1.9-4.3 4.3-4.3h3.7l.8-2.3c.4-1.1 1.7-2 2.9-2h8.6c1.2 0 2.5.9 2.9 2l.8 2.4h3.7c2.4 0 4.3 1.9 4.3 4.3zm-8.6 7.5c0-4.1-3.3-7.5-7.5-7.5-4.1 0-7.5 3.4-7.5 7.5s3.3 7.5 7.5 7.5c4.2-.1 7.5-3.4 7.5-7.5z"></path></svg></span><span style="display:inline-block;padding:2px 3px">Brooke Cagle</span></a>

### Requirements
- Python3
- OpenCV
- Dlib

### Install
- Install Requirements using `pip install -r requirements.txt`
- Add intellicrop to your path

### Available functions
#### intellicrop(img [,size])
Takes an OpenCV image and an optional size (full size image will be returned if not specified) and does cropping

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
cropped = intellicrop(img)
cropped_300 = resize(cropped['img'], 300)

cv2.imwrite('full.jpg', cropped['img'])
cv2.imwrite('s300x300.jpg', cropped_300)

```

### TODO
- Add support to rectangle crop
- Add support to Haar Classifiers when dlib cannot be installed/loaded
- Consider multiple nearby faces and do group cropping

