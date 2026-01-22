from olist.seller import Seller

seller = Seller()
sellers = seller.get_training_data()

print("sellers type:", type(sellers))
print("sellers is None:", sellers is None)
