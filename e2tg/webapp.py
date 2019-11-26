from e2tg import app, main
from flask import render_template, request, jsonify


@app.route('/', methods=['GET', 'POST'])
def application():
    headline = request.values.get('headline', '')
    text = request.values.get('text', '')
    groups = _find_groups(headline, text)
    return render_template('index.html', headline=headline, text=text, groups=groups)


@app.route('/suggest', methods=['GET', 'POST'])
def find_groups():
    headline = request.values.get('headline', '')
    text = request.values.get('text', '')
    num = request.values.get('num', 5)
    return jsonify(_find_groups(headline, text, num))


@app.route('/siblings/<group_id>', methods=['GET'])
def get_parent_groups(group_id):
    sibling_groups = main.load_sibling_groups(group_id)
    return jsonify(sibling_groups)


@app.route('/show-siblings/<group_id>', methods=['GET'])
def show_siblings(group_id):
    sibling_groups = main.load_sibling_groups(group_id)
    return render_template('siblings.html', siblings=sibling_groups)


def _find_groups(headline, text, num=5):
    groups = {}
    if text:
        enrichments = main.get_occupations_from_text(headline, text)
        occupations = [o['concept_label']
                       for o in enrichments.get('enriched_candidates', {}).get('occupations', [])]
        groups = main.load_groups_for_occupations(occupations, num)
    return groups
