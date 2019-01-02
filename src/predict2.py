import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

img_width, img_height = 80, 80
model_path = './models/80_red_model.h5'
model_weights_path = './models/80_red_weights.h5'
test_path = './input_board_red'

model = load_model(model_path)
model.load_weights(model_weights_path)


def predict(file):
    x = load_img(file, target_size=(img_width,img_height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    # check this !
    array = model.predict(x)
    result = array[0]
    answer = np.argmax(result)
    # print(answer)
    return answer


count = [0, 0, 0, 0, 0, 0, 0]

name_array = [
    'ma',
    'phao',
    'si',
    'tinh',
    'tot',
    'tuong',
    'xe'
    ]

# count = [0, 0, 0]
# name_array = [
#     'blank',
#     'green',
#     'red'
#     ]

files = sorted(os.listdir(test_path))

for file in files:
    if file.startswith('.'):
        continue

    result = predict(test_path + '/' + file)
    print(file, result, name_array[result])
    count[result] += 1

print(count)