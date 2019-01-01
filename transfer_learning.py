# taken from https://keras.io/applications/#inceptionv3

from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.callbacks import LambdaCallback
from keras import metrics
import meeshkan
import time

# create the base pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# from experimenting, I find that this network works best
# with a couple intermediary dense layers before getting
# to the final classifier
# this type of thing is difficult to anticipate beforehand
# and comes from tweaking/experience
# feel free to play around with the number of dense layers and
# their size, but 1024 > 512 > 32 > 2 is a sensible default
x = Dense(512, activation='relu')(x)
x = Dense(32, activation='relu')(x)
# and a logistic layer -- we have 2 classes - koopa troopers and tmnt
predictions = Dense(2, activation='softmax')(x)

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=[metrics.categorical_accuracy])

def on_batch_end(batch, logs):
    try:
        print(float(logs['loss']))
        meeshkan.report_scalar("train loss", float(logs['loss']))
    except Exception as e:
        print(e)

meeshkan_callback = LambdaCallback(on_batch_end=on_batch_end)

def _make_generator(destFolder):
    train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies

    train_generator=train_datagen.flow_from_directory(destFolder, # this is where you specify the path to the main data folder
                                                    target_size=(229,229),
                                                    color_mode='rgb',
                                                    batch_size=32,
                                                    class_mode='categorical',
                                                    shuffle=True)
    return train_generator


def make_train_generator():
    return _make_generator('./train/')

def make_test_generator():
    return _make_generator('./test/')

train_generator = make_train_generator()
step_size_train=train_generator.n//train_generator.batch_size
# train the model on the new data for a few epochs
model.fit_generator(generator=train_generator,
                   steps_per_epoch=step_size_train,
                   epochs=1,
                   callbacks=[meeshkan_callback])

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=[metrics.categorical_accuracy])

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
train_generator = make_train_generator()
step_size_train=train_generator.n//train_generator.batch_size
# train the model on the new data for a few epochs
model.fit_generator(generator=train_generator,
                   steps_per_epoch=step_size_train,
                   epochs=1,
                   callbacks=[meeshkan_callback])

model.save('tmnt_koopa_%d.h5' % (int(time.time()*1000),))

test_generator = make_test_generator()
step_size_test=test_generator.n//test_generator.batch_size
model.evaluate_generator(generator=test_generator)