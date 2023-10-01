from bson.objectid import ObjectId
import json
import requests
from datetime import datetime, date
import secrets

# def post_userLogin(data):
#     from config.db import user, nft
    
#     data = dict(data)
    
#     allowed_wallet_types = ["metamask", "coinbase", "trust wallet", "wallet connect"]
#     if data["walletType"].lower() in allowed_wallet_types:
#         user.insert_one(data)
        
#         user.update_one({"_id": data["_id"]}, {"$set": {
#             "createdAt": datetime.now(),
#             "nftProcessed": False,
#             "dmActive": False,
#             "nftCollection": [],
#             "refferaID": secrets.token_hex(6)
#         }})
        
#         nft_data = {
#             "userID": str(data["_id"]),
#             "walletAddress": data["walletAddress"],
#             "nftMetaData": "",
#             "rightAllocated": {
#                 "tshirt": None,
#                 "cap": None,
#                 "hoodie": None,
#                 "cup": None
#             },
#             "lastSyncedOn": None,
#             "isOwned": True,
#             "isAdminVerified": False
#         }
#         nft.insert_one(nft_data)
        
#         message = "Login Created Successfully"
#         user_id = str(data["_id"])
#         response = {"message": message, "walletId": user_id}
#         return response
#     else:
#         return "Invalid Wallet Type"

def post_userLogin(data):
    from config.db import user, nft
    # wallet_address = input("Enter wallet address: ")
    api_key = "b7fb531b-40ef-4855-bcb0-56ff6374948f"

    # Define the API endpoint URL
    url = f"https://api.nftport.xyz/v0/accounts/{data.walletAddress}?chain=polygon"

    # Define headers with the Authorization header
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Make a GET request with streaming
    response = requests.get(url, headers=headers, stream=True)
    nftResponse = response.json()
    Nfts=nftResponse["nfts"]
    
    # print(Nfts)
    data = dict(data)
    
    # Check if a user with the same wallet address already exists
    existing_user = user.find_one({"walletAddress": data["walletAddress"]})
    
    # if existing_user:
    #     return "User already exists"
    
    allowed_wallet_types = ["metamask", "coinbase", "trust wallet", "wallet connect"]
    if data["walletType"].lower() in allowed_wallet_types:
        filtered_nfts = [nft for nft in Nfts if nft.get("cached_file_url") is not None]
        # Insert a new user only if the user doesn't exist
        new_user = {
            "createdAt": datetime.now(),
            "nftProcessed": False,
            "dmActive": False,
            "nftCollection": filtered_nfts,
            "refferaID": secrets.token_hex(6)
        }
        data.update(new_user)
        user.insert_one(data)
        
        nft_data = {
            "userID": str(data["_id"]),
            "walletAddress": data["walletAddress"],
            "nftMetaData": filtered_nfts,
            "rightAllocated": {
                "tshirt": None,
                "cap": None,
                "hoodie": None,
                "cup": None
            },
            "lastSyncedOn": None,
            "isOwned": True,
            "isAdminVerified": False
        }
        nft.insert_one(nft_data)
        message = "Login Created Successfully"
        user_id = str(data["_id"])
        nft_id = str(nft_data["_id"])
        response = {"message": message, "walletId": user_id,"nftId":nft_id}
        return response
    else:
        return "Invalid Wallet Type"

def get_userRights(id):
    from config.db import rights
    
    # user_data = rights.find_one({"walletId": str(id)})
    # if user_data:
    user_data_cursor = rights.find({"walletId": str(id)})
    user_rights_list = []
    
    for user_data in user_data_cursor:
        wallet = user_data["walletId"]
        userLicense_condition = user_data["userLicenseCondition"]
        
        cap_rights = user_data.get("capRights", {})
        tshirt_rights = user_data.get("tshirtRights", {})
        hoodie_rights = user_data.get("hoodieRights", {})
        mug_rights = user_data.get("mugRights", {})
        
        cap_rights_given = cap_rights.get("rightsGiven", False)
        tshirt_rights_given = tshirt_rights.get("rightsGiven", False)
        hoodie_rights_given = hoodie_rights.get("rightsGiven", False)
        mug_rights_given = mug_rights.get("rightsGiven", False)
        
        cap_info = {}
        if cap_rights_given:
            cap_info = {
                "merchantQuantity": cap_rights.get("merchantQuantity", 0),
                "merchTitle": cap_rights.get("merchTitle", ""),
                "licenseFees": cap_rights.get("licenseFees", 0),
                "merchLicenseCondition": cap_rights.get("merchLicenseCondition", ""),
                "licenseTerm": cap_rights.get("licenseTerm", ""),
                "licenseDate": cap_rights.get("licenseDate", "")
            }
        
        tshirt_info = {}
        if tshirt_rights_given:
            tshirt_info = {
                "merchantQuantity": tshirt_rights.get("merchantQuantity", 0),
                "merchTitle": tshirt_rights.get("merchTitle", ""),
                "licenseFees": tshirt_rights.get("licenseFees", 0),
                "merchLicenseCondition": tshirt_rights.get("merchLicenseCondition", ""),
                "licenseTerm": tshirt_rights.get("licenseTerm", ""),
                "licenseDate": tshirt_rights.get("licenseDate", "")
            }
        
        hoodie_info = {}
        if hoodie_rights_given:
            hoodie_info = {
                "merchantQuantity": hoodie_rights.get("merchantQuantity", 0),
                "merchTitle": hoodie_rights.get("merchTitle", ""),
                "licenseFees": hoodie_rights.get("licenseFees", 0),
                "merchLicenseCondition": hoodie_rights.get("merchLicenseCondition", ""),
                "licenseTerm": hoodie_rights.get("licenseTerm", ""),
                "licenseDate": hoodie_rights.get("licenseDate", "")
            }
        
        mug_info = {}
        if mug_rights_given:
            mug_info = {
                "merchantQuantity": mug_rights.get("merchantQuantity", 0),
                "merchTitle": mug_rights.get("merchTitle", ""),
                "licenseFees": mug_rights.get("licenseFees", 0),
                "merchLicenseCondition": mug_rights.get("merchLicenseCondition", ""),
                "licenseTerm": mug_rights.get("licenseTerm", ""),
                "licenseDate": mug_rights.get("licenseDate", "")
            }
        
        user_rights = {
            "walletId": wallet,
            "userLicenseCondition": userLicense_condition,
            "imgSrc": user_data["imgSrc"],
            "capRights": cap_info,
            "tshirtRights": tshirt_info,
            "hoodieRights": hoodie_info,
            "mugRights": mug_info
        }
        # return response
        user_rights_list.append(user_rights)
    if len(user_rights_list)!=0:
        return user_rights_list
    else:
        return "User Rights not found"

def get_product_detail(id, prod,search):
    from config.db import user, product
    
    user_data = user.find_one({"walletAddress": str(id)})
    if user_data:
        data = product.find_one({"_id": ObjectId(prod)})
        if data:
            tags = data["tags"]
            category = data["category"]
            
            if search in tags or search in category:  # Updated this line
                if data["isPublished"] and not data["isDeleted"]:
                    nft_id = data["nftId"]
                    cat = data["category"]
                    img = data["images"]
                    tag = data["tags"]
                    price = data["price"]
                    currency = data["currency"]
                    discount = data["discount"]
                    available = data["availableQuantity"]
                    last_date = data["lastDate"]
                    
                    response = {
                        "nftId": nft_id,
                        "category": cat,
                        "images": img,
                        "tags": tag,
                        "price": price,
                        "currency": currency,
                        "discount": discount,
                        "availableQuantity": available,
                        "lastDate": last_date
                    }
                    return response
                else:
                    return "Product is not published or deleted"
            else:
                return "No Keyword found"
        else:
            return "Product not found"
    else:
        return "Invalid Wallet Id"

