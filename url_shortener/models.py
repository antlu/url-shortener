from flask import url_for

from url_shortener import db


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, unique=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'original_url': self.url,
            'short_url': url_for('shortener.link', id=self.id, _external=True),
            'api_url': url_for('shortener.api_link', id=self.id, _external=True),
        }
