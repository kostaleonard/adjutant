# Adjutant

A package for delivering updates on software tasks over Discord, Slack, and other platforms.

# Installation

```bash
pip install adjutant
```

## Discord

To allow `adjutant` to post to discord as a bot, first follow [these instructions](https://discordpy.readthedocs.io/en/stable/discord.html) for creating a Discord bot and adding it to your Server. You then add your bot's token in `adjutant.init(discord_token='YOUR_TOKEN_HERE')`.

**Note: Be careful not to share your bot's token. Consider storing it in an environment variable or file that is not checked in to version control.**

# Examples

## Post a message

```python
import adjutant
adjutant.init(discord_token='YOUR_TOKEN_HERE')
adjutant.post('Hello, world!')
```

## Post an image

```python
import adjutant
adjutant.init(discord_token='YOUR_TOKEN_HERE')
adjutant.post('My image caption.', file='my_image.png')
```

## As a TensorFlow Callback

By default, `AdjutantCallback()` will create a callback that posts the training and (if available) validation metrics after every epoch. Optional arguments allow it to post arbitrary data, e.g., input samples (as images, raw text, CSV data, etc.), misclassified training samples, the loss curve, neural network output (generated images, text, etc.).

```python
import tensorflow as tf
import adjutant
from adjutant.keras import AdjutantCallback

adjutant.init(discord_token='YOUR_TOKEN_HERE')
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

`AdjutantPredictor()` takes as an argument a function that transforms an input tensor of several samples into any output. The `trigger` argument tells `adjutant` the prefix of the posts on which users are requesting prediction.

```python
import random
import adjutant
from adjutant.keras import AdjutantPredictor

adjutant.init(discord_token='YOUR_TOKEN_HERE')

def prediction_function(input_tensor: np.ndarray) -> str:
    # Prediction logic goes here.
    if random.random() < 0.5:
        return 'This is NOT an image of a dog.'
    return 'This is an image of a dog.'

predictor = AdjutantPredictor(prediction_function)
# This will block while it waits for and handles requests on messages.
predictor.run(trigger='$predict')
```
