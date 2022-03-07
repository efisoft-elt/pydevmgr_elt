

#       _ _            _      __                            
#   ___| (_) ___ _ __ | |_   / /__  ___ _ ____   _____ _ __ 
#  / __| | |/ _ \ '_ \| __| / / __|/ _ \ '__\ \ / / _ \ '__|
# | (__| | |  __/ | | | |_ / /\__ \  __/ |   \ V /  __/ |   
#  \___|_|_|\___|_| |_|\__/_/ |___/\___|_|    \_/ \___|_|   
                                                          
# Make a dummy server and client only for the tutorial puposes 

import json


class TestServer:
    """ A dummy server for test purpose """
    def __init__(self, data=None):
        self.data = {} if data is None else data 
        self.data.setdefault("MOTOR1.POS", 0.0)
        self.data.setdefault("MOTOR2.POS", 0.0)
    
    def receive(self, payload: str):
        payload = json.loads(payload)
        cmd = payload.get("cmd", "UNKNOWN")
        
        try:
            if cmd == "move":
                prefix, args = payload['prefix'], payload['args']
                pos, = args 
                self.data[prefix+".POS"] = pos
                reply = {'answer':0, 'error':0}
            
            elif cmd == "init":
                prefix = payload['prefix']
                self.data[prefix+".POS"] = 0.0
                reply = {'answer':0, 'error':0}

            elif cmd == "read":
                keys = payload['keys']
                reply = {'answer': [self.data[key] for key in keys], 'error':0 }
            elif cmd == "write":
                for key, value in payload['values'].items():
                    self.data[key] = value

                reply = {'answer': 0, 'error': 0}
            
            else:
                raise ValueError("Unknown command")
        
        except Exception as e:
            reply = {'answer':None, 'error':1, 'error_txt':str(e)}
        return json.dumps(reply)
    


class TestClient:
    """ A dummy client for test purposes  """
    def __init__(self, address):
        self.address = address
        self.server = None
            
    def send(self, payload: dict):
        if not self.server:
            raise RuntimeError("Client not connected")
        # In real life this will go over some network 
        reply = self.server.receive(json.dumps(payload))
        
        reply = json.loads(reply)
        if reply['error']:
            raise RuntimeError(reply['error_txt'])
        
        return reply['answer']
    
    def connect(self):
        self.server = TestServer() 

    def disconnect(self):
        self.server = None
        

class TestReadCollector:
    def __init__(self, client):
        self._nodes = set()
        self.client = client
    def add(self, node):
        self._nodes.add(node)
    def read(self, data):
        keys = [node.remote_key for node in self._nodes]
            
        values = self.client.send( {'cmd':'read', 'keys':keys} ) 
        data.update( zip(self._nodes, values) )

class TestWriteCollector:
    def __init__(self, client):
        self._nodes = {}
        self.client = client
    
    def add(self, node, value):
        self._nodes[node] = value
    
    def write(self):
        values = {node.remote_key: value for node, value in self._nodes.items()  }
        self.client.send( {'cmd':'write', 'values':values} )

      



#  _   _           _      
# | \ | | ___   __| | ___ 
# |  \| |/ _ \ / _` |/ _ \
# | |\  | (_) | (_| |  __/
# |_| \_|\___/ \__,_|\___|

# The goal here is to create a Node for the use of our client 

from pydevmgr_core import BaseNode, kjoin, record_class
from typing import Optional, Any 

@record_class 
class TestNode(BaseNode):
    class Config(BaseNode.Config):
        type = "Test" # each object has a kind (this one is a node) and a type 
        suffix: str
        default: Optional[Any] = None
    
    def __init__(self, key=None, client=None, prefix="", **kwargs):
        super().__init__(key=key, **kwargs)
        if client is None:
            raise ValueError("Client is missing")
        self.client = client 
        self.remote_key = kjoin(prefix, self.config.suffix)
    
    @property
    def sid(self):
        return self.client.address # the client address is use as a unic server id this is needs by donwload 
    

    @classmethod
    def new_args(cls, parent, config):
        # This method is used when the node is created from a parent object 
        # in our case the parent (a Device or Interface) will need to pass the 
        # client object and the targeted device prefix
        d = super().new_args(parent, config)
        d.update(
            client =  parent.client, 
            prefix =  parent.remote_key 
        )
        return d
    
    def fget(self):
        return self.client.send( {'cmd': 'read', 'keys':[self.remote_key]} )[0]
    
    def fset(self, value):
        self.client.send( {'cmd':'write', 'values':{self.remote_key:value}} )

    def read_collector(self):
        return TestReadCollector(self.client)

    def write_collector(self):
        return TestWriteCollector(self.client)
    
#  ____             
# |  _ \ _ __   ___ 
# | |_) | '_ \ / __|
# |  _ <| |_) | (__ 
# |_| \_\ .__/ \___|
#       |_|         

# The Rpc construction  will look very similar 
from pydevmgr_core import BaseRpc, kjoin, record_class


@record_class
class TestRpc(BaseRpc):
    class Config(BaseRpc.Config):
        type = "Test"
        method_name: str # method_name is mendatory

    def __init__(self, key=None, client=None, prefix="", **kwargs):
        super().__init__(key=key, **kwargs)
        if client is None:
            raise ValueError("Client is missing")
        self.client = client 
        self.prefix = prefix

    @classmethod
    def new_args(cls, parent, config):
        # This method is used when the node is created from a parent object 
        # in our case the parent (a Device or Interface) will need to pass the 
        # client object and the targeted device prefix
        d = super().new_args(parent, config)
        d.update(
            client =  parent.client, 
            prefix =  parent.remote_key 
        )
        return d

    def fcall(self, *args):
        return  self.client.send({'cmd':self.config.method_name, 'prefix':self.prefix, 'args':list(args)})
       


#  ____             _          
# |  _ \  _____   _(_) ___ ___ 
# | | | |/ _ \ \ / / |/ __/ _ \
# | |_| |  __/\ V /| | (_|  __/
# |____/ \___| \_/ |_|\___\___|

# The node and Rpc we have created will make more sens when creating a device

from pydevmgr_core import BaseDevice, record_class
from pydantic import AnyUrl 

@record_class
class TestMotor(BaseDevice):
    class Config(BaseDevice.Config):
        type = "TestMotor"
        prefix: str
        address: AnyUrl = "ws://127.0.0.1:5678"
    
    position = TestNode.prop('position', suffix="POS")
    rpc_move = TestRpc.prop('move', method_name="move")
    rpc_init = TestRpc.prop('init', method_name="init")

   
    def __init__(self, key=None, client=None, **kwargs):
        super().__init__(key=key, **kwargs)
        
        # at the level of a device the client can be built from 
        # the device configuration 
        if client is None:
            client = TestClient(self.config.address)
        
        self.client = client
        self.remote_key = self.config.prefix
    
    def connect(self):
        self.client.connect()
    
    def disconnect(self):
        self.client.disconnect()
    
    def move(self, pos):
        return self.rpc_move.call(pos)
    
    def init(self):
        return self.rpc_init.call()

from pydevmgr_core import BaseDevice, NodeAlias1
class TestMotor2(TestMotor):
    
    @NodeAlias1.prop('position_mm', node="position")
    def position_mm(self, position):
        return position/1000.




from pydevmgr_core import BaseDevice, NodeAlias1, NodeVar, LocalUtcNode, DequeNode1
from pydantic import Field 
from collections import deque 

class TestMotor3(TestMotor):
    class Data(TestMotor.Data):
        position: NodeVar[float] = 0.0
        position_mm: NodeVar[float] = 0.0
        time: NodeVar[str] = Field(  '2000-01-01T00:00:00.000000', node=LocalUtcNode() )

        position_buffer: NodeVar[deque] = Field( deque(), node = DequeNode1.prop( node="position", maxlen=100 ) )

    @NodeAlias1.prop('position_mm', node="position")
    def position_mm(self, position):
        return position/1000.
   


 

class TestDevice(BaseDevice):
    Node = TestNode # default node constructor 
    Rpc = TestRpc # default rpc constructor 
    class Config(BaseDevice.Config):
        type = "Test"
        prefix: str
        address: AnyUrl = "ws://127.0.0.1:5678"
    
    def __init__(self, key=None, client=None, **kwargs):
        super().__init__(key=key, **kwargs)
        
        # at the level of a device the client can be built from 
        # the device configuration 
        if client is None:
            client = TestClient(self.config.address)
        
        self.client = client
        self.remote_key = self.config.prefix
    
    def connect(self):
        self.client.connect()
    
    def disconnect(self):
        self.client.disconnect()


         






if __name__ == "__main__":
    from pydevmgr_core import download

    client  = TestClient( "ws://127.0.0.1:4856" )
    client.connect()
    
    pos1 = TestNode( client=client, suffix="MOTOR1.POS" )
    move1 = TestRpc( client=client, prefix="MOTOR1", method_name="move" )
    init1 = TestRpc( client=client, prefix="MOTOR1", method_name="init" )


    assert pos1.get() == 0.0
    move1.call(5.6)
    assert pos1.get() == 5.6
    init1.call()
    assert pos1.get() == 0.0



    # #########

    motor1 = TestMotor(prefix="MOTOR1")
    motor1.connect()

    motor2 = TestMotor(client=motor1.client, prefix="MOTOR2")

    assert motor1.position.get() == 0.0
    motor1.move(7.8)
    assert motor1.position.get() == 7.8
 
    assert download([motor1.position, motor2.position]) == [7.8, 0.0] 



    device1 = TestDevice(prefix="MOTOR1",
                node_map = {'position': {"suffix":'POS'}},
                rpc_map = {'move' :{'method_name':'move'}, 
                           'init' :{'method_name':'init'}
                    }, 
        
            )
    device1.connect()
    assert device1.position.get() == 0.0
    


    motor1 = TestMotor2(prefix="MOTOR1", address="ws://127.0.0.1:4567")
    motor1.connect()
    motor1.move(10)
    assert motor1.position_mm.get()*1000 == motor1.position.get()
   

    from pydevmgr_core import DataLink 
    
    
    motor1 = TestMotor3(prefix="MOTOR1", address="ws://127.0.0.1:4567")
    motor1.connect()
    motor1.move(10)
    
    data = motor1.Data()
    dl = DataLink(motor1, data)
    dl.download()

    assert data.position == 10.0
    
    motor1.move(20)
    dl.download()
    assert data.position == 20.0
    assert list(data.position_buffer) == [10.0, 20.0] 
    print(data.time)
    print(data.position_buffer)
    

    print("All good !")

    
    

