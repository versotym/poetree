from typing import Union
import pandas as pd
from tabulate import tabulate
from .config import BASE_URL
from .glob import make_request, metadata, get_content
from .corpus import Corpus


class Poetree:
    '''
    Class corresponding to entire PoeTree collection
    '''

    def __init__(self, base_url:str=BASE_URL):
        '''
        Set API base URL. Create empty dict self.content_ that will 
        hold a list of Corpus instances.
        
        Params:
            base_url (str) : API base URL (default: set in config.py)
        
        Returns:
            None
        '''
        self.base_url = base_url
        self.content_  = dict()


    def get_corpora(self) -> list:
        '''
        Get metadata of all available corpora. Create a new Corpus instance 
        for each corpus, store it in a list and return it.
        
        Params:
            None
        
        Returns:
            (list) : List holding instances of Author       
        '''

        self.content_['corpora'] = get_content(self.base_url, 'corpora', Corpus)
        return self.content_['corpora']
    

    def metadata(
            self, 
            target  : str             = 'corpora',
            output  : str             = 'list', 
            sortby  : Union[str,list] = None, 
            reverse : bool            = False
        ) -> Union[list, pd.DataFrame, None]:
        '''
        Returns metadata of selected target either as a formatted table (tabular=True)
        or as a list as received from API (tabular=False). The list may be
        sorted according to any subdict key.
        
        Params:
            target  (str)      : Metadata of what to return; default: 'corpora'
            output  (str)      : Output format: 'list': list as retrieved from API,
                                 'pandas': pd.DataFrame, 'print': stringified table
                                 printed directly; default: 'list'
            sortby  (str|None) : Subdict key according to which sort the list;
                                 default: None
            reverse (bool)     : Sort in reversed (descending) order; default False  
            
        Returns:
            (list|pd.DataFrame|None) : metadata
        '''
        return metadata(self.content_[target], output, sortby, reverse)
