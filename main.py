import mem_policies as mp
from mem_manager import Manager, Process


def run_menu():
    mem = Manager()
    file = open_file(input("Workload File to use: "))

    process_num = int(file.readline().strip())
    for i in range(0, process_num):
        process = Process(file)
        mem.add_process(process)

    while len(mem.input_queue) > 0:
        mem.finish()


def open_file(file_name):
    file = open(file_name)
    if file.closed:
        print("Error opening file: " + file_name)
        exit(1)

    return file


if __name__ == '__main__':
    run_menu()

