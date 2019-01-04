# python search_bing_api.py --query "turtle" --query "turtle face" --query "cute turtle" --query "turtle close up" --output predict/turtle
# import the necessary packages
import argparse
import numpy as np
from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to the model we will use")
ap.add_argument("-p", "--prediction_image_dir", required=True,
	help="path of input images for predictions")
args = vars(ap.parse_args())

model = load_model(args["model"])
datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies

generator=datagen.flow_from_directory(args["prediction_image_dir"], # this is where you specify the path to the main data folder
                                        target_size=(229,229),
                                        color_mode='rgb',
                                        batch_size=32,
                                        class_mode='categorical',
                                        shuffle=False)

step_size_test=generator.n//generator.batch_size
preds = model.predict_generator(generator, steps=step_size_test)
print('Predicted')
for i, pred in enumerate(preds):
    print(i, ':', np.round(pred), (pred[0] - pred[1]) ** 2)