
import Datebase


class User_Manage:
    onlineUser_Num=0
    db = Datebase.Database()
    def __init__(self):
        self.onlineUser=()

    def Register(self,Name,Password):
        self.db.User_Insert(Name,Password)

    def Modify_Password(self,Name,OldPassword,NewPassword):
        self.db.modify_Password(Name,OldPassword,NewPassword)

    def Login(self,Name,Password):
        if self.db.Login(Name,Password):
            self.onlineUser+=1
            print("Login Success")
        else:
            print("Wrong Password")

if __name__ =="__main__":
    UM=User_Manage()
    Name="nan"
    Password="123456"
    print(132)
    #M.Register(Name,Password)
    # UM.db.User_Insert("ray","111")
    # for i in range(6):
    #     UM.db.Vehicle_Insert("ray")
    #UM.db.Group_Insert("ray", 4,5)
    #UM.db.Queue_Insert("ray",0,1,2)
    #UM.db.User_Update("ray",0)
    #UM.db.Check_User("ray")
    #UM.db.modify_Password("ray","111","123")
    #UM.db.modify_User_Priority("ray","P1")