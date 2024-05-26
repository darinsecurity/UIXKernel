class base64:
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    @classmethod
    def chunk(cls, data, length):
        return [data[i:i+length] for i in range(0, len(data), length)]

    @classmethod
    def int_to_bin(cls, number, length):
        # Convert an integer to a binary string with a specific length
        bin_str = bin(number)[2:]  # Remove the '0b' prefix
        return '0' * (length - len(bin_str)) + bin_str

    @classmethod
    def b64encode(cls, data):
        override = 0
        if len(data) % 3 != 0:
            override = (len(data) + 3 - len(data) % 3) - len(data)
        data += b"\x00" * override

        threechunks = cls.chunk(data, 3)

        binstring = ""
        for chunk in threechunks:
            for x in chunk:
                binstring += cls.int_to_bin(x, 8)

        sixchunks = cls.chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += cls.CHARS[int(element, 2)]

        outstring = outstring[:-override] + "=" * override
        return outstring

    @classmethod
    def b64decode(cls, b64_string):
        base64_chars = cls.CHARS
        base64_map = {char: index for index, char in enumerate(base64_chars)}

        # Pre-calculated binary values for each base64 index
        

        padding_length = b64_string.count('=')
        b64_string = b64_string.rstrip('=')

        decoded_bits = []
        for char in b64_string:
            if char in base64_map:
                value = base64_map[char]
                decoded_bits.append(cls.binary_lookup[value])
            else:
                raise ValueError("Invalid character found in base64 string")

        # Join all the binary strings together
        decoded_bits = ''.join(decoded_bits)

        if padding_length:
            decoded_bits = decoded_bits[:-(padding_length * 2)]

        byte_array = bytearray()
        for i in range(0, len(decoded_bits), 8):
            byte_chunk = decoded_bits[i:i+8]
            if len(byte_chunk) == 8:
                byte_array.append(int(byte_chunk, 2))

        return bytes(byte_array)

    binary_lookup = {index: '0' * (6 - len(bin(index)[2:])) + bin(index)[2:] for index in range(64)}
