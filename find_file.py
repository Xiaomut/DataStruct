import glob


def find_file(name):
    files = glob.glob('Leetcode/*/*/*')
    print(files)
    for file in files:
        if name in file:
            print(file)
        else:
            continue


if __name__ == "__main__":
    find_file('aaaaa')