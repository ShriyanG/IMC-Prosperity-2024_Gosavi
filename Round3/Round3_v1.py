import string
from typing import List

from datamodel import Order, OrderDepth, TradingState, UserId


class Trader:
    starfruit_stack = [5041.824, 5041.824, 5041.824, 5041.824]

    def calc_amethyst(
        self,
        sells,
        buys,
        avg_price,
        best_sell,
        best_buy,
        curr_pos,
        pos_limit,
        prod_state,
    ):
        product = "AMETHYSTS"
        orders: List[Order] = []

        # Go through the sell orders first
        for ask, vol in sells:
            if (ask <= avg_price) and (curr_pos < pos_limit):
                buy_vol = min(-vol, pos_limit - curr_pos)
                curr_pos += buy_vol
                if buy_vol > 0:
                    orders.append(Order(product, ask, buy_vol))

        # Everything in between
        if curr_pos < pos_limit:
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 1, avg_price - 1)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        curr_pos = prod_state
        # Go through the buy orders
        for bid, vol in buys:
            if (bid >= avg_price) and (curr_pos > -pos_limit):
                sell_vol = max(-vol, -pos_limit - curr_pos)
                curr_pos += sell_vol
                if sell_vol < 0:
                    orders.append(Order(product, bid, sell_vol))

        # Everything in between
        if curr_pos > -pos_limit:
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 1, avg_price + 1)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        return orders

    def calc_starfruit(
        self,
        sells,
        buys,
        best_sell,
        best_buy,
        curr_pos,
        pos_limit,
        prod_state,
    ):
        # set up the product and the orders
        product = "STARFRUIT"
        orders: List[Order] = []

        # calculate the price using linear regression
        coefficients = [0.2257766, 0.14053319, 0.23432196, 0.39353907]
        constant = 29.397507911144203
        avg_price = constant
        sell_pr = min(sells, key=lambda x: x[0])[0]
        buy_pr = max(buys, key=lambda x: x[1])[0]
        mid_price = (sell_pr + buy_pr) / 2
        self.starfruit_stack.pop(0)
        self.starfruit_stack.append(mid_price)
        for idx, price in enumerate(self.starfruit_stack):
            avg_price += price * coefficients[idx]
        avg_price = int(round(avg_price))
        avg_price_buy = avg_price - 1
        avg_price_sell = avg_price + 1

        # Go through the sell orders first
        for ask, vol in sells:
            if (ask <= avg_price_buy) and (curr_pos < pos_limit):
                buy_vol = min(-vol, pos_limit - curr_pos)
                curr_pos += buy_vol
                if buy_vol > 0:
                    orders.append(Order(product, ask, buy_vol))

        # Everything in between
        if curr_pos < pos_limit:
            buy_vol = min(2 * pos_limit, pos_limit - curr_pos)
            buy_price = min(best_buy + 1, avg_price_buy)
            orders.append(Order(product, buy_price, buy_vol))
            curr_pos += buy_vol

        curr_pos = prod_state

        # Go through the buy orders
        for bid, vol in buys:
            if (bid >= avg_price_sell) and (curr_pos > -pos_limit):
                sell_vol = max(-vol, -pos_limit - curr_pos)
                curr_pos += sell_vol
                if sell_vol < 0:
                    orders.append(Order(product, bid, sell_vol))

        # Everything in between
        if curr_pos > -pos_limit:
            sell_vol = max(2 * -pos_limit, -pos_limit - curr_pos)
            sell_price = max(best_sell - 1, avg_price_sell)
            orders.append(Order(product, sell_price, sell_vol))
            curr_pos += sell_vol

        return orders

    def calc_orchids(self, sells, buys, curr_pos, pos_limit, prod_state, observations):
        product = "ORCHIDS"
        orders: List[Order] = []
        sells = 0
        sell_limit = -(int(pos_limit / 10))
        best_buy = (
            observations.askPrice
            + observations.importTariff
            + observations.transportFees
        )
        best_sell = max(buys, key=lambda x: x[0])[0]
        for bid, vol in buys:
            if curr_pos > sell_limit and bid >= best_buy and bid == best_sell:
                sell_vol = max(-vol, sell_limit - curr_pos)
                curr_pos += sell_vol
                sells += sell_vol
                if sell_vol < 0:
                    orders.append(Order(product, bid, sell_vol))
        if prod_state <= 0:
            conversions = min(abs(sells), -prod_state)
        return orders, conversions

    def calc_gift_baskets(self, state):
        avg_diff = 380
        std = 76
        products = ["GIFT_BASKET", "CHOCOLATE", "STRAWBERRIES", "ROSES"]
        gift_basket_orders: List[Order] = []
        pos_limits = {
            "GIFT_BASKET": 60,
            "CHOCOLATE": 250,
            "STRAWBERRIES": 350,
            "ROSES": 60,
        }
        mid_prices = {"GIFT_BASKET": 0, "CHOCOLATE": 0, "STRAWBERRIES": 0, "ROSES": 0}
        best_sell = {"GIFT_BASKET": 0, "CHOCOLATE": 0, "STRAWBERRIES": 0, "ROSES": 0}
        best_buy = {"GIFT_BASKET": 0, "CHOCOLATE": 0, "STRAWBERRIES": 0, "ROSES": 0}
        for product in products:
            order_depth: OrderDepth = state.order_depths[product]

            # calculate best prices and volumes
            sells = sorted(order_depth.sell_orders.items())
            buys = sorted(order_depth.buy_orders.items(), reverse=True)

            best_sell[product] = max(buys, key=lambda x: x[0])[0]
            best_buy[product] = min(sells, key=lambda x: x[0])[0]
            mid_prices[product] = (best_sell[product] + best_buy[product]) / 2

        status = mid_prices["GIFT_BASKET"] - (
            mid_prices["CHOCOLATE"] * 4
            + mid_prices["STRAWBERRIES"] * 6
            + mid_prices["ROSES"]
            + avg_diff
        )

        if status > (0.5 * std):
            curr_pos = 0
            if "GIFT_BASKET" in state.position:
                curr_pos = state.position["GIFT_BASKET"]
            sell_vol = -(curr_pos + pos_limits["GIFT_BASKET"])
            if sell_vol < 0:
                gift_basket_orders.append(
                    Order("GIFT_BASKET", best_sell["GIFT_BASKET"], sell_vol)
                )
        if status < (-0.5 * std):
            curr_pos = 0
            if "GIFT_BASKET" in state.position:
                curr_pos = state.position["GIFT_BASKET"]
            buy_vol = pos_limits["GIFT_BASKET"] - curr_pos
            if buy_vol > 0:
                gift_basket_orders.append(
                    Order("GIFT_BASKET", best_buy["GIFT_BASKET"], buy_vol)
                )
        return gift_basket_orders

    def run(self, state: TradingState):
        # Set up other variables:
        avg_amethyst = 10000
        observations = state.observations
        time = state.timestamp
        orchids_observation = observations.conversionObservations["ORCHIDS"]
        conversions = 0
        first_products = ["AMETHYSTS", "STARFRUIT", "ORCHIDS"]

        # Orders to be placed on exchange matching engine
        result = {}
        for product in first_products:
            order_depth: OrderDepth = state.order_depths[product]
            position_limit = 20
            orchid_limit = 100
            curr_position = 0
            if product in state.position:
                curr_position = state.position[product]
            # calculate best prices and volumes
            sells = sorted(order_depth.sell_orders.items())
            buys = sorted(order_depth.buy_orders.items(), reverse=True)

            best_sell_pr = max(sells, key=lambda x: -x[1])[0]
            best_buy_pr = max(buys, key=lambda x: x[1])[0]
            if product == "AMETHYSTS":
                amethyst_orders = self.calc_amethyst(
                    sells,
                    buys,
                    avg_amethyst,
                    best_sell_pr,
                    best_buy_pr,
                    curr_position,
                    position_limit,
                    curr_position,
                )
                result["AMETHYSTS"] = amethyst_orders
            if product == "STARFRUIT":
                starfruit_orders = self.calc_starfruit(
                    sells,
                    buys,
                    best_sell_pr,
                    best_buy_pr,
                    curr_position,
                    position_limit,
                    curr_position,
                )
                result["STARFRUIT"] = starfruit_orders
            if product == "ORCHIDS":
                if time == 0:
                    orchid_orders = [Order("ORCHIDS", buys[0][0], -1)]
                else:
                    orchid_orders, conversions = self.calc_orchids(
                        sells,
                        buys,
                        curr_position,
                        orchid_limit,
                        curr_position,
                        orchids_observation,
                    )
                result["ORCHIDS"] = orchid_orders
        # String value holding Trader state data required.
        # It will be delivered as TradingState.traderData on next execution.

        result["GIFT_BASKET"] = self.calc_gift_baskets(state)
        traderData = "SAMPLE"
        # Sample conversion request. Check more details below.
        return result, conversions, traderData
