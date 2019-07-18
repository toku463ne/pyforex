

class DB(object):
    def __init__(self):
        '''
        connect to database
        '''
        self.connection = None
        self.cursor = None


    def close(self):
        '''
        close connection
        '''
        pass