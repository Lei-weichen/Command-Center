import pymysql

class Database:

    def __init__(self):
        self.db=pymysql.connect("localhost","root","lwc13994908921","commandcenterdb")
        self.cursor=self.db.cursor()

    def db_close(self):
        self.cursor.close()
        self.db.close()

    def Check_User(self,UserName):
        sql="SELECT * FROM user WHERE UserName=\"%s\"" % (UserName)
        self.cursor.execute(sql)
        date=self.cursor.fetchone()
        print("UserName:%s,Password:%s,Priority:%s,Vehicles:%s,Groups:%s,Queues:%s" %(date[0],date[1],date[2],date[4],date[5],date[6]))

    def User_Insert(self,Name,Password):
        sql="INSERT INTO user(UserName,Password) VALUES(\"%s\",\"%s\")" % (Name,Password)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert User Success")
        except:
            self.db.rollback()

    def Admin_Insert(self,Name,Password):
        sql = "INSERT INTO Admin(AdminName,Password) VALUES(\"%s\",\"%s\")" % (Name, Password)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert Admin Success")
        except:
            self.db.rollback()

    def Vehicle_Insert(self,UserName):
        Vehicle_Num=self.get_Vehicle_Num()
        sql = "INSERT INTO vehicles(SeqNum,User) VALUES(%d,\"%s\")" % (Vehicle_Num, UserName)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert Vehicle Success")
            self.User_Vehicle_Update(UserName,Vehicle_Num)
        except:
            self.db.rollback()

    def Group_Insert(self,UserName,*params):
        Group_Num=self.get_Groups_Num()
        Vehicles=[]
        for i in range(len(params)):
            Vehicles.append(params[i])
            self.modify_Vehicle_isAllot(params[i])
        Vehicles_String=str(Vehicles)
        sql = "INSERT INTO groups(SeqNum,User,Vehicles) VALUES(%d,\"%s\",\"%s\")" % (Group_Num, UserName,Vehicles_String)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert Group Success")
            self.User_Group_Update(UserName,Group_Num)
        except:
            self.db.rollback()

    def Queue_Insert(self,UserName,*params):
        Queue_Num=self.get_Queue_Num()
        Groups = []
        for i in range(len(params)):
            Groups.append(params[i])
            self.modify_Group_isAllot(params[i])
        Groups_String = str(Groups)
        sql = "INSERT INTO queues(SeqNum,User,Groups) VALUES(%d,\"%s\",\"%s\")" % (Queue_Num, UserName,Groups_String)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Insert Queue Success")
            self.User_Queue_Update(UserName,Queue_Num)
        except:
            self.db.rollback()

    def User_Vehicle_Update(self,UserName,VehicleNum):
        sql="SELECT Vehicles from user WHERE UserName=\"%s\"" % (UserName)
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        Vehicles_String=""
        #用户已注册车
        if data[0]!=None:
            Vehicles=[]
            for i in data[0]:
                if i != '[' and i != ']' and i != ',' and i !=' ':
                    Vehicles.append(int(i))
            Vehicles.append(VehicleNum)
            Vehicles.sort()
            Vehicles_String=str(Vehicles)
        #用户没注册车
        else:
            Vehicles_String=str([VehicleNum])
        sql = "UPDATE user SET Vehicles=\"%s\" WHERE UserName=\"%s\"" % (Vehicles_String, UserName)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("User Update Vehicle Success")
        except:
            self.db.rollback()


    def User_Group_Update(self,UserName,GroupNum):
        sql="SELECT Groups FROM user WHERE UserName=\"%s\"" % (UserName)
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        Groups_String=""
        #用户注册车组的时候
        if data[0]!=None:
            Groups=[]
            for i in data[0]:
                if i != '[' and i != ']' and i != ',' and i != ' ':
                    Groups.append(int(i))
            Groups.append(GroupNum)
            Groups.sort()
            Groups_String=str(Groups)
        #用户没有注册车组
        else:
            Groups_String=str([GroupNum])
        sql = "UPDATE user SET Groups=\"%s\" WHERE UserName=\"%s\"" % (Groups_String, UserName)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("User Update Group Success")
        except:
            self.db.rollback()

    def User_Queue_Update(self, UserName, QueueNum):
        sql = "SELECT Queues from user WHERE UserName=\"%s\"" % (UserName)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        Queues_String = ""
        # 用户已注册车队
        if data[0] != None:
            Queues = []
            for i in data[0]:
                if i != '[' and i != ']' and i != ',' and i != ' ':
                    Queues.append(int(i))
            Queues.append(QueueNum)
            Queues.sort()
            Queues_String = str(Queues)
        # 用户没注册车
        else:
            Queues_String = str([QueueNum])
        sql = "UPDATE user SET Queues=\"%s\" WHERE UserName=\"%s\"" % (Queues_String, UserName)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("User Update Queue Success")
        except:
            self.db.rollback()

    def modify_Vehicle_isAllot(self,VehicleNum):
        sql = "UPDATE vehicles SET isAllot=1 WHERE SeqNum=\"%s\"" % (VehicleNum)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Vehicle isAllot Update Success")
        except:
            self.db.rollback()

    def modify_Group_isAllot(self,GroupNum):
        sql = "UPDATE groups SET isAllot=1 WHERE SeqNum=\"%s\"" % (GroupNum)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Group isAllot Update Success")
        except:
            self.db.rollback()

    def modify_Password(self,UserName,OldPassword,NewPassword):
        sql = "UPDATE user SET Password=%s WHERE UserName=\"%s\" AND Password=\"%s\"" % (NewPassword,UserName,OldPassword)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Modify Password Success")
        except:
            self.db.rollback()

    def modify_User_Priority(self,UserName,Priority):
        sql="UPDATE user SET Priority=\"%s\" WHERE UserName=\"%s\"" % (Priority,UserName)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print("Modify User Priority Success")
        except:
            self.db.rollback()

    def Login(self,UserName,Password):
        sql="SELECT Password FROM user WHERE UserName=\"%s\"" % (UserName)
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        if data[0]==Password:
            return True
        else:
            return False


    def get_Vehicle_Num(self):
        sql="SELECT COUNT(*) FROM vehicles"
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        return data[0]

    def get_Groups_Num(self):
        sql="SELECT COUNT(*) FROM groups"
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        return data[0]

    def get_Queue_Num(self):
        sql="SELECT COUNT(*) FROM queues"
        self.cursor.execute(sql)
        data=self.cursor.fetchone()
        return data[0]
