from typing import Union
import pandas as pd
from .config import BASE_URL
from .glob import make_request, metadata, get_content
from .author import Author
from .source import Source


class Corpus:
    '''
    Class corresponding to a particular corpus.
    '''

    def __init__(
            self, 
            lang     : Union[str,None]  = None,
            base_url : str              = BASE_URL, 
            metadata : Union[dict,None] = None 
        ):
        '''
        Store corpus metadata (if initialized by Poetree instance) or get them 
        from API (if initialized directly). Create empty dict self.content_
        that will hold lists of Author and Source instances.
        
        Arguments:
            lang     (str|None)  : ISO code of the corpus, required if initialized directly 
            base_url (str)       : API base URL (default: set in config.py)
            metadata (dict|None) : Corpus metadata passed when initialized by Poetree instance
        
        Raises:
            ValueError : If neither [metadata] nor [lang] is passed
        
        Returns:
            None       
        '''
        self.base_url = base_url
        self.content_ = dict()
        if metadata is not None:
            self.metadata_ = metadata
        elif lang is not None:
            self._get_corpus_metadata(lang)
        else:
            raise ValueError (
                'Argument [lang] is required when initializing ' +
                f'{__class__.__name__} instance directly'
            )
        for k, v in self.metadata_.items(): setattr(self, k, v)


    def _get_corpus_metadata(self, lang:str):
        '''
        Get metadata on corpus and store them in self.metadata_
        
        Arguments:
            lang (str) : Language of the corpus (ISO code)
        
        Returns:
            None      
        '''
        self.metadata_ = make_request(self.base_url, 'corpus', corpus=lang)
        self.metadata_['corpus'] = lang


    def get_authors(self, **kwargs) -> list:
        '''
        Get metadata of all available authors. Create a new Author instance for
        each author, store it in a list and return it.
        
        Arguments:
            None
        
        Keyword arguments:
            country     (str) : Limit to authors from certain countries. Either a single 
                                value (country="pt") or stringified list (country="pt,br")
            born_after  (int) : Limit to authors born no sooner than a given year
            born_before (int) : Limit to authors born no later than a given year
            died_after  (int) : Limit to authors that died no sooner than a given year
            died_before (int) : Limit to authors that died no later than a given year
        
        Returns:
            (list) : List holding instances of Author     
        '''
        if 'country' in kwargs and not isinstance(kwargs['country'], list):
            kwargs['country'] = ','.join(kwargs['country'])
        self.content_['authors'] = get_content(
            self.base_url, 'authors', Author, corpus=self.metadata_['corpus'], **kwargs
        )
        return self.content_['authors']
    

    def get_sources(self, **kwargs) -> list:
        '''
        Get metadata of all available sources. Create a new Source instance 
        for each source, store it in a list and return it.
        
        Arguments:
            None
        
        Keyword arguments:
            id_author        (int) : Limit to sources by author with this id(DB)
            wiki             (str) : Limit to sources by author with this wiki id
            viaf             (str) : Limit to sources by author with this viaf id
            published_after  (int) : Limit to sources published no sooner than a given year
            published_before (int) : Limit to sources published no later than a given year
        
        Returns:
            (list) : List holding instances of Source      
        '''
        self.content_['sources'] = get_content(
            self.base_url, 'sources', Source, corpus=self.metadata_['corpus'], **kwargs
        )
        return self.content_['sources']


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
            target  (str)      : Metadata of what to return; default: 'self'
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