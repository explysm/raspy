import raspy_format

value = raspy_format.rasp_get("test.ras", "test", 0, 0)

print(value)

value = raspy_format.rasp_get("test.ras", "test", 0, 1)

print(value)

value = raspy_format.rasp_get("test.ras", "test", 0, 2)

print(value)

value = raspy_format.rasp_get("test.ras", "test", 0, 3)

print(value)
