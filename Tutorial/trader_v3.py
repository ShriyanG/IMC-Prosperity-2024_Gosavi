import string
from typing import List

from datamodel import Order, OrderDepth, TradingState, UserId


class Trader:
    starfruit_stack = [4999.5, 5000.0, 5000.0, 5002.5]

    def calc_amethyst(
        self,
        osell,
        obuy,
        avg_price,
        best_sell,
        best_buy,
        mid_pos,
        curr_pos,
        pos_limit,
        prod_state,
    ):
        product = "AMETHYSTS"
        orders: List[Order] = []

        # Go through the sell orders first
        for ask, vol in osell:
            if (ask <= avg_price) and (curr_pos < pos_limit):
                buy_vol = min(-vol, pos_limit - curr_pos)
                curr_pos += buy_vol
                if buy_vol > 0:
                    orders.append(Order(product, ask, buy_vol))

        # Add any more remaining buy orders

        # Case 1: (More sells currently)
        if (curr_pos < pos_limit) and (prod_state < 0):
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 2, avg_price - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        # Case 2: (More Buys and want to buy at a very low price)
        if (curr_pos < pos_limit) and (prod_state > mid_pos):
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy, avg_price - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        # Case 3: Everything in between
        if curr_pos < pos_limit:
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 1, avg_price - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        curr_pos = prod_state
        # Go through the buy orders
        for bid, vol in obuy:
            if (bid >= avg_price) and (curr_pos > -pos_limit):
                sell_vol = max(-vol, -pos_limit - curr_pos)
                curr_pos += sell_vol
                if sell_vol < 0:
                    orders.append(Order(product, bid, sell_vol))

        # Case 1: (More buys currently)
        if (curr_pos > -pos_limit) and (prod_state > 0):
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 2, avg_price + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        # Case 2: (More Sells and want to sell at a very high price)
        if (curr_pos > -pos_limit) and (prod_state < -mid_pos):
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell, avg_price + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        # Case 3: Everything in between
        if curr_pos > -pos_limit:
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 1, avg_price + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        return orders

    def calc_starfruit(
        self,
        osell,
        obuy,
        prev_prices,
        best_sell,
        best_buy,
        mid_pos,
        curr_pos,
        pos_limit,
        prod_state,
    ):
        # set up the product and the orders
        product = "STARFRUIT"
        orders: List[Order] = []

        # calculate the price using linear regression
        coefficients = [0.33197868, 0.21983134, 0.23500549, 0.21217359]
        constant = 4.961280128746694
        avg_price = constant
        for idx, price in enumerate(prev_prices):
            avg_price += price * coefficients[idx]
        avg_price = int(round(avg_price))
        avg_price_buy = avg_price - 1
        avg_price_sell = avg_price + 1

        # Go through the sell orders first
        for ask, vol in osell:
            if (ask <= avg_price_buy) and (curr_pos < pos_limit):
                buy_vol = min(-vol, pos_limit - curr_pos)
                curr_pos += buy_vol
                if buy_vol > 0:
                    orders.append(Order(product, ask, buy_vol))

        # Add any more remaining buy orders

        # Case 1: (More sells currently)
        if (curr_pos < pos_limit) and (prod_state < 0):
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 2, avg_price_buy - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        # Case 2: (More Buys and want to buy at a very low price)
        if (curr_pos < pos_limit) and (prod_state > mid_pos):
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy, avg_price_buy - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        # Case 3: Everything in between
        if curr_pos < pos_limit:
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 1, avg_price_buy - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        curr_pos = prod_state

        # Go through the buy orders
        for bid, vol in obuy:
            if (bid >= avg_price_sell) and (curr_pos > -pos_limit):
                sell_vol = max(-vol, -pos_limit - curr_pos)
                curr_pos += sell_vol
                if sell_vol < 0:
                    orders.append(Order(product, bid, sell_vol))

        # Case 1: (More buys currently)
        if (curr_pos > -pos_limit) and (prod_state > 0):
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 2, avg_price_sell + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        # Case 2: (More Sells and want to sell at a very high price)
        if (curr_pos > -pos_limit) and (prod_state < -mid_pos):
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell, avg_price_sell + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        # Case 3: Everything in between
        if curr_pos > -pos_limit:
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 1, avg_price_sell + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        return orders

    def run(self, state: TradingState):
        # print("traderData: " + state.traderData)
        # print("Observations: " + str(state.observations))
        # print("Current Positions: " + str(state.position))

        # Set up other variables:
        avg_amethyst = 10000
        avg_starfruit = 4980
        mid_volume = 10

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            position_limit = 20
            curr_position = 0
            if product in state.position:
                curr_position = state.position[product]
            print(
                "Buy Order depth : "
                + str(len(order_depth.buy_orders))
                + ", Sell order depth : "
                + str(len(order_depth.sell_orders))
            )
            print("current position: ", curr_position)
            # calculate best prices and volumes
            osell = sorted(order_depth.sell_orders.items())
            obuy = sorted(order_depth.buy_orders.items(), reverse=True)

            best_sell_pr = max(osell, key=lambda x: -x[1])[0]
            best_buy_pr = max(obuy, key=lambda x: x[1])[0]
            print("sell orders: ", order_depth.sell_orders.items())
            print("buy orders: ", order_depth.buy_orders.items())
            print("sell items: ", best_sell_pr)
            print("buy items: ", best_buy_pr)
            print("product: ", product)
            if product == "AMETHYSTS":
                amethyst_orders = self.calc_amethyst(
                    osell,
                    obuy,
                    avg_amethyst,
                    best_sell_pr,
                    best_buy_pr,
                    mid_volume,
                    curr_position,
                    position_limit,
                    curr_position,
                )
                result["AMETHYSTS"] = amethyst_orders
            if product == "STARFRUIT":
                prev_prices = self.starfruit_stack.copy()
                prev_prices.pop()
                sell_pr = min(osell, key=lambda x: x[0])[0]
                buy_pr = max(obuy, key=lambda x: x[1])[0]
                mid_price = (sell_pr + buy_pr) / 2
                prev_prices.append(mid_price)
                starfruit_orders = self.calc_starfruit(
                    osell,
                    obuy,
                    prev_prices,
                    best_sell_pr,
                    best_buy_pr,
                    mid_volume,
                    curr_position,
                    position_limit,
                    curr_position,
                )
                print("starfruit orders: ", starfruit_orders)
                result["STARFRUIT"] = starfruit_orders

        # String value holding Trader state data required.
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"

        # Sample conversion request. Check more details below.
        conversions = 1
        return result, conversions, traderData
