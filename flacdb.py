import wfdb
import soundfile
import numpy

max_block_size = 2**21

def to_digital(data, hdr):
    data *= hdr.adc_gain
    data += hdr.baseline
    data[numpy.isnan(data)] = -2**15
    data = numpy.around(data).astype('int16')
    return data

def to_physical(data, hdr):
    data = data.astype('float64')
    data[data==-2**15] = numpy.nan
    data -= hdr.baseline
    data /= hdr.adc_gain
    return data

def write_record(rec, path):
    data = to_digital(rec.p_signal.copy(), rec)
    soundfile.write(path + '.flac', data, 125, format='FLAC')

def _read_blocks(hdr, path):
    data = numpy.empty((hdr.sig_len, hdr.n_sig), dtype='int16')

    with soundfile.SoundFile(path + '.flac') as sf:

        blocks = sf.blocks(blocksize=max_block_size, dtype='int16', always_2d=True)

        for i, block in enumerate(blocks):
            data[i*max_block_size:(i+1)*max_block_size] = block

    return data

def read_record(path):
    hdr = wfdb.rdheader(path)

    if hdr.sig_len < max_block_size:
        data, rate = soundfile.read(path + '.flac', dtype='int16', always_2d=True)
    else:
        data = _read_blocks(hdr, path)

    hdr.p_signal = to_physical(data, hdr)

    return hdr
