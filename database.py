import sqlite3
import logging as log

log.basicConfig(filename='')


class UseDB:
    # Status: 0 - Упал, 1 - Живой, 2 - Отключен; 
    # Для AP: 0 - умер, 1,2 - живой, 2 или 1 раз пинг не прошел
    # 3 - живой
    def update_status(self, ip, status):
        self.cur.execute('UPDATE devices SET status=? WHERE ip=?',
                         [status, ip])

    def get_status(self, ip):
        for row in self.cur.execute(f'''SELECT type, status FROM devices 
                                    WHERE ip="{ip}"'''):
            return row

    def get_all(self):
        self.devices_list = []
        for row in self.cur.execute('SELECT * FROM devices'):
            self.devices_list.append(row)
        return self.devices_list
    
    # Type: 0 - UPS, 1 - Сетевое ус-во, 2 - комп
    def get_by_type(self, dev_type):
        self.devices_list = []
        for row in self.cur.execute('SELECT ip FROM devices WHERE type=?',
                                    [dev_type]):
            self.devices_list.append(row)
        return self.devices_list

    def add_device(self, name, ip, dev_type, message=''):
        if dev_type.lower() in ['pc', 'ap', 'ups']:
            dev_type = {'ups': 0,
                        'ap': 1,
                        'pc': 2}[dev_type.lower()]
        elif dev_type not in [0, 1, 2]:
            return 1
        self.cur.execute('''INSERT INTO devices (name, ip, type, message, status)
                        VALUES (?, ?, ?, ?, 0)''', [name, ip, dev_type, message])
        self.con.commit()
        return 0
        

    def __init__(self):
        self.con = sqlite3.connect('devices.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS devices
                         (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                         name TEXT NOT NULL,
                         ip TEXT NOT NULL,
                         type integer NOT NULL,
                         message text,
                         status integer)''')
        self.con.commit()


def test_class():
    UseDB().add_device("test_ap1", "255.255.255.0", 'ap', '')
    return UseDB().get_status("127.0.0.1")
