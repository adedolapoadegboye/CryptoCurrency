import json
import matplotlib.pyplot as plt
from tkinter import *
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os

os.system('clear')


#############################################
def red_green(amount):
    if amount >= 0:
        return "green"
    else:
        return "red"


root = Tk()

root.title("Crypto Currency Portfolio")
# root.iconbitmap(r'c:\codemy.ico')

# ******************* CREATE HEADER **********************
header_name = Label(root, text="Name", bg="white", font="Verdana 8 bold")
header_name.grid(row=0, column=0, sticky=N + S + E + W)

header_rank = Label(root, text="Rank", bg="silver", font="Verdana 8 bold")
header_rank.grid(row=0, column=1, sticky=N + S + E + W)

header_current_price = Label(root, text="Current Price", bg="white", font="Verdana 8 bold")
header_current_price.grid(row=0, column=2, sticky=N + S + E + W)

header_price_paid = Label(root, text="Price Paid", bg="silver", font="Verdana 8 bold")
header_price_paid.grid(row=0, column=3, sticky=N + S + E + W)

header_profit_loss_per = Label(root, text="Profit/Loss Per", bg="white", font="Verdana 8 bold")
header_profit_loss_per.grid(row=0, column=4, sticky=N + S + E + W)

header_1_hr_change = Label(root, text="1 HR Change", bg="silver", font="Verdana 8 bold")
header_1_hr_change.grid(row=0, column=5, sticky=N + S + E + W)

header_24_hr_change = Label(root, text="24 HR Change", bg="white", font="Verdana 8 bold")
header_24_hr_change.grid(row=0, column=6, sticky=N + S + E + W)

header_7_day_change = Label(root, text="7 Day Change", bg="silver", font="Verdana 8 bold")
header_7_day_change.grid(row=0, column=7, sticky=N + S + E + W)

header_current_value = Label(root, text="Current Value", bg="white", font="Verdana 8 bold")
header_current_value.grid(row=0, column=8, sticky=N + S + E + W)

header_profit_loss_total = Label(root, text="Profit/Loss Total", bg="silver", font="Verdana 8 bold")
header_profit_loss_total.grid(row=0, column=9, sticky=N + S + E + W)

# ******************** END HEADER SECTION *******************************************************************


portfolio_profit_loss = 0


def lookup():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '50',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '792c82aa-e50d-4b34-8daf-63d5dfffbc45',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        api = json.loads(response.text)
        print(api)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # My Portfolio
    my_portfolio = [
        {
            "sym": "BTC",
            "amount_owned": 1,
            "price_paid_per": 0
        },

        {
            "sym": "STEEM",
            "amount_owned": 3000,
            "price_paid_per": .80
        },
        {
            "sym": "XRP",
            "amount_owned": 5000,
            "price_paid_per": .20
        },
        {
            "sym": "XLM",
            "amount_owned": 2000,
            "price_paid_per": .10
        },
        {
            "sym": "EOS",
            "amount_owned": 1000,
            "price_paid_per": 2.00
        }
    ]
    portfolio_profit_loss = 0
    total_current_value = 0
    row_count = 1
    pie = []
    pie_size = []
    for x in api:
        for coin in my_portfolio:
            if coin["sym"] == api['data'][0]['symbol']:
                # Do some math
                total_paid = float(coin["amount_owned"]) * float(coin["price_paid_per"])
                current_value = float(coin["amount_owned"]) * float(api['data'][0]["quote"]["USD"]["price"])
                profit_loss = current_value - total_paid
                portfolio_profit_loss += profit_loss
                profit_loss_per_coin = float(api['data'][0]["quote"]["USD"]["price"]) - float(coin["price_paid_per"])
                total_current_value += current_value
                pie.append(api['data'][0]["name"])
                pie_size.append(coin["amount_owned"])

                # print(api['data'][0]["name"])
                # print(" Current Price: ${0:.2f}".format(float(api['data'][0]["quote"]["USD"]["price"])))
                # print(" Profit/Loss Per Coin: ${0:.2f}".format(float(profit_loss_per_coin)))
                # print(" Rank: {0:.0f}".format(float(api['data'][0]["rank"])))
                # print(" Total Paid: ${0:.2f}".format(float(total_paid)))
                # print(" Current Value: ${0:.2f}".format(float(current_value)))
                # print(" Profit/Loss: ${0:.2f}".format(float(profit_loss)))
                # print("---------------------------------------")

                name = Label(root, text=api['data'][0]["name"], bg="white")
                name.grid(row=row_count, column=0, sticky=N + S + E + W)

                rank = Label(root, text=api['data'][0]["cmc_rank"], bg="silver")
                rank.grid(row=row_count, column=1, sticky=N + S + E + W)

                current_price = Label(root, text="${0:.2f}".format(float(api['data'][0]["quote"]["USD"]["price"])),
                                      bg="white", )
                current_price.grid(row=row_count, column=2, sticky=N + S + E + W)

                price_paid = Label(root, text="${0:.2f}".format(float(coin["price_paid_per"])), bg="silver")
                price_paid.grid(row=row_count, column=3, sticky=N + S + E + W)

                profit_loss_per = Label(root, text="${0:.2f}".format(float(profit_loss_per_coin)), bg="white",
                                        fg=red_green(float(profit_loss_per_coin)))
                profit_loss_per.grid(row=row_count, column=4, sticky=N + S + E + W)

                one_hr_change = Label(root, text="{0:.2f}%".format(
                    float(api['data'][0]["quote"]["USD"]["percent_change_1h"])), bg="silver",
                                      fg=red_green(float(api['data'][0]["quote"]["USD"]["percent_change_1h"])))
                one_hr_change.grid(row=row_count, column=5, sticky=N + S + E + W)

                tf_hr_change = Label(root, text="{0:.2f}%".format(
                    float(api['data'][0]["quote"]["USD"]["percent_change_24h"])), bg="white",
                                     fg=red_green(float(api['data'][0]["quote"]["USD"]["percent_change_24h"])))
                tf_hr_change.grid(row=row_count, column=6, sticky=N + S + E + W)

                seven_day_change = Label(root, text="{0:.2f}%".format(
                    float(api['data'][0]["quote"]["USD"]["percent_change_7d"])), bg="silver",
                                         fg=red_green(float(api['data'][0]["quote"]["USD"]["percent_change_7d"])))
                seven_day_change.grid(row=row_count, column=7, sticky=N + S + E + W)

                current_value = Label(root, text="${0:.2f}".format(float(current_value)), bg="white")
                current_value.grid(row=row_count, column=8, sticky=N + S + E + W)

                profit_loss_total = Label(root, text="${0:.2f}".format(float(profit_loss)), bg="silver",
                                          fg=red_green(float(profit_loss)))
                profit_loss_total.grid(row=row_count, column=9, sticky=N + S + E + W)

                row_count += 1

    portfolio_profits = Label(root, text="P/L: ${0:.2f}".format(float(portfolio_profit_loss)), font="Verdana 8 bold",
                              fg=red_green(float(portfolio_profit_loss)))
    portfolio_profits.grid(row=row_count, column=0, sticky=W, padx=10, pady=10)

    root.title("Crypto Currency Portfolio - Portfolio Value: ${0:.2f}".format(float(total_current_value)))
    # total_current_value_output = Label(root, text="P/L: ${0:.2f}".format(float(total_current_value)), font="Verdana 8 bold", fg=red_green(float(portfolio_profit_loss)))
    # total_current_value_output.grid(row=row_count+1, column=1, sticky=W, padx=10, pady=10)
    api = ""
    update_button = Button(root, text="Update Prices", command=lookup)
    update_button.grid(row=row_count, column=9, sticky=E + S, padx=10, pady=10)

    def graph(pie, pie_size):
        labels = pie
        sizes = pie_size
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red']
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    graph_button = Button(root, text="Pie Chart", command=lambda: graph(pie, pie_size))
    graph_button.grid(row=row_count, column=8, sticky=E + S, padx=10, pady=10)


lookup()

root.mainloop()
