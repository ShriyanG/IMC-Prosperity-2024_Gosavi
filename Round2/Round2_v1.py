import string
from typing import List

from datamodel import Order, OrderDepth, TradingState, UserId


class Trader:
    starfruit_stack = [5041.824, 5041.824, 5041.824, 5041.824]
    orchid_position = {}

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

    def calc_orchids(
        self,
        sells,
        buys,
        curr_pos,
        pos_limit,
        prod_state,
        observations,
    ):
        product = "ORCHIDS"
        orders: List[Order] = []
        buy_flag = -1
        if observations.sunlight >= 2500 or (60 <= observations.humidity <= 80):
            buy_flag = 1
        if observations.sunlight < 2500 and (
            observations.humidity < 60 or observations.humidity > 80
        ):
            buy_flag = 0
        for ask, vol in sells:
            if (curr_pos < pos_limit) and buy_flag == 1:
                buy_vol = min(-vol, pos_limit - curr_pos)
                curr_pos += buy_vol
                if buy_vol > 0:
                    orders.append(Order(product, ask, -buy_vol))

        curr_pos = prod_state
        for bid, vol in buys:
            max_price = max(
                (
                    price
                    for price in self.orchid_position
                    if (bid > price and self.orchid_position[price] > 0)
                ),
                default=None,
            )
            if max_price is not None and (curr_pos > -pos_limit):
                sell_vol = max(-vol, -pos_limit - curr_pos)
                curr_pos += sell_vol
                if sell_vol < 0:
                    # print("entered sells")
                    self.orchid_position[max_price] += sell_vol
                    if self.orchid_position[max_price] <= 0:
                        self.orchid_position[max_price] = 0
                    orders.append(Order(product, bid, sell_vol))
        return orders

    def run(self, state: TradingState):
        # Set up other variables:
        avg_amethyst = 10000
        observations = state.observations
        # Orchids information
        trades = state.own_trades
        if "ORCHIDS" in trades:
            # print("orchids trades: ", trades["ORCHIDS"])
            s_trades = trades["ORCHIDS"]
            for trade in s_trades:
                if len(trade.buyer) > 1:
                    price = int(trade.price)
                    quantity = trade.quantity
                    if price in self.orchid_position:
                        self.orchid_position[price] += quantity
                    else:
                        self.orchid_position[price] = quantity
        # print("status: ", self.orchid_position)
        orchids_observation = observations.conversionObservations["ORCHIDS"]
        print("Bid Price:", orchids_observation.bidPrice)
        print("Ask Price:", orchids_observation.askPrice)
        print("Transport Fees:", orchids_observation.transportFees)
        print("Export Tariff:", orchids_observation.exportTariff)
        print("Import Tariff:", orchids_observation.importTariff)
        print("Sunlight:", orchids_observation.sunlight)
        print("Humidity:", orchids_observation.humidity)

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
                orchid_orders = self.calc_orchids(
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
        traderData = "SAMPLE"

        # Sample conversion request. Check more details below.
        conversions = 1
        return result, conversions, traderData
