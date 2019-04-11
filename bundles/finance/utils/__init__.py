from .soup import get_soup, table_to_df, find_after
from .wiki import get_wiki_table_df, wiki_components_list_to_df


class Abstractable(type):
    def __new__(mcs, name, bases, clsdict):
        if '__abstract__' not in clsdict:
            clsdict['__abstract__'] = False
        return super().__new__(mcs, name, bases, clsdict)


def clean_df(df):
    df.volume = df.volume.fillna(0).astype('int64')
    return df.fillna(method='ffill')
