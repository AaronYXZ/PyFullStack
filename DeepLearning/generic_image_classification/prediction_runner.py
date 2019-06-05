import image_model_test_flow as workflow
import model_configuration
import sys
import os

if __name__ == "__main__":
    input_dir = "./data/"
    model_dir = "./model/"
    output_dir = os.path.join(model_dir, "results/")

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-i":
            input_dir = sys.argv[i + 1]
        elif sys.argv[i] == "-o":
            output_dir = sys.argv[i + 1]
        elif sys.argv[i] == "-m":
            model_dir = sys.argv[i + 1]

    model_config = model_configuration.ModelConfiguration()
    workflow.run(input_dir, output_dir, model_dir,model_config, with_stats=False)
