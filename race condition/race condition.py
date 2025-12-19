import threading
import time

value = 0
lock = threading.Lock()

def worker(use_lock):
    global value
    for _ in range(5):
        if use_lock:
            with lock:
                current = value
                time.sleep(0.001)
                value = current + 1
        else:
            current = value
            time.sleep(0.001)
            value = current + 1

threads = [threading.Thread(target=worker, args=(use_lock,)) for use_lock in [True, False] * 2]

for t in threads: t.start()
for t in threads: t.join()

print(f"Ожидалось: 20, Получилось: {value}, Потеряно: {20 - value}")


### КОД С ЗАЩИТОЙ ЧЕРЕЗ БАЗУ ДАННЫХ, МАКСИМАЛЬНАЯ ЗАЩИТА ###


import threading, sqlite3, time

conn = sqlite3.connect(':memory:', check_same_thread=False, isolation_level='EXCLUSIVE')
conn.execute('CREATE TABLE cards (id INTEGER PRIMARY KEY, balance INTEGER)')
conn.execute('INSERT INTO cards VALUES (1, 100)')
conn.commit()

def worker():
    for _ in range(5):
        with sqlite3.connect(':memory:', check_same_thread=False) as local_conn:
            local_conn.execute('CREATE TABLE IF NOT EXISTS cards (id INTEGER PRIMARY KEY, balance INTEGER)')
            cursor = local_conn.execute('SELECT balance FROM cards WHERE id=1')
            balance = cursor.fetchone()[0]
            time.sleep(0.01)
            local_conn.execute('UPDATE cards SET balance=? WHERE id=1', (balance + 10,))
            local_conn.commit()

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

final = conn.execute('SELECT balance FROM cards WHERE id=1').fetchone()[0]
print(f"Ожидалось: 300, Получилось: {final}, Потеряно: {300 - final}")

