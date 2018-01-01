import math


class Bitmap_Entry:


    def __init__(self, key, record_number, mem_loc):

        self.key = key
        self.record_list = []
        self.record_list.append(record_number)
        self.compressed_bitstring = ""
        self._int = 0

    def __repr__(self):
        return str(self.record_list)

    # METHOD FOR ADDING RECORD NUMBER TO RECORD LIST
    def append(self, record_number, mem_loc):
        self.record_list.append(record_number)
        #self.mem_list.append(mem_loc)

    # METHOD FOR COMPUTING RUN LENGTH ENCODING
    def encode_compressed_bitstring(self):

        bitstring = ""
        for num in range(len(self.record_list)):
            if num == 0:
                difference = self.record_list[num]
            else:
                difference = self.record_list[num] - self.record_list[num - 1] - 1

            i = math.ceil(math.log2(difference + 1))
            bitstring += ("1" * (i - 1) + "0")
            bitstring += "{0:b}".format(difference)

        self.compressed_bitstring = bitstring
        #self._int = int(bitstring,2)
        self.record_list = []

    # METHOD TO GET BITSTRING FROM RUN LENGTH ENCODED
    def decode_compressed_string(self, n):

        compressed = self.compressed_bitstring
        string = ""

        while (len(compressed) > 0):

            num_bits = compressed.find("0") + 1

            compressed = compressed[num_bits:]

            space = int(str(compressed[:num_bits]), 2)

            string += "0" * space
            string += "1"

            compressed = compressed[num_bits:]

        # MAKE SURE ALL STRINGS ARE THE SAME SIZE
        if (len(string) < n):
            string += "0" * (n - len(string))

        return string

    # METHOD TO GET A RECORD LIST BACK FROM RUN LENGTH ENCODED STRING
    def populate_record_list(self):

        compressed = self.compressed_bitstring

        new_record_list = []

        while (len(compressed) > 0):
            num_bits = compressed.find("0") + 1
            compressed = compressed[num_bits:]

            space = int(str(compressed[:num_bits]), 2)

            print("space: " + str(space))

            if (len(new_record_list) == 0):
                new_record_list.append(space)
            else:
                new_record_list.append(new_record_list[-1]+space+1)

            compressed = compressed[num_bits:]

        return new_record_list
