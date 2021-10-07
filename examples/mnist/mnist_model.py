"""Trains a new model on the MNIST dataset."""

import os
from typing import Tuple, Dict, Any, Optional
from datetime import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, History
import wandb
from wandb.keras import WandbCallback

DEFAULT_TENSORBOARD_LOGDIR = os.path.join('logs', 'mnist')
DEFAULT_MODEL_CHECKPOINT_FILENAME = os.path.join('models', 'mnist_model.h5')
DEFAULT_MODEL_ARGS = {'input_shape': (28, 28)}
DEFAULT_TRAIN_ARGS = {'epochs': 10,
                      'batch_size': 32,
                      'validation_split': 0.2,
                      'use_wandb': True,
                      'tensorboard_logdir': None,
                      'model_checkpoint_filename': None,
                      'overfit_single_batch': False}
MAX_PIXEL_VALUE = 255
WANDB_PROJECT_TITLE = 'mnist'


def get_dataset() -> Tuple[Tuple[np.ndarray, np.ndarray],
                           Tuple[np.ndarray, np.ndarray]]:
    """Returns the dataset that will be fed into the model as 2 2-tuples:
    (x_train, y_train), (x_test, y_test). The returned dataset will be
    normalized.

    :return: (x_train, y_train), (x_test, y_test)
    """
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = _normalize_images(x_train)
    x_test = _normalize_images(x_test)
    return (x_train, y_train), (x_test, y_test)


def _normalize_images(images: np.ndarray) -> np.ndarray:
    """Returns the image data normalized into the range [0, 1].

    :param images: The images to be normalized. A uint8 tensor of shape
        (m, w, h), where m is the number of samples, w is the image width, h is
        the image height.
    :return: The normalized images as a float32 tensor of the same shape as
        images.
    """
    return images.astype(np.float32) / MAX_PIXEL_VALUE


def get_model(model_args: Optional[Dict[str, Any]] = None) -> \
        tf.keras.Model:
    """Returns the model that will be used for training, testing, and
    prediction.

    :param model_args: The model arguments. If unspecified, will use
        DEFAULT_MODEL_ARGS. If specified, will be completed with
        DEFAULT_MODEL_ARGS if there are any missing values.
    :return: The Keras Model.
    """
    if not model_args:
        model_args = DEFAULT_MODEL_ARGS
    else:
        model_args = {**DEFAULT_MODEL_ARGS, **model_args}
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=model_args['input_shape']),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])
    return model


def train_model(model: tf.keras.Model,
                x_train: np.ndarray,
                y_train: np.ndarray,
                train_args: Optional[Dict[str, Any]] = None) -> History:
    """Trains the model and returns the History object from training.

    :param model: The Keras Model.
    :param x_train: The normalized training images.
    :param y_train: The training labels.
    :param train_args: The training arguments. If unspecified, will use
        DEFAULT_TRAIN_ARGS. If specified, will be completed with
        DEFAULT_TRAIN_ARGS if there are missing values.
    :return: The training history.
    """
    if not train_args:
        train_args = DEFAULT_TRAIN_ARGS
    else:
        train_args = {**DEFAULT_TRAIN_ARGS, **train_args}
    callbacks = []
    if train_args['use_wandb']:
        wandb.init(project=WANDB_PROJECT_TITLE, dir='.')
        callbacks.append(WandbCallback())
    if train_args['tensorboard_logdir']:
        log_dir = os.path.join(str(train_args['tensorboard_logdir']),
                               'logs_{0}'.format(datetime.now()))
        tensorboard_callback = TensorBoard(log_dir=log_dir)
        callbacks.append(tensorboard_callback)
    if train_args['model_checkpoint_filename']:
        checkpoint_callback = ModelCheckpoint(
            train_args['model_checkpoint_filename'],
            save_best_only=True)
        callbacks.append(checkpoint_callback)
    if train_args['overfit_single_batch']:
        x_train = x_train[:train_args['batch_size']]
        y_train = y_train[:train_args['batch_size']]
    return model.fit(x=x_train, y=y_train,
                     batch_size=train_args['batch_size'],
                     epochs=train_args['epochs'],
                     validation_split=train_args['validation_split'],
                     callbacks=callbacks)


def eval_model(model: tf.keras.Model, x_test: np.ndarray,
               y_test: np.ndarray) -> float:
    """Evaluates the model on the test set and returns the accuracy.

    :param model: The Keras Model.
    :param x_test: The normalized test images.
    :param y_test: The test labels.
    :return: The accuracy on the test set.
    """
    return model.evaluate(x=x_test, y=y_test, return_dict=True)['accuracy']


def main() -> None:
    """Runs the program."""
    (x_train, y_train), (x_test, y_test) = get_dataset()
    model = get_model()
    train_args = {
        'use_wandb': True,
        'tensorboard_logdir': DEFAULT_TENSORBOARD_LOGDIR,
        'model_checkpoint_filename': DEFAULT_MODEL_CHECKPOINT_FILENAME}
    _ = train_model(model, x_train, y_train, train_args=train_args)
    test_acc = eval_model(model, x_test, y_test)
    print('Test accuracy: {0}'.format(test_acc))


if __name__ == '__main__':
    main()