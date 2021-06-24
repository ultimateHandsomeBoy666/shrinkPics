import tinify
import os


tinify.key = "j2h729DzSXz5ZfkTJ5Lq4dXZl8dcKSbQ"
total_old_size = 0
total_new_size = 0


def get_file_size_KB(file):
    file_size = os.path.getsize(file) / 1024.0
    return round(file_size, 2)


def get_file_size_MB(file):
    file_size = os.path.getsize(file) / 1024.0 / 1024.0
    return round(file_size, 2)


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
            old_file_size = get_file_size_KB(sub_file)
            total_old_size += old_file_size
            if is_pic(sub_file):
                print(colored(255, 25, 25,
                              "current file: {0} is pic, size: {1}, tinify it...".format(sub_file, str(old_file_size))))

                source = tinify.from_file(sub_file)
                source.to_file(sub_file)

                new_file_size = get_file_size_KB(sub_file)
                total_new_size += new_file_size

                print(colored(255, 25, 25, "tinify done! now the pic size: {0}, shrunk by {1}%".format(
                    str(new_file_size), str(100 - 100 * new_file_size / old_file_size))))
            else:
                total_new_size += old_file_size
                print("current file: {0} is pic, size: {1}".format(sub_file, str(old_file_size)))


def is_pic(file):
    return file.endswith(".jpg") \
           or file.endswith(".jpeg") \
           or file.endswith(".png") \



if __name__ == '__main__':
    print("current path: " + os.path.curdir)
    compress(os.path.curdir)
    if total_new_size == total_old_size:
        print("compress done! But no pics were found in the directory.")
    else:
        print("compress done! All pics shrunk from {0}KB({1}MB) to {2}KB({3}MB), shrunk by {4}%.".format(
            total_old_size, total_old_size / 1024, total_new_size, total_new_size / 1024,
            str(100 - 100 * total_new_size / total_old_size)))

