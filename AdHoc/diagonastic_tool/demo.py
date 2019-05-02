from bs4 import BeautifulSoup
from noise_add import NoiseAdd


def shrink(html, field, num, **kwargs):
    with open(html) as tmp:
        soup = BeautifulSoup(tmp, "html.parser")
    tag = soup.find(field)
    string = tag.string

    shrinked_string = string


def expand(html, field):
    with open(html) as tmp:
        soup = BeautifulSoup(tmp, "html.parser")
    tag = soup.find(field)
    ptag = tag.find_parent()
    while ptag.name != "line":
        ptag = ptag.find_parent()
    attributes = tag.attrs
    expanded_string = ptag.text.strip()
    tag.string =expanded_string
    for k, v in attributes.items():
        if k == "data-value":
            tag[k] = expanded_string
        else:
            tag[k] = v
    print("test")
    html = soup.prettify("utf-8")
    with open("resources/output.html", "wb") as file:
        file.write(html)
def diff_pos(html, field):
    with open(html) as tmp:
        soup = BeautifulSoup(tmp, "html.parser")
    tag = soup.find(field)
    ptag = tag.find_parent()
    while ptag.name != "line":
        ptag = ptag.find_parent()
    attributes = tag.attrs
    expanded_string = ptag.text.strip()
    tag.string =expanded_string
    for k, v in attributes.items():
        if k == "data-value":
            tag[k] = expanded_string
        else:
            tag[k] = v
    print("test")
    html = soup.prettify("utf-8")
    with open("resources/output.html", "wb") as file:
        file.write(html)


if __name__ == '__main__':
    html = "resources/diff_pos.html"
    field = "invoice_number"
    # field = "invoice_number"
    # runner = NoiseAdd(inpath, outpath, field)
    # runner.add_noise()

