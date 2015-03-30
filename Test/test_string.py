import json
server_msg = {'From':'193.48.125.67','To':'193.48.125.68','MsgType':'Order','OrderName':'ConnectTo'}
print server_msg
print type(server_msg)
print type("jxkdbfgsdkbgj")
print json.loads(json.dumps(server_msg))["MsgType"]
print type(json.loads(json.dumps(server_msg))["MsgType"])
print (json.loads(json.dumps(server_msg))["MsgType"]).encode("utf-8")
print (json.loads(json.dumps(server_msg))["MsgType"]).encode("utf-8") != "End"