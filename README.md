# flacdb
Compress Physionet dat files to flac, achieves ~2.7x compression

### Install Requirements

```
pip3 install numpy wfdb soundfile
```

### Example Usage

```
import flacdb
import os

path = '/mimic3wdb/train/3000989_0002'
rec = wfdb.rdrecord(path)
flacdb.write_record(rec, path)

try:
  assert(rec == flacdb.read_record(path))
  os.remove(path + '.dat')
except:
  print('flac compression failed')
```
