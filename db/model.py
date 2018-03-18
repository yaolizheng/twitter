from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
import uuid


def init_database(cluster, keyspace, db_user, db_pass):
    try:
        auth_provider = PlainTextAuthProvider(
            username=db_user, password=db_pass)
        connection.setup(cluster, keyspace, auth_provider=auth_provider)
        sync_table(User)
        sync_table(Tweet)
        sync_table(Relation)
    except Exception:
        raise


class User(Model):

    __table_name__ = 'user'

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()


class Tweet(Model):

    __table_name__ = 'tweet'

    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    user_id = columns.UUID(index=True)
    time_stamp = columns.Text()
    content = columns.Text()


class Relation(Model):

    __table_name__ = 'relation'

    follower = columns.UUID(primary_key=True)
    followee = columns.UUID(primary_key=True)
