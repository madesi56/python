import os

#with open ("isolamisteriosa.txt",'rt') as f1, open("output.txt",'wt') as f2:
#    c=0
#    for i in f1.readlines():
#        c+=1
#        if (c % 2 ==0):
#            pass
#        else:
#            f2.writelines(f"{str(c)} : {i}")


#with open ("isolamisteriosa.txt",'rt') as f1, open("output.txt",'at') as f2:
#    c=0
#    for i in f1.readlines():
#        c+=1
#        if (c % 2 ==0):
#           f2.writelines(f"{str(c)} : {i}")

#with open ("isolamisteriosa.txt",'rb') as f1:
#    f1.tell()
#    f1.seek(119)
#    str = f1.read(7)
#    f1.seek(-9,os.SEEK_END)    
#    str = f1.read()
#    print (str.decode)
#    f1.close()

subject_value = [1,2,3]
match subject_value:
    case [1,*resto]:
        print (f"il resto è {resto}")

  