# PKS_Komunikator
Navrhnite a implementujte program s použitím vlastného protokolu nad protokolom UDP (User Datagram Protocol) transportnej vrstvy sieťového modelu TCP/IP. Program umožní komunikáciu dvoch účastníkov v lokálnej sieti Ethernet, teda prenos textových správ a ľubovoľného súboru medzi počítačmi (uzlami).

## Classes
- [ ] ConnectionManager - Manges connection between two nodes
- [ ] Communication - Piece of communication between two nodes (consists of packets [fragments])
- [ ] Packet - Self explanatory. Headers + Data
- [ ] Data - This is a interface which will provide a unified methods for encrypting data
- [ ] File (Data) - Data type
- [ ] Message (Data) - Data type
- [ ] Receiver - Mode of the communicator
- [ ] Sender - Mode of the communicator
- [ ] ThreadManager - Manages multiple threads. (One for establishing and keeping connection alive. One for 
  communication between endpoints. )
- [ ] Assembler - Handles data packet encryption and data packet decryption.
- [ ] Menu - Menu for sender mode
- [ ] Flags (enum) - Communication packet flags
- [ ] Constants - Contains constant values of the program
- [ ] Settings - Contains settings of communicator session