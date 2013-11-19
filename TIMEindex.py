import codecs
import os
import re

from whoosh import index
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME
from whoosh.analysis import StemmingAnalyzer, SimpleAnalyzer
from whoosh.analysis.filters import LowercaseFilter
from whoosh.analysis.tokenizers import Tokenizer, RegexTokenizer
from whoosh.analysis.acore import Token
from whoosh.compat import u, text_type


class StanfordTokenizer(Tokenizer):

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return True
        return False

    def __call__(self, value, positions=False, chars=False, keeporiginal=False,
                 removestops=True, start_pos=0, start_char=0, tokenize=True,
                 mode='', **kwargs):

        assert isinstance(value, text_type), "%s is not unicode" % repr(value)

        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        # The default: expression matches are used as tokens
        for i, match in enumerate(value.split('\n')):
            fields = match.strip().split('\t')
            word, lemma, pos, ne = fields if len(fields) is 4 else ["", "", "", ""]
            t.text = match.strip().split('\t')[0]
            t.lemma = lemma
            t.part_of_speech = pos
            t.named_entity = ne
            t.boost = 1.0
            if keeporiginal:
                t.original = t.text
            t.stopped = False
            if positions:
                t.pos = start_pos + i
            if chars:
                t.startchar = start_char + match.start()
                t.endchar = start_char + match.end()
            yield t

def StanfordAnalyzer(lowercase=False):
    tokenizer = StanfordTokenizer()
    if lowercase:
        tokenizer = tokenizer | LowercaseFilter()
    return tokenizer

schema = Schema(id=ID(stored=True),
                path=ID(stored=True),
                body=TEXT(analyzer=StanfordAnalyzer()),
                year=DATETIME(stored=True),
                tags=KEYWORD(stored=True),
                names=KEYWORD(stored=True))

if __name__ == '__main__':

    if not os.path.exists('../TIMEindex'):
        os.mkdir('../TIMEindex')

    ix = index.create_in('../TIMEindex', schema=schema, indexname="TIME")
    ix = index.open_dir('../TIMEindex', indexname="TIME")
    writer = ix.writer()

    for decade in os.listdir('../rich_texts_txt'):
        if decade.startswith('.'): continue
        path = os.path.join('../rich_texts_txt', decade)
        datetime = '1-1-%s' % int(decade[:-1])
        print datetime
        for filename in os.listdir(path):
            print filename
            with codecs.open(os.path.join(path, filename), encoding='utf-8') as infile:
                infile = infile.read()
            writer.add_document(id=unicode(filename), path = u(os.path.join(path, filename)), body=unicode(infile), year=datetime)

    # store the documents in the index
    writer.commit()