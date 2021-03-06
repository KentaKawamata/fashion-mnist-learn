#!/usr/bin/python3
# -*- encoding: UTF-8 -*-
from keras.datasets import fashion_mnist
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import matplotlib.pyplot as plt
import os
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import keras.backend.tensorflow_backend as KTF
from keras.utils import plot_model

def CNN(input_shape):
  model=Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(28,28,1)))
  model.add(Conv2D(64,(3,3),activation='relu'))
  model.add(MaxPooling2D(pool_size=(2,2)))
  model.add(Dropout(0.25))
  model.add(Flatten())
  model.add(Dense(128,activation='relu'))
  model.add(Dropout(0.5))
  model.add(Dense(10,activation='softmax'))
  early = EarlyStopping(monitor='val_loss', min_delta=0, patience=0, verbose=0, mode='auto')

  return model

def plot_history(history):

  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  #loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()

def main():
   
  batch_size = 128
  num_classes = 10
  epochs = 100
  img_rows, img_cols = 28, 28

  (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

  #デフォルトのフォーマットの規格を設定
  if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
  else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

  x_train = x_train.astype('float32')
  x_test = x_test.astype('float32')
  x_train /= 255
  x_test /= 255
    
  print('x_train shape:', x_train.shape)
  print(x_train.shape[0], 'train samples')
  print(x_test.shape[0], 'test samples')

  # one-hot表現
  y_train = keras.utils.to_categorical(y_train, num_classes)
  y_test = keras.utils.to_categorical(y_test, num_classes)

  model = CNN(input_shape)
  early = EarlyStopping()

  model.summary()
  plot_model(model, to_file="model.png", show_shapes=True, show_layer_names=True)

  model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam', metrics=['accuracy'])

  history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, \
                      verbose=1, validation_data=(x_test, y_test), callbacks=[early])

  plot_history(history)
   
  loss, acc = model.evaluate(x_test, y_test, verbose=0)
  print('Test loss:', loss)
  print('Test accuracy:', acc)

  print('save the architecture of a CNN model')
  json_string = model.to_json()
  open('cnn_model.json', 'w').write(json_string)
  print('save weight datasets!!')
  model.save_weights('mnist.h5')


if __name__ == "__main__":

  main()
