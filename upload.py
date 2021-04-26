#!/usr/bin/env python
import sys
import os
import subprocess
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(10)  # 10 ecc symbols

# INPUT:
# Takes in the name of a file to read (filein),
# and a file name (filename).

# OUTPUT:
# Doesn't return a value, but writes files in the
# format filename + i + .mp4

def main(argv):
        filein = str(sys.argv[1])
        filename = str(sys.argv[2])
        i = 0

        with open(filein, "rb") as f:
            fullname = os.path.basename(filename) + str(i)
            byte = f.read()

            outfile = open(fullname, "wb")
            
            if len(byte) % 2 == 1:
                byte += '0'.encode("utf-8")

            outfile.write(byte)
            outfile.close()

            # Do rsencode
            file_data = subprocess.check_output("cat " + fullname, shell=True)
            encoded_file_data = rsc.encode(file_data)
            rsoutfile = open("rs" + fullname, "wb")
            rsoutfile.write(encoded_file_data)
            subprocess.call("rm " + fullname, shell=True)

            rsname = "rs" + fullname

            subprocess.call("cat " + rsname + " | ./lvdo/src/lvdoenc -s 640x480 -q 6 --qmin 1 --qmax 4 | x264 --input-res 640x480 --fps 1 --profile high --level 5.1 --tune stillimage --crf 22 --colormatrix bt709 --me dia --merange 0 -o " + fullname + ".mkv -", shell=True)
            subprocess.call("rm " + rsname, shell=True)
            # subprocess.call("ffmpeg -i " + fullname + ".mkv -codec copy " + fullname + ".mp4", shell=True)
            subprocess.call("ffmpeg -i " + fullname + ".mkv -c copy " + fullname + ".mp4", shell=True)
            subprocess.call("rm " + fullname + ".mkv", shell=True)

            #Upload video to youtube
            subprocess.call("./youtube-upload/bin/youtube-upload --title=\"" + fullname + "\" " + fullname + ".mp4", shell=True)
            subprocess.call("rm "  + fullname + ".mp4", shell=True)


        # Return the number of mp4s made.
        return i


if __name__ == '__main__':
        main(sys.argv[1:])
