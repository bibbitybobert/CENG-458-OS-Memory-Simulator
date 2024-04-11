SDSMT CSC 458 Project 2: Memory Simulator

This program is a simple memory simulator that can organize memory in 7 different ways:
1. continuous with a first fit algorithm
2. continuous with a best fit algorithm
3. continuous with a worst fit algorithm
4. segmented with a first fit algorithm
5. segmented with a best fit algorithm
6. segmented with a worst fit algorithm
7. paged memory

The way this program goes about this is by reading in a text file with each process to be put into memory set out like:
<process id>
<start time> <process lifetime>
<number of segments> <segment size> * n

when reading in the file, it will automatically convert the in data into a Process class that will be fed to the
Memory Manager class. The memory manager class, upon recieving a new process will first make sure that all processes
in the input queue are in memory if they can be. After making sure that all processes are in memory according to
the Policy set by the user and the algorithm selected, the memory manager will then make sure that there were no
processes that ended their lifetime in between the arrival of the last process and the arrival of the new process.
If there were processes that ended their lifetime, the memory manager will let the memory class remove these processes
from memory, freeing up space for new processes. After all of this has been done, finally the memory manager class will
add a new process to the queue (really a list as they don't need to be unqueued) of processes waiting to be put into
memory. Once the new process has been put into the queue, the program reads the next process details from the input
file. If there is no more processes to be read in, the program will go to the next important time, which will be the
first process to end its lifespan. The program will keep running until all processes have ended and the maximum memory
in the memory class is equal to the total free memory.

HOW TO RUN
Since this is a python project, in order to run it you just need to be in the Memory_Simulator directory (where this
readme is) and in the terminal execute the command:

python3 main.py

this wil prompt you with the memory size you would like the simulator to have, the memory management policy, the
algorithm for VSP/SEG or page size for PAG, and finally will ask for the input file.

This program should work with no additional libraries other than the ones included in Python 3.11