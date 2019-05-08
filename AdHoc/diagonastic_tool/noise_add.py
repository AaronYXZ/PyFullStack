import os
import random
import numpy as np
import pandas as pd
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import fnmatch


class NoiseAdd:

    def __init__(self, inpath, outpath, field,
                 dicts={"shrink": 0.2, "expand": 0.2, "random": 0.1, "swap": 0.05, "diff_pos": 0.05}):
        """

        :param inpath: input path for files to be modified
        :param outpath: output path for files after modification
        :param field:
        :param dicts:
        """

        self._inpath = inpath
        self._outpath = outpath
        self._field = field
        self._dicts = dicts
        self._metadata = defaultdict(set)
        self._files = self._collect_htmls(inpath, field)
        self._file_num = len(self._files)
        self._swap_map = {"invoice_number": "invoice_order_number", "vendor_name": "bill_to_name"}
        self._tokenizer = "\s+"
        # String defaultTokenizerRegexp = "(([\\s:#_;'\\ǀ\"\\|\\[\\]\\(\\)\\*•■])|(\\s,)|(\\s-)|(\\.\\s))"

    def _collect_htmls(self, path, field):
        """
        :param path: path to original data
        :param field: field we want the htmls to have
        :return: a list of html files that are guanranteed to have the field specified
        """
        files = []
        for file in fnmatch.filter(os.listdir(path), "*.html"):
            with open(os.path.join(path, file)) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            if soup.find(field) != None:
                files.append(file)
        random.shuffle(files)

        return files


    def get_metadata(self, type="csv", name="change_log", path = "."):
        """

        :param type: type  of the output file, by default is csv
        :param name: name of the output file
        :param path: path of the output file
        :return: save the change log to user specified path, by default it's a 2-column csv,
        first column being name of html, second colunn being type of changed made on that html
        """
        types = ['csv']
        meta = []
        for k, vs in self._metadata.items():
            for v in vs:
                meta.append({"type": k, "file": v})
        if type == "csv":
            pd.DataFrame(meta).to_csv(os.path.join(path, self._field + "_" + name + ".csv"), index=None)
        else:
            raise TypeError("type must be one of the followings: ".format(types))


    @property
    def dicts(self):
        return self._dicts

    @dicts.setter
    def dicts(self, dicts):
        types = {"shrink", "expand", "random", "swap", "diff_pos"}
        total = 0.0
        for k, v in dicts.items():
            if not isinstance(k, str):
                raise TypeError("key of the dictionary must be a string")
            if not isinstance(v, float):
                raise TypeError("value of the dictionary must be a float")
            if k not in types:
                raise ValueError("noise type must be in one of the {}".format(types))
            if v > 1.0 or v < 0.0:
                raise ValueError("percentage of each type must be between 0.0 and 1.0")
            total += v
            if total > 1.0:
                raise ValueError("sum of all types can't be larger than 1.0")
        self._dicts = dicts

    @property
    def swap_map(self):
        return self._swap_map

    @swap_map.setter
    def swap_map(self, dict):
        self._swap_map = dict

    def add_noise(self):
        self._swap_tag()
        self._diff_pos_tag()
        self._expand_tag()
        self._shrink_tag(1)
        self._random_tag()

    def _swap_tag(self):
        print("--------------------------------------------------------------")
        print("Working on swaping tags")

        try:
            perc = self._dicts["swap"]
        except KeyError:
            print("No percentage set for {}, skip this part".format("") )
            return
        try:
            swap_to = self._swap_map[self._field]
        except KeyError:
            print("No swap map has been defined for field {}".format(self._field))
            return

        num_of_files = max(1, int(perc * self._file_num))  # use fixed # of files


        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            swap_to_tag = soup.find(swap_to)
            if swap_to_tag == None:
                continue
            swap_to_attributes = swap_to_tag.attrs.copy()

            tag = soup.find(self._field)  ## find the tag associated with the working field, say invoice_number
            attributes = tag.attrs  ## get all attributes of the tag, such as class, data-value, style
            ptag = tag.find_parent()  ## find the parent line tag
            while ptag.name != "line":
                ptag = ptag.find_parent()

            swap_to_tag.name = self._field
            for k, v in attributes.items():
                if k == "data-value":
                    pass
                else:
                    swap_to_tag[k] = v
            tag.name = swap_to
            for k, v in swap_to_attributes.items():
                if k == "data-value":
                    pass
                else:
                    tag[k] = v
            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            # remove this file from list of to-be-modified files
            self._files.remove(file)
            # add this file to the list of modified files
            self._metadata['swap'].add(file)
            num_of_files -= 1
            # if # modified files reached pre-defined limit, stop this process and proceed to next process
            if num_of_files == 0:
                break
        print("Finished swapping tags")

    def _diff_pos_tag(self):
        """

        :return: find the exact match of current filed's text, untag the current field and tag the match in place
        """
        print("--------------------------------------------------------------")
        print("Working on different position tags")

        try:
            perc = self._dicts["diff_pos"]
        except KeyError:
            print("No percentage set for diff_pos")
            return
        num_of_files = max(1, int(perc * self._file_num))
        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            tag = soup.find(self._field)  ## find the tag associated with the working field, say invoice_number
            attributes = tag.attrs  ## get all attributes of the tag, such as class, data-value, style
            ptag = tag.find_parent()  ## find the parent line tag
            while ptag.name != "line":
                ptag = ptag.find_parent()

            ori_string = tag.string
            if ori_string == None:
                ori_string = tag.find("formatting").string
            template = re.compile("\s*" + ori_string + "\s*")
            candidate_tags = soup.findAll("formatting", text=template)  # find all <formatting> tag
            if len(candidate_tags) == 0:
                continue
            random.shuffle(candidate_tags)
            candidate = None
            for c in candidate_tags:
                if len(c.findChildren()) == 0 and c.find_parent().name == "line":
                    candidate = c
                    break
            # pick a random tag to modify from all candidate tags
            if candidate == None:
                break
            # match ori string to candidate string to get begin and end index
            # candidate string is divided to 3 parts: :begin, begin:end (the ori_string to be covered), end:
            candidate_string = candidate.string
            begin = candidate_string.index(ori_string)
            end = begin + len(ori_string)
            begin_string = candidate_string[:begin]
            end_string = candidate_string[end:]
            new_tag = soup.new_tag(
                self._field)  ## create a new tag exactly the same as original field tag, use it to wrap either line texts, or a sibling
            for k, v in attributes.items():
                new_tag[k] = v
            new_tag.string = ori_string
            candidate.clear()
            candidate.append(new_tag)
            new_tag.insert_before(begin_string)
            new_tag.insert_after(end_string)
            tag.unwrap()
            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            # remove this file from list of to-be-modified files
            self._files.remove(file)
            # add this file to the list of modified files
            self._metadata['diff_pos'].add(file)
            num_of_files -= 1
            # if # modified files reached pre-defined limit, stop this process and proceed to next process
            if num_of_files == 0:
                break

        print("Finished different position tags")

    def _shrink_tag(self, n):
        """

        :param n: number of tokens to be dropped in order to shrink the field, should be an integer from 1 to len(field) -1

        :return: modify the html tags in place
        """
        print("--------------------------------------------------------------")
        print("Working on shrinking tags")

        try:
            perc = self._dicts["shrink"]
        except KeyError:
            print("No percentage is set for shrink")
            return
        num_of_files = max(1, int(perc * self._file_num))
        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            tag = soup.find(self._field)
            ptag = tag.find_parent()
            while ptag.name != "line":
                ptag = ptag.find_parent()
            # check if there's child tag <formatting></formatting>
            ftag = tag.find("formatting")
            pattern = re.compile(self._tokenizer)
            if ftag == None:
                ori_string = tag.string
            else:
                ori_string = ftag.string
            tokens = re.split(pattern, ori_string)

            ## if tokens less than 2, then not suitable for shrink, skip this file
            if len(tokens) < 2:
                continue
            other_string = tokens[-n]
            end_index = ori_string.rfind(other_string) ## reverse find to get the index of last occuracne of found token
            shrinked_string = ori_string[:end_index] ## shrinked string

            if ftag == None:
                tag.string = shrinked_string
                tag['data-value'] = shrinked_string
                ptag.append(other_string)
            else:
                ftag.string = shrinked_string
                tag['data-value'] = shrinked_string
                ptag.append(shrinked_string)

            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            self._files.remove(file)
            self._metadata['shrink'].add(file)
            num_of_files -= 1
            if num_of_files == 0:
                break
        print("Finished shrinking tags")

    ## shrink by character, n is the number of character
    def _shrink_tag_by_char(self, n):

        print("--------------------------------------------------------------")
        print("Working on shrinking tags by character")


        perc = self._dicts["shrink"]
        num_of_files = max(1, int(perc * self._file_num))
        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp)
            tag = soup.find(self._field)
            ptag = tag.find_parent()
            while ptag.name != "line":
                ptag = ptag.find_parent()
            ori_string = tag.string
            shrinked_string = ori_string[:-n]
            other_string = ori_string[-n]
            tag.string = shrinked_string
            tag['data-value'] = shrinked_string
            ptag.append(other_string)
            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            self._files.remove(file)
            self._metadata['shrink'].add(file)
            num_of_files -= 1
            if num_of_files == 0:
                break
        ## ToDo expand by token
    def _expand_tag(self):
        """

        :return: modify html inplace, expand the field tag to whole line
        """

        print("--------------------------------------------------------------")
        print("Working on expanding tags")

        perc = self._dicts["expand"]
        num_of_files = max(1, int(perc * self._file_num))
        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            tag = soup.find(self._field)  ## find the tag associated with the working field, say invoice_number
            attributes = tag.attrs  ## get all attributes of the tag, such as class, data-value, style
            ptag = tag.find_parent()  ## find the parent line tag
            while ptag.name != "line":
                ptag = ptag.find_parent()
            ori_string = tag.string
            stag = tag.find_previous_sibling()  ## find the sibiling tag

            if stag == None:  ## if sibiling tag is not found, then get all text of the line, and wrap it with field tag
                expanded_string = ptag.text.strip()
                ptag.clear()
                ptag.string = expanded_string
            else:  ## if sibling tag is found, wrap it's string with field tag (so two field tags in total, data-value is two strings combined)
                stag_string = stag.string
                expanded_string = stag_string + ori_string

            new_tag = soup.new_tag(
                self._field)  ## create a new tag exactly the same as original field tag, use it to wrap either line texts, or a sibling
            for k, v in attributes.items():
                if k == "data-value":
                    new_tag[k] = expanded_string
                else:
                    new_tag[k] = v

            if stag == None:
                ptag.string.wrap(new_tag)
            else:
                stag.wrap(new_tag)

            # write the modified html to output path
            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            # remove this file from list of to-be-modified files
            self._files.remove(file)
            # add this file to the list of modified files
            self._metadata['expand'].add(file)
            num_of_files -= 1
            # if # modified files reached pre-defined limit, stop this process and proceed to next process
            if num_of_files == 0:
                break

        print("Finished expanding tags")

    ## ToDo random pick a text and put tag around it
    def _random_tag(self):
        print("--------------------------------------------------------------")
        print("Working on randomly creating tags")

        perc = self._dicts["random"]
        num_of_files = max(1, int(perc * self._file_num))
        for file in self._files:
            full_file = os.path.join(self._inpath, file)
            with open(full_file) as tmp:
                soup = BeautifulSoup(tmp, "html.parser")
            tag = soup.find(self._field)  ## find the tag associated with the working field, say invoice_number
            attributes = tag.attrs  ## get all attributes of the tag, such as class, data-value, style
            ptag = tag.find_parent()  ## find the parent line tag
            while ptag.name != "line":
                ptag = ptag.find_parent()

            all_tags = soup.findAll("formatting")
            random.shuffle(all_tags)
            candidate = None
            for c in all_tags:
                if c.find_parent().name == "line" and len(c.findChildren()) == 0:
                    candidate = c
                    break
            if candidate == None:
                continue
            ori_string = candidate.string
            new_tag = soup.new_tag(self._field)  ## create a new tag exactly the same as original field tag, use it to wrap either line texts, or a sibling
            for k, v in attributes.items():
                if k == "data-value":
                    new_tag[k] = ori_string
                else:
                    new_tag[k] = v
            candidate.string.wrap(new_tag)

            tag.unwrap()
            html = soup.prettify("utf-8")
            outfile = os.path.join(self._outpath, file)
            with open(outfile, "wb") as tmp:
                tmp.write(html)
            # remove this file from list of to-be-modified files
            self._files.remove(file)
            # add this file to the list of modified files
            self._metadata['random'].add(file)
            num_of_files -= 1
            # if # modified files reached pre-defined limit, stop this process and proceed to next process
            if num_of_files == 0:
                break
        print("Finished randomly creating tags")


