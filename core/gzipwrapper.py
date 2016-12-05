import gzip

class GzipWrapper(object):

    def __init__(self, input, filename = None):
        self.input = input
        self.buffer = ''
        self.zipper = gzip.GzipFile(filename, mode = 'wb', fileobj = self)

    def read(self, size=-1):
        if (size < 0) or len(self.buffer) < size:
            for s in self.input:
                self.zipper.write(s)
                if size > 0 and len(self.buffer) >= size:
                    self.zipper.flush()
                    break
            else:
                self.zipper.close()
            if size < 0:
                ret = self.buffer
                self.buffer = ''
        else:
            ret, self.buffer = self.buffer[:size], self.buffer[size:]
        return ret

    def flush(self):
        pass

    def write(self, data):
        self.buffer += data

    def close(self):
        self.input.close()