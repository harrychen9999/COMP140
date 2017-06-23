def format(number):
    if number<=5999 and number>=1000:
        number=str(number)
        second=number[-3]+number[-2]
        second= int(second)
        minute=second/60
        real_minute=minute+int(number[0])
        real_second=second-minute*60
        if second==0:
            real_second="00"
        real_minute=str(real_minute)
        real_second=str(real_second)
        tenth=number[-1]
        print real_minute+":"+real_second+"."+tenth
    if number<1000 and number>=100:
        number=str(number)
        second=number[-3]+number[-2]
        second= int(second)
        minute=second/60
        real_minute=minute
        real_second=second-minute*60
        if second==0:
            real_second="00"
        real_minute=str(real_minute)
        real_second=str(real_second)
        tenth=number[-1]   
        print real_minute+":"+real_second+"."+tenth
    if number<100 and number>=10:
        number=str(number)
        second=number[-2]  
        real_second="0"+str(second)
        tenth=number[-1]
        print "0"+":"+real_second+"."+tenth
    if number<10:
        number=str(number)
        print "0"+":"+"00"+"."+number
