# -*- coding: utf-8 -*-
import re
import numpy as np
from collections import Counter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import itertools
from igraph import *

min_freq = 4

filename = './sample.txt'
data = [l.replace('。', '。\n') for l in open(filename, 'r', encoding='utf-8')]
sentenses = [re.sub(' ', '', u) for u in data if len(u) != 0]
print(len(sentenses))

tokenizer = Tokenizer()
char_filters = [UnicodeNormalizeCharFilter()]
token_filters = [CompoundNounFilter()]#, POSStopFilter(['記号']), LowerCaseFilter()]
analyzer = Analyzer(char_filters, tokenizer, token_filters)
dt = [analyzer.analyze(s) for s in sentenses]
print(len(dt))
noums = [[item.surface for item in t if '名詞' in item.part_of_speech] for t in dt]
pairlist = [list(itertools.combinations(ns, 2)) for ns in noums if len(ns)>=2]

all_pairs = []
for u in pairlist:
    all_pairs.extend(u)

pcount = Counter(all_pairs)
print('pair frequency', sorted(pcount.items(), key=lambda x: x[1], reverse=True)[:30])

restrict_pcount = {k: pcount[k] for k in pcount.keys() if pcount[k]>=min_freq}
str_edge = restrict_pcount.keys()

vertices = list(set([v[0] for v in str_edge] + [v[1] for v in str_edge]))
print(vertices)
edges = [(vertices.index(u[0]), vertices.index(u[1])) for u in str_edge]

g = Graph(vertex_attrs={'label': vertices, 'name': vertices}, edges=edges, directed=False)
plot(g, vertex_size=30, bbox=(800, 800), vertiex_color='white')
