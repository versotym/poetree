from typing import Union
import pandas as pd
from tabulate import tabulate
from .config import BASE_URL
from .glob import make_request, metadata, get_content
from .poem import Poem


class Source:
    '''
    Class corresponding to a particular source.
    '''

    def __init__(
            self, 
            lang     : Union[None,str] = None, 
            base_url : str             = BASE_URL, 
            id_      : Union[None,int] = None,
            id_poem  : Union[None,int] = None, 
            metadata : dict            = None, 
        ):
        '''
        Store source metadata (if initialized by Poetree instance) or get them 
        from API (if initialized directly). Create empty dict self.content_ 
        that will hold lists of Authors and Poem instances respectively.

        Arguments:
            lang     (str|None)  : ISO code of the corpus, required if initialized directly 
            base_url (str)       : API base URL (default: set in config.py)
            id_      (int|None)  : Id(DB) of the source
            id_poem  (int|None)  : Id(DB) of the poem its source is to be found
            metadata (dict|None) : Author metadata passed when initialized by Poetree instance
        
        Raises:
            ValueError : If neither [metadata] nor [lang] is passed
                       : If neither [metadata] nor one of [id_, id_poem] is passed

        Returns:
            None    
        '''
        self.base_url = base_url
        self.content_ = dict()

        if metadata is not None:
            self.metadata_ = metadata
        elif lang is None:
            raise ValueError (
                f'Argument [lang] is required when initializing {__class__.__name__} instance directly'
            )
        elif id_ is not None:
            self._get_source_metadata(lang, 'id_source', id_)
        elif id_poem is not None:
            self._get_source_metadata(lang, 'id_poem', id_poem)
        else:
            raise ValueError (
                f'One of the arguments [id_,id_poem] is required when initializing {__class__.__name__} instance directly'
            )
        for k, v in self.metadata_.items(): setattr(self, k, v)
                

    def _get_source_metadata(
            self, 
            lang    : str, 
            id_type : str, 
            id_val  : Union[int,str]
        ):
        '''
        Get metadata on author and store them in self.metadata_
        
        Arguments:
            lang    (str)     : ISO code of the corpus
            id_type (str)     : Which identifier to use for retrueving author 
            id_val  (int|str) : Identifier value
        
        Returns:
            None      
        '''
        self.metadata_ = make_request(
            self.base_url, 
            'source', 
            **{'corpus': lang, id_type: id_val}
        )
        self.metadata_['corpus'] = lang


    def get_poems(self, **kwargs) -> list:
        '''
        Get metadata of poems in the source. Create a new Poem instance 
        for each poem, store it in a list and return it.
        
        Arguments:
            None
        
        Returns:
            (list) : List holding instances of Poem      
        '''
        self.content_['poems'] = get_content(
            self.base_url, 'poems', Poem, 
            corpus = self.metadata_['corpus'], 
            id_source = self.metadata_['id_'],
            **kwargs
        )
        return self.content_['poems']     
    

    def metadata(
            self, 
            target  : str             = 'self',
            output  : str             = 'list', 
            sortby  : Union[str,list] = None, 
            reverse : bool            = False
        ) -> Union[list, pd.DataFrame, None]:
        '''
        Returns targt metadata either as a formatted table (tabular=True)
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
        if target == 'self':
            return metadata([self], output, sortby, reverse)    
        else:
            return metadata(self.content_[target], output, sortby, reverse)  