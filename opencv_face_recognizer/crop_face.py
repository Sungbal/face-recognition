import cv2
import numpy as np
import os

def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    CASCADE_PATH = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
    #CASCADE_PATH = '../haarcascades/haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)

    if (len(faces) == 0):
        return None, None
    elif (len(faces) > 1):
        best_sz = 0
        best_ind = 0
        for idx in range(len(faces)):
            face = faces[idx]
            sz = face[0] * face[1]
            if (sz > best_sz):
                best_sz = sz
                best_ind = idx
            else:
                pass
        (x,y,w,h) = faces[best_ind]
        return gray[y:y+w, x:x+h], faces[best_ind]
    else:
        (x,y,w,h) = faces[0]
        return gray[y:y+w, x:x+h], faces[0]

def _main(args):
    data_dir = 'images/17'
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, data_dir)
    print ('\nDATA IN : ' + data_dir)

    if (os.path.exists(data_dir)):
        print ('Data loading...\n')
        cnt = 1
        accept = 1
        for image_name in os.listdir(data_dir):
            image_path = os.path.join(data_dir, image_name)
            
        # try:
            image = cv2.imread(image_path)
            if image is not None:
                print ('[Load Image: #' + str(cnt) +'] '+ image_path)
                cnt = cnt + 1

                face, rect = detect_face(image)
                if (rect is not None):
                    fname = str(accept) + '.jpeg'
                    sv_dir = os.path.join(data_dir, 'crop', fname)
                    print ('                Save Image #' + fname)
                    cv2.imwrite(sv_dir, face)
                    accept = accept + 1
                else:
                    print('     !!!!        Face not found')
            else:
                pass

        # except ValueError:
        #     print('Path provided is not a valid file: {}'.format(image_path))
    else:
        print('Directory does not exist.')
        exit(1)

    print('Saved %d faces in %s' %(accept-1, data_dir))


if (__name__ == '__main__'):
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    _main(args)