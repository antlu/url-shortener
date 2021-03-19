from http import HTTPStatus

from flask import Blueprint, jsonify, redirect, render_template, request
import validators

from url_shortener import db
from url_shortener.models import Link
from url_shortener.utilities import error_response, hash_string


bp = Blueprint('shortener', __name__)

@bp.route('/api/', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        links = Link.query.all()
        return jsonify([link.to_json() for link in links])

    request_data = request.json or request.form
    url = request_data.get('url')
    if url is None or not validators.url(url):
        return error_response('Invalid URL')
    id_ = request_data.get('id') or hash_string(url)
    link_by_id = Link.query.get(id_)
    link_by_url = Link.query.filter_by(url=url).one_or_none()

    if link_by_id is not None:
        if (link_by_url is not None and link_by_id is not link_by_url
            or link_by_url is None):
            return error_response('Alias already exists', HTTPStatus.CONFLICT)

    if link_by_url is not None:
        if link_by_id is None:
            return error_response(
                'URL exists with ID {0}'.format(link_by_url.id),
                HTTPStatus.CONFLICT
            )
        return link_by_id.to_json()

    new_link = Link(id=id_, url=url)
    db.session.add(new_link)
    db.session.commit()
    return (new_link.to_json(), HTTPStatus.CREATED)

@bp.route('/api/<id>', methods=['GET'])
def api_link(id):
    link = Link.query.get(id)
    if link is None:
        return error_response('Not found', HTTPStatus.NOT_FOUND)
    return link.to_json()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/<id>', methods=['GET'])
def link(id):
    link = Link.query.get_or_404(id)
    return redirect(link.url)
