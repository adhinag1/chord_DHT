# Chord Distributed Hash Table
Create a basic distributed hash table (DHT) with an architecture similar to the Chord system. I used Apache Thrift to communicate between peers.

## Steps to run:

Run the initializer to fill the finger table for all the DHT nodes. Nodes should be stored in a text file and passed as argument to the init script.

Nodes should be stored in this format:
<ip1>:<port1>
<ip2>:<port2>

> chmod +x init (for permission to run the init script)
> ./init <file_name_where_nodes are stored>


1) Run this "./server <port_arg>" script to start the server
2) Run ./init <filename_arg> to populate the finger table to the hosts specified in the file passed as argument.
3) Run the test script(client) to make RPC to the server.
