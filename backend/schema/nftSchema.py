from bson.objectid import ObjectId
import json
from datetime import datetime, date
import secrets
from model.nft import NftModel 
from model.user import * 
from model.rights import *
from config.db import *

import secrets
#
def post_CreateDRM(data: rightsModel):
    data = data.dict()
    
    # Check for valid user using Wallet ID
    if not user.find_one({"_id": ObjectId(data["walletId"])}):
        return "Invalid Wallet ID"
    
    # Check if NFT is there or not
    if not nft.find_one({"_id": ObjectId(data["nftId"])}):
        return "Invalid NFT ID"
    
    # Checks for user License Condition
    if data["userLicenseCondition"] not in ["Copyright", "C BY", "CC BY-SA"]:
        return "Please enter a valid license Condition"
    
    license_conditions = ["", "Negotiable", "Non-Negotiable"]
    
    # Check user license conditions for each category
    categories = ["capRights","tshirtRights", "hoodieRights", "mugRights"]
    rights_exists = rights.find_one({"walletId":data["walletId"],"nftId":data['nftId']})
    # print(rights_exists)
    any_category_valid = False
    if rights_exists is not None:
        for Category_rights in categories:
            if data[Category_rights]["merchantQuantity"] == "":
                data[Category_rights]["merchantQuantity"] = 0
            if rights_exists[Category_rights]["merchantQuantity"] == "":
                rights_exists[Category_rights]["merchantQuantity"] = 0
            if (
                int(data[Category_rights]["merchantQuantity"]) > 0
                and int(rights_exists[Category_rights]["merchantQuantity"]) > 0
            ):
                # print(rights_exists[Category_rights]["merchantQuantity"])
                return "rights already allocated"
        for category in categories:
            print(rights_exists[category],data[category],sep="\n\n")

            if category not in data:
                continue  # Skip this category if it's not entered correctly

            # Check if the category has the merchLicenseCondition key
            if "merchLicenseCondition" not in data[category]:
                continue  # Skip this category if the license condition is missing

            if data[category]["merchLicenseCondition"] not in license_conditions:
                return f"Please enter valid {category} Merch license Condition"
            merch_quantity = data[category].get("merchantQuantity", "")  # string
            if merch_quantity:
                merch_quantity = int(merch_quantity)  # integer
                if not (100 <= merch_quantity <= 1000):
                    return f"Please select quantity between 100 and 1000 for {category}"
            else:
                data[category]["merchantQuantity"] = 0

            # if int(merch_quantity) > 0:
            #     data[category]["rightsGiven"] = True

            if rights_exists[category]["merchantQuantity"] == "":
                rights_exists[category] = data[category]
            if rights_exists[category]["merchantQuantity"] == 0:
                rights_exists[category] = data[category]
            print(rights_exists[category],data[category],sep="\n\n")

            # At least one category is valid, set the flag to True
            any_category_valid = False
        # Only insert into the database if at least one category or single data is valid
        if any_category_valid:
            # update data into the database
            update_info = rights.update_one({"_id": rights_exists["_id"]}, {"$set": rights_exists}).modified_count
            return f"{update_info} rights req updated"
    # Variable to keep track of whether any category is valid

    for category in categories:
        if category not in data:
            continue  # Skip this category if it's not entered correctly
        
        # Check if the category has the merchLicenseCondition key
        if "merchLicenseCondition" not in data[category]:
            continue  # Skip this category if the license condition is missing
        
        if data[category]["merchLicenseCondition"] not in license_conditions:
            return f"Please enter valid {category} Merch license Condition"
        
        merchant_quantity_str = data[category].get('merchantQuantity', '')
        if merchant_quantity_str:
            merchant_quantity = int(merchant_quantity_str)
            if not (100 <= merchant_quantity <= 1000):
                return f"Please select quantity between 100 and 1000 for {category}"
        else:
            data[category]["merchantQuantity"] = 0
        
        if int(data[category]["merchantQuantity"]) > 0:
            data[category]["rightsGiven"] = False
        
        # At least one category is valid, set the flag to True
        any_category_valid = True
    
    # Only insert into the database if at least one category or single data is valid
    if any_category_valid:
        # Insert data into the database
        rights.insert_one(data)

        # Update the inserted data
        rights.update_one({"_id": data["_id"]}, {"$set": {
            "capRights.drmNumber": secrets.token_hex(8),
            "tshirtRights.drmNumber": secrets.token_hex(8),
            "hoodieRights.drmNumber": secrets.token_hex(8),
            "mugRights.drmNumber": secrets.token_hex(8),
            "isAdminVerified": bool(False)
        }})
    
        return "Rights Requested"
    
    return "Please enter valid data for at least one category or single data"




def get_nftRightsRequest():
    from config.db import rights
    lst=[]
    right=rights.find()
    if right:
        for item in right:
            item["_id"]=str(item["_id"])
            lst.append(item)
        return lst
    else:
        return "No Rights"

def patch_NftRights(id,data):
    from config.db import rights, user, admin
    data = dict(data)
    
    #Check Admin is valid using unique id
    if admin.find_one({"_id":ObjectId(id)}):
        
        #Check if any Rights are there or not
        r=rights.find_one({"_id": ObjectId(data["rightsId"])})
        if r:
            
            #Check if rights are already given or not
            if r["capRights"]["rightsGiven"]==False:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set":{"capRights.rightsGiven": data["capRights"]["rightsGiven"]}})
            # else: 
                # return "Cap Rights already Given"
            if r["tshirtRights"]["rightsGiven"]==False:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set":{"tshirtRights.rightsGiven": data["tshirtRights"]["rightsGiven"]}})
            # else:
                # return "tshirt Rights already Given"
            if r["hoodieRights"]["rightsGiven"]==False:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set":{"hoodieRights.rightsGiven": data["hoodieRights"]["rightsGiven"]}})
            # else:
                # return "tshirt Rights already Given"
            if r["mugRights"]["rightsGiven"]==False:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set":{"mugRights.rightsGiven": data["mugRights"]["rightsGiven"]}})
            # else:
                # return "tshirt Rights already Given"
            rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set":{"isAdminVerified": data["isAdminVerified"]}})
            
            #Code to give Rights
            if data["capRights"]["rightsGiven"]==True:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set": {"capRights.licenseDate":datetime.now()}})
            if data["tshirtRights"]["rightsGiven"]==True:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set": {"tshirtRights.licenseDate":datetime.now()}})
            if data["hoodieRights"]["rightsGiven"]==True:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set": {"hoodieRights.licenseDate":datetime.now()}})
            if data["mugRights"]["rightsGiven"]==True:
                rights.update_one({"_id": ObjectId(data["rightsId"])}, {"$set": {"mugRights.licenseDate":datetime.now()}})
            return "Rights Given"
        else:
            return "Invalid Right ID"
    else:
        return "Invalid Admin"
    
def get_Nft(userID):
    from config.db import nft
    lst=[]
    data=nft.find_one({"userID":userID})
    if data:
        for i in data['nftMetaData']['nfts']:
            # i["_id"]=str(i["_id"])
            # i["userID"]=str(i["userID"])

            lst.append(Nft_filter_schema(i))
        return lst
    else:
        return "Invalid NFT ID"

def Nft_filter_schema(item):
    return {
        "name":item['name'],
        "cached_file_url":item['cached_file_url'],
    }

def post_UploadMeta(nft_data):
    # Import your database connection or model here
    from config.db import nft

    try:
        # Convert the Pydantic model instance to a dictionary
        nft_data_dict = nft_data.dict()

        # Insert the NFT metadata into the "nft" collection
        inserted_result = nft.insert_one(nft_data_dict)

        # Check if the insertion was successful
        if inserted_result.acknowledged:
            return "NFT metadata uploaded successfully."
        else:
            return "Failed to upload NFT metadata."
    except Exception as e:
        # Log internal errors
        logging.error(f"Database insertion error: {e}")
        return "Failed to upload NFT metadata."

