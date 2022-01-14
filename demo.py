import time

jsod = []


jsod.append({"isim":"alex","yas":12})
jsod.append({"isim":"emirtaha","yas":12})
jsod.append({"isim":"emir","yas":12})

output = [x for x in jsod if x["isim"] is not "alex"]
print(str(time.time()).split(".")[0])
print(output)