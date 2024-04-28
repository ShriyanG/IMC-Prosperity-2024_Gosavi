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
