from noise_add import NoiseAdd


inpath = "resources"
# outpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/practice_data/output"
outpath = "resources/output"
field = "invoice_number"

if __name__ == '__main__':

    runner = NoiseAdd(inpath, outpath, field)
    runner.add_noise()