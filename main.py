import sys

from readerselecter import reader_selector


def main(directory: str):
    reader_selector(directory)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main("C:/Users/david.watson/Documents/Clients/ARAG/2022/Lareau")



# ToDo create a command line executable file
# ToDo create a make command to run the script
