import string
from typing import List

from datamodel import Order, OrderDepth, TradingState, UserId


class Trader:
    starfruit_stack = [5041.824, 5041.824, 5041.824, 5041.824]
    orchid_sells = {}

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
        print("current position: ", curr_pos)
        print("orders: ", self.orchid_sells)
        product = "ORCHIDS"
        price_diff = -1.5
        orders: List[Order] = []
        sell_limit = -pos_limit
        buy_limit = pos_limit
        best_buy = min(sells, key=lambda x: x[0])[0]
        conversions = 0
        best_sell = max(buys, key=lambda x: x[0])[0]
        conversions_buy = (
            observations.askPrice
            + observations.importTariff
            + observations.transportFees
        )

        # set up the sells first check if the conditions are not buying conditions
        if not (observations.sunlight >= 2500 and 60 <= observations.humidity <= 80):
            # put in the orders
            for bid, vol in buys:
                diff = bid - conversions_buy
                if curr_pos > sell_limit and bid == best_sell and (diff >= price_diff):
                    sell_vol = max(-vol, sell_limit - curr_pos)
                    curr_pos += sell_vol
                    if sell_vol < 0:
                        orders.append(Order(product, bid, sell_vol))

        if prod_state <= 0:
            min_sell = min(
                (sell for sell in self.orchid_sells if conversions_buy < sell),
                default=None,
            )
            if min_sell is not None:
                conversions = min(
                    -prod_state,
                    sum(
                        quantity
                        for sell, quantity in self.orchid_sells.items()
                        if conversions_buy <= sell
                    ),
                )
                total_conversions = 0
                for sell, quantity in sorted(self.orchid_sells.items()):
                    used_conversions = min(conversions - total_conversions, quantity)
                    total_conversions += used_conversions
                    self.orchid_sells[sell] -= used_conversions
                    if self.orchid_sells[sell] == 0:
                        del self.orchid_sells[sell]
                    if total_conversions == conversions:
                        break
        return orders, conversions

    def run(self, state: TradingState):
        # Set up other variables:
        avg_amethyst = 10000
        observations = state.observations
        orchids_observation = observations.conversionObservations["ORCHIDS"]
        conversions = 0

        trades = state.own_trades
        if "ORCHIDS" in trades:
            s_trades = trades["ORCHIDS"]
            for trade in s_trades:
                if len(trade.seller) > 1:
                    price = int(trade.price)
                    quantity = trade.quantity
                    if price not in self.orchid_sells:
                        self.orchid_sells[price] = quantity
                    else:
                        self.orchid_sells[price] += quantity

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
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
                orchid_orders, conversions = self.calc_orchids(
                    sells,
                    buys,
                    curr_position,
                    orchid_limit,
                    curr_position,
                    orchids_observation,
                )
                # result["ORCHIDS"] = orchid_orders

        # String value holding Trader state data required.
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"

        # Sample conversion request. Check more details below.
        return result, conversions, traderData
