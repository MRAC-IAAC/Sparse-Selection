#http://datahacker.rs/005-how-to-create-a-panorama-image-using-opencv-with-python/

import cv2
import numpy as np
import copy
import glob
import os


path = "G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/frames/*.*"
for index, file in enumerate(glob.glob(path)):
    #print(index)
    n = 1
    path_to_crnfile = glob.glob(path)[index == 1]
    path_to_nxtfile = glob.glob(path)[index + n]

    img = path_to_crnfile
    img2 = path_to_nxtfile
    print('image 1', img)
    print('image 2', img2)

    img01 = cv2.imread(img)
    img02 = cv2.imread(img2)

    #cv2.imshow('image', img01)
    #cv2.imshow('image 2', img02)

    img01_gray = cv2.cvtColor(img01, cv2.COLOR_BGR2GRAY)
    img02_gray = cv2.cvtColor(img02, cv2.COLOR_BGR2GRAY)

    # Create our ORB detector and detect keypoints and descriptors
    orb = cv2.ORB_create(nfeatures=2000)

    # Find the key points and descriptors with ORB
    keypoints1, descriptors1 = orb.detectAndCompute(img01, None)
    keypoints2, descriptors2 = orb.detectAndCompute(img02, None)

    # Create a BFMatcher object.
    # It will find all of the matching keypoints on two images
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

    # Find matching points
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)


    def draw_matches(img01, keypoints1, img02, keypoints2, matches):
        r, c = img01.shape[:2]
        r1, c1 = img02.shape[:2]

        # Create a blank image with the size of the first image + second image
        output_img = np.zeros((max([r, r1]), c + c1, 3), dtype='uint8')
        output_img[:r, :c, :] = np.dstack([img01, img01, img01])
        output_img[:r1, c:c + c1, :] = np.dstack([img02, img02, img02])

        # Go over all of the matching points and extract them
        for match in matches:
            img1_idx = match.queryIdx
            img2_idx = match.trainIdx
            (x1, y1) = keypoints1[img1_idx].pt
            (x2, y2) = keypoints2[img2_idx].pt

            # Draw circles on the keypoints
            cv2.circle(output_img, (int(x1), int(y1)), 4, (0, 255, 255), 1)
            cv2.circle(output_img, (int(x2) + c, int(y2)), 4, (0, 255, 255), 1)

            # Connect the same keypoints
            cv2.line(output_img, (int(x1), int(y1)), (int(x2) + c, int(y2)), (0, 255, 255), 1)

        return output_img


    all_matches = []
    for m, n in matches:
        all_matches.append(m)

    img03 = draw_matches(img01_gray, keypoints1, img02_gray, keypoints2, all_matches[:30])
    #cv2.imshow('image3', img03)
    #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Matches_{}.jpg'.format(index), img03)

    # Finding the best matches
    good = []
    for m, n in matches:
        if m.distance < 0.5 * n.distance:
            good.append(m)


    def warpImages(img01, img02, H):
        rows1, cols1 = img01.shape[:2]
        rows2, cols2 = img02.shape[:2]

        list_of_points_1 = np.float32([[0, 0], [0, rows1], [cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
        temp_points = np.float32([[0, 0], [0, rows2], [cols2, rows2], [cols2, 0]]).reshape(-1, 1, 2)

        # When we have established a homography we need to warp perspective
        # Change field of view
        list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

        list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

        [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

        translation_dist = [-x_min, -y_min]

        H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

        output_img = cv2.warpPerspective(img01, H_translation.dot(H), (x_max - x_min, y_max - y_min))
        a = copy.deepcopy(output_img)
        output_img[translation_dist[1]:rows1 + translation_dist[1],
        translation_dist[0]:cols1 + translation_dist[0]] = img02
        b = copy.deepcopy(a)
        b = b * 0
        b[translation_dist[1]:rows1 + translation_dist[1], translation_dist[0]:cols1 + translation_dist[0]] = img02

        return output_img, a, b

    # Set minimum match condition
    MIN_MATCH_COUNT = 10

    if len(good) > MIN_MATCH_COUNT:
        # Convert keypoints to an argument for findHomography
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        # Establish a homography
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        im, a, b = warpImages(img01, img02, M)
        #cv2.imshow('img_01', a)
        #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/image1_{}.jpg'.format(index), a)
        #cv2.imshow('img_02', b)
        #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/image2_{}.jpg'.format(index), b)
        #cv2.imshow('result', im)
        #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Stitching_{}.jpg'.format(index), im)


        # Overlap

        new_mask = a & b
        # Mask Visualization

        new_mask_gray = cv2.cvtColor(new_mask, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(new_mask_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imshow('mask', thresh1)
        #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/thresh_{}.jpg'.format(index), thresh1)
        # Print Overlap
        overlap = int(new_mask.mean())
        print(f'Overlap = {overlap:.2f}%')
        # Save Overlap Image

    if overlap <= 70 and overlap >= 60:
        i = 1
        #cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Photogrammetry/Ph1_{}.jpg'.format(index), img01)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Photogrammetry/Ph2_{}.jpg'.format(index), img02)
        cv2.imshow('img_01', a)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/image1_{}.jpg'.format(index), a)
        cv2.imshow('img_02', b)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/image2_{}.jpg'.format(index), b)
        cv2.imshow('result', im)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Stitching_{}.jpg'.format(index), im)
        cv2.imshow('image3', img03)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Matches_{}.jpg'.format(index), img03)
        cv2.imshow('mask', thresh1)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/thresh_{}.jpg'.format(index), thresh1)
        cv2.imwrite('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/Ph2_{}.jpg'.format(index), img02)
        i += 1
        print("Image saved \n")
        break
        cv2.waitKey(0)
        cv2.destroyAllWindows()
#Call Last image

#list_of_files = glob.glob('G:/Mi unidad/01_TERM II - GROUP WORK FOLDER/SOFTWARE II - GROUP WORK FOLDER/06_Videos/images/*.*')
#latest_file = max(list_of_files, key=os.path.getctime)
#limg = cv2.imread(latest_file) #<--can use this to see if you have the latest file
#cv2.imshow('Last_Image', limg)



#cv2.waitKey(0)
#cv2.destroyAllWindows()