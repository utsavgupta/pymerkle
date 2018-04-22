import hashlib

class Merkle(object):

    def __init__(self, path, h = None):

        # Keeping the hash function configurable, this would also help in testing
        self._h = self._sha256_digest if h is None else h 
            
        f = open(path, "r")
        self._hashes = map(self._h, [str(a) + b for a, b in enumerate([line[:-1] for line in f.readlines()])])
        f.close()
        
        offset = len(self._hashes) - 1
        self._index = dict(zip(self._hashes, range(0 + offset, len(self._hashes) + offset)))

        self._tree = self._generate_merkle_tree(self._hashes, self._hashes)

    @property
    def tree(self):
        """
           Return the array representation of the Merkle tree (full binary hash tree)
        """
        
        return self._tree

    def root_hash(self):
        """
           Returns the root of the Merkle tree

           Returns None if the tree is empty
        """
        
        if(len(self._tree) < 1):
            None
        else:
            return self._tree[0]

    def _sha256_digest(self, datum):
        """
           Helper function to generate the SHA-256 hex digest of stringified argument
    
           Example:

              __sha256_digest("Hello")
        
              "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"
        """
        
        return hashlib.sha256(str(datum)).hexdigest()

    def _is_odd(self, n):
        """
           Helper function to check if a number is odd or not
        """

        return n % 2 == 1

            
    def _merge_pair(self, pair):
        """
           Accepts tuple of atleast two elements (a, b)

           Concatenates both values and then generates hex digest using the given
           hash function

           Example: 
              __merge_pair("Hello", "World")

              "872e4e50ce9990d8b041330c47c9ddd11bec6b503ae9386a99da8584e9bb12c4"
        """
    
        return self._h(pair[0] + pair[1])

    def _generate_merkle_tree(self, curr, children = list()):
        """
           Generates and returns the array representation of the Merkle tree.

           Where the element at the 0th position is the root element, has it's left child at 1 and right at 2.
           
           For the node n at postion N, the left child is stored at index (2 * N) + 1 and the right child is 
           stored at index (2 * N) + 2.
           
           The function is designed to handle fill binary trees. Ie the number of elements to be added to the
           tree can only be 0,2,4,8,16 .. 2^n
           
           Example:
              __generate_merkle_tree([h(a), h(b), h(c), h(d)])
           
              [h(h(h(a) + h(b)) + h(h(c) + h(d))), h(h(a) + h(b)), h(h(c) + h(d)), h(a), h(b), h(c), h(d)] 
        """
    
        hash_pairs = [(curr[i], curr[i + 1]) for i in xrange(0, len(curr) - 1, 2)]
        parents = map(self._merge_pair, hash_pairs)

        if(len(parents) < 2):
            return parents + children
        else:
            return self._generate_merkle_tree(parents, parents + children)
    
    def _merkle_path(self, index, partial_path):
        """
           Generates the Merkle path from the given index.
        """
        
        if index == 0 :
            return partial_path
        else:
            if(self._is_odd(index)):
                partial_path.append("1" + self.tree[index + 1])
                return self._merkle_path((index - 1) / 2, partial_path)
            else:
                partial_path.append("0" + self.tree[index - 1])
                return self._merkle_path((index - 2) / 2, partial_path)

    def merkle_path(self, hash_value):
        """
           Returns the Merkle path or authentication path for the given hash, if  present
           else returns None.
        """
        
        if hash_value not in self._index.keys():
            return None
        else:
            return self._merkle_path(self._index[hash_value], [])
