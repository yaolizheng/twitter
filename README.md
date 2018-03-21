# Basic twitter server

## Getting Started

### Prerequisites

You will need a Debian 8 box, memcached server and Cassandra server to run the server.

### Installing
- copy source code to /usr/local/lib/python2.7/dist-packages/twitter/
- run deployment script
```
cd /usr/local/lib/python2.7/dist-packages/twitter/tools && ./deployment.sh
```
- install config file and change parameters
```
cp config /etc
```
- install bin file and service file
```
cp twitter /usr/sbin/
cp twitter.service /lib/systemd/system/
systemctl daemon-reload
systemctl enable twitter
service twitter restart
```

## Modules

### Server modules

**http_server.py**: main module for web application
**db/model.py**: cassandra database module
**twitter.py**: core service module
**handlers/base.py**: base handler module
**handler/feed.py**: handler module for getting feeds
**handler/follow.py**: handler module for following and unfollowing
**handler/status.py**: handler module for health check
**handler/tweet.py**: handler module for posting tweet
**handler/user.py**: handler module for adding user

### Test modules

**client_test.py**: base module for testing
**functional_test.py**: module for functional test
**scale_test.py**: module for scale test


## API design

URL                     method      data              parameter         description                             retrun value
/follow/follower_id     POST        followee_id                         Follower_id follows followee_id         
/follow/follower_id     GET                                             Get followee for follower_id            list of followees
/follow/follower_id     delete      followee_id                         Follower_id unfollows followee_id
/tweet/user_id          POST        tweet                               Post tweet for user_id                  tweet id
/tweet/user_id          GET                                             Get user_id's tweets                    list of tweets
/tweet/user_id          DELETE      tweet_id                            Delete tweet_id
/feed/user_id           GET                                             Get feed for user_id                    list of tweets       
/user                   POST        name                                Create user                             user_id
/user                   GET                           user_id           Get user_id                             user name
/user                   DELETE      user_id                             Delete user_id


## Database schema

```
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
```
