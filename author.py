from typing import Union
import pandas as pd
from .config import BASE_URL
from .glob import make_request, metadata, get_content
from .source import Source
from .poem import Poem


class Author:
    '''
    Class corresponding to a particular author.
    '''

    def __init__(
            self, 
            lang     : Union[None,str] = None, 
            base_url : str             = BASE_URL, 
            id_      : Union[None,int] = None,
            wiki     : Union[None,str] = None, 
            viaf     : Union[None,str] = None,
            metadata : dict            = None 
        ):
        '''
        Store author metadata (if initialized by Poetree instance) or get them 
        from API (if initialized directly). Create empty dict self.content_ 
        that will hold lists of Source and Poem instances.

        Arguments:
            lang     (str|None)  : ISO code of the corpus, required if initialized directly 
            base_url (str)       : API base URL (default: set in config.py)
            id_      (int|None)  : Id(DB) of the author
            wiki     (str|None)  : Wiki id of the author
            viaf     (str|None)  : Viaf id of the author
            metadata (dict|None) : Author metadata passed when initialized by Poetree instance
        
        Raises:
            ValueError : If neither [metadata] nor [lang] is passed
                       : If neither [metadata] nor one of [id_, wiki, viaf] is passed

        Returns:
            None    
        '''
        self.base_url = base_url
        self.content_ = dict()

        if metadata is not None:
            self.metadata_ = metadata
        elif lang is None:
            raise ValueError (
                'Argument [lang] is required when initializing ' +
                f'{__class__.__name__} instance directly'
            )
        elif id_ is not None:
            self._get_author_metadata(lang, 'id_author', id_)
        elif wiki is not None:
            self._get_author_metadata(lang, 'wiki', wiki)
        elif viaf is not None:
            self._get_author_metadata(lang, 'viaf', viaf)
        else:
            raise ValueError (
                'One of the arguments [id_,wiki,viaf] is required when initializing ' +
                f'{__class__.__name__} instance directly'
            )
        for k, v in self.metadata_.items(): setattr(self, k, v)


    def _get_author_metadata(
            self, 
            lang    : str, 
            id_type : str, 
            id_val  : Union[int,str],
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
            'author',
            **{'corpus': lang, id_type: id_val}
        )
        self.metadata_['corpus'] = lang
        

    def get_sources(self, **kwargs) -> list:
        '''
        Get metadata of sources by the author. Create a new Source instance 
        for each source, store it in a list and return it.
        
        Arguments:
            None
        
        Keyword arguments:
            published_after  (int) : Limit to sources published no sooner than a given year
            published_before (int) : Limit to sources published no later than a given year
        
        Returns:
            (list) : List holding instances of Source      
        '''
        self.content_['sources'] = get_content(
            self.base_url, 'sources', Source, 
            corpus = self.metadata_['corpus'], 
            id_author = self.metadata_['id_'],
            **kwargs
        )
        return self.content_['sources']         
    

    def get_poems(self, **kwargs) -> list:
        '''
        Get metadata of poems by the author. Create a new Poem instance 
        for each poem, store it in a list and return it.
        
        Arguments:
            None
        
        Keyword arguments:
            id_source  (int) : Limit to poems from certain source
        
        Returns:
            (list) : List holding instances of Poem      
        '''
        self.content_['poems'] = get_content(
            self.base_url, 'poems', Poem, 
            corpus = self.metadata_['corpus'], 
            id_author = self.metadata_['id_'],
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