#https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/

import cv2

# Opens the Video file
cap = cv2.VideoCapture('C:/Users/aebro/Desktop/test_1.mp4')
#cap = cv2.VideoCapture(0)
i = 1
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i % 2 == 0:
        cv2.imwrite('C:/Users/aebro/Desktop/frames/frame' + str(i) + '.jpg', frame)
    i += 1
    print('frame', i)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('Size', width, height)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps, 'fps \n')

    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
