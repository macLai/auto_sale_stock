auto_sale_stock
===============
###ABOUT
自动计算'新浪财经'[^sina]的过往数据，随机挑取50个股票的随机时间的数据叠加计算
[^sina]:'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%d.phtml?year=%d&jidu=%d'%(gupiaoNum,startYear,startSeason)

###算法
底线为当前价格的96%，股价上升时提升底线，下降如触碰底线则卖出。
初始本金 = 1 <br />
卖出一只股票后本金 = 买入前本金 * (抛售价 / 买入价) <br />
最终本金 = 50只股票卖出后的结果

###OUTPUT
1. 股票链接
2. 股票名称
3. 买入价
4. 卖出后的(抛售价 / 买入价)
5. 当前的盈亏

![screenshot](/screenshot.png)