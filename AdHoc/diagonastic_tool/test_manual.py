from noise_add import NoiseAdd


if __name__ == '__main__':
    test = False
    if test:
        inpath = "resources/sample"
        outpath = "resources/output"
    else:
        inpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/NosieAddingPlayground/train_ori"
        outpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/NosieAddingPlayground/bill_to_name"

    field = "bill_to_name"
    # if os.path.exists(inpath):
    #     os.removedirs(inpath)
    runner = NoiseAdd(inpath, outpath, field)
    # runner.dicts = {"diff_pos": 0.2}
    runner.dicts = {"shrink": 0.02, "expand": 0.02, "random": 0.02, "swap": 0.02, "diff_pos": 0.02}
    runner.add_noise()
    runner.get_metadata()

