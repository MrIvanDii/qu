import sqlite3


class GeoDataManager:

    def __init__(self):
        pass

    def add_data_into_db(self, ip, port, format_, country, work_status, using_status):
        conn = sqlite3.connect('/Users/martinanikola/PycharmProjects/PropshtScrapping_V2/Proxy/proxies.db')
        cur = conn.cursor()

        try:
            cur.execute('''
                    INSERT INTO proxy_servers (ip, port, format, country, work_status, using_status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (ip, port, format_, country, work_status, using_status))

            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Proxy with IP {ip} and port {port} already exists in the database.")

        conn.close()
