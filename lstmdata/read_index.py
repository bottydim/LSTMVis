from whoosh.fields import Schema, NUMERIC, TEXT
from whoosh.highlight import HtmlFormatter
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

__author__ = 'Hendrik Strobelt'

schema = Schema(index=NUMERIC(stored=True), content=TEXT(stored=True))


def query_index(_query, no_results=20, htmlFormat=False, directory =''):
    results = []
    ix = open_dir(directory)

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse('"|| '+_query+'"')
        # query = QueryParser("content", ix.schema).parse(_query)
        print query
        results = searcher.search(query, limit=no_results)
        print results
        if htmlFormat:
            results.formatter = HtmlFormatter()
            return map(lambda y: {'index': y['index'], 'text': y.highlights('content')}
                       , sorted(results, key=lambda k: k['index']))
        else:
            return map(lambda y: {'index': y['index'], 'text': y['content']}
                       , sorted(results, key=lambda k: k['index']))
