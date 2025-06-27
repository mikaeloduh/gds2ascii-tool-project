import unittest
import struct
import io
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gds2ascii import readStream, appendName, extractData, unpack_4byte_real, unpack_8byte_real


class TestGds2Ascii(unittest.TestCase):

    def test_unpack_4byte_real_positive(self):
        # Test unpacking a positive 4-byte real number in GDSII format
        data = bytes([0x41, 0x10, 0x00, 0x00])  # 0x41100000 = 01000001 00010000 00000000 00000000 = 1.0 in GDSII format
        result = unpack_4byte_real(data)
        expected = 1.0
        self.assertAlmostEqual(result, expected, places=6)

    def test_unpack_4byte_real_negative(self):
        # Test unpacking a negative 4-byte real number in GDSII format
        data = bytes([0xC1, 0x10, 0x00, 0x00])  # 0xC1100000 = 11000001 00010000 00000000 00000000 = -1.0 in GDSII format
        result = unpack_4byte_real(data)
        expected = -1.0
        self.assertAlmostEqual(result, expected, places=6)

    def test_unpack_4byte_real_zero(self):
        # Test unpacking zero as a 4-byte real number
        data = bytes([0x00, 0x00, 0x00, 0x00])  # Represents 0.0
        result = unpack_4byte_real(data)
        expected = 0.0
        self.assertEqual(result, expected)

    def test_unpack_4byte_real_half(self):
        # Test unpacking 0.5 as a 4-byte real number
        data = bytes([0x40, 0x80, 0x00, 0x00])  # 0x40800000 = 01000000 10000000 00000000 00000000 = 0.5 in GDSII format
        result = unpack_4byte_real(data)
        expected = 0.5
        self.assertAlmostEqual(result, expected, places=6)

    def test_unpack_4byte_real_one_and_half(self):
        # Test unpacking 1.5 as a 4-byte real number
        data = bytes([0x41, 0x18, 0x00, 0x00])  # 0x41180000 = 01000001 00011000 00000000 00000000 = 1.5 in GDSII format
        result = unpack_4byte_real(data)
        expected = 1.5
        self.assertAlmostEqual(result, expected, places=6)

    def test_unpack_4byte_real_two_and_quarter(self):
        # Test unpacking 2.25 as a 4-byte real number
        data = bytes([0x41, 0x24, 0x00, 0x00])  # 0x41240000 = 01000001 00100100 00000000 00000000 = 2.25 in GDSII format
        result = unpack_4byte_real(data)
        expected = 2.25
        self.assertAlmostEqual(result, expected, places=6)

    def test_unpack_8byte_real_positive(self):
        # Test unpacking a positive 8-byte real number in GDSII format
        data = bytes([0x41, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 0x4110000000000000 = 
        # 01000001 00010000 00000000 00000000 00000000 00000000 00000000 00000000 = 1.0 in GDSII format
        result = unpack_8byte_real(data)
        expected = 1.0
        self.assertAlmostEqual(result, expected, places=12)

    def test_unpack_8byte_real_negative(self):
        # Test unpacking a negative 8-byte real number in GDSII format
        data = bytes([0xC1, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 0xC110000000000000 = 
        # 11000001 00010000 00000000 00000000 00000000 00000000 00000000 00000000 = -1.0 in GDSII format
        result = unpack_8byte_real(data)
        expected = -1.0
        self.assertAlmostEqual(result, expected, places=12)

    def test_unpack_8byte_real_zero(self):
        # Test unpacking zero as an 8-byte real number
        data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # Represents 0.0
        result = unpack_8byte_real(data)
        expected = 0.0
        self.assertEqual(result, expected)

    def test_unpack_8byte_real_half(self):
        # Test unpacking 0.5 as an 8-byte real number
        data = bytes([0x40, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 0x4080000000000000 = 
        # 01000000 10000000 00000000 00000000 00000000 00000000 00000000 00000000 = 0.5 in GDSII format
        result = unpack_8byte_real(data)
        expected = 0.5
        self.assertAlmostEqual(result, expected, places=12)

    def test_unpack_8byte_real_one_and_half(self):
        # Test unpacking 1.5 as an 8-byte real number
        data = bytes([0x41, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 0x4118000000000000 = 
        # 01000001 00011000 00000000 00000000 00000000 00000000 00000000 00000000 = 1.5 in GDSII format
        result = unpack_8byte_real(data)
        expected = 1.5
        self.assertAlmostEqual(result, expected, places=12)

    def test_unpack_8byte_real_two_and_quarter(self):
        # Test unpacking 2.25 as an 8-byte real number
        data = bytes([0x41, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # 0x4124000000000000 = 
        # 01000001 00100100 00000000 00000000 00000000 00000000 00000000 00000000 = 2.25 in GDSII format
        result = unpack_8byte_real(data)
        expected = 2.25
        self.assertAlmostEqual(result, expected, places=12)

    def test_append_name_header(self):
        # Test converting GDSII record type to 'HEADER' name
        record = [4, [0x00, 0x02], []]  # Record with HEADER type
        result = appendName(record)
        expected = 'HEADER'
        self.assertEqual(result, expected)

    def test_append_name_bgnlib(self):
        # Test converting GDSII record type to 'BGNLIB' name
        record = [4, [0x01, 0x02], []]  # Record with BGNLIB type
        result = appendName(record)
        expected = 'BGNLIB'
        self.assertEqual(result, expected)

    def test_append_name_endlib(self):
        # Test converting GDSII record type to 'ENDLIB' name
        record = [4, [0x04, 0x00], []]  # Record with ENDLIB type
        result = appendName(record)
        expected = 'ENDLIB'
        self.assertEqual(result, expected)

    def test_read_stream_valid_data(self):
        # Test reading a valid GDSII record from a byte stream
        data = struct.pack('>hbb', 6, 0x00, 0x02) + b'\x00\x01'  # Valid GDSII record
        stream = io.BytesIO(data)
        result = readStream(stream)
        self.assertEqual(result[0], 6)          # Record length
        self.assertEqual(result[1], [0x00, 0x02])  # Record type
        self.assertEqual(len(result[2]), 1)     # Data length

    def test_read_stream_invalid_data(self):
        # Test reading invalid/incomplete data from stream
        data = b'\x00'  # Incomplete data that cannot form a valid record
        stream = io.BytesIO(data)
        result = readStream(stream)
        self.assertEqual(result, -1)  # Should return -1 for invalid data

    def test_extract_data_no_data_type(self):
        # Test extracting data from record with no data type (data type 0)
        record = [4, [0x00, 0x00], []]  # Record with no data type
        result = extractData(record)
        self.assertEqual(result, [])  # Should return empty list

    def test_extract_data_bit_array(self):
        # Test extracting data from bit array type record (data type 1)
        record = [4, [0x00, 0x01], []]  # Record with bit array type
        result = extractData(record)
        self.assertEqual(result, [])  # Should return empty list

    def test_extract_data_2byte_signed_int(self):
        # Test extracting 2-byte signed integers from record (data type 2)
        data = [struct.pack('>h', 100), struct.pack('>h', -50)]  # Two 2-byte signed integers
        record = [8, [0x0D, 0x02], data]
        result = extractData(record)
        self.assertEqual(result, [100, -50])  # Should extract both integers

    def test_extract_data_4byte_signed_int(self):
        # Test extracting 4-byte signed integers from record (data type 3)
        data = [struct.pack('>l', 1000), struct.pack('>l', -500)]  # Two 4-byte signed integers  
        record = [12, [0x10, 0x03], data]
        result = extractData(record)
        self.assertEqual(result, [1000, -500])  # Should extract both integers

    def test_extract_data_4byte_real(self):
        # Test extracting 4-byte real numbers from record (data type 4)
        data = [bytes([0x41, 0x10, 0x00, 0x00])]  # 4-byte real representing 1.0
        record = [8, [0x1B, 0x04], data]
        result = extractData(record)
        self.assertAlmostEqual(result[0], 1.0, places=6)  # Should extract 1.0

    def test_extract_data_4byte_real_decimal(self):
        # Test extracting 4-byte real decimal numbers from record (data type 4)
        data = [bytes([0x40, 0x80, 0x00, 0x00]), bytes([0x41, 0x18, 0x00, 0x00])]  # 0.5 and 1.5
        record = [12, [0x1B, 0x04], data]
        result = extractData(record)
        self.assertAlmostEqual(result[0], 0.5, places=6)   # Should extract 0.5
        self.assertAlmostEqual(result[1], 1.5, places=6)   # Should extract 1.5

    def test_extract_data_8byte_real(self):
        # Test extracting 8-byte real numbers from record (data type 5)
        data = [bytes([0x41, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])]  # 8-byte real representing 1.0
        record = [12, [0x03, 0x05], data]
        result = extractData(record)
        self.assertAlmostEqual(result[0], 1.0, places=12)  # Should extract 1.0

    def test_extract_data_ascii_string(self):
        # Test extracting ASCII string data from record (data type 6)
        data = [b'H', b'e', b'l', b'l', b'o']  # ASCII string "Hello"
        record = [9, [0x19, 0x06], data]
        result = extractData(record)
        self.assertEqual(result, ['H', 'e', 'l', 'l', 'o'])  # Should extract each character


if __name__ == '__main__':
    unittest.main()