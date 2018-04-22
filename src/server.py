import merkle

from wsgiref.simple_server import make_server
import json
import re
import os

test_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../test_data/extract.csv")

mtree = merkle.Merkle(test_data)

def not_found(env, rs, obj):
    status = "404 Not Found"
    headers = [("Content-Type", "application/json")]
    rs(status, headers)
    
    return json.dumps( { "status": obj + " not found" } )

def ok_found(env, rs, merkle_path):
    status = "200 OK"
    headers = [("Content-Type", "application/json")]
    rs(status, headers)
    
    return json.dumps( { "status": "found", "path": merkle_path } )

def get_merkle_path(env, rs, obj):
    h = obj.groups()[0]
    print "Hash extracted from request %s" % h

    mpath = mtree.merkle_path(h)

    if mpath is not None:
        return ok_found(env, rs, mpath)
    else:
        return not_found(env, rs, "hash")

urls = [
    (r'^/hash/(.+)$', get_merkle_path)
]

def hash_server(env, rs):

    # Dispatch calls to the respective handlers
    path = env['PATH_INFO']

    for regx, handler in urls:
        path_param = re.match(regx, path)

        if path_param:
            return handler(env, rs, path_param)

    return not_found(env, rs, "path")

if __name__ == '__main__':
    httpd = make_server('', 8080, hash_server)

    httpd.serve_forever()
