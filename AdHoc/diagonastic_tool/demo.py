from noise_add import NoiseAdd

if __name__ == '__main__':

    inpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/data-quality-data_HPE"
    outpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/HPE_output"

    field = "invoice_number"

## use case 1: default

    # pass 3 arguments to the constructur: input path, output path, field to be modified. will use default
    # runner = NoiseAdd(inpath, outpath, field)
    # call add_noise method on NoiseAdd instance
    # runner.add_noise()
    # retrieve results from the specified output path

## use case 2: specify noise types
    runner = NoiseAdd(inpath, outpath, field)
    runner.dicts = {"shrink": 0.3, "expand": 0.2, "random": 0.05}
    runner.add_noise()




