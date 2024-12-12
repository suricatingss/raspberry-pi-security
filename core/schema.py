import mysql.connector
class mysql_db:

    def __init__(self):
        self.__con = mysql.connector.connect(host='suricatingss.xyz', user='pi_alarm', password="password", database='pi_alarm', ssl_disabled=True)
        self.__cursor = self.__con.cursor()

    def __del__(self):
        try:
            self.__con.close()
        except: pass

    def Execute(self, query, args=None):
        if args is not None and not isinstance(args, tuple): args = (args,)

        if args is None: self.__cursor.execute(query)
        else: self.__cursor.execute(query, args)

        self.__con.commit() # guardar se necessário

    def FetchOneRow(self, query, args=None):
        if args is not None and not isinstance(args, tuple): args = (args,)
        if args is None: self.__cursor.execute(query)
        else: self.__cursor.execute(query, args)
        #self.con.commit()
        return self.__cursor.fetchone()

    def FetchOneElement(self, query, args=None):
        if args is not None and not isinstance(args, tuple): args = (args,)
        if args is None:
            self.__cursor.execute(query)
        else:
            self.__cursor.execute(query, args)

        #self.con.commit()
        return self.__cursor.fetchone()[0]

    def FetchAll(self, query, args=None):
        if args is not None and not isinstance(args, tuple): args = (args,)
        if args is None: self.__cursor.execute(query)
        else: self.__cursor.execute(query, args)

        #self.con.commit()
        return self.__cursor.fetchall()

    def Close(self):
        self.__con.commit()
        self.__con.close()

if __name__ == "__main__":
    datatest = mysql_db()
