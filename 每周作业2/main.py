sql_in = input("sql>").strip()
action = sql_in.split()[0]
def insert_action():
    print('insert')
def select_action():
    print('select')
def delete_action():
    print('delete')
def update_action():
    print('update')
action_info = {
    "insert":insert_action,
    "update":update_action,
    "delete":delete_action,
    "select":select_action
}

res = action_info.get(action)
if res:
    pass

action_info.get("select")
print((action_info.get(res)))