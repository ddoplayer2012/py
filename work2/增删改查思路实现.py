sql_in = input("sql>").strip()
action = sql_in.split()[0]
action_info = {
    "insert":insert_action,
    "update":update_action,
    "delete":delete_action,
    "select":select_action
}

res = action_info.get(action)
if res:
    pass



