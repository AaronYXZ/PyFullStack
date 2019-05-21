from noise_add import NoiseAdd


if __name__ == '__main__':
    test = False
    if test:
        inpath = "resources/sample"
        outpath = "resources/output"
    else:
        inpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/data-quality-data_HPE"
        outpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/HPE_output"

    field = "vendor_name"
    # if os.path.exists(inpath):
    #     os.removedirs(inpath)
    runner = NoiseAdd(inpath, outpath, field)
    runner.add_noise()
    runner.get_metadata()