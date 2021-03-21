import random

from locust import HttpUser, between, events, task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from url_shortener.models import Link
from url_shortener.settings import TestConfig

URLS_NUMBER = 10

engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    Link.metadata.create_all(engine)

    for n in range(URLS_NUMBER):
        link = Link(
            id='example{0}'.format(n),
            url='http://example{0}.com'.format(n),
        )
        session.add(link)
    session.commit()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    Link.metadata.drop_all(engine)
    session.close()


class User(HttpUser):
    wait_time = between(5, 15)

    @task
    def get_all_api_urls(self):
        self.client.get('/api/')

    @task(3)
    def get_api_url(self):
        self.client.get('/api/example{0}'.format(random.randrange(URLS_NUMBER)))
