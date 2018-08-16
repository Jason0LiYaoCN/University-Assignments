class Hashtable:
    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size
        self.data = [None] *self.size
    
    def put(self, key, data):
        hash_value = self.hash_function(key)

        if self.slots[hash_value] == None:
            self.slots[hash_value] = key
            self.data[hash_value] = data
        else:
            if self.slots[hash_value] == key:
                self.data[hash_value] = data # replace
            else:
                next_slot = self.rehash(hash_value)
                while self.slots[next_slot] != None\
                and self.slots[next_slot] != key:
                    next_slot = self.rehash(next_slot)
                
                if self.slots[next_slot] == None:
                    self.slots[next_slot] = key
                    self.data[next_slot] = data
                else:
                    self.data[next_slot] = data

    def hash_function(self, key):
        return key % self.size

    def rehash(self, old_hash):
        return (old_hash + 1) % self.size
    