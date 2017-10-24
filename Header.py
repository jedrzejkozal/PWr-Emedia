

class Header:
    def __init__(self):
        self.map = {}

    def __str__(self):
        string = ""
        for key in self.map:
            string += key + ' - ' + self.map[key] + "\n"
        return string

    def add_property(self, name, value):
        self.map[name] = value

    def get_property(self, name):
        return self.map[name]
"""
h = Header ()
h.map["test"] = "a"
h.map["test1"] = "b"
print h.map

h1 = Header ()
h1.add_property("test", "a")
h1.add_property("test1", "b")
print h1.map

print h1.get_property("test")
"""
