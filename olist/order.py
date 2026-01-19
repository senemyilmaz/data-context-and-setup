import pandas as pd
import numpy as np

from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        orders = self.data['orders'].copy()

        if is_delivered:
            orders = orders.query("order_status == 'delivered'").copy()

        # datetime
        orders.loc[:, 'order_delivered_customer_date'] = pd.to_datetime(
            orders['order_delivered_customer_date'], errors='coerce'
        )
        orders.loc[:, 'order_estimated_delivery_date'] = pd.to_datetime(
            orders['order_estimated_delivery_date'], errors='coerce'
        )
        orders.loc[:, 'order_purchase_timestamp'] = pd.to_datetime(
            orders['order_purchase_timestamp'], errors='coerce'
        )

        # delay vs expected (hours)
        orders.loc[:, 'delay_vs_expected'] = (
            orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']
        ) / np.timedelta64(24, 'h')

        # keep only positive delays
        orders.loc[:, 'delay_vs_expected'] = orders['delay_vs_expected'].clip(lower=0)

        # wait time (hours)
        orders.loc[:, 'wait_time'] = (
            orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(24, 'h')

        # expected wait time (hours)
        orders.loc[:, 'expected_wait_time'] = (
            orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']
        ) / np.timedelta64(24, 'h')

        return orders[[
            'order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
            'order_status'
        ]]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        # $CHALLENGIFY_BEGIN
        # import data
        reviews = self.data['order_reviews']

        def dim_five_star(d):
            if d == 5:
                return 1
            else:
                return 0

        def dim_one_star(d):
            if d == 1:
                return 1
            else:
                return 0

        reviews.loc[:, 'dim_is_five_star'] =\
            reviews['review_score'].apply(dim_five_star)

        reviews.loc[:, 'dim_is_one_star'] =\
            reviews['review_score'].apply(dim_one_star)

        return reviews[[
            'order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score'
        ]]
        # $CHALLENGIFY_END
    def get_number_items(self):
        """
        Returns a DataFrame with:
        order_id, number_of_items
        """
        # $CHALLENGIFY_BEGIN
        data = self.data
        items = \
            data['order_items']\
            .groupby('order_id',
                     as_index=False).agg({'order_item_id': 'count'})
        items.columns = ['order_id', 'number_of_items']
        return items
        # $CHALLENGIFY_END

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        # $CHALLENGIFY_BEGIN
        data = self.data
        sellers = \
            data['order_items']\
            .groupby('order_id')['seller_id'].nunique().reset_index()
        sellers.columns = ['order_id', 'number_of_sellers']

        return sellers
        # $CHALLENGIFY_END

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
