class Policy:
    def __init__(self, number):
        self.name = ""
        self.name_ext = ""
        self.num = number
        match self.num:
            case 1:
                self.name = "VSP"
                self.name_ext = "Variable-Size Partitioning"
            case 2:
                self.name = "PAG"
                self.name_ext = "Paging"
            case 3:
                self.name = "SEG"
                self.name_ext = "Segmentation"
            case _:
                print("Unknown Policy number")
                exit(1)


class Algorithm:
    def __init__(self, number):
        self.name = ""
        self.num = number

        match self.num:
            case 1:
                self.name = "First Fit"
            case 2:
                self.name = "Best Fit"
            case 3:
                self.name = "Worst Fit"
            case _:
                print("Unknown Algorithm number")
                exit(1)


class Process:
    def __init__(self, file_to_read):
        self.id = int(file_to_read.readline().strip())
        temp = file_to_read.readline().strip().split(' ')
        self.arr_time = int(temp[0])
        self.lifetime = int(temp[1])
        temp = file_to_read.readline().strip().split(' ')
        file_to_read.readline()  # used to get rid of newlines inbetween processes
        self.mem_count = int(temp.pop(0))
        self.mem_pieces = []
        self.total_mem_size = 0
        for j in temp:
            self.mem_pieces.append(int(j))
            self.total_mem_size += int(j)


class MemMap:
    def __init__(self, size):
        self.total_size = 0
        self.max_size = size
        self.next = 0
        self.p_start = []
        self.p_end = []
        self.p_id = []


    def add(self, process):
        self.p_id.append(process.id)
        self.p_start.append(self.next)
        self.next = self.next + process.total_mem_size
        self.p_end.append(self.next - 1)


    def print(self):
        if len(self.p_id) == 0 :
            print((' ' * 7) + 'Memory Map: 0-' + str(self.max_size) + ': Hole')
        else:
            if self.p_start[0] != 0:
                print((' ' * 18) + 'Memory Map: 0-' + str(self.p_start[0]-1) + ': Hole')
            else:
                print((' ' * 18) + 'Memory Map: 0-' + str(self.p_end[0]) + ': Process ' + self.p_id[0])

            for i in range(1, len(self.p_id)):
                if self.p_start

        if self.next != self.max_size:
            print((' ' * 18) + str(self.next) + '-' + str(self.max_size-1) + ': Hole')

class Manager:
    def __init__(self):
        self.v_clock = -1
        self.allocated_mem = 0
        self.mem_size = int(input("Memory size: ").strip())
        self.policy = Policy(int(input("Memory management policy (1 - VSP, 2 - PAG, 3 - SEG): ").strip()))
        if self.policy.name == "VSP" or self.policy.name == "SEG":
            self.alg = Algorithm(int(input("Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ").strip()))
        else:
            self.p_f_size = int(input("Page/Frame size: ").strip())

        self.input_queue = []
        self.in_queue_val = []
        self.mem_map = MemMap(self.mem_size)
        self.spacing = ' ' * 7

    def print_queue(self):
        print('\t Input Queue:' + str(self.in_queue_val))


    def add_process(self, process):
        if process.arr_time != self.v_clock:
            if len(self.input_queue) > 0:
                self.move_to_mem()
            self.v_clock = process.arr_time
            print('t = ' + str(self.v_clock) + ': Process ' + str(process.arr_time) + ' arrives')
        else:
            print(self.spacing + 'Process ' + str(process.arr_time) + ' arrives')

        self.input_queue.append(process)
        self.in_queue_val.append(process.id)
        self.print_queue()

    def move_to_mem(self):
        for p in self.input_queue:
            print(self.spacing + 'MM moves Process ' + p.id + ' to memory')
            self.input_queue.pop(0)
            self.input_queue.pop(0)
            self.print_queue()
            self.mem_map.print()

