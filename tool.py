

from datetime import datetime

def generate_unique_id():
    current_time = datetime.now()
    unique_id = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
    return unique_id

# 生成唯一ID
unique_id = generate_unique_id()



