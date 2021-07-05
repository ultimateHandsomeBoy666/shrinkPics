import concurrent.futures
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import tinify
import os


# tinify.key = "j2h729DzSXz5ZfkTJ5Lq4dXZl8dcKSbQ"
total_pic_old_size = 0
total_pic_new_size = 0
total_pic_num = 0

# all thread pool tasks futures
futures = []

# tinypng API key cache file
API_KEY_CACHE_PATH = "key_cache.txt"

# indicate weather the program running into error
error = False


def create_thread_pool():
    core_num = get_cpu_core_num()
    pool = ThreadPoolExecutor(max_workers=core_num, thread_name_prefix="thread_for_tiny")
    return pool


def get_cpu_core_num():
    return os.cpu_count()


def get_file_size_KB(file):
    file_size = os.path.getsize(file) / 1024.0
    return round(file_size, 2)


def get_file_size_MB(file):
    file_size = os.path.getsize(file) / 1024.0 / 1024.0
    return round(file_size, 2)


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def compress(path, thread_pool):
    global total_pic_old_size
    global total_pic_new_size
    global total_pic_num
    global futures

    if not os.path.isdir(path):
        file = path

        old_file_size = get_file_size_KB(file)
        old_file_size_str = str(round(old_file_size, 2))

        total_pic_old_size += old_file_size

        if is_pic(file):
            total_pic_num += 1

            future = thread_pool.submit(tiny_task, file, old_file_size)
            futures.append(future)
            future.add_done_callback(tiny_task_result_callback)
        else:
            print("current file: {0}, size: {1}KB".format(file, old_file_size_str))
    else:
        for file in os.listdir(path):
            sub_file = os.path.join(path, file)
            compress(sub_file, thread_pool)


def is_pic(file):
    return file.endswith(".jpg") \
           or file.endswith(".jpeg") \
           or file.endswith(".png")


def tiny_task(file, old_file_size):
    print(colored(25, 255, 25,
                  "\ncurrent file is pic: {0}, size: {1}KB, tinify it...".format(file, str(round(old_file_size, 2)))))
    print(colored(25, 255, 25,
                  "current tiny thread is {0}".format(threading.current_thread().name)))
    try:
        source = tinify.from_file(file)
        source.to_file(file)
        return get_file_size_KB(file), old_file_size, file
    except tinify.AccountError:
        global error
        error = True
        print(colored(255, 25, 25, "\nyour API key is invalid! try a new one!"))


def tiny_task_result_callback(future):
    global total_pic_old_size
    global total_pic_new_size

    result = future.result()
    if result is None:
        return

    new_file_size = result[0]
    old_file_size = result[1]
    file = result[2]

    total_pic_new_size += new_file_size

    new_file_size_str = str(round(new_file_size, 2))
    percent_str = str(round(100 - 100 * new_file_size / old_file_size, 2))

    print(colored(25, 255, 25, "file {0} tinify done! now the pic size: {1}KB, shrunk by {2}%".format(
        file, new_file_size_str, percent_str)))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        # no API key, try cache
        if not os.path.exists(API_KEY_CACHE_PATH):
            raise Exception("no API key input and no cached key found!")
        else:
            with open("./" + API_KEY_CACHE_PATH, 'r') as f:
                key = f.read()
                print("find cached API key: {0}".format(key))
                tinify.key = key
    else:
        key = sys.argv[1]
        tinify.key = key
        with open("./" + API_KEY_CACHE_PATH, 'w+') as f:
            f.write(key)

    print("current path: " + os.path.curdir)

    thread_pool = create_thread_pool()
    compress(os.path.curdir, thread_pool)

    # wait until all tasks done
    concurrent.futures.wait(futures)

    if error:
        print(colored(255, 25, 25, "\nError occurred, please check if you run this program properly."))
    elif total_pic_num == 0:
        print("\nDone! But no pics were found in the directory.")
    else:
        print(colored(255, 198, 35,
                      "\nCompress done! All pics shrunk from {0}KB({1}MB) to {2}KB({3}MB), shrunk by {4}%.".format(
                          round(total_pic_old_size, 2),
                          round(total_pic_old_size / 1024, 2), round(total_pic_new_size, 2),
                          round(total_pic_new_size / 1024, 2),
                          str(round(100 - 100 * total_pic_new_size / total_pic_old_size, 2)))))



