import merkle
import requests
import hashlib
import json
import os

SERVER_URL = "http://localhost:8080"
HASH_API = SERVER_URL + "/hash"
SAMPLE_DATASET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../test_data/extract.csv")

def get_index(size):
    
    while True:
        idx = input("Row number (Between 1 and " + str(size) + "): ") - 1

        if (idx >= 0 and idx < size):
            return idx

def sha256(datum):
    return hashlib.sha256(str(datum)).hexdigest()
            
def fetch_path(h):
    resp = requests.get(HASH_API + "/" + h)
    j = json.loads(resp.text)

    if str(j["status"]) == "found":
        return (str(j["status"]), map(str, j["path"]))
    else:
        return (str(j["status"]), [])

def audit_presence(linum, row, root_1):
    h = sha256(str(linum) + row)

    (status, hashes) = fetch_path(h)

    if status == "found":
        print "The following path was received for %s\n" % h
        print hashes
        print ""
        
        root_2 = reduce(lambda x, y: sha256(x + y[1:]) if y[0] == "1" else sha256(y[1:] + x), hashes, h)

        print "Calculated root from the received path -> %s" % root_2
        
        if root_1 == root_2:
            return "Success"

    return "Failure"

def main():
    print "Starting Merkle Tree Demo Client App ..."

    print "[*] Calculating Merkle Root"
    mroot = merkle.Merkle(SAMPLE_DATASET).root_hash()

    print "[*] Caching rows"

    f = open(SAMPLE_DATASET, "r")
    rows = [line[:-1] for line in f.readlines()]
    f.close()

    print "%d rows read" % len(rows)

    # Display menu
    while True:
        print "Menu"
        print "===================="
        print "1. Merkle root"
        print "2. Display row"
        print "3. Update row"
        print "4. Audit presence"
        print "5. Exit demo"

        choice = input("> ")
        
        if choice == 1:
            print mroot
        elif choice == 2:
            print rows[get_index(len(rows))]
        elif choice == 3:
            idx = get_index(len(rows))
            text = raw_input()
            rows[idx] = text
            print "Row %d updated successfully!" % (idx + 1)
        elif choice == 4:
            idx = get_index(len(rows))
            print audit_presence(idx, rows[idx], mroot)
        elif choice == 5:
            print "Bye!"
            break
    

if __name__ == '__main__':
    main()
