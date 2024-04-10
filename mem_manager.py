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


# class MemMap:
#     def __init__(self, size):
#         self.total_size = 0
#         self.max_size = size
#         self.next = 0
#         self.p_start = []
#         self.p_end = []
#         self.p_id = []
#         self.a_mem = self.max_size
#         self.fin_times = []
#         self.next_fin_time = 100001
#         self.next_fin_process = -1
#
#     def add(self, process, clock):
#         self.p_id.append(process.id)
#         self.p_start.append(self.next)
#         self.fin_times.append(clock + process.lifetime)
#         if clock + process.lifetime < self.next_fin_time:
#             self.next_fin_time = clock + process.lifetime
#             self.next_fin_process = process.id
#         self.next = self.next + process.total_mem_size
#         self.p_end.append(self.next - 1)
#         self.a_mem -= process.total_mem_size
#         self.organize()
#
#     def process_end(self):
#         idx = self.p_id.index(self.next_fin_process)
#         p_mem_size = self.p_end[idx] - self.p_start[idx] + 1
#         self.a_mem += p_mem_size
#         self.next = self.p_start[idx]
#         self.p_start.pop(idx)
#         self.p_end.pop(idx)
#         self.p_id.pop(idx)
#         self.fin_times.pop(idx)
#         self.next_fin_time = 100001
#         for i in range(0, len(self.fin_times)):
#             if self.fin_times[i] < self.next_fin_time:
#                 self.next_fin_time = self.fin_times[i]
#                 self.next_fin_process = self.p_id[i]
#
#     def print(self):
#         last = 0
#         if len(self.p_id) == 0:
#             print((' ' * 7) + 'Memory Map: 0-' + str(self.max_size) + ': Hole')
#         else:
#             line = (' ' * 7) + 'Memory Map:'
#             for i in range(0, len(self.p_id)):
#                 if self.p_start[i] == last:
#                     line += str(self.p_start[i]) + '-' + str(self.p_end[i]) + ': Process ' + str(self.p_id[i])
#                     last = self.p_end[i] + 1
#                 else:
#                     line += str(last) + '-' + str(self.p_start[i]-1) + ': Hole\n'
#                     line += ((' ' * 18)
#                              + str(self.p_start[i]) + '-' + str(self.p_end[i]) + ': Process ' + str(self.p_id[i]))
#                     last = self.p_end[i] + 1
#                 print(line)
#                 line = (' ' * 18)
#
#         if self.p_end[-1] != self.max_size - 1:
#             print((' ' * 18) + str(self.p_end[-1]) + '-' + str(self.max_size-1) + ': Hole')
#
#     def organize(self):
#         for i in range(len(self.p_id)):
#             swapped = False
#             for j in range(0, len(self.p_id) - i - 1):
#                 if self.p_start[j] > self.p_start[j+1]:
#                     self.p_start[j], self.p_end[j + 1] = self.p_start[j+1], self.p_start[j]
#                     self.p_end[j], self.p_end[j+1] = self.p_end[j+1], self.p_end[j]
#                     self.p_id[j], self.p_id[j+1] = self.p_id[j+1], self.p_id[j]
#                     self.fin_times[j], self.fin_times[j+1] = self.fin_times[j+1], self.fin_times[j]
#                     swapped = True
#                 if not swapped:
#                     break


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
        self.mem = BetterMem(self.mem_size/10)
        self.spacing = ' ' * 8

    def print_queue(self):
        print((' ' * 8) + 'Input Queue:' + str(self.in_queue_val))

    def new_mem_add(self, process):
        if self.policy.name == 'VSP':
            if self.alg.name == 'First Fit':
                self.mem.add_first(process, self.v_clock)
        else:
            print('WIP. please wait for further iterations')
            exit(1)

    def add_process(self, process):
        if process.arr_time != self.v_clock:
            if len(self.input_queue) > 0:
                self.move_to_mem()

            start = '\nt = ' + str(self.v_clock) + ': '
            while process.arr_time > self.mem.next_end[0][0]:
                self.v_clock = self.mem.next_end[0][0]
                print(start + 'Process ' + str(self.mem.next_end[0][1]) + ' completes')
                start = (' ' * 8)
                self.mem.process_end()
                self.mem.print_mem()

            self.v_clock = process.arr_time
            print('\nt = ' + str(self.v_clock) + ': Process ' + str(process.id) + ' arrives')
        else:
            print(self.spacing + 'Process ' + str(process.id) + ' arrives')

        self.input_queue.append(process)
        self.in_queue_val.append(process.id)
        self.print_queue()

    def finish(self):
        if len(self.input_queue) > 0:
            self.move_to_mem()

        start = '\nt = ' + str(self.v_clock) + ': '
        while len(self.mem.next_end) > 0:
            self.v_clock = self.mem.next_end[0][0]
            print(start + 'Process ' + str(self.mem.next_end[0][1]) + ' completes')
            start = (' ' * 8)
            self.mem.process_end()
            self.mem.print_mem()

    def move_to_mem(self):
        max_hole_size = self.mem.max_hole_size()
        while len(self.input_queue) > 0 and self.input_queue[0].total_mem_size <= max_hole_size:
            print(self.spacing + 'MM moves Process ' + str(self.in_queue_val[0]) + ' to memory')
            self.mem.add_first(self.input_queue[0], self.v_clock)
            self.input_queue.pop(0)
            self.in_queue_val.pop(0)
            self.print_queue()
            self.mem.print_mem()


class BetterMem:
    def __init__(self, size):
        self.mem = [0] * int(size)
        self.holes = [[0, size]]
        self.size = size
        self.free = size * 10
        self.next_end = [[100001, -1]]

    def add_first(self, process, clock):
        mem_blk = int(process.total_mem_size/10)
        first_hole = -1
        for i in self.holes:
            if i[1] == mem_blk:
                first_hole = i[0]
                self.holes.remove(i)
                break
            if i[1] > mem_blk:
                first_hole = i[0]
                self.holes.append([i[0] + mem_blk, i[1]-mem_blk])
                self.holes.remove(i)
                break

        if first_hole != -1:
            for i in range(first_hole, first_hole + mem_blk):
                if i < len(self.mem):
                    self.mem[i] = process.id
                    self.free -= 10

            self.next_end.append([clock + process.lifetime, process.id])
            self.next_end.sort()

    def print_mem(self):
        print((' ' * 8) + 'Memory Map:')
        end = 0
        while end != len(self.mem):
            start = end
            while end+1 != len(self.mem) and self.mem[end] == self.mem[end+1]:
                end += 1

            if self.mem[start] == 0:
                print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10) - 1) + ': Hole')
            else:
                print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10)-1) + ': Process ' + str(self.mem[start]))
            end += 1

    def process_end(self):
        end_id = self.next_end[0][1]
        self.next_end.pop(0)
        new_hole = -1
        for i in range(len(self.mem)):
            if self.mem[i] == end_id:
                if new_hole == -1:
                    new_hole = i
                    self.holes.append([i, 0])
                self.mem[i] = 0
                self.holes[-1][1] += 1
                self.free += 10

        self.holes.sort()

    def max_hole_size(self):
        max_size = 0
        for i in self.holes:
            if i[1] > max_size:
                max_size = i[1]

        return max_size * 10
