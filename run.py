#! /usr/bin/python

import json
from collections import Counter

from flask import Flask, request, jsonify, make_response, render_template

from pandas import Series, to_datetime

from whoosh import index
import whoosh
from whoosh import qparser

from TIMEindex import StanfordTokenizer, StanfordAnalyzer

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def data():
    ix = whoosh.index.open_dir('../TIMEindex/', indexname='TIME')

    with ix.searcher() as searcher:

        def search(query):
            query = qparser.QueryParser("body", ix.schema).parse(query)
            return searcher.search(query, groupedby="year")

        def to_series(query):
            results = search(query)
            try:
                labels, counts = zip(*Counter(result['year'] for result in results).items())
            except ValueError:
                return Series()
            return Series(counts, map(to_datetime, labels))
        
        series = to_series(request.form['q'].strip())
        return json.dumps([{'_id': i, 'date': x.strftime('%d-%b-%Y'), 'y': y} for i, (x, y) in enumerate(sorted(series.iteritems()))])

@app.route('/')
def index():
    return render_template('index.html', title="TIME series")


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000, use_reloader=True, threaded=True)


