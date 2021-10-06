# Adjutant

A package for delivering updates on long-running software tasks over Discord, Slack, and other platforms.

# Installation

```bash
pip install adjutant
```

# Examples

## Post a message

```python
import adjutant
adjutant.post('Hello, world!')
```

## Post an image

```python
import adjutant
adjutant.post('My image caption.', image_filename='my_image.png')
```

## As a TensorFlow Callback

By default, `AdjutantCallback()` will create a callback that posts the training and (if available) validation metrics after every epoch. Optional arguments allow it to post arbitrary data, e.g., input samples (as images, raw text, CSV data, etc.), misclassified training samples, the loss curve, neural network output (generated images, text, etc.).

```python
import tensorflow as tf
from adjutant.keras import AdjutantCallback

callbacks = [AdjutantCallback()]

# TODO add MNIST model
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')])
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])
model.fit(
    x=x_train,
    y=y_train,
    batch_size=32,
    epochs=10,
    validation_split=0.2,
    callbacks=callbacks)
```

## Request ML model prediction on an input

```python
import random
from adjutant.keras import AdjutantPredictor

def prediction_function(input_tensor: np.ndarray) -> str:
    # Prediction logic goes here.
    if random.random() < 0.5:
        return 'This is NOT an image of a dog.'
    return 'This is an image of a dog.'

predictor = AdjutantPredictor()
while True:
    predictor.run()
```
