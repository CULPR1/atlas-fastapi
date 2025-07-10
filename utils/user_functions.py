from config.init import client,profile,connect_error,operate_error

def dict_profile(user_id , password , role , name = None ):
    return {
        "user_id" : user_id.strip(),
        "password" : password.strip(),
        "name" : name,
        "role" : role.lower(),
        "balance" : 0.0
    }

def check_user(user_id ):
    if profile.count_documents({"user_id" : user_id}) > 0:
        return "account is there" ,True
    else:
        return "no account with that user_id" , False


def register_user(user_id,password,role,name):
    check_str, check_bool = check_user(user_id)
    if check_bool is False: 
        with client.start_session() as session:
            try:
                result = profile.insert_one(dict_profile(user_id,password,role,name),session=session)
                if result.inserted_id:
                    return f"user {user_id} successfully registered"
                else:
                    return f"user not added"
                # session.commit_transaction()
            except operate_error as e:
                print ("MongoDB error : ", e)
                session.abort_transaction()
            except operate_error as e:
                print ("MongoDB error : ", e)
                session.abort_transaction()
            except Exception as e:
                print ("General error : ", e)
                session.abort_transaction()
    
    else :
        return "account with same user_id is already there, Either login or use another user_id"
            
def login_user(user_id , password ):
    result = list(profile.find({"user_id" : user_id, "password" : password}))
    if profile.count_documents({"user_id" : user_id, "password" : password}) == 1:
        return "Successfully logged in" , result[0]["role"]
    else:
        return "No user of those credentials", None
#print(check_user("mark_123"))

#print(register_user("malcom_234","456","buyer","Malcom"))

#print(login_user("malcom_234","56"))
# # Add first seller
# print("\n=== Registering Sellers ===")
# print("Seller 1:", register_user("seller_001", "sellerpass1", "seller", "John Doe"))
# print("Seller 2:", register_user("seller_002", "sellerpass2", "seller", "Jane Smith"))

# # Add first buyer
# print("\n=== Registering Buyers ===")
# print("Buyer 1:", register_user("buyer_001", "buypass1", "buyer", "Alice Johnson"))
# print("Buyer 2:", register_user("buyer_002", "buypass2", "buyer", "Bob Williams"))

# # Verify all accounts were created
# print("\n=== Verification ===")
# print("Check seller_001:", check_user("seller_001"))
# print("Check seller_002:", check_user("seller_002"))
# print("Check buyer_001:", check_user("buyer_001"))
# print("Check buyer_002:", check_user("buyer_002"))

# # Test login functionality
# print("\n=== Test Logins ===")
# print("Seller 1 login:", login_user("seller_001", "sellerpass1"))
# print("Buyer 1 login:", login_user("buyer_001", "buypass1"))
# print("Failed login test:", login_user("seller_001", "wrongpass"))


