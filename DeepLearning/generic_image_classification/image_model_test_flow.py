import os
import numpy as np
import tensorflow as tf
import fnmatch
import cv2
import json

# Adding Seed so that random initialization is consistent
from numpy.random import seed


def init_sess_and_model_arch(model_dir):
    tf.set_random_seed(1)
    seed(1)

    # Load the trained model architecture
    graph = tf.get_default_graph()
    sess = tf.Session(graph=graph)
    saver = tf.train.import_meta_graph(os.path.join(model_dir, 'model_best.meta'))
    saver.restore(sess, tf.train.latest_checkpoint(model_dir))

    return sess, graph


def apply_ds_to_image(image_dir, f):
    fin = os.path.join(image_dir, f)
    print("processing {}".format(fin))
    # Read the image from  file
    small_image = cv2.imread(fin)
    image = cv2.resize(small_image, (512, 512), 0, 0, cv2.INTER_LINEAR)
    image = image.astype(np.float32)
    image = np.multiply(image, 1.0 / 255.0)
    return image


def build_label_array(label_name):
    # pos_func is function to find if the image is of positive class
    # 0 index is positive class
    label = np.zeros(2)
    index = 0 if label_name == config.classes[0] else 1
    label[index] = 1
    return label


def classify_image(test_image, sess, graph):
    images = np.array([test_image])

    x = graph.get_tensor_by_name("x:0")
    y_pred = graph.get_tensor_by_name('y_pred:0')
    test_result_probs = sess.run(y_pred, feed_dict={x: images})
    return test_result_probs


def cat_func(image, cat_dir):
    image_name = image.split("/")[-1]
    images = fnmatch.filter(os.listdir(cat_dir), image_name)
    return True if images else False


def get_class_and_score(classes, test_probs):
    index = 0 if test_probs[0] > test_probs[1] else 1
    return classes[index], test_probs[index]


def build_extended_results(test_results, labels_json_path):
    with open(labels_json_path, "r") as f:
        gold_labels_dict = json.load(f)

    extended_results = []
    for result in test_results:
        doc_id = result["Id"]
        try:
            pred = result["Prediction"]
            score = result["Score"]
            label = gold_labels_dict[doc_id]
            result = "Correct" if pred == label else "Wrong"
            extended_results.append(
                {"Id": doc_id, "Prediction": pred, "Score": score, "Label": label, "Result": result})
        except Exception as ignore:
            print("Evaluation of {} document has caused error. Skipped.".format(doc_id))

    return extended_results


def calc_p_r_f1(results):
    stats_dict = {clazz: calc_prf1_class(clazz, results) for clazz in config.classes}
    stats_dict["Accuracy"] = np.mean([1 if x["Result"] == "Correct" else 0 for x in results])
    return stats_dict


def calc_prf1_class(clazz, results):
    tp = len([x for x in results if ((x["Prediction"] == clazz) & (x["Label"] == clazz))])
    fp = len([x for x in results if ((x["Prediction"] == clazz) & (x["Label"] != clazz))])
    fn = len([x for x in results if ((x["Prediction"] != clazz) & (x["Label"] == clazz))])
    p = float(tp) / (tp + fp + 0.00001)
    r = float(tp) / (tp + fn + 0.00001)
    f1 = p * r * 2 / (p + r + 0.00001)
    return {"TP": tp, "FP": fp, "FN": fn, "P": p * 100, "R": r * 100, "F1": f1 * 100}


def write_stat_results(output_dir, stats_dict, test_results):
    with open(os.path.join(output_dir, "accuracy.txt"), "w") as f:
        f.write("Overall Test Accuracy: {}%".format(np.round(stats_dict["Accuracy"], 4) * 100))

    with open(os.path.join(output_dir, "stats.csv"), "w") as f:
        f.write("Class,TP,FP,FN,P,R,F1\n")
        for key in stats_dict:
            if key != "Accuracy":
                row = "%s,%d,%d,%d,%.2f%%,%.2f%%,%.2f%%" % (key, stats_dict[key]["TP"], stats_dict[key]["FP"],
                                                            stats_dict[key]["FN"], stats_dict[key]["P"],
                                                            stats_dict[key]["R"], stats_dict[key]["F1"])
                f.write("{}\n".format(row))

    with open(os.path.join(output_dir, "output-results.csv"), "w") as f:
        f.write("Data,Gold,Prediction,Result,Score\n")
        for result in test_results:
            result_list = [result["Id"], result["Label"], result["Prediction"], result["Result"], result["Score"]]
            f.write("{}\n".format(",".join(result_list)))


def process_image(fin, graph, input_dir, sess):
    image = apply_ds_to_image(input_dir, fin)
    test_result_probs = classify_image(image, sess, graph)
    prediction, score = get_class_and_score(config.classes, test_result_probs[0])
    return prediction, score


def run_prediction_on_unseen(input_dir, output_dir, model_dir, write_results=True, class_threshold_dict={}):
    sess, graph = init_sess_and_model_arch(model_dir)
    test_files = os.listdir(input_dir)
    test_results = []

    for fin in test_files:
        prediction, score = process_image(fin, graph, input_dir, sess)
        # if prediction in class_threshold_dict and score < class_threshold_dict[prediction]:
        #     prediction = config.classes[0] if prediction != config.classes[0] else config.classes[1]
        test_results.append({"Id": fin, "Prediction": prediction, "Score": str(score)})
        print("Completed processing of {}".format(fin))

    if write_results:
        with open(output_dir + "/output-results.csv", "w") as f:
            f.write("Data,Prediction,Score\n")
            for result in test_results:
                result_list = [result["Id"], result["Prediction"], result["Score"]]
                f.write("{}\n".format(",".join(result_list)))

    return test_results


def calc_stats(label_json_path, output_dir, test_results):
    extended_results = build_extended_results(test_results, label_json_path)
    stats_dict = calc_p_r_f1(extended_results)
    write_stat_results(output_dir, stats_dict, extended_results)


def run_test_with_stats(input_dir, label_json_path, model_dir, output_dir):
    test_results = run_prediction_on_unseen(input_dir, output_dir, model_dir, write_results=False)
    calc_stats(label_json_path, output_dir, test_results)


def run(input_dir, output_dir, model_dir, model_config, label_json_path="", with_stats=False):
    global config
    config = model_config

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if not os.path.exists(output_dir):
        print("Input directory does not exist!")
        return

    if not os.path.exists(model_dir):
        print("Model directory does not exist!")
        return

    if with_stats:
        if (label_json_path != "") | (not os.path.exists(output_dir)):
            run_test_with_stats(input_dir, label_json_path, model_dir, output_dir)
        else:
            print("Missing or bad gold label json path, cannot execute!")
    else:
        run_prediction_on_unseen(input_dir, output_dir, model_dir)
