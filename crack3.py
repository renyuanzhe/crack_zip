
"""
创建多个进程，将密码本划分成不同段，并行尝试
我们使用multiprocessing.Process来创建进程，而不是concurrent.futures.ProcessPoolExecutor。这样，我们就可以在进程之间共享multiprocessing.Value对象了。
"""

import multiprocessing
import os
import zipfile

def read_file_segment(file_path, start, end):
    with open(file_path, 'r') as f:
        f.seek(start)
        while f.tell() < end:
            line = f.readline()
            yield line.strip()

def extract_file(zip_file_path, file_path, start, end, password_found):
    password_generator = read_file_segment(file_path, start, end)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for password in password_generator:
            if password_found.value:
                return
            try:
                zip_file.extractall(pwd=bytes(password, 'utf-8'))
                print('Found password: ', password)
                password_found.value = True
                return
            except:
                pass

def main():
    password_found = multiprocessing.Value('b', False)

    file_path = 'passwords.txt'
    zip_file_path = './john.zip'
    num_workers=4
    file_size = os.path.getsize(file_path)
    segment_size = file_size // num_workers  # Assume 4 processes

    processes = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=extract_file, args=(zip_file_path, file_path, i * segment_size, (i + 1) * segment_size, password_found))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()