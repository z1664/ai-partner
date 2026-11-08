#存储
import os
import json
from config import SESSION_DATA_DIR
#导入时自动创建会话文件夹
os.makedirs(SESSION_DATA_DIR, exist_ok=True)
def save_file(session_id:str, data:dict):
    #原样吧dic写入json
    file_path = os.path.join(SESSION_DATA_DIR, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#读取会话原始json
def load_file(session_id:str)->dict | None:
    file_path = os.path.join(SESSION_DATA_DIR, f"{session_id}.json")
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("error")
        return None

#列出全部会话，按文件修改时间倒序排序
def list_all_session_ids()->list[str]:
    if not os.path.exists(SESSION_DATA_DIR):
        return []
    temp = []
    for fname in os.listdir(SESSION_DATA_DIR):
        if fname.endswith(".json"):
            full_path = os.path.join(SESSION_DATA_DIR, fname)
            mtime = os.path.getmtime(full_path) #mtime越大时间越新
            sid = fname[:-5]
            temp.append((mtime,sid))
    temp.sort(reverse=True,key = lambda x:x[0])#降序
    sid_list = [item[1] for item in temp]
    return sid_list

#删除会话
def delete_file(session_id:str)->bool:
    file_path = os.path.join(SESSION_DATA_DIR, f"{session_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
