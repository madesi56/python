class MyIterator:
    def __iter__(self):
        self.myattr = 2
        return self
    def __next__(self):
        if (self.myattr < 300):
            n=self.myattr
            self.myattr *=2
            return n
        else:
            raise StopIteration

m = MyIterator()
mi = iter(m)
for i in mi:
    print(i)
