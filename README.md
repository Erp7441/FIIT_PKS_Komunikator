# PKS_Komunikator
Navrhnite a implementujte program s použitím vlastného protokolu nad protokolom UDP (User Datagram Protocol) transportnej vrstvy sieťového modelu TCP/IP. Program umožní komunikáciu dvoch účastníkov v lokálnej sieti Ethernet, teda prenos textových správ a ľubovoľného súboru medzi počítačmi (uzlami).

## Classes
- [ ] ConnectionManager - Manges connection between two nodes
- [ ] Communication - Piece of communication between two nodes (consists of packets [fragments])
- [x] Packet - Self explanatory. Headers + Data
- [x] Data - This is a interface which will provide a unified methods for encrypting data
- [x] File (Data) - Data type
- [x] Message (Data) - Data type
- [ ] Receiver - Mode of the communicator
- [ ] Sender - Mode of the communicator
- [ ] ThreadManager - Manages multiple threads. (One for establishing and keeping connection alive. One for 
  communication between endpoints. )
- [ ] Assembler - Handles data packet encryption and data packet decryption.
- [ ] Menu - Menu for sender mode
- [ ] Flags - Communication packet flags
- [ ] Constants - Contains constant values of the program. (Doesn't have to be a class)
- [ ] Settings - Contains settings of communicator session
- [ ] Tests - Functions for testing purposes

## Optimal project structure

- connection
  - Communication.py
  - ConnectionManager.py
- data
  - Assembler.py
  - Data.py
  - File.py
  - Message.py
- modes
  - Receiver.py
  - Sender.py
- packet
  - Flags.py
  - Packet.py
- utils
  - Constants.py
  - Menu.py
  - Settings.py
  - Tests.py
  - ThreadManager.py
- main.py