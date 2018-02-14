#!/usr/bin/env python3
"""
Generates EGS legacy JSON files from Redis datastore.
Used as a stopgap to allow this old code to rely on JSON that isn't being
made by the backend anymore. This will eventually go away, and for now can
just be run on a cron job.

To use:

./make_json.py /path/to/json/file/location

Update REDIS_INFO and REDIS_JSON_DATA_FILES with the keys/data to extract
from Redis.
"""

import os
import sys
import hashlib
import json
import time

from redis import StrictRedis
import redis.exceptions


"""
    WARNING!

    Move this file outside of this folder before adding credentials. If you have
    poor access rules set, this file may leak these credentials.
"""
REDIS_INFO = {
    'host': 'localhost',
    'port': 6379,
    'auth': None
}

REDIS_JSON_DATA_FILES = [
    '_ethgasAPI',
    '_validated',
    '_txDataLast10k',
    '_gasguzz',
    '_predictTable',
    '_priceWait',
    '_miners',
    '_topMiners'
]

def main():
    """int main()"""
    global REDIS_JSON_DATA_FILES, REDIS_INFO

    json_hashes = {}

    try:
        if REDIS_INFO['auth'] is None:
            redis_client = StrictRedis(
                    host=REDIS_INFO['host'],
                    port=int(REDIS_INFO['port'])
                )
        else:
            redis_client = StrictRedis(
                host=REDIS_INFO['host'],
                port=int(REDIS_INFO['port']),
                password=REDIS_INFO['auth']
            )
    except redis.exceptions.ConnectionError:
        print("Could not connect to Redis", file=sys.stderr)
        sys.exit(1)

    while True:
        try:
            if len(sys.argv) != 2:
                print("No output location specified.", file=sys.stderr)
                sys.exit(1)
            else:
                output_dir = os.path.realpath(sys.argv[1])
                if not os.path.isdir(output_dir):
                    print("Output directory invalid.", file=sys.stderr)
                    sys.exit(1)

                for redis_key in REDIS_JSON_DATA_FILES:
                    filename = redis_key[1:] + '.json'
                    output_filepath = os.path.join(output_dir, filename)
                    json_result = redis_client.get(redis_key)
                    if json_result is None:
                        print("Could not get Redis data for key %s", file=sys.stderr)
                    else:
                        try:
                            json_hash = hashlib.sha1(json_result).hexdigest()
                            if filename in json_hashes:
                                # check to see if this has even changed
                                # if not, skip the disk hit/stat change
                                if json_hash == json_hashes[filename]:
                                    print("[%s] %s hasn't changed, skipping" % (int(time.time()), filename))
                                    continue

                            jsondata = json.loads(json_result)
                            with open(output_filepath, 'w') as f:
                                print("[%s] Writing %s" % (int(time.time()), filename))
                                f.write(json.dumps(jsondata, ensure_ascii=True, allow_nan=False))
                                json_hashes[filename] = json_hash

                        except (json.JSONDecodeError, ValueError) as e:
                            print("Redis data retrieved for %s is invalid JSON, skipping write." % redis_key, file=sys.stderr)
            time.sleep(15)
        except KeyboardInterrupt:
            print("Keyboard interrupt caught, clean exit.")
            sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()