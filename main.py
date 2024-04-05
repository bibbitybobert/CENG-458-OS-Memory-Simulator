import mem_policies as mp
from mem_manager import Manager, Process


def run_menu():
    mem = Manager()
    file = open_file(input("Workload File to use: "))

    process_num = int(file.readline().strip())
    for i in range(0, process_num):
        process = Process(file)
        mem.input_queue.append(process)

    run_mem_mod(mem)


def open_file(file_name):
    file = open(file_name)
    if file.closed:
        print("Error opening file: " + file_name)
        exit(1)

    return file


def run_mem_mod(mm):




if __name__ == '__main__':
    run_menu()

