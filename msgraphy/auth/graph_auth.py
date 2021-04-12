import atexit, msal


class FileSystemTokenCache(msal.SerializableTokenCache):

    def __init__(self, filename, save_on_exit=False):
        self.__filename = filename
        super(FileSystemTokenCache, self).__init__()
        self.load()
        if save_on_exit:
            atexit.register(self.save)

    def load(self):
        try:
            with open(self.__filename, 'r') as file:
                self.deserialize(file.read())
        except:
            pass

    def save(self):
        with open(self.__filename, 'w') as file:
            file.write(self.serialize())


