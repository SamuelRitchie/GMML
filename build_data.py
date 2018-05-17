from collections import defaultdict
from nltk.corpus import wordnet as wn
import logging
logger = logging.getLogger(__name__)


def get_word_dependencies(word):
    logger.info("fetching word '%s' dependencies in WordNet..." % word)
    list_music = [word]
    for a in wn.synset('%s.n.01' % word).hyponyms():
        list_music.append(a.name())
        temp = a.name()
        for b in wn.synset(temp).hyponyms():
            list_music.append(b.name())
            temp2 = b.name()
            for c in wn.synset(temp2).hyponyms():
                list_music.append(c.name())
    with open('data/%s_dependencies.txt' % word, 'w') as f:
        f.write('\n'.join(list_music))


def generate_network(word, network=defaultdict(set)):
    logger.info("building network for word '%s' subtree..." % word)
    words, target = wn.words(), wn.synset('%s.n.01' % word)
    targets = set(open('data/%s_dependencies.txt' % word).read().split('\n'))
    nouns = {noun for word in words for noun in wn.synsets(word, pos='n') if noun.name() in targets}
    for noun in nouns:
        for path in noun.hypernym_paths():
            if target not in path:
                continue
            for i in range(path.index(target),len(path)-1):
                if not path[i].name() in targets:
                    continue
                network[noun.name()].add(path[i].name())
    with open('data/%s_network.tsv' % word, 'w') as out:
        for key, vals in network.items():
            for val in vals:
                out.write(key.split('.')[0]+'\t'+val.split('.')[0]+'\n')
