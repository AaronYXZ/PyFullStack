import tensorflow as tf
import model_utilities as utils

'''
Instantiates Model Architecture based on whats provided in the configuration file
'''


class ModelArch:

    def __init__(self, model_config):
        self.x = tf.placeholder(tf.float32,
                                shape=[None, model_config.img_size, model_config.img_size, model_config.num_channels],
                                name='x')

        # labels
        self.true_y = tf.placeholder(tf.float32, shape=[None, model_config.num_classes], name='y_true')
        self.y_true_cls = tf.argmax(self.true_y, dimension=1)

        # Network graph params
        self.filter_size_conv1 = model_config.filter_size_conv1
        self.num_filters_conv1 = model_config.num_filters_conv1
        self.filter_size_conv2 = model_config.filter_size_conv2
        self.num_filters_conv2 = model_config.num_filters_conv2
        self.filter_size_conv3 = model_config.filter_size_conv3
        self.num_filters_conv3 = model_config.num_filters_conv3
        self.fc_layer_size = model_config.fc_layer_size

        # learning rate
        self.learning_rate = model_config.learning_rate

        # Build conv net with default params
        self.layer_conv1 = utils.create_convolutional_layer(input=self.x,
                                                            num_input_channels=model_config.num_channels,
                                                            conv_filter_size=self.filter_size_conv1,
                                                            num_filters=self.num_filters_conv1)
        self.layer_conv2 = utils.create_convolutional_layer(input=self.layer_conv1,
                                                            num_input_channels=self.num_filters_conv1,
                                                            conv_filter_size=self.filter_size_conv2,
                                                            num_filters=self.num_filters_conv2)

        self.layer_conv3 = utils.create_convolutional_layer(input=self.layer_conv2,
                                                            num_input_channels=self.num_filters_conv2,
                                                            conv_filter_size=self.filter_size_conv3,
                                                            num_filters=self.num_filters_conv3)

        self.layer_flat = utils.create_flatten_layer(self.layer_conv3)

        self.layer_fc1 = utils.create_fc_layer(input=self.layer_flat,
                                               num_inputs=self.layer_flat.get_shape()[1:4].num_elements(),
                                               num_outputs=self.fc_layer_size,
                                               use_relu=True)

        self.layer_fc2 = utils.create_fc_layer(input=self.layer_fc1,
                                               num_inputs=self.fc_layer_size,
                                               num_outputs=model_config.num_classes,
                                               use_relu=False)

        self.y_pred = tf.nn.softmax(self.layer_fc2, name='y_pred')
        self.y_pred_cls = tf.argmax(self.y_pred, dimension=1, name="y_pred_cls")
        self.cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.layer_fc2, labels=self.true_y)
        self.cost = tf.reduce_mean(self.cross_entropy)
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
        self.correct_prediction = tf.equal(self.y_pred_cls, self.y_true_cls)
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_prediction, tf.float32), name="accuracy")
