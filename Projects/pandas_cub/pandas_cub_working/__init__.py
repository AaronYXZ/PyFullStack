import numpy as np

__version__ = '0.0.1'


class DataFrame:

    def __init__(self, data):
        """
        A DataFrame holds two dimensional heterogeneous data. Create it by
        passing a dictionary of NumPy arrays to the values parameter

        Parameters
        ----------
        data: dict
            A dictionary of strings mapped to NumPy arrays. The key will
            become the column name.
        """
        # check for correct input types
        self._check_input_types(data)
        ## start with one underscore indicates this is a private method

        # check for equal array lengths
        self._check_array_lengths(data)

        # convert unicode arrays to object
        self._data = self._convert_unicode_to_object(data)

        # Allow for special methods for strings
        self.str = StringMethods(self)
        self._add_docs()

    def _check_input_types(self, data): ## test_input_types
        if not isinstance(data, dict):
            raise TypeError("`data` must be a dictionary of 1-D NumPy arrays")
        for key, val in data.items():
            if not isinstance(key, str):
                raise TypeError('All column names must be a string')
            if not isinstance(val, np.ndarray):
                raise TypeError('All values must be a 1-D NumPy array')
            else:
                if val.ndim != 1:
                    raise ValueError('Each value must be a 1-D NumPy array')


    def _check_array_lengths(self, data): ## test_array_length
        for i, val in enumerate(data.values()):
            if i == 0:
                length = len(val)
            elif len(val) != length:
                raise ValueError("All arrays must be the same length")



    def _convert_unicode_to_object(self, data):
        new_data = {}
        for key, value in data.items():
            if value.dtype.kind == "U":
                new_data[key] = value.astype("object")
            else:
                new_data[key] = value
        return new_data

    def __len__(self):
        """
        Make the builtin len function work with our dataframe

        Returns
        -------
        int: the number of rows in the dataframe
        """
        return len(next(iter(self._data.values())))
        # for value in self._data.values():
        #     return len(value)

    @property
    def columns(self):
        """
        _data holds column names mapped to arrays
        take advantage of internal ordering of dictionaries to
        put columns in correct order in list. Only works in 3.6+

        Returns
        -------
        list of column names
        """
        return list(self._data)
        ## this is how python design dictionary: if you pass one to list, it will iterate all keys in this
        # dictionary (ignoring values) and return all keys as a list

    @columns.setter
    def columns(self, columns):
        """
        Must supply a list of columns as strings the same length
        as the current DataFrame

        Parameters
        ----------
        columns: list of strings

        Returns
        -------
        None
        """
        if not isinstance(columns, list):
            raise TypeError("columns must be a list")
        if len(columns) != len(self._data):
            raise ValueError("columns must be the same length as original columns")
        for col in columns:
            if not isinstance(col, str):
                raise TypeError("All column names must be strings")
        if len(columns) != set(columns):
            raise ValueError("columns has duplicates. This is not allowed")
        self._data = dict(zip(columns, self._data.values()))


    @property
    def shape(self):
        """
        Returns
        -------
        two-item tuple of number of rows and columns
        """
        return len(self), len(self._data)

    def _repr_html_(self):
        """
        Only on Jupyter Notebook!

        Used to create a string of HTML to nicely display the DataFrame
        in a Jupyter Notebook. Different string formatting is used for
        different data types.

        The structure of the HTML is as follows:
        <table>
            <thead>
                <tr>
                    <th>data</th>
                    ...
                    <th>data</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
                ...
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
            </tbody>
        </table>
        """
        pass

    @property
    def values(self):
        """
        Returns
        -------
        A single 2D NumPy array of the underlying data
        """
        return np.column_stack(list(self._data.values()))

    @property
    def dtypes(self):
        """
        Returns
        -------
        A two-column DataFrame of column names in one column and
        their data type in the other
        """
        DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}
        col_names = np.array(list(self._data.keys()))
        dtypes = [DTYPE_NAME[v.dtype.kind] for v in self._data.values()]
        dtypes = np.array(dtypes)
        new_data = {"Column Name":col_names, "Data Type":dtypes}
        return DataFrame(new_data)

    def __getitem__(self, item):
        """
        Use the brackets operator to simultaneously select rows and columns
        A single string selects one column -> df['colname']
        A list of strings selects multiple columns -> df[['colname1', 'colname2']]
        A one column DataFrame of booleans that filters rows -> df[df_bool]
        Row and column selection simultaneously -> df[rs, cs]
            where cs and rs can be integers, slices, or a list of integers
            rs can also be a one-column boolean DataFrame

        Returns
        -------
        A subset of the original DataFrame
        """
        # select a single column -> df['colname']
        if isinstance(item, str):
            return DataFrame({item: self._data[item]})

        # select multiple columns -> df[['colname1', 'colname2']]
        if isinstance(item, list):
            return DataFrame({col: self._data[col] for col in item})

        # boolean selection
        if isinstance(item, DataFrame):
            if item.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')

            bool_arr = next(iter(item._data.values()))
            if bool_arr.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')

            new_data = {}
            for col, values in self._data.items():
                new_data[col] = values[bool_arr]
            return DataFrame(new_data)

        if isinstance(item, tuple):
            return self._getitem_tuple(item)
        else:
            raise TypeError('Select with either a string, a list, or a row and column '
                            'simultaneous selection')

# ToDo
    def _getitem_tuple(self, item):
        # simultaneous selection of rows and cols -> df[rs, cs]
        if len(item) != 2:
            raise ValueError('Pass either a single string or a two-item tuple inside the '
                             'selection operator.')
        row_selection = item[0]
        col_selection = item[1]
        if isinstance(row_selection, int):
            row_selection = [row_selection]
        elif isinstance(row_selection, DataFrame):
            if row_selection.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')
            row_selection = next(iter(row_selection._data.values()))
            if row_selection.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')
        elif not isinstance(row_selection, (list, slice)):
            raise TypeError('Row selection must be either an int, slice, list, or DataFrame')

        if isinstance(col_selection, int):
            col_selection = [self.columns[col_selection]]
        elif isinstance(col_selection, str):
            col_selection = [col_selection]
        elif isinstance(col_selection, list):
            new_col_selction = []
            for col in col_selection:
                if isinstance(col, int):
                    new_col_selction.append(self.columns[col])
                else:
                    new_col_selction.append(col)
            col_selection = new_col_selction
        elif isinstance(col_selection, slice):
            start = col_selection.start
            stop = col_selection.stop
            step = col_selection.step
            if isinstance(start, str):
                start = self.columns.index(col_selection.start)
            if isinstance(stop, str):
                stop = self.columns.index(col_selection.stop) + 1

            col_selection = self.columns[start:stop:step]
        else:
            raise TypeError('Column selection must be either an int, string, list, or slice')

        new_data = {}
        for col in col_selection:
            new_data[col] = self._data[col][row_selection]
        return DataFrame(new_data)

    def _ipython_key_completions_(self):
        # allows for tab completion when doing df['c
        return self.columns

    def __setitem__(self, key, value):
        # adds a new column or a overwrites an old column
        if not isinstance(key, str):
            raise NotImplementedError("Setting column is only done with a string")
        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError("The numpy array must be 1D")
            if len(value) != len(self):
                raise ValueError("Length of setting array must match length of DataFrame")
        elif isinstance(value, DataFrame):
            if value.shape[1] != 1:
                raise ValueError("Setting DataFrame must be one column")
            if len(value) != len(self):
                raise ValueError("Setting DataFrame must be the same length")
            value = next(iter(value._data.values()))
        elif isinstance(value, (int, bool, str, float)):
            value = np.repeat(value, len(self))
        else:
            raise TypeError("Setting object must be array, DataFrame, int, float, string, boolean")

        if value.dtype.kind == 'U':
            value = value.astype("object")
        self._data[key] = value


    def head(self, n=5):
        """
        Return the first n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return self[:n, :]

    def tail(self, n=5):
        """
        Return the last n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return self[-n:, :]

    #### Aggregation Methods ####

    def min(self):
        return self._agg(np.min)

    def max(self):
        return self._agg(np.max)

    def mean(self):
        return self._agg(np.mean)

    def median(self):
        return self._agg(np.median)

    def sum(self):
        return self._agg(np.sum)

    def var(self):
        return self._agg(np.var)

    def std(self):
        return self._agg(np.std)

    def all(self):
        return self._agg(np.all)

    def any(self):
        return self._agg(np.any)

    def argmax(self):
        return self._agg(np.argmax)

    def argmin(self):
        return self._agg(np.argmin)

    def _agg(self, aggfunc):
        """
        Generic aggregation function that applies the
        aggregation to each column

        Parameters
        ----------
        aggfunc: str of the aggregation function name in NumPy

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            try:
                new_data[col] =np.array([aggfunc(value)])
            except TypeError:
                pass
        return DataFrame(new_data)

    def isna(self):
        """
        Determines whether each value in the DataFrame is missing or not

        Returns
        -------
        A DataFrame of booleans the same size as the calling DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            if value.dtype.kind == "O":
                new_data[col] = value == None
            else:
                new_data[col] = np.isnan(value)
        return DataFrame(new_data)

    def count(self):
        """
        Counts the number of non-missing values per column

        Returns
        -------
        A DataFrame
        """
        df = self.isna()
        new_data = {}
        length = len(self)
        for col, value in df._data.items():
            new_data[col] = np.array([length - value.sum()])
        return DataFrame(new_data)


    def unique(self):
        """
        Finds the unique values of each column

        Returns
        -------
        A list of one-column DataFrames
        """
        dfs = []
        for col, values in self._data.items():
            uniques = np.unique(values)
            dfs.append(DataFrame({col: uniques}))
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def nunique(self):
        """
        Find the number of unique values in each column

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for col, values in self._data.items():
            new_data[col] = np.array([len(set(values))])
        return DataFrame(new_data)

    def value_counts(self, normalize=False):
        """
        Returns the frequency of each unique value for each column

        Parameters
        ----------
        normalize: bool
            If True, returns the relative frequencies (percent)

        Returns
        -------
        A list of DataFrames or a single DataFrame if one column
        """
        dfs = []
        for col, values in self._data.items():
            keys, raw_counts = np.unique(values, return_counts=True)
            order = np.argsort(-raw_counts)
            keys = keys[order]
            raw_counts = raw_counts[order]

            if normalize:
                raw_counts = raw_counts / raw_counts.sum()
            dfs.append(DataFrame({col: keys, "count":raw_counts}))
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def rename(self, columns):
        """
        Renames columns in the DataFrame

        Parameters
        ----------
        columns: dict
            A dictionary mapping the old column name to the new column name

        Returns
        -------
        A DataFrame
        """
        if not isinstance(columns, dict):
            raise TypeError("Columns must be a dict")

        new_data = {}
        for col, value in self._data.items():
            new_col = columns.get(col, col)
            new_data[new_col] = value

        return DataFrame(new_data)



    def drop(self, columns):
        """
        Drops one or more columns from a DataFrame

        Parameters
        ----------
        columns: str or list of strings

        Returns
        -------
        A DataFrame
        """
        if isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError("columns must be either a string or a list of strings")

        new_data = {}
        for col, values in self._data.items():
            if not col in columns:
                new_data[col] = values
        return DataFrame(new_data)

    #### Non-Aggregation Methods ####

    def abs(self):
        """
        Takes the absolute value of each value in the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.abs)

    def cummin(self):
        """
        Finds cumulative minimum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.minimum.accumulate)

    def cummax(self):
        """
        Finds cumulative maximum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.maximum.accumulate)

    def cumsum(self):
        """
        Finds cumulative sum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.cumsum)

    def clip(self, lower=None, upper=None):
        """
        All values less than lower will be set to lower
        All values greater than upper will be set to upper

        Parameters
        ----------
        lower: number or None
        upper: number or None

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.clip, a_min=lower, a_max=upper)

    def round(self, n):
        """
        Rounds values to the nearest n decimals

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.round, decimals=n)

    def copy(self):
        """
        Copies the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg(np.copy)

    def _non_agg(self, funcname, **kwargs):
        """
        Generic non-aggregation function

        Parameters
        ----------
        funcname: numpy function
        kwargs: extra keyword arguments for certain functions

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            if value.dtype.kind == "O":
                new_data[col] = value.copy()
            else:
                new_data[col] = funcname(value, **kwargs)
        return DataFrame(new_data)

    def diff(self, n=1):
        """
        Take the difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_shifted = np.roll(values, n)
            values = values - values_shifted
            if n >= 0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values
        return self._non_agg(func)

    def pct_change(self, n=1):
        """
        Take the percentage difference between the current value and
        the nth value above it.

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        def func(values):
            values = values.astype('float')
            values_shifted = np.roll(values, n)
            values = (values - values_shifted) / values_shifted
            if n >= 0:
                values[:n] = np.NAN
            else:
                values[n:] = np.NAN
            return values
        return self._non_agg(func)

    #### Arithmetic and Comparison Operators ####
    """
    https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
    """

    def __add__(self, other):  ## this is called when we do "df + 5"
        return self._oper('__add__', other)

    def __radd__(self, other): ## this is called when we do "5 + df"
        return self._oper('__radd__', other)

    def __sub__(self, other):
        return self._oper('__sub__', other)

    def __rsub__(self, other):
        return self._oper('__rsub__', other)

    def __mul__(self, other):
        return self._oper('__mul__', other)

    def __rmul__(self, other):
        return self._oper('__rmul__', other)

    def __truediv__(self, other):
        return self._oper('__truediv__', other)

    def __rtruediv__(self, other):
        return self._oper('__rtruediv__', other)

    def __floordiv__(self, other):
        return self._oper('__floordiv__', other)

    def __rfloordiv__(self, other):
        return self._oper('__rfloordiv__', other)

    def __pow__(self, other):
        return self._oper('__pow__', other)

    def __rpow__(self, other):
        return self._oper('__rpow__', other)

    def __gt__(self, other):
        return self._oper('__gt__', other)

    def __lt__(self, other):
        return self._oper('__lt__', other)

    def __ge__(self, other):
        return self._oper('__ge__', other)

    def __le__(self, other):
        return self._oper('__le__', other)

    def __ne__(self, other):
        return self._oper('__ne__', other)

    def __eq__(self, other):
        return self._oper('__eq__', other)

    def _oper(self, op, other):
        """
        Generic operator function

        Parameters
        ----------
        op: str name of special method
        other: the other object being operated on

        Returns
        -------
        A DataFrame
        """
        if isinstance(other, DataFrame):
            if other.shape[1] != 1:
                raise ValueError("DataFrame must be a single column")
            else:
                other = next(iter(other._data.values()))

        new_data = {}
        for col, value in self._data.items():
            method = getattr(value, op)
            new_data[col] = method(other)
        return DataFrame(new_data)

    def sort_values(self, by, asc=True):
        """
        Sort the DataFrame by one or more values

        Parameters
        ----------
        by: str or list of column names
        asc: boolean of sorting order

        Returns
        -------
        A DataFrame
        """

        if isinstance(by, str):
            order = np.argsort(self._data[by])
        elif isinstance(by, list):
            by = [self._data[col] for col in by[::-1]]
            order = np.lexsort(by)
        else:
            raise TypeError("by must be either a string or a list")
        if not asc:
            order = order[::-1]
        return self[order.tolist(), :]

    def sample(self, n=None, frac=None, replace=False, seed=None):
        """
        Randomly samples rows the DataFrame

        Parameters
        ----------
        n: int
            number of rows to return
        frac: float
            Proportion of the data to sample
        replace: bool
            Whether or not to sample with replacement
        seed: int
            Seeds the random number generator

        Returns
        -------
        A DataFrame
        """
        if seed:
            np.random.seed(seed)
        if frac is not None:
            if frac <= 0:
                raise ValueError('`frac` must be positive')
            n = int(frac * len(self))
        if n is not None:
            if not isinstance(n, int):
                raise TypeError('`n` must be an int')
            rows = np.random.choice(np.arange(len(self)), size=n, replace=replace).tolist()
        return self[rows, :]

    def pivot_table(self, rows=None, columns=None, values=None, aggfunc=None):
        """
        Creates a pivot table from one or two 'grouping' columns.

        Parameters
        ----------
        rows: str of column name to group by
            Optional
        columns: str of column name to group by
            Optional
        values: str of column name to aggregate
            Required
        aggfunc: str of aggregation function

        Returns
        -------
        A DataFrame
        """
        if rows is None and columns is None:
            raise ValueError('`rows` or `columns` cannot both be `None`')

        if values is not None:
            val_data = self._data[values]
            if aggfunc is None:
                raise ValueError('You must provide `aggfunc` when `values` is provided.')
        else:
            if aggfunc is None:
                aggfunc = 'size'
                val_data = np.empty(len(self))
            else:
                raise ValueError('You cannot provide `aggfunc` when `values` is None')

        if rows is not None:
            row_data = self._data[rows]

        if columns is not None:
            col_data = self._data[columns]

        if rows is None:
            pivot_type = 'columns'
        elif columns is None:
            pivot_type = 'rows'
        else:
            pivot_type = 'all'

        from collections import defaultdict
        d = defaultdict(list)
        if pivot_type == 'columns':
            for group, val in zip(col_data, val_data):
                d[group].append(val)
        elif pivot_type == 'rows':
            for group, val in zip(row_data, val_data):
                d[group].append(val)
        else:
            for group1, group2, val in zip(row_data, col_data, val_data):
                d[(group1, group2)].append(val)

        agg_dict = {}
        for group, vals in d.items():
            arr = np.array(vals)
            func = getattr(np, aggfunc)
            agg_dict[group] = func(arr)

        new_data = {}
        if pivot_type == 'columns':
            for col_name in sorted(agg_dict):
                value = agg_dict[col_name]
                new_data[col_name] = np.array([value])
        elif pivot_type == 'rows':
            row_array = np.array(list(agg_dict.keys()))
            val_array = np.array(list(agg_dict.values()))

            order = np.argsort(row_array)
            new_data[rows] = row_array[order]
            new_data[aggfunc] = val_array[order]
        else:
            row_set = set()
            col_set = set()
            for group in agg_dict:
                row_set.add(group[0])
                col_set.add(group[1])
            row_list = sorted(row_set)
            col_list = sorted(col_set)
            new_data = {}
            new_data[rows] = np.array(row_list)
            for col in col_list:
                new_vals = []
                for row in row_list:
                    new_val = agg_dict.get((row, col), np.nan)
                    new_vals.append(new_val)
                new_data[col] = np.array(new_vals)
        return DataFrame(new_data)

    def _add_docs(self):
        agg_names = ['min', 'max', 'mean', 'median', 'sum', 'var',
                     'std', 'any', 'all', 'argmax', 'argmin']
        agg_doc = \
        """
        Find the {} of each column
        
        Returns
        -------
        DataFrame
        """
        for name in agg_names:
            getattr(DataFrame, name).__doc__ = agg_doc.format(name)


class StringMethods:

    def __init__(self, df):
        self._df = df

    def capitalize(self, col):
        return self._str_method(str.capitalize, col)

    def center(self, col, width, fillchar=None):
        if fillchar is None:
            fillchar = ' '
        return self._str_method(str.center, col, width, fillchar)

    def count(self, col, sub, start=None, stop=None):
        return self._str_method(str.count, col, sub, start, stop)

    def endswith(self, col, suffix, start=None, stop=None):
        return self._str_method(str.endswith, col, suffix, start, stop)

    def startswith(self, col, suffix, start=None, stop=None):
        return self._str_method(str.startswith, col, suffix, start, stop)

    def find(self, col, sub, start=None, stop=None):
        return self._str_method(str.find, col, sub, start, stop)

    def len(self, col):
        return self._str_method(str.__len__, col)

    def get(self, col, item):
        return self._str_method(str.__getitem__, col, item)

    def index(self, col, sub, start=None, stop=None):
        return self._str_method(str.index, col, sub, start, stop)

    def isalnum(self, col):
        return self._str_method(str.isalnum, col)

    def isalpha(self, col):
        return self._str_method(str.isalpha, col)

    def isdecimal(self, col):
        return self._str_method(str.isdecimal, col)

    def islower(self, col):
        return self._str_method(str.islower, col)

    def isnumeric(self, col):
        return self._str_method(str.isnumeric, col)

    def isspace(self, col):
        return self._str_method(str.isspace, col)

    def istitle(self, col):
        return self._str_method(str.istitle, col)

    def isupper(self, col):
        return self._str_method(str.isupper, col)

    def lstrip(self, col, chars):
        return self._str_method(str.lstrip, col, chars)

    def rstrip(self, col, chars):
        return self._str_method(str.rstrip, col, chars)

    def strip(self, col, chars):
        return self._str_method(str.strip, col, chars)

    def replace(self, col, old, new, count=None):
        if count is None:
            count = -1
        return self._str_method(str.replace, col, old, new, count)

    def swapcase(self, col):
        return self._str_method(str.swapcase, col)

    def title(self, col):
        return self._str_method(str.title, col)

    def lower(self, col):
        return self._str_method(str.lower, col)

    def upper(self, col):
        return self._str_method(str.upper, col)

    def zfill(self, col, width):
        return self._str_method(str.zfill, col, width)

    def encode(self, col, encoding='utf-8', errors='strict'):
        return self._str_method(str.encode, col, encoding, errors)

    def _str_method(self, method, col, *args):
        old_values = self._df._data[col]
        if old_values.dtype.kind != 'O':
            raise TypeError('The `str` accessor only works with string columns')
        new_values = []
        for val in old_values:
            if val is None:
                new_values.append(val)
            else:
                new_val = method(val, *args)
                new_values.append(new_val)
        arr = np.array(new_values)
        return DataFrame({col: arr})


def read_csv(fn):
    """
    Read in a comma-separated value file as a DataFrame

    Parameters
    ----------
    fn: string of file location

    Returns
    -------
    A DataFrame
    """
    from collections import defaultdict
    values = defaultdict(list)
    with open(fn) as f:
        header = f.readline()
        column_names = header.strip('\n').split(',')
        for line in f:
            vals = line.strip('\n').split(',')
            for val, name in zip(vals, column_names):
                values[name].append(val)
    new_data = {}
    for col, vals in values.items():
        try:
            new_data[col] = np.array(vals, dtype='int')
        except ValueError:
            try:
                new_data[col] = np.array(vals, dtype='float')
            except ValueError:
                new_data[col] = np.array(vals, dtype='O')
    return DataFrame(new_data)