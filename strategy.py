import akshare as ak
import matplotlib.pyplot as plt

fund_name = ak.fund_name_em()
avg_0 = avg_1 = avg_2 = 0.0
tot_earn_0 = tot_earn_1 = tot_earn_2 = 0.0
name_list = []
month_rate = []
week_rate = []
week_earn=[]
month_earn=[]
total_width, n = 0.8, 2
width = total_width / n
for symbol in ["513050", "512200", "516160", "515220", "512480", "512660", "510150", "513100"]:
    name = fund_name[fund_name["基金代码"] == symbol]["基金简称"].values[0]
    for mode in [0, 1, 2]:  # mode == 0 代表完全按照等额定投，mode==1表示上涨时少投，下跌时多投，mode==2代表上涨时多投，下跌时少投
        for period in ["weekly", "monthly"]:
            if period == "weekly":
                base_money = 2500
            elif period == "monthly":
                base_money = 10000
            for start_date in ["20180101"]:
                for end_date in ["20230309"]:
                    df = ak.fund_etf_hist_em(symbol=symbol, period=period, start_date=start_date, end_date=end_date,
                                             adjust="qfq")
                    s = df["收盘"]
                    tot_share = 0
                    tot_budge = 0
                    former_price = s[0]
                    for price in s:
                        money = base_money
                        if mode == 0:
                            money = base_money
                        elif mode == 1:
                            if price > former_price:
                                money = base_money * 0.5
                            elif price < former_price:
                                money = base_money * 1.5
                            else:
                                money = base_money
                        elif mode == 2:
                            if price > former_price:
                                money = base_money * 1.5
                            elif price < former_price:
                                money = base_money * 0.5
                            else:
                                money = base_money
                        tot_share += money / price
                        tot_budge += money
                        former_price = price
                    tot_value = tot_share * s[len(s) - 1]
                    earn = tot_value - tot_budge
                    interest_rate = earn / tot_budge
                    rule = "完全定额规则"
                    if mode == 0:
                        rule = "定额规则"
                        avg_0 += interest_rate
                        tot_earn_0 += earn
                    elif mode == 1:
                        rule = "追跌规则"
                        avg_1 += interest_rate
                        tot_earn_1 += earn
                    elif mode == 2:
                        rule = "追涨规则"
                        avg_2 += interest_rate
                        tot_earn_2 += earn
                    if period == "weekly":
                        name_list.append(name + rule)
                        week_rate.append(interest_rate)
                        week_earn.append(earn)
                    else:
                        month_rate.append(interest_rate)
                        month_earn.append(earn)

                    print("mode={0:5},单次基准基金:{1:5d},投资间隔:{2:8},基金代号:{3:5},名称:{4:13},"
                          "从{5:10}到{6:10},总投资额度{7:.3f},共盈利:{8:.3f},收益率为:{9:.5f}"
                          .format(rule, base_money, period, symbol, name, start_date, end_date,
                                  tot_budge, earn, interest_rate))
print("定额投资规则综合收益率{0:.5f},追跌投资规则综合收益率{1:.5f},追涨投资规则综合收益率{2:.5f}".format(avg_0 / 16,
                                                                                                         avg_1 / 16,
                                                                                                         avg_2 / 16))
print("定额投资规则综合收益{0:.5f},追跌投资规则综合收益{1:.5f},追涨投资规则综合收益{2:.5f}".format(tot_earn_0 / 16,
                                                                                                         tot_earn_1 / 16,
                                                                                                         tot_earn_2 / 16))
plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(30, 15), dpi=150)
x = list(range(len(name_list)))
plt.xlabel(u"标的与策略")
plt.ylabel(u"收益率")
plt.xticks(fontsize=4)
plt.bar(x, week_rate, width=width, label="week", fc="y")
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, month_rate, width=width, label="month", tick_label=name_list, fc="r")
plt.legend()
plt.show()

plt.rcParams['font.sans-serif'] = ['simHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(30, 15), dpi=150)
x = list(range(len(name_list)))
plt.xlabel(u"标的与策略")
plt.ylabel(u"总收益")
plt.xticks(fontsize=4)
plt.bar(x, week_earn, width=width, label="week", fc="y")
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, month_earn, width=width, label="month", tick_label=name_list, fc="r")
plt.legend()
plt.show()
