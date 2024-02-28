import grpc
import market_pb2
import market_pb2_grpc
def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = market_pb2_grpc.MarketStub(channel)

    print("Welcome to the Seller Portal!")
    address = input("Enter your address (ip:port): ")
    uuid = input("Enter your UUID: ")
    while True:
        print("\nSelect an option:")
        print("1. Register as a seller")
        print("2. Sell an item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Display your items")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_seller(stub, address, uuid)
        elif choice == '2':
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            quantity = int(input("Enter quantity: "))
            description = input("Enter item description: ")
            price_per_unit = float(input("Enter price per unit: "))
            sell_item(stub, name, category, quantity, description, address, price_per_unit, uuid)
        elif choice == '3':
            item_id = int(input("Enter item ID to update: "))
            price_per_unit = float(input("Enter new price per unit: "))
            quantity = int(input("Enter new quantity: "))
            update_item(stub, item_id, price_per_unit, quantity, address, uuid)
        elif choice == '4':
            item_id = int(input("Enter item ID to delete: "))
            delete_item(stub, item_id, address, uuid)
        elif choice == '5':
            display_seller_items(stub, address, uuid)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

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

if __name__ == '__main__':
    main()
