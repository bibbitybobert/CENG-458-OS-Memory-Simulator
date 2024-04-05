
def get_file():
    fileName = input("File name: ")
    file = open(fileName, 'r')
    if file.closed:
        print("ERROR opening file")
        exit(1)

    return file

def contiguous(mem_size):
    alg = input('Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ')
    if alg != '1' or alg != '2' or alg != '3':
        print('Invalid algorithm option, please select 1-3')
        exit(1)

    file = get_file()

    print("This is VSP")


def paging(mem_size):
    pg_size = input('Page/Frame size: ')
    print('this is paging')


def segmentation(mem_size):
    alg = input('Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ')
    if alg != '1' or alg != '2' or alg != '3':
        print('Invalid algorithm option, please select 1-3')
        exit(1)

    print('this is segmentation')
