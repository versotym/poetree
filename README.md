[![PyPI version](https://badge.fury.io/py/poetree.svg)](https://badge.fury.io/py/poetree)

# poetree
Poetree library provides an easy way to get data from PoeTree API.

[PoeTree](https://versologie.cz/poetree) is a standardized collection of poetry corpora comprising over 330,000 poems in ten languages (Czech, English, French, German, Hungarian, Italian, Portuguese, Russian, Slovenian and Spanish). Each corpus has been deduplicated, enriched with Universal Dependencies, provided with additional metadata and converted into a unified JSON structure.

## Install
```console
pip install poetree
```
or
```console
pip3 install poetree
```

## Usage
```python
import poetree
```

There are five classes available:
- ```Poetree``` represents the entire PoeTree collection [\[documentation\]](https://versologie.cz/poetree/python-doc/poetree)
- ```Corpus``` represents single corpus [\[documentation\]](https://versologie.cz/poetree/python-doc/corpus)
- ```Author``` represents single author [\[documentation\]](https://versologie.cz/poetree/python-doc/author)
- ```Source``` represents single book [\[documentation\]](https://versologie.cz/poetree/python-doc/source)
- ```Poem``` represents single poem [\[documentation\]](https://versologie.cz/poetree/python-doc/poem)

Each class has properties corresponding to the keys returned by API. To get for instance the number of authors and the number of poems in PoeTree.cs:

```python
corpus = poetree.Corpus('cs')
print('number of authors:', corpus.n_authors)
print('number of poems:', corpus.n_poems)
```
```console
number of authors: 606
number of poems: 80229
```

###  get_corpora(), get_authors(), get_sources(), get_poems()
Class instance may be created directly (as in the example above) or one may use a more general class to create a number of children instances by means of ```get_[something]()``` methods. To get for instance all the authors in PoeTree.en born between 1750 and 1760:

```python
corpus = poetree.Corpus('en')
for author in corpus.get_authors(born_after=1750, born_before=1760):
    print(f'{author.name} ({author.born})')
```
```console
Barlow, Joel (1754)
Blake, William (1757)
Crabbe, George (1754)
Freneau, Philip Morin (1752)
Roberts, David (1757)
Wheatley, Phillis (1753)
```

Analogous methods in other classes are as follow:

<img src="https://versologie.cz/poetree/img/classes.png" style="width:300px;"/>

Objects created by ```get_[something]()``` are also stored in their parent object's property ```data_[something]``` for later use:

```python
corpus = poetree.Corpus('en')
corpus.get_authors(born_after=1750, born_before=1760)
print([x.name for x in corpus.content_['authors']])
```
```console
['Barlow, Joel', 'Blake, William', 'Crabbe, George', 'Freneau, Philip Morin', 'Roberts, David', 'Wheatley, Phillis']
```

To iterate over all corpora, over all authors, over all their poems:
```python
pt = poetree.Poetree()
for corpus in pt.get_corpora():
    for author in corpus.get_authors():
        for poem in author.get_poems():
            # Do stuff...
```

### metadata()
Each class provides```metadata()``` method. By default it gives access to all metadata properties of the class:

```python
corpus = poetree.Corpus('de')
metadata = corpus.metadata(output='pandas')
print(metadata)
```
```console
  corpus                                               desc  n_authors  n_poems  n_lines  n_types  n_tokens
0     de  Compiled by Klemens Bobenhausen and Benjamin H...        245    53133  1701234   678426  12482485
```

It can also be used to get metadata of all children instances it created using the ```target``` attribute:
```python
corpus = poetree.Corpus('pt')
corpus.get_authors()
df = corpus.metadata(target='authors', output='pandas') 
print(df)
```
```console
    id_                                     name                    viaf       wiki country  born  died  n_poems corpus
0    20                      Alberto de Oliveira                29092555   Q1789301      br  1857  1937        1     pt
1     6                   Antônio Gonçalves Dias                73988798    Q611997      br  1823  1864       15     pt
2     1  Augusto de Carvalho Rodrigues dos Anjos                44342515    Q769887      br  1884  1914      306     pt
3    11                          Basílio da Gama                84492428   Q1789371      pt  1740  1795        6     pt
4     4                  Cláudio Manuel da Costa                41967264   Q1789904      br  1729  1789      190     pt
5    25               Delminda Silveira de Sousa                99136109  Q10264874      br  1854  1932      548     pt
6     8          Emílio Nunes Correia de Meneses                71253555  Q10272640      br  1866  1918       90     pt
7    17               Francisco de Sá de Meneses                32338601   Q4403329      pt  1600  1664       12     pt
8    15                   Gonçalves de Magalhães                88876973   Q2532628      br  1811  1882       56     pt
9    16                 Gregório de Matos Guerra               122323020    Q983565      br  1636  1696      704     pt
10   13                Gustavo de Paula Teixeira                60882245  Q10293150      br  1881  1937      122     pt
11   23               José Pedro Xavier Pinheiro               121971768  Q15631816      br  1822  1882      100     pt
12   14          José Joaquim Correia de Almeida                50626334  Q25859802      br  1820  1905      953     pt
13    7                 José de Santa Rita Durão   730145601965601320827   Q6958165      br  1722  1784       10     pt
14    5                     João da Cruz e Sousa                 4972695   Q2609059      br  1861  1898      407     pt
15   10             Juvêncio de Araújo Figueredo  4738150325583310090002  Q10313264      br  1865  1927      438     pt
16   24            Laurindo José da Silva Rabelo    65149066775765602956   Q6501838      br  1826  1864      184     pt
17    9             Luís Nicolau Fagundes Varela                24730690   Q2088965      br  1841  1875      215     pt
18    3                       Luís Vaz de Camões                34454091       Q590      pt  1524  1580       10     pt
19    2  Manuel Maria Barbosa l'Hedois du Bocage                66536132    Q630116      pt  1765  1805      146     pt
20   18             Múcio Scevola Lopes Teixeira                11159986  Q10334840      br  1857  1926       86     pt
21   19             Nicolau Tolentino de Almeida                54191676    Q740967      pt  1740  1811      244     pt
22   21   Olavo Brás Martins dos Guimarães Bilac                73898176    Q982354      br  1865  1918       75     pt
23   22    Sebastião Cícero dos Guimarães Passos                25942646  Q10292895      br  1867  1909       75     pt
24   12                    Tomás Antônio Gonzaga                19760014   Q1334602      br  1744  1810      110     pt
```

### get_body(), get_all()

When ```Poem``` instance is created, only its metadata are fetched from API. To get the body (lines, words and their annotation) one needs to call ```get_body()``` method first.

```python
poem = poetree.Poem(id_=1, lang='cs')
body = poem.get_body()
print(body[0])
```
```console
{'id_': 1, 'id': 0, 'id_stanza': 1, 'text': 'Tvá loď jde po vysokém moři,', 'part': False, 'words': [{'id_': 1, 'id': 1, 'id_sentence': 1, 'head': 2, 'deprel': 'det', 'form': 'Tvá', 'lemma': 'tvůj', 'upos': 'DET', 'xpos': 'PSFS1-S1------1', 'feats': 'Case=Nom|Gender=Fem|Number=Sing|PronType=Dem'}, {'id_': 2, 'id': 2, 'id_sentence': 1, 'head': 3, 'deprel': 'nsubj', 'form': 'loď', 'lemma': 'loď', 'upos': 'NOUN', 'xpos': 'NNFS1-----A----', 'feats': 'Case=Nom|Gender=Fem|Number=Sing|Polarity=Pos'}, {'id_': 3, 'id': 3, 'id_sentence': 1, 'head': 0, 'deprel': 'root', 'form': 'jde', 'lemma': 'jít', 'upos': 'VERB', 'xpos': 'VB-S---3P-AA---', 'feats': 'Mood=Ind|Number=Sing|Person=3|Polarity=Pos|Tense=Pres|VerbForm=Fin|Voice=Act'}, {'id_': 4, 'id': 4, 'id_sentence': 1, 'head': 6, 'deprel': 'case', 'form': 'po', 'lemma': 'po', 'upos': 'ADP', 'xpos': 'RR--6----------', 'feats': 'AdpType=Prep|Case=Loc'}, {'id_': 5, 'id': 5, 'id_sentence': 1, 'head': 6, 'deprel': 'amod', 'form': 'vysokém', 'lemma': 'vysoký', 'upos': 'ADJ', 'xpos': 'AANS6----1A----', 'feats': 'Case=Loc|Degree=Pos|Gender=Neut|Number=Sing|Polarity=Pos'}, {'id_': 6, 'id': 6, 'id_sentence': 1, 'head': 3, 'deprel': 'obl', 'form': 'moři', 'lemma': 'moře', 'upos': 'NOUN', 'xpos': 'NNNS6-----A----', 'feats': 'Case=Loc|Gender=Neut|Number=Sing|Polarity=Pos'}, {'id_': 7, 'id': 7, 'id_sentence': 1, 'head': 9, 'deprel': 'punct', 'form': ',', 'lemma': ',', 'upos': 'PUNCT', 'xpos': 'Z:-------------', 'feats': '_'}]}
```

To retrieve both the metadata and the body of the poem at the same time, there is a method ```get_all()```

```python
poem = poetree.Poem(id_=1, lang='cs')
metadata_and_body = poem.get_all()
```
