def blackjack3(card):
    card_value={
                "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
                "T":10,"J":10,"Q":10,"K":10
               }
    counter=0
    card=list(card)
    for index in range(0,3):
        if card[index]=="A":
            counter+=1
    if counter==3:
        return 3
    if counter==1:
        sum1=0
        for index in range(0,3):
            if card[index]!="A":
                card[index]=card_value[card[index]]
                sum1=sum1+card[index]
        if sum1<=10:
            for index in range(0,3):
                if card[index]=="A":
                    card[index]=11
            sum_total=card[0]+card[1]+card[2]   
        else:
            for index in range(0,3):
                if card[index]=="A":
                    card[index]=1
            sum_total=card[0]+card[1]+card[2]
        return sum_total
    if counter==2:
        sum1=0
        for index in range(0,3):
            if card[index]!="A":
                card[index]=card_value[card[index]]   
                sum1=sum1+card[index]
        if sum1<=9:
            total_sum=12+sum1
        else:
            total_sum=2+sum1
        return total_sum  

        