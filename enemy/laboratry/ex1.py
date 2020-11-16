import cv2

for i in range(5):
    image = cv2.imread(f'walk_rigint_{i + 6}.png')
    # print(f'walk_rigint_{i + 5}.png')
    flipped_image = cv2.flip(image, 1)
    cv2.imwrite(f'walk_left_{i + 6}.png', flipped_image)
    print(i)