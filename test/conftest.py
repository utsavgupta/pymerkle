import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest
import os
import src.merkle as merkle

def pytest_sessionstart(session):

    f = open("./test.dat", "w")

    lines = [chr(c) + "\n" for c in xrange(97, 105)]
    
    f.writelines(lines)

    f.close()

def pytest_sessionfinish(session, exitstatus):

    os.remove("./test.dat")
    exit(exitstatus)
    
    
@pytest.fixture(scope="session")
def mtree():
    return merkle.Merkle("./test.dat", lambda x: x)

@pytest.fixture(scope="session")
def test_data():
    f = open("./test.dat", "r")
    data = [ line[:-1] for line in f.readlines() ]
    f.close()

    return data
    
