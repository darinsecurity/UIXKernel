class base64:
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    @classmethod
    def chunk(cls, data, length):
        return [data[i:i+length] for i in range(0, len(data), length)]

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
                binstring += format(x, '08b')

        sixchunks = cls.chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += cls.CHARS[int(element, 2)]

        outstring = outstring[:-override] + "=" * override
        return outstring

    @classmethod
    def b64decode(cls, b64_string):
        # Base64 character set
        base64_chars = cls.CHARS
        base64_map = {char: index for index, char in enumerate(base64_chars)}

        # Remove padding characters and compute the padding length
        padding_length = b64_string.count('=')
        b64_string = b64_string.rstrip('=')

        # Convert base64 characters to their corresponding values
        decoded_bits = ""
        for char in b64_string:
            if char in base64_map:
                value = base64_map[char]
                # Convert the value to a 6-bit binary string and append to the result
                decoded_bits += format(value, '06b')
            else:
                raise ValueError("Invalid character found in base64 string")

        # Remove the padding bits from the binary string
        if padding_length:
            decoded_bits = decoded_bits[:-(padding_length * 2)]

        # Split the binary string into bytes (8 bits each)
        byte_array = bytearray()
        for i in range(0, len(decoded_bits), 8):
            byte_chunk = decoded_bits[i:i+8]
            if len(byte_chunk) == 8:
                byte_array.append(int(byte_chunk, 2))

        return bytes(byte_array)
