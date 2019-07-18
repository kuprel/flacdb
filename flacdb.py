import wfdb
import soundfile
import numpy

def to_digital(rec):
    data = rec.p_signal.copy()
    data *= rec.adc_gain
    data += rec.baseline
    data[numpy.isnan(data)] = -2**15
    data = numpy.around(data).astype('int16')
    return data

def to_physical(data, hdr):
    data = data.astype('float64')
    data[data==-2**15] = numpy.nan
    data -= hdr.baseline
    data /= hdr.adc_gain
    return data

def read_record(path, blocksize=2**20):
    rec = wfdb.rdheader(path)
    data = numpy.zeros((rec.sig_len, rec.n_sig), dtype='int16')

    with open(path + '.flac', 'rb') as f:

        sf = soundfile.SoundFile(f)

        blocks = sf.blocks(dtype='int16', blocksize=blocksize)

        for i, block in enumerate(blocks):
            if rec.n_sig == 1: block = numpy.expand_dims(block, axis=1)
            data[i*blocksize:(i+1)*blocksize] = block

        rec.p_signal = to_physical(data, rec)

    return rec

def write_record(rec, path):
    data = to_digital(rec)
    with open(path + '.flac', 'wb') as f:
        soundfile.write(f, data, 125, format='FLAC')
