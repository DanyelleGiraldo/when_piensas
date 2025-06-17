"""Basic connection example.
"""

import redis

r = redis.Redis(
    host='redis-15429.c16.us-east-1-3.ec2.redns.redis-cloud.com',
    port=15429,
    decode_responses=True,
    username="default",
    password="oZjz0rph5VgN21CVmAIs0AwpmteV5d9s",
)

success = r.set('foo', 'bar')
# True

result = r.get('foo')
print(result)
# >>> bar

