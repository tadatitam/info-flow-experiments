import re                                       # regular expressions
import common

class Interests:
    
    def __init__(self):
        self.data = []
        self.label = -1 
        
    def setLabel(self, lbl):
        self.label = lbl
                
    def index(self, ad):
        return self.data.index(ad)
        
    def size(self):
        return len(self.data)
    
    def remove_interest(self):
        self.data = []      
        
    def set_from_string(self, str):
        chunks = re.split('@', str)
        if len(chunks)==1:
            chunks = re.split(',', str)
        for i in range(0, len(chunks)):
            chunks[i] = chunks[i].replace("&amp;", "&").strip()
        self.data.extend(chunks)
    
    def add_interest(self, int):
        self.data.append(int)
        
    def copy(self):
        temp = Interests()
        temp.data = self.data[:]
        return temp

    def display(self):
        print self.data
    
    def union(self, int2):
        temp = self.copy()
#       print "old temp:", temp.display()
        for int in int2.data:
#           print "in"
#           print int
            if int not in temp.data:
                temp.add_interest(int)
#           print "new temp:", temp.display()
#           raw_input("wait")
        return temp
        
    def gen_int_vec(self, ints):                # self is int_union # generates a vector of ints
        vec = [0]*self.size()
        for int in self.data:
            if int in ints.data:
                vec[self.index(int)] += 1.
        return vec