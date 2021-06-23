import tinify
import os


tinify.key = "j2h729DzSXz5ZfkTJ5Lq4dXZl8dcKSbQ"


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def compress(path):
    if not os.path.isdir(path):
        return
    for file in os.listdir(path):
        sub_file = os.path.join(path, file)
        if os.path.isdir(file):
            compress(sub_file)
        else:
            print("current file: " + sub_file)
            if is_pic(file):
                print(colored(255, 25, 25, "last file is pic, tinify it..."))
                source = tinify.from_file(sub_file)
                source.to_file(sub_file)
                print(colored(255, 25, 25, "last file is pic, tinify done!"))


def is_pic(file):
    return file.endswith(".jpg") \
           or file.endswith(".jpeg") \
           or file.endswith(".png") \



if __name__ == '__main__':
    print("current path: " + os.path.curdir)
    compress(os.path.curdir)
