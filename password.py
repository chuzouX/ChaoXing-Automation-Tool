import hashlib

Salt = str(input("请输入salt的值:"))
Salt = Salt[::-1]+"xy521"
Ypassword = hashlib.sha512(Salt.encode()).hexdigest()

print("你的密码为:"+Ypassword)