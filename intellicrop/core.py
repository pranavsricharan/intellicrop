import cv2
import dlib


DETECTOR = dlib.get_frontal_face_detector()


def get_face_bounds(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = DETECTOR(gray, 1)
    return rects


def resize(img, size_x, size_y=None):
    size_y = size_y or size_x
    h, w = img.shape[:2]
    if size_y < h or size_x < w:
        scaling_factor_x = size_x/float(w)
        scaling_factor_y = size_y/float(h)
        scaling_factor = min(scaling_factor_x, scaling_factor_y)

        return cv2.resize(img, None, fx=scaling_factor,
                          fy=scaling_factor,
                          interpolation=cv2.INTER_AREA)
    return img


def get_relative_bounds(img, bounds):
    h, w = img.shape[:2]
    (x1, y1), (x2, y2) = bounds['pt1'], bounds['pt2']
    return ((x1/w), (y1/h)), ((x2/w), (y2/h))


def relative_to_absolute(img, rel_pt1, rel_pt2):
    rel_x1, rel_y1 = rel_pt1
    rel_x2, rel_y2 = rel_pt2
    h, w = img.shape[:2]
    x1, y1, x2, y2 = map(int, [w * rel_x1, h * rel_y1, w * rel_x2, h * rel_y2])
    w, h = x2 - x1, y2 - y1
    return {'pt1': (x1, y1), 'pt2': (x2, y2), 'w': w, 'h': h}


def get_sub_image(img, relative_bounds):
    (x1, y1), (x2, y2), _ = relative_to_absolute(img, *relative_bounds)
    return img[y1:y2, x1:x2]


def get_square_bounds(img, pt1, pt2):
    img_h, img_w = img.shape[:2]
    (x1, y1), (x2, y2) = pt1, pt2
    w, h = x2 - x1, y2 - y1

    if max(w, h) > min(img_h, img_w):
        w = h = min(img_h, img_w)

    if w > h:
        diff = w - h
        if diff % 2 == 0:
            top_inc = bottom_inc = diff // 2
        else:
            top_inc = diff // 2
            bottom_inc = diff - top_inc
        y1 -= top_inc
        y2 = y2 + bottom_inc

    elif h > w:
        diff = h - w
        if diff % 2 == 0:
            left_inc = right_inc = diff // 2
        else:
            left_inc = diff // 2
            right_inc = diff - left_inc
        x1 -= left_inc
        x2 = x2 + right_inc
    else:
        flag = False

        # Decrease boundary if it's greater than width
        while w < x2 - x1:
            if flag:
                x2 -= 1
            else:
                x1 += 1
            flag = not flag

        while h < y2 - y1:
            if flag:
                y2 -= 1
            else:
                y1 += 1
            flag = not flag

        # Increase boundary if it's lesser than width
        while w > x2 - x1:
            if flag:
                x2 += 1
            else:
                x1 -= 1
            flag = not flag

        while h > y2 - y1:
            if flag:
                y2 += 1
            else:
                y1 -= 1
            flag = not flag

    # Correct out of bounds
    if x1 < 0:
        x1, x2 = 0, x2 - x1

    if y1 < 0:
        y1, y2 = 0, y2 - y1

    if x2 > img_w:
        x1, x2 = (x1 - x2 - img_w), img_w

    if y2 > img_h:
        y1, y2 = (y1 - y2 - img_h), img_h

    return (x1, y1), (x2, y2)


def crop(img, face, spacing):
    img_h, img_w = img.shape[:2]
    (x1, y1), (x2, y2), w, h = face['pt1'], face['pt2'], face['w'], face['h']

    pixels_right = img_w - x2
    pixels_bottom = img_h - y2

    # Capture the region around face bounds
    if spacing == 'l':
        inc = 1.15
        top_inc = 1.45
    elif spacing == 'm':
        inc = 0.85
        top_inc = 1.1
    else:
        inc = 0.5
        top_inc = 0.75

    x1 = 0 if x1 < w * inc else x1 - int(w * inc)
    y1 = 0 if y1 < h * top_inc else y1 - int(h * top_inc)

    x2 = img_w if w * inc > img_w - x2 else x2 + int(w * inc)
    y2 = img_h if h * inc > img_h - y2 else y2 + int(h * inc)

    (x1, y1), (x2, y2) = get_square_bounds(img, (x1, y1), (x2, y2))
    img = img[y1:y2, x1: x2]
    w, h = x2 - x1, y2 - y1
    bounds = {'pt1': (x1, y1), 'pt2': (x2, y2), 'w': w, 'h': h}
    return bounds, img


def center_crop(img):
    h, w = img.shape[:2]

    if w > h:
        diff = w - h
        x1 = diff // 2
        x2 = w - diff // 2
        y1, y2 = 0, h
    else:
        diff = h - w
        y1 = diff // 2
        y2 = h - diff // 2
        x1, x2 = 0, w

    img = img[y1:y2, x1:x2]
    w, h = x2 - x1, y2 - y1
    bounds = {'pt1': (x1, y1), 'pt2': (x2, y2), 'w': w, 'h': h}
    return bounds, img


def intellicrop(img, size=None, spacing='m'):
    # Resize image and find relative face position for improved performance
    resized_img = resize(img, 1000)

    faces = get_face_bounds(resized_img)
    largest_face = None
    for face in faces:
        x, y = face.left(), face.top()
        w, h = face.right() - x, face.bottom() - y
        face_bounds = {'pt1': (x, y), 'pt2': (
            face.right(), face.bottom()), 'w': w, 'h': h}
        if largest_face is None:
            largest_face = face_bounds
            continue

        if w * h > largest_face['w'] * largest_face['h']:
            largest_face = face_bounds

    if largest_face:
        h, w = resized_img.shape[:2]
        (rel_x1, rel_y1), (rel_x2, rel_y2) = get_relative_bounds(
            resized_img, largest_face)
        crop_function = crop
        face_bounds = relative_to_absolute(
            img, (rel_x1, rel_y1), (rel_x2, rel_y2))
        args = (img, face_bounds, spacing)
        found = True

    else:
        crop_function = center_crop
        args = (img,)
        found = False

    crop_bounds, cropped_img = crop_function(*args)
    relative_bounds = get_relative_bounds(img, crop_bounds)
    result = {'found': found, 'img': cropped_img, 'bounds': crop_bounds,
              'relative_bounds': relative_bounds}

    if size:
        result['img'] = resize(result['img'], size)
    return result
