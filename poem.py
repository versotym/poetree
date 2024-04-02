from typing import Union
import pandas as pd
from .config import BASE_URL
from .glob import make_request, metadata


class Poem:
    '''
    Class corresponding to a particular poem.
    '''

    def __init__(
            self, 
            lang     : Union[None,str] = None, 
            base_url : str             = BASE_URL, 
            id_      : Union[None,int] = None,
            metadata : dict            = None
        ):
        '''
        Store poem metadata (if initialized by Poetree instance) or get them 
        from API (if initialized directly). 

        Arguments:
            lang     (str|None)  : ISO code of the corpus, required if initialized directly 
            base_url (str)       : API base URL (default: set in config.py)
            id_      (int|None)  : Id(DB) of the poem
            metadata (dict|None) : Poem metadata passed when initialized by Poetree instance
        
        Raises:
            ValueError : If neither [metadata] nor [lang] is passed
                       : If neither [metadata] nor id_ is passed

        Returns:
            None    
        '''
        self.base_url = base_url
        self.content_ = list()

        if metadata is not None:
            self.metadata_ = metadata
        elif lang is None:
            raise ValueError (
                'Argument [lang] is required when initializing ' +
                f'{__class__.__name__} instance directly'
            )
        elif id_ is None:
            raise ValueError (
                'One of the arguments [id_,wiki,viaf] is required when initializing ' +
                f'{__class__.__name__} instance directly'
            )
        else:
            self._get_poem_metadata(lang, id_)
        for k, v in self.metadata_.items(): setattr(self, k, v)


    def _get_poem_metadata(self, lang: str, id_:Union[int,str]):
        '''
        Get metadata on poem and store them in self.metadata_
        
        Arguments:
            lang (str)     : ISO code of the corpus
            id_  (int|str) : Id of the poem
        
        Returns:
            None      
        '''
        self.metadata_ = make_request(
            self.base_url, 
            'poem',
            **{'corpus': lang, 'id_poem': id_, 'lines': 0}
        )
        self.metadata_['corpus'] = lang


    def get_body(self, **kwargs):
        '''
        Get body of the poem (if not fetched yet), store it in self.content_
        and return it

        Arguments:
            None
                
        Returns:
            (dict) : Object representing body of the poem      
        '''
        if len(self.content_) == 0:
            response = make_request(
                self.base_url, 
                'poem',
                **{'corpus': self.corpus, 'id_poem': self.id_, **kwargs}
            )
            self.content_ = response['body']
        return self.content_


    def get_all(self):
        '''
        Get body of the poem (if not fetched yet), store it in self.content_
        and return it together with metadata

        Arguments:
            None
                
        Returns:
            (dict) : Object representing body and metadata of the poem      
        '''
        if len(self.content_) == 0:
            self.get_body()
            
        return {**self.metadata_, **{'body': self.content_}}


    def metadata(
            self, 
            target  : str             = 'self',
            output  : str             = 'list', 
            sortby  : Union[str,list] = None, 
            reverse : bool            = False
        ) -> Union[list, pd.DataFrame, None]:
        '''
        Returns target metadata either as a formatted table (tabular=True)
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