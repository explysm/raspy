import raspy_format

si = raspy_format.get("test.ras", "test", 0, 0)
si2 =  raspy_format.get("test.ras", "test", 0, 1)
si3 = raspy_format.get("test.ras", "test", 0, 2)
si4 = raspy_format.get("test.ras", "test", 0,3)

si5 = raspy_format.get("test.ras", "test2", 0, 0)
si6 = raspy_format.get("test.ras", "test2", 0, 1)
si7 = raspy_format.get("test.ras", "test2", 0, 2)
si8 = raspy_format.get("test.ras", "test2", 0, 3)

print("--- Test List 1 ---")

print(si)
print(si2)
print(si3)
print(si4)

print("--- Test List 2 ---")

print(si5)
print(si6)
print(si7)
print(si8)


raspy_format.convert("test.ras", "json", "test.json")
