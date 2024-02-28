import grpc
import market_pb2
import market_pb2_grpc

def register_seller(stub, address, uuid):
    request = market_pb2.RegisterSellerRequest(address=address, uuid=uuid)
    response = stub.RegisterSeller(request)
    print("Market prints:", response.result)

def sell_item(stub, name, category, quantity, description, seller_address, price_per_unit, seller_uuid):
    request = market_pb2.SellItemRequest(name=name, category=category, quantity=quantity, description=description, seller_address=seller_address, price_per_unit=price_per_unit, seller_uuid=seller_uuid)
    response = stub.SellItem(request)
    print("Market prints:", response.result)
    print("Seller prints:", response.item_id)

def update_item(stub, item_id, price_per_unit, quantity, seller_address, seller_uuid):
    request = market_pb2.UpdateItemRequest(item_id=item_id, price_per_unit=price_per_unit, quantity=quantity, seller_address=seller_address, seller_uuid=seller_uuid)
    response = stub.UpdateItem(request)
    print("Market prints:", response.result)

def delete_item(stub, item_id, seller_address, seller_uuid):
    request = market_pb2.DeleteItemRequest(item_id=item_id, seller_address=seller_address, seller_uuid=seller_uuid)
    response = stub.DeleteItem(request)
    print("Market prints:", response.result)

def display_seller_items(stub, seller_address, seller_uuid):
    request = market_pb2.DisplaySellerItemsRequest(address=seller_address, uuid=seller_uuid)
    response = stub.DisplaySellerItems(request)
    print("Market prints:", response)
    for item in response.items:
        print("Seller prints:", item)

def search_item(stub, item_name="", category="ANY"):
    request = market_pb2.SearchItemRequest(name=item_name, category=category)
    response = stub.SearchItem(request)
    print("Market prints:", response)
    for item in response.items:
        print("Buyer prints:", item)

def buy_item(stub, item_id, quantity, buyer_address):
    request = market_pb2.BuyItemRequest(item_id=item_id, quantity=quantity, buyer_address=buyer_address)
    response = stub.BuyItem(request)
    print("Market prints:", response.result)

def add_to_wish_list(stub, item_id, buyer_address):
    request = market_pb2.AddToWishListRequest(item_id=item_id, buyer_address=buyer_address)
    response = stub.AddToWishList(request)
    print("Market prints:", response.result)

def rate_item(stub, item_id, rating, buyer_address):
    request = market_pb2.RateItemRequest(item_id=item_id, rating=rating, buyer_address=buyer_address)
    response = stub.RateItem(request)
    print("Market prints:", response.result)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = market_pb2_grpc.MarketStub(channel)

    while True:
        print("Select an option:")
        print("1. Register as a seller")
        print("2. Sell an item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Display seller items")
        print("6. Search item")
        print("7. Buy item")
        print("8. Add item to wish list")
        print("9. Rate item")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            address = input("Enter your address (ip:port): ")
            uuid = input("Enter your UUID: ")
            register_seller(stub, address, uuid)
        elif choice == '2':
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            quantity = int(input("Enter quantity: "))
            description = input("Enter item description: ")
            seller_address = input("Enter your address (ip:port): ")
            price_per_unit = float(input("Enter price per unit: "))
            seller_uuid = input("Enter your UUID: ")
            sell_item(stub, name, category, quantity, description, seller_address, price_per_unit, seller_uuid)
        elif choice == '3':
            item_id = int(input("Enter item ID to update: "))
            price_per_unit = float(input("Enter new price per unit: "))
            quantity = int(input("Enter new quantity: "))
            seller_address = input("Enter your address (ip:port): ")
            seller_uuid = input("Enter your UUID: ")
            update_item(stub, item_id, price_per_unit, quantity, seller_address, seller_uuid)
        elif choice == '4':
            item_id = int(input("Enter item ID to delete: "))
            seller_address = input("Enter your address (ip:port): ")
            seller_uuid = input("Enter your UUID: ")
            delete_item(stub, item_id, seller_address, seller_uuid)
        elif choice == '5':
            seller_address = input("Enter your address (ip:port): ")
            seller_uuid = input("Enter your UUID: ")
            display_seller_items(stub, seller_address, seller_uuid)
        elif choice == '6':
            item_name = input("Enter item name to search (leave blank to display all items): ")
            category = input("Enter item category (ELECTRONICS, FASHION, OTHERS, ANY): ")
            search_item(stub, item_name, category)
        elif choice == '7':
            item_id = int(input("Enter item ID to buy: "))
            quantity = int(input("Enter quantity to buy: "))
            buyer_address = input("Enter your address (ip:port): ")
            buy_item(stub, item_id, quantity, buyer_address)
        elif choice == '8':
            item_id = int(input("Enter item ID to add to wish list: "))
            buyer_address = input("Enter your address (ip:port): ")
            add_to_wish_list(stub, item_id, buyer_address)
        elif choice == '9':
            item_id = int(input("Enter item ID to rate: "))
            rating = int(input("Enter rating (1-5): "))
            buyer_address = input("Enter your address (ip:port): ")
            rate_item(stub, item_id, rating, buyer_address)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
