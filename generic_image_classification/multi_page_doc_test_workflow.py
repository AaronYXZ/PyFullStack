import image_model_test_flow as test_flow
import fnmatch
import os
import re


def find_next_pages(page_1, page_file_dir):
    page_prefix = "-".join(page_1.split("-")[:-2])
    pages = fnmatch.filter(os.listdir(page_file_dir), page_prefix + "-page-*.png")
    pages.remove(page_1)
    return pages


def find_all_pages(page_1, page_file_dir):
    page_prefix = "-".join(page_1.split("-")[:-2])
    pages = fnmatch.filter(os.listdir(page_file_dir), page_prefix + "-page-*.png")
    return pages if len(pages) > 0 else [page_1]


def find_any_page(page_1, page_file_dir):
    page_prefix = "-".join(page_1.split("-")[:-2])
    pages = fnmatch.filter(os.listdir(page_file_dir), page_prefix + "-page-*.png")
    return True if pages else False


def test_whole_doc(input_dir, image_id, sess, graph):
    prediction, score = "", 0.0
    for f in find_all_pages(image_id, input_dir):
        prediction, score = test_flow.process_image(f, graph, input_dir, sess)
        if prediction == config.classes[0]:
            break

    return prediction, score


def get_doc_id(page_id):
    regex = "-page-\d{1,2}\..+$"
    return re.sub(regex, "", page_id)


def run_multi_page_prediction(input_dir, output_dir, model_dir, write_result=True):
    sess, graph = test_flow.init_sess_and_model_arch(model_dir)
    test_files = os.listdir(input_dir)
    test_results = []

    for image_id in test_files:
        # if page 1 returns stamp, then done, otherwise see if there is page 2 and or 3 and if so, is it stamp?
        if "page-1" in image_id:
            doc_id = get_doc_id(image_id)
            prediction, score = test_whole_doc(input_dir, image_id, sess, graph)
            if prediction != "":
                test_results.append([doc_id, prediction, str(score)])
            else:
                print("No prediction was made on {}!".format(doc_id))

    if write_result:
        with open(output_dir + "/output-results.csv", "w") as f:
            f.write("Document,Result,Score")
            for test_result in test_results:
                f.write("{}\n".format(",".join(test_result)))

    return test_results


def run_multi_page_with_stats(test_dir, labels_json_path, model_dir, output_dir):
    test_results = run_multi_page_prediction(test_dir, output_dir, model_dir, write_result=False)
    test_flow.calc_stats(labels_json_path, output_dir, test_results)


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
            run_multi_page_with_stats(input_dir, label_json_path, model_dir, output_dir)
        else:
            print("Missing or bad gold label json path, cannot execute!")
    else:
        run_multi_page_prediction(input_dir, output_dir, model_dir)
