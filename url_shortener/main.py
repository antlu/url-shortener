import hashlib
from http import HTTPStatus
import os

from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import validators


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
db = SQLAlchemy(app)

def hash_string(string, length=6):
    bytestring = string.encode()
    return hashlib.sha1(bytestring).hexdigest()[:length]

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'original_url': self.url,
            'short_url': url_for('link', id=self.id, _external=True),
            'api_url': url_for('api_link', id=self.id, _external=True),
        }

def error_response(message, code=HTTPStatus.BAD_REQUEST):
    return ({'error': message}, code)

@app.route('/api/', methods=['GET', 'POST'])
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

@app.route('/api/<id>', methods=['GET'])
def api_link(id):
    link = Link.query.get(id)
    if link is None:
        return error_response('Not found', HTTPStatus.NOT_FOUND)
    return link.to_json()

@app.route('/<id>', methods=['GET'])
def link(id):
    link = Link.query.get_or_404(id)
    return redirect(link.url)
