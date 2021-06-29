import sys

import tinify
import os


# tinify.key = "j2h729DzSXz5ZfkTJ5Lq4dXZl8dcKSbQ"
total_pic_old_size = 0
total_pic_new_size = 0
API_KEY_CACHE_PATH = "key_cache"


def get_file_size_KB(file):
    file_size = os.path.getsize(file) / 1024.0
    return round(file_size, 2)


def get_file_size_MB(file):
    file_size = os.path.getsize(file) / 1024.0 / 1024.0
    return round(file_size, 2)


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def compress(path):
    global total_pic_old_size
    global total_pic_new_size
    if not os.path.isdir(path):
        file = path
        old_file_size = get_file_size_KB(file)
        old_file_size_str = str(round(old_file_size, 2))

        if is_pic(file):
            print(colored(255, 25, 25,
                          "current file is pic: {0}, size: {1}KB, tinify it...".format(file,
                                                                                       old_file_size_str)))

            source = tinify.from_file(file)
            source.to_file(file)

            total_pic_old_size += old_file_size
            new_file_size = get_file_size_KB(file)
            total_pic_new_size += new_file_size

            new_file_size_str = str(round(new_file_size, 2))
            percent_str = str(round(100 - 100 * new_file_size / old_file_size, 2))

            print(colored(255, 25, 25, "tinify done! now the pic size: {0}KB, shrunk by {1}%".format(
                new_file_size_str, percent_str)))
        else:
            print("current file: {0}, size: {1}KB".format(file, old_file_size_str))
    else:
        for file in os.listdir(path):
            sub_file = os.path.join(path, file)
            compress(sub_file)


def is_pic(file):
    return file.endswith(".jpg") \
           or file.endswith(".jpeg") \
           or file.endswith(".png") \



if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # no API key, try cache
        if not os.path.exists(API_KEY_CACHE_PATH):
            raise Exception("no API key input and no cached key found!")
        else:
            tinify.key = sys.argv[1]
    else:
        key = sys.argv[1]
        tinify.key = key
        with open("/" + API_KEY_CACHE_PATH, 'rw') as f:
            f.write(key)
    print("current path: " + os.path.curdir)
    compress(os.path.curdir)
    if total_pic_old_size == total_pic_new_size:
        print("Done! But no pics were found in the directory.")
    else:
        print("compress done! All pics shrunk from {0}KB({1}MB) to {2}KB({3}MB), shrunk by {4}%.".format(
            round(total_pic_old_size, 2), round(total_pic_old_size / 1024, 2), round(total_pic_new_size, 2),
            round(total_pic_new_size / 1024, 2), str(round(100 - 100 * total_pic_new_size / total_pic_old_size, 2))))

