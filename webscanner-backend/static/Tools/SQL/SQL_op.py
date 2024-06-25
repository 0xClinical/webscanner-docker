import psycopg2
import re
import os
import hashlib

class SQL:
    def __init__(self):
        self.conn = self.__connectSQL__()
        self.cursor = self.conn.cursor()

    def __connectSQL__(self):
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'damn'),
                password=os.getenv('DB_PASSWORD', '123000123'),
                database=os.getenv('DB_NAME', 'scanner')
            )
            print("Connected to the database successfully.")
            return conn
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("Connection attempt finished.")

    def init_db(self):
        try:
            create_table_vul = '''
                CREATE TABLE IF NOT EXISTS url_scanner (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL,
                    type TEXT NOT NULL
                );
                '''
            self.cursor.execute(create_table_vul)
            
            create_table_users = '''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password CHAR(32) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                '''
            self.cursor.execute(create_table_users)
            self.conn.commit()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def insert_user(self, email, password, role='user'):
        try:
            insert_query = '''
                INSERT INTO users (email, password, role)
                VALUES (%s, MD5(%s), %s)
            '''
            self.cursor.execute(insert_query, (email, password, role))
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def get_user(self, user_id):
        try:
            select_query = "SELECT id, email, role, created_at FROM users WHERE id = %s"
            self.cursor.execute(select_query, (user_id,))
            user = self.cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def update_user(self, user_id, email=None, password=None, role=None):
        try:
            fields = []
            values = []
            if email:
                fields.append("email = %s")
                values.append(email)
            if password:
                fields.append("password = MD5(%s)")
                values.append(password)
            if role:
                fields.append("role = %s")
                values.append(role)
            
            if fields:
                update_query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
                values.append(user_id)
                self.cursor.execute(update_query, tuple(values))
                self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def delete_user(self, user_id):
        try:
            delete_query = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(delete_query, (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()
    def user_exists(self, email):
        try:
            query = "SELECT 1 FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def login_user(self, email, password):
        try:
            query = '''
                SELECT id, email, role, created_at, password FROM users WHERE email = %s
            '''
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            if result:
                user_id, email, role, created_at, stored_password = result
                if stored_password == hashlib.md5(password.encode()).hexdigest():
                    return {"id": user_id, "email": email, "role": role, "created_at": created_at}
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.closeSQL()

    def insertSQL(self, data_list):
        try:
            insert_query = "INSERT INTO url_scanner (url, type) VALUES (%s, %s)"
            self.cursor.execute(insert_query, tuple(data_list))
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def selectSQL(self):
        try:
            select_query = "SELECT url, type FROM url_scanner"
            self.cursor.execute(select_query)
            results = self.cursor.fetchall()
            list_url = []
            counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # 暴力破解
            bf = ['暴力破解']
            # 文件包含漏洞
            include = ['文件包含漏洞']
            # 目录遍历漏洞
            dum = ['目录遍历漏洞']
            # 文件上传和下载漏洞
            file = ['文件上传和下载漏洞']
            # SQL time blinds vulnerability
            time_blinds = ['SQL time blinds vulnerability']
            # SQL bool blinds vulnerability
            bool_blinds = ['SQL bool blinds vulnerability']
            # SQL inject vulnerability
            SQL_inject = ['SQL inject vulnerability']
            # CSRF漏洞
            CSRF = ['CSRF漏洞']
            # PHP反序列化漏洞
            PHP = ['PHP反序列化漏洞']
            # XSS Href
            Href = ['XSS Href']
            # XSS POST Reflected
            XSS_POST = ['XSS POST Reflected']
            # XSS GET Reflected
            XSS_GET = ['XSS GET Reflected']
            # XSS Stored
            XSS_Stored = ['XSS Stored']
            # XSS JavaScript
            XSS_JavaScript = ['XSS JavaScript']
            # XSS DOM
            XSS_DOM = ['XSS DOM']
            for ret in results:
                pattern1 = r'暴力破解漏洞'
                if re.search(pattern1, ret[1]) is not None:
                    counter[0] += 1
                    bf.append(ret[0])

                pattern2 = r'文件包含漏洞'
                if re.search(pattern2, ret[1]) is not None:
                    counter[1] += 1
                    include.append(ret[0])

                pattern3 = r'目录遍历漏洞'
                if re.search(pattern3, ret[1]) is not None:
                    counter[2] += 1
                    dum.append(ret[0])

                pattern4 = r'文件上传和下载漏洞'
                if re.search(pattern4, ret[1]) is not None:
                    counter[3] += 1
                    file.append(ret[0])

                pattern5 = r'SQL time blinds vulnerability'
                if re.search(pattern5, ret[1]) is not None:
                    counter[4] += 1
                    time_blinds.append(ret[0])

                pattern6 = r'SQL bool blinds  vulnerability'
                if re.search(pattern6, ret[1]) is not None:
                    counter[5] += 1
                    bool_blinds.append(ret[0])

                pattern7 = r'SQL inject vulnerability'
                if re.search(pattern7, ret[1]) is not None:
                    counter[6] += 1
                    SQL_inject.append(ret[0])

                pattern8 = r'CSRF漏洞'
                if re.search(pattern8, ret[1]) is not None:
                    counter[7] += 1
                    CSRF.append(ret[0])

                pattern9 = r'PHP反序列化漏洞'
                if re.search(pattern9, ret[1]) is not None:
                    counter[8] += 1
                    PHP.append(ret[0])

                pattern10 = r'XSS Href'
                if re.search(pattern10, ret[1]) is not None:
                    counter[9] += 1
                    Href.append(ret[0])

                pattern11 = r'XSS POST Reflected'
                if re.search(pattern11, ret[1]) is not None:
                    counter[10] += 1
                    XSS_POST.append(ret[0])

                pattern12 = r'XSS GET Reflected'
                if re.search(pattern12, ret[1]) is not None:
                    counter[11] += 1
                    XSS_GET.append(ret[0])

                pattern13 = r'XSS Stored'
                if re.search(pattern13, ret[1]) is not None:
                    counter[12] += 1
                    XSS_Stored.append(ret[0])

                pattern14 = r'XSS JavaScript'
                if re.search(pattern14, ret[1]) is not None:
                    counter[13] += 1
                    XSS_JavaScript.append(ret[0])

                pattern15 = r'XSS DOM'
                if re.search(pattern15, ret[1]) is not None:
                    counter[14] += 1
                    XSS_DOM.append(ret[0])

            list_url.append(counter)
            list_url.append(bf)
            list_url.append(include)
            list_url.append(dum)
            list_url.append(file)
            list_url.append(time_blinds)
            list_url.append(bool_blinds)
            list_url.append(SQL_inject)
            list_url.append(CSRF)
            list_url.append(PHP)
            list_url.append(Href)
            list_url.append(XSS_POST)
            list_url.append(XSS_GET)
            list_url.append(XSS_Stored)
            list_url.append(XSS_JavaScript)
            list_url.append(XSS_DOM)

            return list_url
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def deleteSQL(self):
        try:
            truncate_query = "TRUNCATE TABLE url_scanner"
            self.cursor.execute(truncate_query)
            self.conn.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.closeSQL()

    def closeSQL(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
