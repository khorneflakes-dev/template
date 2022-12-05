import os
from dotenv import load_dotenv

load_dotenv()

instance_ip = os.getenv('INSTANCE_IP')
instance_name = os.getenv('INSTANCE_NAME')
db_user_name = os.getenv('DB_USER_NAME')
db_name = os.getenv('DB_NAME')
print(instance_ip)
print(instance_name)
print(db_user_name)
print(db_name)
