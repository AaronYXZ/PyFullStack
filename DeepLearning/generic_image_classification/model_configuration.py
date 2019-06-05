class ModelConfiguration:

    def __init__(self):
        self.batch_size = 32
        self.classes = ['cat', 'dog']
        self.num_classes = len(self.classes)

        self.learning_rate = 1e-4

        # % of the data automatically used for validation
        self.validation_size = 0.2

        # image parameters
        self.img_size = 512
        self.num_channels = 3

        ##  Network graph params
        self.learning_rate = 1e-4

        self.filter_size_conv1 = 3
        self.num_filters_conv1 = 32
        self.filter_size_conv2 = 3
        self.num_filters_conv2 = 32
        self.filter_size_conv3 = 3
        self.num_filters_conv3 = 64
        self.fc_layer_size = 128

        self.image_extension = "jpg"

