import image_model_test_flow as workflow
import model_configuration
import sys

if __name__ == "__main__":
    # input_dir = "./data/"
    # label_json_path = "./labels.json"
    # output_path = "./model/results/"
    # model_dir = "./model/"

    input_dir = "/Users/nelsonc/Downloads/dogs-vs-cats/val-small/"
    label_json_path = "/Users/nelsonc/Downloads/dogs-vs-cats/labels.json"
    output_path = "/Users/nelsonc/Downloads/dogs-vs-cats/models/temp_model-9"
    model_dir = "/Users/nelsonc/Downloads/dogs-vs-cats/models/temp_model-9"

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-i":
            input_dir = sys.argv[i + 1]
        elif sys.argv[i] == "-j":
            label_json_path = sys.argv[i + 1]
        elif sys.argv[i] == "-o":
            output_path = sys.argv[i + 1]
        elif sys.argv[i] == "-m":
            model_dir = sys.argv[i + 1]

    model_config = model_configuration.ModelConfiguration()
    workflow.run(input_dir, output_path, model_dir, model_config, with_stats=True, label_json_path=label_json_path)
