from e2tg import app, main
from flask import render_template, request


@app.route('/', methods=['GET', 'POST'])
def app():
    headline = request.form.get('doc_headline', '')
    text = request.form.get('doc_text', '')
    groups = {}
    if text:
        enrichments = main.get_occupations_from_text(headline, text)
        occupations = [o['term']
                       for o in enrichments.get('enriched_candidates', {}).get('occupations', [])]
        groups = main.load_groups_for_occupations(occupations, 5)

    print(groups)
    return render_template('index.html', headline=headline, text=text, groups=groups)
