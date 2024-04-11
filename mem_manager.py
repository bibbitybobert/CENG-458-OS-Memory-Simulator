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
        self.v_clock = -1
        self.allocated_mem = 0
        self.alg = None
        self.p_f_size = 0
        self.mem_size = int(input("Memory size: ").strip())
        self.policy = Policy(int(input("Memory management policy (1 - VSP, 2 - PAG, 3 - SEG): ").strip()))
        if self.policy.name == "VSP" or self.policy.name == "SEG":
            self.alg = Algorithm(int(input("Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ").strip()))
        else:
            self.p_f_size = int(input("Page/Frame size: ").strip())

        self.input_queue = []
        self.in_queue_val = []
        self.turnarounds = []
        self.mem = BetterMem(self.mem_size/10)
        self.spacing = ' ' * 8

    def print_queue(self):
        print((' ' * 8) + 'Input Queue:' + str(self.in_queue_val).replace(',', ''))

    def add_process(self, process):
        if process.arr_time != self.v_clock:
            if len(self.input_queue) > 0:
                self.move_to_mem()

            first = True
            start = (' ' * 8)
            while process.arr_time > self.mem.next_end[0][0]:
                self.v_clock = self.mem.next_end[0][0]
                if first:
                    start = '        \nt = ' + str(self.v_clock) + ': '
                    first = False
                print(start + 'Process ' + str(self.mem.next_end[0][1]) + ' completes')
                start = (' ' * 8)
                self.mem.process_end()
                if self.policy.name == "PAG":
                    self.mem.print_mem_paging()
                else:
                    self.mem.print_mem()

            if len(self.input_queue) > 0:
                self.move_to_mem()

            self.v_clock = process.arr_time
            print('        ')
            print('t = ' + str(self.v_clock) + ': Process ' + str(process.id) + ' arrives')
        else:
            print(self.spacing + 'Process ' + str(process.id) + ' arrives')

        self.input_queue.append(process)
        self.in_queue_val.append(process.id)
        self.print_queue()

    def finish(self):
        while self.mem.free != self.mem_size:
            start = '        \nt = ' + str(self.v_clock) + ': '
            while len(self.mem.next_end) > 0 and self.mem.next_end[0][0] == self.v_clock:
                self.v_clock = self.mem.next_end[0][0]
                print(start + 'Process ' + str(self.mem.next_end[0][1]) + ' completes')
                start = (' ' * 8)
                self.mem.process_end()
                if self.policy.name == "PAG":
                    self.mem.print_mem_paging()
                else:
                    self.mem.print_mem()
            else:
                for i in self.input_queue:
                    if i.total_mem_size <= self.mem.max_hole_size():
                        self.move_to_mem()

            if not self.mem.next_end[0][1] == -1:
                self.v_clock = self.mem.next_end[0][0]
            else:
                break

    def move_to_mem(self):
        max_hole_size = self.mem.max_hole_size()
        change = False
        while len(self.input_queue) > 0:
            change = False
            i = 0
            while len(self.input_queue) > i >= 0:
                mem_move = False
                if self.policy.name == "VSP":
                    if self.input_queue[i].total_mem_size <= max_hole_size:
                        print(self.spacing + 'MM moves Process ' + str(self.input_queue[i].id) + ' to memory')
                        self.turnarounds.append(self.mem.add_vsp(self.input_queue[i], self.v_clock, self.alg.name))
                        mem_move = True
                elif self.policy.name == "SEG":
                    if self.input_queue[i].total_mem_size <= self.mem.free:
                        print(self.spacing + 'MM moves Process ' + str(self.input_queue[i].id) + ' to memory')
                        self.turnarounds.append(self.mem.add_seg(self.input_queue[i], self.v_clock, self.alg.name))
                        mem_move = True
                elif self.policy.name == 'PAG': #paging
                    if self.input_queue[i].total_mem_size <= self.mem.free:
                        print(self.spacing + 'MM moves Process ' + str(self.input_queue[i].id) + ' to memory')
                        self.turnarounds.append(self.mem.add_paging(self.input_queue[i], self.v_clock, self.p_f_size))
                        mem_move = True

                if mem_move:
                    self.in_queue_val.remove(self.input_queue[i].id)
                    self.input_queue.remove(self.input_queue[i])
                    self.print_queue()
                    if self.policy.name == "PAG":
                        self.mem.print_mem_paging()
                    else:
                        self.mem.print_mem()
                    i = 0
                    change = True
                else:
                    i += 1
            if not change:
                break


class BetterMem:
    def __init__(self, size):
        self.mem = [[0,-1]] * int(size)
        self.holes = [[0, size]]
        self.size = size
        self.free = size * 10
        self.next_end = [[100001, -1]]

    def add_vsp(self, process, clock, alg_name):
        mem_blk = int(process.total_mem_size/10)
        first_hole = self.find_hole(alg_name, mem_blk)
        if first_hole != -1:
            for i in range(first_hole, first_hole + mem_blk):
                if i < len(self.mem):
                    self.mem[i] = [process.id, -1]
                    self.free -= 10

        self.next_end.append([clock + process.lifetime, process.id])
        self.next_end.sort()

        return (clock+process.lifetime) - process.arr_time

    def add_seg(self, process, clock, alg_name):
        for j in range(process.mem_count):
            mem_blk = int(process.mem_pieces[j]/10)
            first_hole = self.find_hole(alg_name, mem_blk)
            if first_hole != -1:
                for i in range(first_hole, first_hole + mem_blk):
                    if i < len(self.mem):
                        self.mem[i] = [process.id, j]
                        self.free -= 10

        self.next_end.append([clock + process.lifetime, process.id])
        self.next_end.sort()
        return (clock + process.lifetime) - process.arr_time

    def add_paging(self, process, clock, pg_size):
        while process.total_mem_size % pg_size != 0:
            process.total_mem_size += 10
        for j in range(int(process.total_mem_size / pg_size)):
            first_hole = self.find_hole("First Fit", int(pg_size/10))
            if first_hole != -1:
                for i in range(first_hole, first_hole + int(pg_size/10)):
                    if i < len(self.mem):
                        self.mem[i] = [process.id, j + 1]
                        self.free -= 10

        self.next_end.append([clock + process.lifetime, process.id])
        self.next_end.sort()

        return (clock + process.lifetime) - process.arr_time

    def find_hole(self, alg, mem_blk):
        hole_idx = -1
        if alg == 'First Fit':
            for i in self.holes:
                if i[1] == mem_blk:
                    first_hole = i[0]
                    self.holes.remove(i)
                    return first_hole
                if i[1] > mem_blk:
                    first_hole = i[0]
                    self.holes.append([i[0] + mem_blk, i[1] - mem_blk])
                    self.holes.sort()
                    self.holes.remove(i)
                    return first_hole

        elif alg == 'Best Fit':
            best_hole = [-1, 100001]
            for i in self.holes:
                if i[1] == mem_blk:
                    best_hole = i
                    self.holes.remove(i)
                    return best_hole[0]
                elif mem_blk < i[1] < best_hole[1]:
                    best_hole = i

            self.holes.append([best_hole[0] + mem_blk, best_hole[1] - mem_blk])
            self.holes.sort()
            self.holes.remove(best_hole)
            return best_hole[0]

        elif alg == 'Worst Fit':
            worst_hole = [-1, 0]
            for i in self.holes:
                if i[1] >= mem_blk and i[1] > worst_hole[1]:
                    worst_hole = i

            self.holes.append([worst_hole[0] + mem_blk, worst_hole[1] - mem_blk])
            self.holes.sort()
            self.holes.remove(worst_hole)
            return worst_hole[0]
        else:
            print('unknown alg quitting')
            exit(-1)

    def print_mem(self):
        print((' ' * 8) + 'Memory Map: ')
        end = 0
        while end != len(self.mem):
            start = end
            while end+1 != len(self.mem) and self.mem[end][0] == self.mem[end+1][0] and self.mem[end][1] == self.mem[end+1][1]:
                end += 1

            if self.mem[start][0] == 0:
                print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10) - 1) + ': Hole')
            else:
                if self.mem[start][1] != -1:
                    print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10)-1) +
                          ': Process ' + str(self.mem[start][0]) + ', Segment ' + str(self.mem[start][1]))
                else:
                    print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10) - 1) +
                          ': Process ' + str(self.mem[start][0]))
            end += 1

    def print_mem_paging(self):
        print((' ' * 8) + 'Memory Map: ')
        end = 0
        while end != len(self.mem):
            start = end
            while end + 1 != len(self.mem) and self.mem[end][0] == self.mem[end + 1][0] and self.mem[end][1] == \
                    self.mem[end + 1][1]:
                end += 1

            if self.mem[start][0] == 0:
                print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10) - 1) + ': Free Frame(s)')
            else:
                print((' ' * 16) + str(start * 10) + '-' + str(((end + 1) * 10) - 1) +
                      ': Process ' + str(self.mem[start][0]) + ', Page ' + str(self.mem[start][1]))
            end += 1

    def process_end(self):
        end_id = self.next_end[0][1]
        self.next_end.pop(0)
        new_hole = -1
        for i in range(len(self.mem)):
            if self.mem[i][0] == end_id:
                if new_hole == -1:
                    new_hole = i
                    self.holes.append([i, 0])
                self.mem[i] = [0, -1]
                self.holes[-1][1] += 1
                self.free += 10
            elif new_hole != -1:
                self.holes.sort()
                self.consolidate_holes()
                new_hole = -1

        self.holes.sort()
        self.consolidate_holes()

    def max_hole_size(self):
        max_size = 0
        for i in self.holes:
            if i[1] > max_size:
                max_size = i[1]

        return max_size * 10

    def consolidate_holes(self):
        changed = True
        while changed:
            changed = False
            for i in range(len(self.holes) - 1):
                if i == len(self.holes) - 1:
                    break
                if self.holes[i][0] + self.holes[i][1] == self.holes[i+1][0]:
                    changed = True
                    self.holes.append([self.holes[i][0], self.holes[i][1] + self.holes[i+1][1]])
                    self.holes.pop(i+1)
                    self.holes.pop(i)
                    self.holes.sort()
