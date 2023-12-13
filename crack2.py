import multiprocessing
import zipfile

"""
用一个主进程，每次读取密码本中的一行，而不是全部读取，并创建多个进程来尝试密码
"""
def worker(zip_file_path, password_queue):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        while True:
            password = password_queue.get()
            if password is None:
                break
            try:
                zip_file.extractall(pwd=bytes(password, 'utf-8'))
                print('Found password: ', password)
                break
            except:
                pass

def main():
    zip_file_path = './john.zip'
    password_file_path = 'passwords.txt'
    num_workers = 4

    password_queue = multiprocessing.Queue()



    workers = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(zip_file_path, password_queue))
        p.start()
        workers.append(p)

    with open(password_file_path, 'r') as f:
        for line in f:
            password = line.strip()
            password_queue.put(password)

    for _ in range(num_workers):#None被用作一个信号，告诉工作进程没有更多的密码需要尝试了。每个工作进程在从队列中取出一个密码并尝试使用它后，都会检查取出的密码是否为None。如果是，那么它知道所有的密码都已经尝试过，所以它可以退出。
        password_queue.put(None)

    for p in workers:
        p.join()

if __name__ == '__main__':
    main()