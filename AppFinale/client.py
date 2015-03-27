import socket
import json

# IP Jerome : '193.48.125.68' port: 6030

data = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Ident', u'EquipmentType':'Robot'}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('193.48.125.68', 6030))
result = json.dumps(data)
lenght = len(result)

s.send(result+"\r\n")

print result
result_into_json = json.loads(result)
print result_into_json["From"]

s.close()