#!/usr/bin/env python
import sys
import os
import subprocess
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(10)  # 10 ecc symbols

# INPUT:
# Takes in an array of youtube linksa (filein)
# and a file name for the final result.

# OUTPUT:
# Doesn't return a value, but writes a the wanted file

def main(argv):
  filename = str(sys.argv[1])
  videos = sys.argv[2:]

  # i = 0
  # for video in videos:
  #   i +=1
  #   subprocess.call("youtube-dl " + video + " -o chunk" + str(i) + ".mp4", shell=True)

  #   subprocess.call("ffmpeg -i chunk" + str(i) + ".mp4 -r 1 -f rawvideo temp", shell=True)
  #   subprocess.call("cat temp | ./lvdo/src/lvdodec -s 640x480 -q 6 --qmin 1 --qmax 4 | cat > chunk" + str(i), shell=True)
  #   subprocess.call("rm temp", shell=True)
  #   subprocess.call("rm chunk"+str(i)+".mp4", shell=True)

  #   print('--------------------------------------------------')
  #   subprocess.call("cat chunk" + str(i) + " | ./ezpwd-reed-solomon/rsencode_16 --decode > part" + str(i), shell=True)

  # full_file = bytearray()
  # for i in range(1,i+1):
  #   f = open("part" + str(i), "rb")
  #   byte = f.read(65536)
  #   full_file.extend(byte)
  #   f.close()


  # f = open(filename, "wb")
  # f.write(full_file)
  # f.close()
  subprocess.call("youtube-dl " + videos[0] + " -o chunk" + ".mp4", shell=True)

  # subprocess.call("ffmpeg -i chunk" + ".mp4 -r 1 -f rawvideo temp", shell=True)
  # subprocess.call("cat temp | ./lvdo/src/lvdodec -s 640x480 -q 6 --qmin 1 --qmax 4 | cat > chunk", shell=True)
  # subprocess.call("rm temp", shell=True)
  # subprocess.call("rm chunk"+".mp4", shell=True)

  subprocess.call("ffmpeg -i " + "chunk.mp4 -c copy " + "temp.mkv", shell=True)
  subprocess.call("ffmpeg -i temp.mkv -r 1 -f rawvideo - | ./lvdo/src/lvdodec -s 640x480 -q 6 --qmin 1 --qmax 4 | cat > chunk", shell=True)
  subprocess.call("rm temp.mkv", shell=True)
  subprocess.call("rm chunk"+".mp4", shell=True)

  print('--------------------------------------------------')
  chunkFile = subprocess.check_output("cat chunk", shell=True)
  decoded = rsc.decode(chunkFile)[0]
  outfile = open(filename, "wb")
  outfile.write(decoded)
  outfile.close()

  sys.exit()

if __name__ == '__main__':
        main(sys.argv[1:])
