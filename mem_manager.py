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


class Manager:
    def __init__(self):
        self.v_clock = 0
        self.allocated_mem = 0
        self.mem_size = int(input("Memory size: ").strip())
        self.policy = Policy(int(input("Memory management policy (1 - VSP, 2 - PAG, 3 - SEG): ").strip()))
        if self.policy.name == "VSP" or self.policy.name == "SEG":
            self.alg = Algorithm(int(input("Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ").strip()))
        else:
            self.p_f_size = int(input("Page/Frame size: ").strip())

        self.input_queue = []
        self.mem_map = ''

    


