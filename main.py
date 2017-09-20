# IMPORT LIBRARIES
from tensorflow.contrib.data import Dataset, Iterator
import tensorflow as tf
import random
import os

#############################################
# Simple code to read images into Tensorflow.
# Put all images in a folder, and change the DATASET_PATH below.
# Rune Wetteland - 20.09.2017
#############################################

# DEFINE PATH TO FOLDER WITH IMAGES
DATASET_PATH = "../Dataset/color_dataset/plot_images/"

# DEFINE PARAMETERS
NUM_CLASSES = 2
BATCH_SIZE  = 1
N_EPOCH     = 2

# CREATE ARRAY OF FILENAMES
img_arrary = []
lbl_arrary = []
for image in os.listdir(DATASET_PATH):
    if image[-3:] in ["png", "jpg", "jpeg", "bmp"]:
        img_arrary.append(DATASET_PATH + image)
        lbl_arrary.append(random.randint(0,1))  # (Append own labels here instead of random labels)

# Check that both arrays are same size
assert len(img_arrary) == len(lbl_arrary)

# Parsing function (decodes images into tensors)
def input_parser(img_path, label):
    # convert the label to one-hot encoding
    one_hot = tf.one_hot(label, NUM_CLASSES)

    # read the img from file
    img_file = tf.read_file(img_path)
    img_decoded = tf.image.decode_image(img_file)

    return img_decoded, one_hot

# Define tensorflow constants for each dataset
train_imgs = tf.constant(img_arrary)
train_labels = tf.constant(lbl_arrary)

# create TensorFlow Dataset objects
tf_dataset = Dataset.from_tensor_slices((train_imgs, train_labels))

# Parse dataset
tf_dataset = tf_dataset.map(map_func=input_parser, num_threads=None)

# Repeats the dataset n times (optional)
#tf_dataset = tf_dataset.repeat(2)

# Shuffle dataset (optional)
tf_dataset = tf_dataset.shuffle(buffer_size=len(img_arrary)*2)

# Set batch size
tf_dataset = tf_dataset.batch(BATCH_SIZE)

# Define an iterator
iterator = tf_dataset.make_initializable_iterator()
next_element = iterator.get_next()

# Start a session
with tf.Session() as sess:

    # Compute for N_EPOCH epochs.
    for _ in range(N_EPOCH):
        sess.run(iterator.initializer)
        while True:
            try:
                # Load new batch
                current_batch = sess.run(next_element)
                # [Use current batch to train model here]
            except tf.errors.OutOfRangeError:
                break

        # [Perform end-of-epoch calculations here.]
        print('Perform end-of-epoch calculations here')
