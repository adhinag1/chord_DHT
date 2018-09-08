import sys
import glob

sys.path.append('gen-py')
sys.path.insert(0, glob.glob('/home/yaoliu/src_code/local/lib/lib/python2.7/site-packages')[0])

from chord import FileStore
from chord.ttypes import NodeID, RFile, RFileMetadata, SystemException

from hashlib import sha256

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def make_socket(ipAddress, port):
    transport = TSocket.TSocket(ipAddress, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    file_store = FileStore.Client(protocol)
    transport.open()
    return file_store;
    
    
class TestChord:
    transport = TSocket.TSocket(sys.argv[1], int(sys.argv[2]))
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    filestore = FileStore.Client(protocol)
    transport.open()
    
    def __init__(self):
        pass

    def test_write_file(self, rfile):
        node = self.filestore.findSucc(rfile.meta.contentHash)
        print "node id: ", node
        assert node.id == "162f2ef78020a93545457290a21d4ea634d4bca22aff8530e2011209be88ff82", "Test_Write_file - Node returned is wrong"
        print "Test case passed 1 -- get successor node for key: ", rfile.meta.contentHash

        
        file_store = make_socket(node.ip, node.port)
        file_store.writeFile(rfile)
        read_file = file_store.readFile(rfile.meta.filename, rfile.meta.owner)
        assert str(read_file.meta.filename) == str(rfile.meta.filename), "Test_Write_file - Filename mismatch"
        assert str(read_file.meta.version) == str(rfile.meta.version), "Test_Write_file - version mismatch"
        assert str(read_file.meta.owner) == str(rfile.meta.owner), "Test_Write_file - owner mismatch"
        assert str(read_file.meta.contentHash) == str(rfile.meta.contentHash), "Test_Write_file - contentHash mismatch"
        assert str(read_file.content) == str(rfile.content), "Test_Write_file - Content mismatch"
        print "Test case passed 2 -- Write file: file name - %s, owner - %s" % (rfile.meta.filename, rfile.meta.owner)
        
        
        """try:
            self.filestore.writeFile(rfile)
            raise AssertionError("Test_Write_file - No Exception on invalid write")
        except SystemException as err:
            assert err.message == "Key is not associated with the node", "Test_Write_file - Message Content Mismatch"
            print "Test case passed 3 -- ", err.message"""
        
        
    def test_read_file(self, filename, owner):
        
        node = self.filestore.findSucc(sha256(owner + ":" + filename).hexdigest())
        assert node.id == "162f2ef78020a93545457290a21d4ea634d4bca22aff8530e2011209be88ff82", "Test_Read_File - Node returned is wrong"
        print "Test case passed 4 -- get successor node for key: ", sha256(owner + ":" + filename).hexdigest()
        
        file_store = make_socket(node.ip, node.port)
        rfile.content = "This is a test program"
        file_store.writeFile(rfile)
        read_file = file_store.readFile(filename, owner)
        assert read_file.meta.filename == rfile.meta.filename, "Test_Read_file - Filename mismatch"
        assert str(read_file.meta.version) == str(int(rfile.meta.version) + 1), "Test_Read_file - version mismatch"
        assert read_file.meta.owner == rfile.meta.owner, "Test_Read_file - owner mismatch"
        assert read_file.meta.contentHash == rfile.meta.contentHash, "Test_Read_file - contentHash mismatch"
        assert read_file.content == rfile.content, "Test_Read_file - Content mismatch"
        print "Test case passed 5 -- write file: file name - %s, owner - %s" % (filename, owner)
        
        rfile.meta.filename = "test_p2.txt"
        rfile.meta.contentHash = sha256(owner + ":" + rfile.meta.filename).hexdigest()
        node = self.filestore.findSucc(rfile.meta.contentHash) 
        assert node.id == "162f2ef78020a93545457290a21d4ea634d4bca22aff8530e2011209be88ff82", "Test_Read_File - Node returned is wrong"
        print "Test case passed 6 -- get successor node for key: ", rfile.meta.contentHash
        
        file_store = make_socket(node.ip, node.port)
        file_store.writeFile(rfile)
        read_file = file_store.readFile(rfile.meta.filename, owner)
        assert read_file.meta.filename == rfile.meta.filename, "Test_Read_file - Filename mismatch"
        assert read_file.meta.version == rfile.meta.version, "Test_Read_file - version mismatch"
        assert read_file.meta.owner == rfile.meta.owner, "Test_Read_file - owner mismatch"
        assert read_file.meta.contentHash == rfile.meta.contentHash, "Test_Read_file - contentHash mismatch"
        assert read_file.content == rfile.content, "Test_Read_file - Content mismatch"
        print "Test case passed 7 -- write file: file name - %s, owner - %s" % (rfile.meta.filename, owner)
        
        rfile.meta.filename = "p2.txt"
        rfile.meta.owner = "AravindKumar"
        rfile.meta.contentHash = sha256(rfile.meta.owner + ":" + rfile.meta.filename).hexdigest()
        node = self.filestore.findSucc(rfile.meta.contentHash)
        assert node.id == "162f2ef78020a93545457290a21d4ea634d4bca22aff8530e2011209be88ff82", "Test_Read_File - Node returned is wrong"
        print "Test case passed 8 -- get successor node for key: ", rfile.meta.contentHash
        
        file_store = make_socket(node.ip, node.port)
        file_store.writeFile(rfile)
        read_file = file_store.readFile(rfile.meta.filename, rfile.meta.owner)
        assert read_file.meta.filename == rfile.meta.filename, "Test_Read_file - Filename mismatch"
        assert read_file.meta.version == rfile.meta.version, "Test_Read_file - version mismatch"
        assert read_file.meta.owner == rfile.meta.owner, "Test_Read_file - owner mismatch"
        assert read_file.meta.contentHash == rfile.meta.contentHash, "Test_Read_file - contentHash mismatch"
        assert read_file.content == rfile.content, "Test_Read_file - Content mismatch"
        print "Test case passed 9 -- write file: file name - %s, owner - %s" % (rfile.meta.filename, rfile.meta.owner)
        
        rfile.meta.filename = "p2_p2.txt"
        rfile.meta.owner = "AravindKumarDhinagaran"
        rfile.meta.contentHash = sha256(rfile.meta.owner + ":" + rfile.meta.filename).hexdigest()
        node = self.filestore.findSucc(rfile.meta.contentHash)        
        assert node.id == "162f2ef78020a93545457290a21d4ea634d4bca22aff8530e2011209be88ff82", "Test_Read_File - Node returned is wrong"
        print "Test case passed 10 -- get successor node for key: ", rfile.meta.contentHash 
        
        file_store = make_socket(node.ip, node.port)
        file_store.writeFile(rfile)
        read_file = file_store.readFile(rfile.meta.filename, rfile.meta.owner)
        assert read_file.meta.filename == rfile.meta.filename, "Test_Read_file - Filename mismatch"
        assert read_file.meta.version == rfile.meta.version, "Test_Read_file - version mismatch"
        assert read_file.meta.owner == rfile.meta.owner, "Test_Read_file - owner mismatch"
        assert read_file.meta.contentHash == rfile.meta.contentHash, "Test_Read_file - contentHash mismatch"
        assert read_file.content == rfile.content, "Test_Read_file - Content mismatch"
        print "Test case passed 11 -- write file: file name - %s, owner - %s" % (rfile.meta.filename, rfile.meta.owner)
        
        try:
            file_store.readFile(filename, 'invalid')
            raise AssertionError("Test_Read_file - No Exception on invalid owner name")
        except SystemException as err:
            print "Test case passed 12 -- ", err.message

        try:
            file_store.readFile('invalid', owner)
            raise AssertionError("Test_Read_file - No Exception on invalid filename")
        except SystemException as err:
            print "Test case passed 13 -- ", err.message
        
        try:
            self.filestore.readFile(filename, owner)
            raise AssertionError("Test_Read_file - No Exception on invalid read")
        except SystemException as err:
            assert err.message == "Key is not associated with the node", "Test_Read_file - Message Content Mismatch"
            print "Test case passed 14 -- ", err.message
        
        
    def test_negative_cases(self, filestore, key):
        
        try:
            filestore.findSucc(key)
            raise AssertionError("Test_Find_Succ - No Exception on empty finger table")
        except SystemException as err:
            assert err.message == "Fingertable not exist for the current node", "Test_Find_Succ - message content mismatch"
            print "Test case passed 15 -- ", err.message

        try:
            filestore.findPred(key)
            raise AssertionError("Test_Find_Pred - No Exception on empty finger table")
        except SystemException as err:
            assert err.message == "Fingertable not exist for the current node", "Test_Find_Pred - message content mismatch"
            print "Test case passed 16 -- ", err.message

        try:
            filestore.getNodeSucc()
            raise AssertionError("Test_Get_Node_Succ - No Exception on empty finger table")
        except SystemException as err:
            assert err.message == "Fingertable not exist for the current node", "Test_Node_Succ - message content mismatch"
            print "Test case passed 17 -- ", err.message

        
if __name__ == '__main__':
    rf_metadata = RFileMetadata()
    rf_metadata.filename = "file_name"
    rf_metadata.version = 0
    rf_metadata.owner = "owner_name"
    rf_metadata.contentHash = sha256(rf_metadata.owner + ":" + rf_metadata.filename).hexdigest()
    rfile = RFile()
    rfile.meta = rf_metadata
    rfile.content = "This is my first apache thrift programming experience"

    try:
        t = TestChord()
        t.test_write_file(rfile)
        t.test_read_file(rf_metadata.filename, rf_metadata.owner)
        #t.test_negative_cases(make_socket('128.226.180.166', 9095), rfile.meta.contentHash)
    except Thrift.TException as tx:
        print('%s' % tx.message)