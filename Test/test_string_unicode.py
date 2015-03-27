import json

data_ident = {u'From':'193.48.125.67', u'To':'193.48.125.68', u'MsgType':'Ident', u'EquipmentType':'Robot'}
result_ident = json.dumps(data_ident)
data_converted = result_ident.encode("utf-8")

print (json.loads(result_ident)["MsgType"]).encode("utf-8") != "End"
print (json.loads(result_ident)["MsgType"]).encode("utf-8") != "Ident"
print result_ident