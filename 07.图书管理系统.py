"""
某社区图书馆需要开发一个简单的图书管理系统。系统需要支持会员登录、图书借阅、图书归还等功能。系统中有两种类型的会员:
普通会员和VIP会员,他们的借书权限不同。你需要使用面向对象编程的思想,设计并实现这个图书管理系统。
核心功能:
        1. 会员登录:会员通过卡号和密码登录系统
        2. 借书:会员可以借阅库存中有余量的图书
        3. 还书:会员可以归还借阅的图书
        4. 查看我的借阅:展示当前会员已经借阅的图书列表
        5. 退出系统
借阅规则:
        1. 普通会员最多可借3本
        2. VIP会员最多可借 6+VIP等级 本 (VIP等级,默认为1)
注意:
        1. 登录成功(卡号和密码均正确)后,才可以访问该系统
        2. 图书库存不足,或当前会员借书数量达到最大借书数量,不能再借新书
"""


from abc import ABC,abstractmethod
import json


#图书系统
class Books:
    def __init__(self,code,headline,author,total_num):
        self.code = code                #编码
        self.headline = headline        #标题
        self.author = author            #作者
        self.total_num = total_num      #总数
        self.__available_quantity = total_num  #可用数量

    def borrow_book(self):                  #借书
        if self.__available_quantity > 0:
            self.__available_quantity -= 1
            return True
        return False

    def return_book(self):                      #还书
        self.__available_quantity += 1

    def get_available_quantity(self):           #展示可用数量
        return self.__available_quantity




#会员数据  抽象类
class Member(ABC):
    def __init__(self,card_number,name,password):
        self.card_number = card_number      #卡号
        self.name = name                    #名字
        self.__password = password          #密码
        self.__borrow_book=[]               # 每个会员借的书装起来

    #会员借书
    #book只是形参"占位符",当调用Books里面的方法的时候,
    # 需要传入一个Books类型的对象,这个对象会被赋值给book.对象可以调用Books方发
    def borrow_book(self,book : Books):
        # 会员借书数量是否已超过最大限制数
        if len(self.__borrow_book) >= self.get_max_books():
            print("借书已超过最大限制")
            return False
        #借书
        if book.borrow_book():
            self.__borrow_book.append(book)
            print(f"{self.name}已成功借阅图书:{book.headline}!")
            return True
        else:
            print(f"借阅失败!图书:{book.headline}已借完!")
            return False

    #还书
    def return_book(self,book : Books):
        #判断是否有这本书
        if book in self.__borrow_book:
            book.return_book()
            self.__borrow_book.remove(book)
            print(f"已成功归还图书:{book.headline}!")
        else:
            print(f"归还失败,您没有借阅:{book.headline}!")

    def get___password(self):       # get密码
        return self.__password

    def get_borrow_book(self):      #get会员借阅的书籍列表
        return self.__borrow_book

    #借阅书籍的最多数量(要在子类实现)
    @abstractmethod  #装饰器
    def get_max_books(self) -> int:
        pass


#普通会员类
class NormalMember(Member):
    def get_max_books(self) -> int :  # 借书最多限制
        return 3


#Vip会员调用
class VIPMember(Member):
    def __init__(self,card_number,name,password,grade):
        Member.__init__(self,card_number,name,password)
        self.grade = grade

    def get_max_books(self) -> int:
        return 6 + self.grade


#图书管理系统
class LibrarySystem:
    def __init__(self):
        self.books = {}       # 书籍列表--> {编号"A001" : {books对象},"A002" : {books对象}}
        self.members = {}      #  会员列表--> {卡号"N001" : {Member对象}}
        self.now_member : Member|None = None  # 当前登录会员
        #把书和会员信息读取进来
        self.load_books_data()
        self.load_member_data()

    def load_books_data(self):
        with open("面向对象高级案例数据/books.json", "r", encoding="utf-8") as f:
            books_data = json.load(f)
            for book in books_data:
                self.books[book["编号"]] =Books(book["编号"],book["标题"],book["作者"],book["数量"])
            print("加载书籍数据成功!")

    def load_member_data(self):
        with open("面向对象高级案例数据/members.json", "r", encoding="utf-8") as f:
            members_data = json.load(f)
            for member in members_data:
                if member["卡号"].startswith ("N"):
                    self.members[member["卡号"]] =  NormalMember(member["卡号"], member["姓名"], member["密码"])
                elif member["卡号"].startswith ("V"):
                    self.members[member["卡号"]] =  VIPMember(member["卡号"], member["姓名"], member["密码"],member["会员等级"])
            print("会员信息加载完成!")


    #登录
    def login(self):
      print("\n【登录】")
      while True:
          card_number = input("请输入会员卡号:")
          # 卡号是否正确
          if card_number not in self.members:
              print("登录失败,该卡号不存在!")
              continue

          password = input("请输入会员密码:")
          # 密码是否正确
          member = self.members[card_number]  # 获取到了会员的信息, 拿到的是卡号这个key的整个对象,所以能用方法
          if member.get___password() == password:  #有了所有信息才能查找密码
              print(f"登录成功!欢迎您{member.name}~")
              self.now_member = member
              return True
          else:
              print("密码错误,请重新输入!")
              continue

     #借阅图书
    def borrow_books(self):
        #1.展示当前图书列表
        for book in self.books.values():  #只获取价值,也就是对象
            print(f"编码:{book.code},标题:{book.headline},作者{book.author},总数:{book.total_num},可用数量:{book.get_available_quantity()}")

     #2.输入图书编号借书
        code = input("\n请输入要借阅图书的编码:")
        if code not in self.books:
            print("借阅失败,图书编号不存在")
            return
        self.now_member.borrow_book(self.books[code])

    #归还图书
    def return_books(self):
        #1.展示当前会员的借阅列表
        borrowed_books = self.now_member.get_borrow_book()
        print("【已借阅的图书列表:】")
        for book in borrowed_books:
            print(f"编码:{book.code},标题:{book.headline}")

        code = input("请输入要归还图书的编码:")
        if code not in self.books:
            print("归还失败,未找到有该编号的图书.")
            return
        self.now_member.return_book(self.books[code])

    def show_borrowed_books(self):
        borrowed_books = self.now_member.get_borrow_book()
        #判断是不是空列表
        if len(borrowed_books) > 0 :
            print("【已借阅的图书列表:】")
            for book in borrowed_books:
                print(f"编码:{book.code},标题:{book.headline},作者{book.author}")
        else:
            print("您还没有借阅人和图书!")


    def run(self):
        if self.login():
            try:
                while True:
                    print("\n1.借阅图书")
                    print("2.归还图书")
                    print("3.查看借阅")
                    print("4.退出系统")
                    choice = input("请选择操作(1-4):")
                    match choice:
                        case "1":
                            self.borrow_books()
                        case "2":
                            self.return_books()
                        case "3":
                            self.show_borrowed_books()
                        case "4":
                            print("退出成功,Bay~")
                            break
                        case _:
                            print("无效选项,请重新选择!")
            except Exception as e:
                print(f"操作过程中出现异常问题{e}")
        else:
            print("登录失败,程序退出.")

if __name__ == '__main__':
    ls = LibrarySystem()
    ls.run()



