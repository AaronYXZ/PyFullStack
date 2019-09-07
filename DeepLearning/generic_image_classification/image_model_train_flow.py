import dataset
import tensorflow as tf
import model_architecture
import os
import shutil

# Adding Seed so that random initialization is consistent
from numpy.random import seed


def load_data(train_path, img_size, classes, val_size):
    data, file_names = dataset.read_train_sets(train_path, img_size, img_size, classes, validation_size=val_size,
                                               image_ext=config.image_extension)
    print("Complete reading input data. Will Now print a snippet of it")
    print("Number of files in Training-set:\t{}".format(data.train.num_examples))
    print("Number of files in Validation-set:\t{}".format(data.valid.num_examples))

    return data, file_names


def show_progress(epoch, feed_dict_train, feed_dict_validate, val_loss, session, model_arch):
    acc = session.run(model_arch.accuracy, feed_dict=feed_dict_train)
    val_acc = session.run(model_arch.accuracy, feed_dict=feed_dict_validate)
    msg = "Training Epoch {0} --- Training Accuracy: {1:>6.1%}, Validation Accuracy: {2:>6.1%},  Validation Loss: {3:.3f}"
    print(msg.format(epoch + 1, acc, val_acc, val_loss))


def save_models(f_result, max_acc, output_path, saver, session, val_acc, val_result):
    if max_acc < val_acc:
        saver.save(session, os.path.join(output_path, 'model_best'))
        max_acc = val_acc
    with open(f_result, 'a') as f:
        for item in val_result:
            f.write("%s\n" % item)
    return max_acc


def set_seeds(tf_seed, np_seed):
    tf.set_random_seed(tf_seed)
    seed(np_seed)


def test_validation(epoch, feed_dict_tr, feed_dict_val, model_arch, session):
    tr_loss, tr_acc, tr_result = session.run([model_arch.cost, model_arch.accuracy, model_arch.y_pred],
                                             feed_dict=feed_dict_tr)
    val_loss, val_acc, val_result = session.run([model_arch.cost, model_arch.accuracy, model_arch.y_pred],
                                                feed_dict=feed_dict_val)
    # show_progress(epoch, feed_dict_tr, feed_dict_val, val_loss, session, model_arch)
    msg = "Training Epoch {0} --- Training Accuracy: {1:>6.1%}, " \
          "Validation Accuracy: {2:>6.1%},  Validation Loss: {3:.3f}"
    print(msg.format(epoch + 1, tr_acc, val_acc, val_loss))

    return val_acc, val_result


def run_train(train_path, model_config, output_path, num_iteration=300):
    global config
    config = model_config

    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)

    set_seeds(1, 1)
    model_arch = model_architecture.ModelArch(config)

    session = tf.Session()
    session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    f_label = '{}/labels.txt'.format(output_path)
    f_result = '{}/result.txt'.format(output_path)
    f_training = '{}/training.txt'.format(output_path)
    f_validation = '{}/validation.txt'.format(output_path)

    data, _ = load_data(train_path, config.img_size, config.classes, config.validation_size)

    with open(f_training, 'w') as f:
        for item in data.train.file_names:
            f.write("%s\n" % item)

    with open(f_validation, 'w') as f:
        for item in data.valid.file_names:
            f.write("%s\n" % item)
    ##########################################################

    max_acc = 0
    for i in range(num_iteration):
        print('iteration {}'.format(i))

        x_valid_batch, y_valid_batch, _, valid_cls_batch = data.valid.next_batch(config.batch_size)
        x_batch, y_true_batch, _, cls_batch = data.train.next_batch(config.batch_size)

        with open(f_label, 'a') as f:
            for item in y_valid_batch:
                f.write("%s\n" % item)

        feed_dict_train = {model_arch.x: x_batch, model_arch.true_y: y_true_batch}
        feed_dict_val = {model_arch.x: x_valid_batch, model_arch.true_y: y_valid_batch}

        session.run(model_arch.optimizer, feed_dict=feed_dict_train)

        if i % int(data.train.num_examples / config.batch_size) == 0:
            epoch = int(i / int(data.train.num_examples / config.batch_size))

            val_acc, val_result = test_validation(epoch, feed_dict_train, feed_dict_val, model_arch, session)
            saver.save(session, os.path.join(output_path, 'model'))
            max_acc = save_models(f_result, max_acc, output_path, saver, session, val_acc, val_result)
