**IMC-Prosperity-2024**

**Final Rank:**

**Round Strategies**

**Round 1 products to trade (Amethysts and Starfruit)**

**Amethysts:** The price was stable at an average of 10,000 so I used the straightforward strategy of market-taking and market-making.

**Starfruit:** After graphing the prices from the data given it seemed to follow trends pretty clearly and it seemed to fit with linear regression pretty well. After running the linear regression model it seemed to have an RMSE of above 0.9 in some cases even 0.95 so the model seemed to fit it very well. I then optimized the number of coefficients by running it on a test dataset in the model as well as on the backtest and it seemed like 4 seemed to be an ideal number so I used the last 4 timestamps for the price prediction.

**Manual Trading:** This manual trading round was based on the optimization of the bids on the scuba gear. The first step was to model the linear probability of accepting the bid and I created a linear probability distribution using python by incrementing by 1 from 900 to 1000 and calculating the probability at each step. I then ran a simulation and used a double for loop to calculate the maximum profit from the fish accepting everything below the low bid multiplied by the price difference between the selling point and the lowest bid and added that to the difference between the highest bid and lowest bid multiplied by the price difference between the selling price and the highest bid. After calculating the optimal points I eyeballed from printing the graph and added 1 to each to account for more bids being accepted. 

**Round 2 products to trade (Amethysts, Starfruit, Orchids):**

**Amethysts and Starfruit:** The results of the first round fared pretty well for these products so I decided to keep the strategy the same on these. 

**Orchids:** I tried modeling the price using a linear regression model but this did not seem to work very well. I graphed the prices from the different markets on a graph as well as the price discrepancies of the orchids between the markets to look for arbitraging opportunities. There were two main cases which was selling on the local market and buying from the South Island market and buying on the local market and selling on the South Island market. I decided to go with the first option since it did not cost extra to hold a sell position but it did for holding a buy position and anytime there was a discrepancy I used the conversions to trigger an automatic buy and profit from the arbitraging. 

**Manual Trading:** This trading challenge closely modeled the famous currency arbitraging problem. I modeled this by using that algorithm to set up an adjacency graph structure where each node represented a different good and the edge between them represented the conversion rate. After finding all the cycles I calculated which one returned the largest ratio then I also did some manual calculations to check if I missed some easy conversion rate switches since we had 5 total moves to make.


**Round 3 products to trade (Amethysts, Starfruit, Orchids, Gift baskets, Strawberries, Roses, Chocolates):**

**Amethysts and Starfruit:** No changes to the strategy

**Orchids:** I made changes from the last round in the last round I started out with the position limits for the sell position at first and then hold a stack to check if at anytime there were better buy opportunities then to buy immediately for a price below and make a profit. While this may work in theory, in a days worth of trading this did not work well in my favor so I decided to reduce my risk by only starting with one sell position as this is needed to use conversions and then to use the same arbitraging strategy. 

**Gift Baskets:** After graphing the summation of the separate goods that make up the gift basket and the price the actual gift basket there seemed to be a good opportunity for pairs trading. I used the backtester to check and see what range works best for the price divergence between two total price of the goods and the gift basket similar to the concept of the Bollinger bands. 

**Chocolates, Roses and Strawberries:** I set up a correlation matrix between these goods to check if there was another opportunity for pairs trading but this did not seem to work. I also set up the Bollinger bands for each separate products and it seemed to potentially work for chocolate and roses but the PnL was relatively low and if the range was reduced for the Bollinger bands then there was a good chance that I would end up with a negative for these goods so I decided not to risk it after the last round and my decent PnL on the gift baskets. 

**Manual Trading:** This Manual Trading round was pretty tricky since other people’s decisions were also factored into the total PnL. I decided to set up a graph for a visual and rank the profits for each square in the expedition. The first expedition was pretty much a guaranteed profit so I decided to go for the cell with the fourth or fifth greatest profit since others might pick the first couple which may decrease the profit. The second expedition seemed to have profits up until the 10% mark of people choosing a tile so I essentially eyeballed it and used the graph to pick a tile that would give a profit for one of the largest possible percentages of people picking that respective tile. I did not take the risk for the third expedition as I would have to be pretty lucky to get a profit on that tile with the increased cost of the expedition. 



**Round 4 products to trade (Amethysts, Starfruit, Orchids, Gift baskets, Strawberries, Roses, Chocolates, Coconut Coupons, Coconuts):**

**Amethysts and Starfruit:** No changes to the strategy

**Orchids:** No changes to the strategy

**Gift baskets, Strawberries, Roses, Chocolates:** No changes to the strategy

**Coconut Coupons:** The coupons mimicked buy options and I tried to model the price of the coupons using the Black-Scholes option pricing model and this prediction seemed to work very well with the previous data that was provided. I used the backtester to then see what range for a price differential would work best for buying and selling these options. 

**Coconuts:** The coconuts did seem to be trading in trends so I tried to model the price using linear regression but this did not seem to work too well and was heavily dependent on the last price. Instead I used Bollinger Bands on coconuts and I used a a standard deviation value of 1.95 above and below since this generated a decent PnL without any loss on the backtester. I decided to use this rather than the prototypical 2.0 standard deviations since this had a higher upside for profits. 

**Manual Trading:** This was pretty much the same manual trading problem from the first round but it was made more difficult since other’s bids were taken into account for the higher bid. I tried graphing this again but I just went ahead and eyeballed it instead and used judgement from the previous round. I wanted to get more bids even if the profit for each one was not the high for the lower bid so I took the results from the first round for the average lower bid and went a little higher than that. For the higher bid I wanted to maximize my chances of receiving matches for the bid rather than for profit so I took the average for the higher bid from round 1 and I went higher than this. 



**Round 5 products to trade (Amethysts, Starfruit, Orchids, Gift baskets, Strawberries, Roses, Chocolates, Coconut_Coupons, Coconuts):**

I did an analysis on each round after the traders were being disclosed for rounds 1, 3, and 4. For round 1, I tried mimicking the strategy of some of the profitable traders however this did not generate too large of a difference in PnL and I decided to continue with my strategy. For Round 3, I kept my strategy for the gift basket but for chocolates and roses it seemed like Remy was making suboptimal trades and Vinnie was making optimal trades so I decided to use those two traders as indicators for buy and sell signals. I did the same for round 4 goods but they turned out to not be as profitable and I decided to stick with my original strategy. 

**Amethysts and Starfruit:** No changes to the strategy

**Orchids:** No changes to the strategy

**Gift baskets and Coconut Coupons:** No changes to the strategy

**Chocolate and Roses:** Use Remy and Vinnie as buy and sell signals for these two commodities. 
