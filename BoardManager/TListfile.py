class TList(list):  # https://stackoverflow.com/a/30341258
    """
    List allowing list-like objects (such as tuples) as indexes.
    """
    def __getitem__(self, index):
        if hasattr(index, "__iter__"):
            # index is list-like, traverse downwards
            item = self
            for i in index:
                item = item[i]
            return item
        # index is not list-like, let list.__getitem__ handle it
        return super().__getitem__(index)
