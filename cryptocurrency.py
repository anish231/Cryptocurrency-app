import requests
import json
from tkinter import*
import sqlite3


conn=sqlite3.connect("crypto.db")
curs=conn.cursor()
curs.execute("drop table if exists coindb")
curs.execute("create table coindb(SNO integer,Symbol text,amount_owned integer,price_per_coin real)")
conn.commit()
curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(0,'BTC',2,3200))
conn.commit()
curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(1,'XRP',2,5))
conn.commit()
curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(2,'EOS',100,2.05))
conn.commit()
curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(3,'LTC',75,25))
conn.commit()
curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(4,'XMR',10,40.05))
conn.commit()
add=[5]


def reset():
    for cell in root.winfo_children():
        cell.destroy()

    draw_header()
    my_portfolio()







def my_portfolio():
    api_request=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=b7ab30b2-58ed-46c2-a289-62c4d6ec0044")
    api=json.loads(api_request.content)
    

    def font_color(a):
        if(a>=0):
            return "green"
        elif(a<0):
            return "red"
    
    def add_coin():
        
        print(entCoinName.get(),type(entCoinName.get()))
        curs.execute("insert into coindb values('%d','%s','%d', '%f')"%(add[0],entCoinName.get(),int(entNCoins.get()),float(entPrice.get())))
        conn.commit()
        add[0]+=1
        reset();

    def update_coin():
        curs.execute("update coindb set amount_owned=%d,price_per_coin=%f where SNO=%d"%(int(entNCoins_update.get()),float(entPrice_update.get()),int(entSNO_update.get())))
        conn.commit()
        reset();
        
    def del_coin():
        curs.execute("delete from coindb where SNO=%d"%(int(entSNO_del.get()),))
        reset();
    

    curs.execute("select * from coindb")
    lst=curs.fetchall()
    print(lst)

    #lst=[
    #    {"symbol":"BTC"
    #     ,"amount_owned":2
    #     ,"price_per_coin":3200},
    #    {"symbol":"XRP"
    #     ,"amount_owned":2
    #     ,"price_per_coin":5},
    #      {"symbol":"EOS"
    #     ,"amount_owned":100
    #     ,"price_per_coin":2.05},
    #      {"symbol":"LTC"
    #     ,"amount_owned":75
    #     ,"price_per_coin":25},
    #      {"symbol":"XMR"
    #     ,"amount_owned":10
    #     ,"price_per_coin":40.05}
    #    ]
    total_pl=0
    ro=1
    amount_paid=0
    total_spent=0
    for i in range(0,300):
        for coin in lst:
            if(coin [1]==api["data"][i]["symbol"]):
                total_amount=coin [2]*coin [3]
                current_amount=coin [2]*api["data"][i]["quote"]["USD"]["price"]
                amount_paid=current_amount+amount_paid
                plcoin=api["data"][i]["quote"]["USD"]["price"]-coin [3]
                total_pl=total_pl+(plcoin*coin [2])
                total_spent+=total_amount
                coin_name=Label(root,text="{}".format(coin [0]),bg="grey",).grid(row=ro,column=0,padx=2,pady=2)
                coin_name=Label(root,text=api["data"][i]["name"]+"-"+api["data"][i]["symbol"],bg="grey",).grid(row=ro,column=1,padx=2,pady=2)
                coin_name=Label(root,text="${0:.2f}".format( api["data"][i]["quote"]["USD"]["price"]),bg="grey",).grid(row=ro,column=2,padx=2,pady=2)
                coin_name=Label(root,text="{}".format(coin [2]),bg="grey",).grid(row=ro,column=3,padx=2,pady=2)
                coin_name=Label(root,text="${0:.2f}".format(total_amount),bg="grey",).grid(row=ro,column=4,padx=2,pady=2)
                coin_name=Label(root,text="${0:.2f}".format(current_amount),bg="grey",).grid(row=ro,column=5,padx=2,pady=2)
                coin_name=Label(root,text="${0:.2f}".format(plcoin),bg="grey",fg=font_color(plcoin)).grid(row=ro,column=6,padx=2,pady=2)
                coin_name=Label(root,text="${0:.2f}".format(plcoin*coin [2]),bg="grey",fg=font_color(plcoin*coin [2])).grid(row=ro,column=7,padx=2,pady=2)
                #print(api["data"][i]["name"]+"-",end=" ")
                #print(api["data"][i]["symbol"])
                #print("Price- ${0:.2f}".format( api["data"][i]["quote"]["USD"]["price"]))
                #print("Number of Coin: ",coin["amount_owned"])
                #print("Total Amount paid: $",total_amount)
                #print("Current Value: ${0:.2f}".format(current_amount))
                #print("P/L Per Coin: ${0:.2f}".format(plcoin))
                #print("Total P/L with Coin: ${0:.2f}".format(plcoin*coin["amount_owned"]))
                #print("............................")
                ro+=1

    #print("Total P/L with Coins: ${0:.2f}".format(total_pl))
    coin_name=Label(root,text="${0:.2f}".format(amount_paid),bg="grey",).grid(row=ro,column=5,padx=2,pady=2)
    coin_name=Label(root,text="${0:.2f}".format(total_pl),bg="grey",fg=font_color(total_pl)).grid(row=ro,column=7,padx=2,pady=2)
    
    api=""
    coin_name=Label(root,text="${0:.2f}".format(total_spent),bg="grey",fg="black").grid(row=ro,column=4,padx=2,pady=2)
    refresh=Button(root,text="REFRESH",bg="grey",fg="black",command=reset).grid(row=ro+1,column=7,padx=2,pady=2)

    #add Coin
    entCoinName=Entry(root,bg="grey")
    entCoinName.grid(row=ro+1,column=1)
    entPrice=Entry(root,bg="grey")
    entPrice.grid(row=ro+1,column=2)
    entNCoins=Entry(root,bg="grey")
    entNCoins.grid(row=ro+1,column=3)
    Insert=Button(root,text="ADD",command=add_coin,bg="grey").grid(row=ro+1,column=4)

    #update Coin
    entSNO_update=Entry(root,bg="grey")
    entSNO_update.grid(row=ro+2,column=0)
    entCoinName_update=Entry(root,bg="grey")
    entCoinName_update.grid(row=ro+2,column=1)
    entPrice_update=Entry(root,bg="grey")
    entPrice_update.grid(row=ro+2,column=2)
    entNCoins_update=Entry(root,bg="grey")
    entNCoins_update.grid(row=ro+2,column=3)
    update=Button(root,text="Update",command=update_coin,bg="grey").grid(row=ro+2,column=4)

    #delete Coin
    entSNO_del=Entry(root,bg="grey")
    entSNO_del.grid(row=ro+3,column=0)
    dele=Button(root,text="DELETE",command=del_coin,bg="grey").grid(row=ro+3,column=4)


root=Tk()
root.title("Cryptocurrency")

def draw_header():
    sr_code=Label(root,text="SERIAL CODE NO",bg="blue").grid(row=0,column=0,padx=2,pady=2)
    coin_name=Label(root,text="COIN NAME",bg="blue").grid(row=0,column=1,padx=2,pady=2)
    PRICE=Label(root,text="PRICE",bg="blue").grid(row=0,column=2,padx=2,pady=2)
    COINS_OWNED=Label(root,text="COINS OWNED",bg="blue").grid(row=0,column=3,padx=2,pady=2)
    TOTAL_AMOUNT_PAID=Label(root,text="TOTAL AMOUNT PAID",bg="blue").grid(row=0,column=4,padx=2,pady=2)
    CURRENT_VALUE=Label(root,text="CURRENT VALUE",bg="blue").grid(row=0,column=5,padx=2,pady=2)
    PL_PER_COIN=Label(root,text="P/L PER COIN",bg="blue").grid(row=0,column=6,padx=2,pady=2)
    TOTAL_PL_with_COIN=Label(root,text="TOTAL P/L with COIN",bg="blue").grid(row=0,column=7,padx=2,pady=2)
    
draw_header()
my_portfolio()
root.mainloop()
curs.close()
conn.close()