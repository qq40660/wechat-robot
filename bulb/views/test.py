from push import BaseClient
import sys

user = "2768715080"
msg = sys.argv[1]

client = BaseClient(email="hellojohn201@gmail.com", passwd="13878300")
result = client.send_msg(user, msg)
