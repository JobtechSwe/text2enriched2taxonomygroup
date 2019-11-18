from e2tg import app, main
from flask import render_template, request


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/groups', methods=['POST'])
def show_groups():
    enrichments = main.get_occupations_from_text(request.form['doc_headline'],
                                                 request.form['doc_text'])
    occupations = [o['term']
                   for o in enrichments.get('enriched_candidates', {}).get('occupations', [])]
    groups = main.load_groups_for_occupations(occupations, 5)
    print(groups)
    return render_template('groups.html',
                           occupations=occupations,
                           groups=groups)

