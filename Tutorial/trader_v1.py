import string
from typing import List

from datamodel import Order, OrderDepth, TradingState, UserId


class Trader:

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        print("Current Positions: " + str(state.position))

        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            position_limit = 20
            curr_position = 10
            if product in state.position:
                curr_position = state.position[product]
            print(
                "Buy Order depth : "
                + str(len(order_depth.buy_orders))
                + ", Sell order depth : "
                + str(len(order_depth.sell_orders))
            )

            if len(order_depth.buy_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if abs(best_bid_amount) < position_limit:
                    diff = abs(position_limit) - abs(curr_position)
                    curr_position += diff
                    print("buy order: ", product, best_bid, diff)
                    orders.append(Order(product, best_bid, diff))

            if len(order_depth.sell_orders) != 0:
                best_bid, best_bid_amount = list(order_depth.sell_orders.items())[0]
                if abs(best_bid_amount) < position_limit:
                    diff = abs(position_limit) - abs(curr_position)
                    curr_position -= diff
                    print("sell order: ", product, best_bid, diff)
                    orders.append(Order(product, best_bid, -diff))

            result[product] = orders

        # String value holding Trader state data required.
        # It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE"

        # Sample conversion request. Check more details below.
        conversions = 1
        return result, conversions, traderData
