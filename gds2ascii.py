######################################################################
#                                                                    #
#  Author: Michael Duh                                               #
#  Date: 25 Jan 2017                                                 #
#                                                                    #
#  This is a software to convert GDSii file to ASCii format          #
#  To use this software please put your .gds file in the same        #
#  folder. Output file will generate as JSON file.                   #
#                                                                    #
######################################################################

import sys
import struct
import json


# Reading Hex stream.
#
# input  : Hex format from raw file
# return : (list) [ record length, [record type, data type], [data1, data2, ...] ]
def readStream(stream):
    try:
        rec_data = []
        rec_size = struct.unpack('>h', stream.read(2))[0]
        stream.seek(0, 1)
        rec_type = struct.unpack('>b', stream.read(1))[0]
        stream.seek(0, 1)
        dat_type = struct.unpack('>b', stream.read(1))[0]
        stream.seek(0, 1)
        dat_size = {0x00: 1, 0x01: 1, 0x02: 2, 0x03: 4, 0x04: 4, 0x05: 8, 0x06: 1}
        for i in list(range(0, (rec_size-4)//dat_size[dat_type])):
            rec_data.append( stream.read(dat_size[dat_type]) )
            stream.seek(0, 1)
        return [rec_size, [rec_type, dat_type], rec_data]
    
    except:
        return -1

# Reading Hex stream.
#
# input  : (list) [ record length, [record type, data type], [data1, data2, ...] ]
# return : (string) record name 
def appendName(record):
    name_list = {0x00 : 'HEADER',
                0x01 : 'BGNLIB',
                0x02 : 'LIBNAME',
                0x03 : 'UNITS',
                0x04 : 'ENDLIB',
                0x05 : 'BGNSTR',
                0x06 : 'STRNAME',
                0x07 : 'ENDSTR',
                0x08 : 'BONDARY',
                0x09 : 'PATH',
                0x0A : 'SERF',
                0x0B : 'AREF',
                0x0C : 'TEXT',
                0x0D : 'LAYER',
                0x0E : 'DATATYPE',
                0x0F : 'WIDTH',
                0x10 : 'XY',
                0x11 : 'ENDEL',
                0x12 : 'SNAME',
                0x13 : 'COLROW',
                0x15 : 'NODE',
                0x16 : 'TEXTTYPE', 
                0x17 : 'PRESENTATION', 
                0x19 : 'STRING', 
                0x1A : 'STRANS', 
                0x1B : 'MAG', 
                0x1C : 'ANGLE', 
                0x1F : 'REFLIBS', 
                0x20 : 'FONTS', 
                0x21 : 'PATHTYPE', 
                0x22 : 'GENERATIONS', 
                0x23 : 'ATTRATABLE', 
                0x26 : 'ELFLAGS', 
                0x2A : 'NODETYPE', 
                0x2B : 'PROPATTR', 
                0x2C : 'PROPVALUE', 
                0x2D : 'BOX', 
                0x2E : 'BOXTYPE', 
                0x2F : 'PLEX', 
                0x32 : 'TAPENUM', 
                0x33 : 'TAPECODE', 
                0x36 : 'FORMAT', 
                0x37 : 'MASK', 
                0x38 : 'ENDMASKS'
                }
    return name_list[record[1][0]]

# Extracting Hex Data to readable ASCii
#
# input  : (list) [ record length, [record type, data type], [data1, data2, ...] ]
# return : (list) [ASCii data, ASCii data, ... ]
def extractData(record):
    data = []
    if record[1][1] == 0x00:
        return data

    elif record[1][1] == 0x01:
        return data

    elif record[1][1] == 0x02:
        for i in list(range(0, (record[0]-4)//2)):
            data.append( struct.unpack('>h', record[2][i])[0] )
        return data 

    elif record[1][1] == 0x03:
        for i in list(range(0, (record[0]-4)//4)):
            data.append( struct.unpack('>l', record[2][i])[0] )
        return data

    elif record[1][1] == 0x04:
        for i in list(range(0, (record[0]-4)//4)):
            data.append( struct.unpack('>f', record[2][i])[0] )
        return data

    elif record[1][1] == 0x05:
        for i in list(range(0, (record[0]-4)//8)):
            data.append( struct.unpack('>d', record[2][i])[0] )
        return data

    else:
        for i in list(range(0, (record[0]-4))):
            data.append( struct.unpack('>c', record[2][i])[0].decode("utf-8") )
        return data

# Main 
# Command argument 1 : input .gds file path
# Command argument 2 : output file path
def main():
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    asciiOut = []

    with open(inputFile, mode='rb') as ifile:   
        while True:
            record = readStream(ifile)
            data = extractData(record)
            name = appendName(record)
            asciiOut.append([name, data])        
            print([name, data])
            if record[1][0] == 0x04:
                break

        with open(outputFile, 'w') as ofile:
            json.dump(asciiOut, ofile, indent=4)


if __name__ == '__main__':
    main()
    
