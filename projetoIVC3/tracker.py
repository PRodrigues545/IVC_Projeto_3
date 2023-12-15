import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
tracker = cv2.TrackerCSRT_create()

x, y, w, h = 300, 240, 100, 100
bbox = (x, y, w, h)

_, frame = cap.read()

img = cv2.rectangle(img=frame, pt1=(x, y), pt2=(x+w, y+h), color=255, thickness=2)
img = cv2.flip(img, 1)  # Invert the camera horizontally
cv2.imshow("Image", img)
tracker.init(frame, bbox)

def tracking():
    global cap  # Use the global cap object

    ret, frame = cap.read()

    if ret:
        track_ok, bbox = tracker.update(frame)
        if track_ok:
            x, y, w, h = bbox
            image_show = cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=255, thickness=2)
            center_x = x + w / 2
        else:
            image_show = frame.copy()
            cv2.putText(img=image_show,
                        text="Tracking failed",
                        org=(5, 35),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255),
                        thickness=2)
        cv2.imshow(winname="Image", mat=image_show)
    return center_x

def camara_loop():
    if not cap.isOpened():
        cap.open(0)
        _, image = cap.read()
    else:
        ret, image = cap.read()
        if not ret:
            print("Error")
        else:
            image = cv2.flip(image, 1)  # Invert the camera horizontally
            cv2.imshow("Image", image)
            center = tracking()
            if center is not None:
                image_out = image.copy()
                center_x = int(center)
                flipped_center_x = image.shape[1] - center_x  # Calculate flipped center
                cv2.circle(image_out, center=(flipped_center_x, int(image.shape[0] / 2)), radius=3,
                           color=(0, 255, 0), thickness=-1)
                cv2.imshow("Result", image_out)
                return flipped_center_x
