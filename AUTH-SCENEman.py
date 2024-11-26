import sys
import os
from binary_reader import BinaryReader


FilePaths = sys.argv[1:]

for FilePath in FilePaths:

    FILENAME = os.path.splitext(os.path.basename(FilePath))[0]
    EXTNAME = os.path.splitext(os.path.basename(FilePath))[1]
    INPUTDIR = os.path.dirname(FilePath)
    OUTPUTDIR = os.path.join(INPUTDIR,(FILENAME + EXTNAME + ".unpack"))
    os.makedirs(OUTPUTDIR,exist_ok=True)
    auth = open (FilePath,"rb")
    reader = BinaryReader(auth.read())
    reader.seek(24)
    MTBW_Offset1 = reader.read_int32()
    MTBW_Count1 = reader.read_int32()
    MTBW_Offset2 = reader.read_int32()
    MTBW_Count2 = reader.read_int32()
    OMT_Offset = reader.read_int32()
    OMT_Count = reader.read_int32()
    reader.seek(MTBW_Offset1)
    for m1 in range(MTBW_Count1):
        MTBW1_Size = reader.read_uint32()
        MTBW1_PAD = reader.read_bytes(12)
        MTBW1_File = reader.read_bytes(MTBW1_Size)
        OUTPUTPATH1 = os.path.join(OUTPUTDIR,f"Camera1" + "-" + (str(m1)) + ".MTBW")
        with open (OUTPUTPATH1,mode="wb")as output1:
            output1.write(MTBW1_File)
    reader.seek(MTBW_Offset2)
    for m2 in range(MTBW_Count2):
        MTBW2_Size = reader.read_uint32()
        MTBW2_PAD = reader.read_bytes(12)
        MTBW2_File = reader.read_bytes(MTBW2_Size)
        OUTPUTPATH2 = os.path.join(OUTPUTDIR,f"Camera2" + "-" + (str(m2)) + ".MTBW")
        with open (OUTPUTPATH2,mode="wb")as output2:
            output2.write(MTBW1_File)
    reader.seek(OMT_Offset)
    for o in range(OMT_Count):
        OMT_Size = reader.read_uint32()
        OMT_PAD = reader.read_bytes(12)
        ReturnOffset=reader.pos()
        reader.seek(ReturnOffset+8)
        BoneCount = reader.read_uint32()
        reader.seek(ReturnOffset)
        if BoneCount == 19:
            name="Hand"
        elif BoneCount == 24:
            name="Body"
        elif BoneCount == 56:
            name="Face"
        else:
            name="Unknown"
        OMT_File = reader.read_bytes(OMT_Size)
        OUTPUTPATH3 = os.path.join(OUTPUTDIR,f"Character" + "-" + (str(o))  + "-" + name + ".omt")
        with open (OUTPUTPATH3,mode="wb")as output3:
            output3.write(OMT_File)

        

