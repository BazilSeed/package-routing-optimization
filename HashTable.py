# Creation of HashMap Class



class HashMap:
    def __init__(self, min_capacity=47):
        # Create empty buckets so multiple keys can share the same index (collision handling).
        self.list = []
        for i in range(min_capacity):
            self.list.append([])

    # Add a new key/item or update the item if the key already exists
    # Citing source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
    def insert(self, key, item):
        # Choose a bucket using the key’s hash value.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # If the key is already stored here, replace the existing item.
        for pair in bucket_list:
            if pair[0] == key:
                pair[1] = item
                return True

        # Otherwise, store a new [key, item] pair in this bucket.
        bucket_list.append([key, item])
        return True

    # Find and return the item stored for a given key
    def lookup(self, key):
        # Go to the bucket where the key would be stored.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Search the bucket for the matching key.
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]

        # Key not found.
        return None
