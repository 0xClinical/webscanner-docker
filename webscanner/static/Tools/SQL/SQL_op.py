import psycopg2
import re


class SQL:
    def __init__(self):
        self.conn = self.__connectSQL__()
        self.cursor = self.conn.cursor()

    def __connectSQL__(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                user="damn",
                password="123000123",  # 替换为你的PostgreSQL密码
                database="scanner"
            )
            cursor = conn.cursor()
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS url_scanner (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL,
                    type TEXT NOT NULL
                );
                '''
            cursor.execute(create_table_query)
            conn.commit()
            return conn
            print("Table created successfully.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("damn!")

    def insertSQL(self, conn, cursor, data_list):
        # 执行插入语句
        insert_query = "INSERT INTO url_scanner (url, type) VALUES (%s, %s)"
        values = tuple(data_list)
        cursor.execute(insert_query, values)

        # 提交更改
        conn.commit()

    def selectSQL(self, cursor):
        """
        :param cursor: 创建SQL实例之后，填入self.cursor即可
        :return: 返回一个list表单的list表单，表单中是不同网址的具体url，没有计数，list元素的第一项是漏洞类型描述
        """
        # 执行查询语句
        select_query = "SELECT url, type FROM url_scanner"
        cursor.execute(select_query)

        # 获取查询结果
        results = cursor.fetchall()

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

    def deleteSQL(self, conn, cursor):
        """
        该函数置空数据库中的表，并重置计数器
        :param conn:
        :param cursor:
        :return:
        """
        truncate_query = "TRUNCATE TABLE url_scanner"
        cursor.execute(truncate_query)

        # 提交更改
        conn.commit()

    def closeSQL(self):
        # 关闭游标对象和数据库连接
        self.cursor.close()
        self.conn.close()
