from image_model_train_flow import run_train
import model_configuration
import sys

if __name__ == "__main__":
    input_dir = "./data/"
    output_path = "./model/"
    num_iter = 500

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-i":
            input_dir = sys.argv[i + 1]
        elif sys.argv[i] == "-o":
            output_path = sys.argv[i + 1]
        elif sys.argv[i] == "-n":
            num_iter = int(sys.argv[i + 1])

    model_config = model_configuration.ModelConfiguration()
    run_train(input_dir, model_config, output_path, num_iter)
