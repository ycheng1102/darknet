import os
import tarfile


print("Extract train.tar.gz & test.tar.gz ...")

with tarfile.open('train.tar.gz') as tf:
  tf.extractall('data')
with tarfile.open('test.tar.gz') as tf:
  tf.extractall('data')
os.rename('data/test', 'data/val')

print("Done!")