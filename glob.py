import requests
import json
from typing import Union, Any
from tabulate import tabulate
import pandas as pd

def make_request(
        base_url : str, 
        endpoint : str, 
        **kwargs
    ) -> Union[dict,list]:
    '''
    Send request to PoeTree API. Returns the decoded JSON response.
    We catch two types of errors: (1) Server response with a status
    code other than 200, (2) invalid JSON response.
    
    Arguments:
        url      (string) : API method name
        **kwargs (dict)   : URL parameters

    Returns:
        response (dict|list) : response JSON decoded
    '''
    if not base_url.endswith('/'):
        base_url += '/'
    url = requests.compat.urljoin(base_url, endpoint)
    response = requests.get(url, kwargs)
    if response.status_code == 200:
        try:
            return json.loads(response.text)
        except:
            raise Exception(f'Invalid JSON response')
    else:
        raise Exception(f'Server responded with status code {response.status_code}: {response.reason}')


def get_content(
        base_url : str,
        endpoint : str,
        class_   : Any,
        **kwargs
    ) -> list:
    '''
    Get metadata on subordinate elements (Poetree->Corpus->Author/Source->Poem).
    
    Params:
        None
    
    Returns:
        (list) : List holding instances of subordinate class       
    '''
    response = make_request(base_url, endpoint, **kwargs)
    content = list()
    for r in response:
        if endpoint != 'corpora':
            r['corpus'] = kwargs['corpus']
        content.append(
            class_(base_url=base_url, metadata=r)
        )
    return content 
    

def metadata(
        instances : list, 
        output    : str             = 'list', 
        sortby    : Union[str,None] = None,
        reverse   : bool            = False,
    ) -> Union[list, pd.DataFrame, None]:
    '''
    Takes a list of instances (corpora, authors, sources...) and returns
    their metadata (values stored in self.data_). Metadata are returned either
    as a formatted table (tabular=True) or as a list as received from 
    API (tabular=False).
    
    Arguments:
        instances (list)     : Instances their metadata to be returned
        output    (str)      : Output format: 'list': list as retrieved from API,
                               'pandas': pd.DataFrame, 'print': stringified table
                               printed directly; default: 'list'
        sortby    (str|None) : Subdict key according to which sort the list;
                                default: None
        reverse   (bool)     : Sort in reversed (descending) order; default False

    Returns:
        (list|pd.DataFrame|None) : metadata
    '''
    if sortby is not None:
        instances = sorted(
            instances, key=lambda d: (
                d.metadata_[sortby] is not None, d.metadata_[sortby]
            ), reverse=reverse
        )
    if output == 'list':
        return [x.metadata_ for x in instances]
    if output == 'pandas':
        return pd.DataFrame([x.metadata_ for x in instances])
    if output == 'print':
        header = instances[0].metadata_.keys()
        body = [list([val if val else '' for val in x.metadata_.values()]) for x in instances]
        print(tabulate(body, header, maxcolwidths=[50]*len(header)))
         