from picamera2 import Picamera2, MappedArray, Preview
import cv2
import time
import numpy as np

picam2 = Picamera2()

#config = picam2.create_preview_configuration(main={"size": (480, 640)})
#picam2.configure(config)
picam2.start()

array = picam2.capture_array("main")

print(array.shape)

Tile_dict = {'tile0': [0, 240, 0, 160], 'tile1': [0, 240, 160, 320], 'tile2': [0, 240, 320, 480], 'tile3': [0, 240, 480, 640], 'tile4': [240, 480, 0, 160], 'tile5': [240, 480, 160, 320], 'tile6': [240, 480, 320, 480], 'tile7': [240, 480, 480, 640]}



def create_rgb(color):
    red, green, blue = int(color[0]), int(color[1]), int(color[2])
    return (red, green, blue)


def tilesRGB(frame, Tile_dict = {}):
    k = 0
    tiles_rgb_values = []
    for tileCoord in Tile_dict.values():
        tile = frame[tileCoord[0]:tileCoord[1],tileCoord[2]:tileCoord[3]]

        img = tile
        height, width, _ = np.shape(img)
        print(height, width)
        print(img.shape)

        data = np.reshape(img, (height * width, 4))
        data = np.float32(data)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
        #print(centers)

        rgb_values = []

        for index, row in enumerate(centers):
            rgb = create_rgb(row)
            rgb_values.append(rgb)

        tiles_rgb_values.append(rgb_values[0])
        #print(rgb_values)
        k+=1

    return tiles_rgb_values

#print(tilesRGB(array, Tile_dict))

def data_differs(data1, data2, threshold=0.01):
    # Compares if the new data differs from the old data beyond a threshold
    if data1 is None or data2 is None:
        return True
    return np.linalg.norm(np.array(data1) - np.array(data2)) > threshold
last_data = None
while True:
    start_time = time.time()
    result = tilesRGB(array, Tile_dict)
    result_x = ""
    for x in result:
        str_x = str(x)
        result_x += str_x[1:-1] + ","
    current_data = result_x
    print(result_x) 
    if data_differs(current_data, last_data):
        print(result_x) 
        #s.sendall(str(current_data).encode())
        last_data = current_data
        # Ensure 60Hz operation
    time.sleep(max(0, (1/60) - (time.time() - start_time)))

#cv2.imshow("Image", array)
cv2.waitKey(0)
