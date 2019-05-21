from noise_add import NoiseAdd

def diff_pos(html, field):
    with open(html) as tmp:
        soup = BeautifulSoup(tmp, "html.parser")
    tag = soup.find(field)
    ptag = tag.find_parent()
    while ptag.name != "line":
        ptag = ptag.find_parent()
    attributes = tag.attrs

if __name__ == '__main__':

    inpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/data-quality-data_HPE"
    outpath = "/Users/aaronyu/Desktop/Project15_DiagnosticTool/data-quality-data_HPE_noisy"

    field = "vendor_name"

    # construct an instance from NoiseAdd
    # pass 3 arguments to the constructur: input path, output path, field to be modified. will use default
    runner = NoiseAdd(inpath, outpath, field)

## use case 1: default settings

    # call add_noise method on NoiseAdd instance
    runner.add_noise()
    # get metadata - which file was modified by calling get_metadata() method
    runner.get_metadata()

## use case 2: specify noise types

    # dict keys must be one of these ["shrink", "expand", "random", "diff_pos", "swap"]
    # dict values must be float ranging from 0.0 to 1.0, sum of all values shouldn't be more than 1.0
    runner.dicts = {"shrink": 0.3, "expand": 0.2, "random": 0.05}


## use case 3: specify swapping relationships
    runner.swap_map = {"invoice_number": "vendor_zip"}







