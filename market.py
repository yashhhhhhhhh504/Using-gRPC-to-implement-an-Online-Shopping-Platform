import grpc
import time
import market_pb2
import market_pb2_grpc

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MarketServicer(market_pb2_grpc.MarketServicer):
    def __init__(self):
        # Initialize any necessary data structures
        self.sellers = {}
        self.items = {}

    def RegisterSeller(self, request, context):
        # Implement RegisterSeller functionality
        address = request.address
        uuid = request.uuid
        if address in self.sellers:
            return market_pb2.RegisterSellerResponse(result="FAIL")
        else:
            self.sellers[address] = uuid
            print(f"Seller join request from {address}, uuid = {uuid}")
            return market_pb2.RegisterSellerResponse(result="SUCCESS")

    def SellItem(self, request, context):
        # Implement SellItem functionality
        # Process request and store item details
        item_id = len(self.items) + 1
        item_details = { "id": item_id, "name": request.name, "category": request.category, "quantity": request.quantity, "description": request.description, "seller_address": request.seller_address, "price_per_unit": request.price_per_unit }
        self.items[item_id] = item_details
        print(f"Sell Item request from {request.seller_address}")
        return market_pb2.SellItemResponse(result="SUCCESS", item_id=item_id)

    def UpdateItem(self, request, context):
        # Implement UpdateItem functionality
        item_id = request.item_id
        if item_id in self.items:
            if self.items[item_id]['seller_address'] == request.seller_address:
                self.items[item_id]['price_per_unit'] = request.price_per_unit
                self.items[item_id]['quantity'] = request.quantity
                print(f"Update Item {item_id} request from {request.seller_address}")
                return market_pb2.UpdateItemResponse(result="SUCCESS")
            else:
                return market_pb2.UpdateItemResponse(result="FAIL")
        else:
            return market_pb2.UpdateItemResponse(result="FAIL")

    def DeleteItem(self, request, context):
        # Implement DeleteItem functionality
        item_id = request.item_id
        if item_id in self.items:
            if self.items[item_id]['seller_address'] == request.seller_address:
                del self.items[item_id]
                print(f"Delete Item {item_id} request from {request.seller_address}")
                return market_pb2.DeleteItemResponse(result="SUCCESS")
            else:
                return market_pb2.DeleteItemResponse(result="FAIL")
        else:
            return market_pb2.DeleteItemResponse(result="FAIL")

    def DisplaySellerItems(self, request, context):
        # Implement DisplaySellerItems functionality
        seller_address = request.address
        items_list = []
        for item_id, item_details in self.items.items():
            if item_details['seller_address'] == seller_address:
                item_info = f"Item ID: {item_details['id']}, Price: ${item_details['price_per_unit']}, Name: {item_details['name']}, Category: {item_details['category']}, Description: {item_details['description']}, Quantity Remaining: {item_details['quantity']}, Seller: {item_details['seller_address']}"
                items_list.append(item_info)
        print(f"Display Items request from {seller_address}")
        return market_pb2.DisplaySellerItemsResponse(items=items_list)

    def SearchItem(self, request, context):
        # Implement SearchItem functionality
        item_name = request.name
        category = request.category
        items_list = []
        for item_id, item_details in self.items.items():
            if (item_name == "" or item_details['name'] == item_name) and (category == "ANY" or item_details['category'] == category):
                item_info = f"Item ID: {item_details['id']}, Price: ${item_details['price_per_unit']}, Name: {item_details['name']}, Category: {item_details['category']}, Description: {item_details['description']}, Quantity Remaining: {item_details['quantity']}, Seller: {item_details['seller_address']}"
                items_list.append(item_info)
        print(f"Search request for Item name: {item_name}, Category: {category}")
        return market_pb2.SearchItemResponse(items=items_list)

    def BuyItem(self, request, context):
        # Implement BuyItem functionality
        item_id = request.item_id
        quantity = request.quantity
        buyer_address = request.buyer_address
        if item_id in self.items and self.items[item_id]['quantity'] >= quantity:
            self.items[item_id]['quantity'] -= quantity
            print(f"Buy request {quantity} of item {item_id}, from {buyer_address}")
            return market_pb2.BuyItemResponse(result="SUCCESS")
        else:
            return market_pb2.BuyItemResponse(result="FAIL")

    def AddToWishList(self, request, context):
        # Implement AddToWishList functionality
        item_id = request.item_id
        buyer_address = request.buyer_address
        # Implement wish list logic
        return market_pb2.AddToWishListResponse(result="SUCCESS")

    def RateItem(self, request, context):
        # Implement RateItem functionality
        item_id = request.item_id
        rating = request.rating
        buyer_address = request.buyer_address
        # Implement rating logic
        return market_pb2.RateItemResponse(result="SUCCESS")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market server started...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
