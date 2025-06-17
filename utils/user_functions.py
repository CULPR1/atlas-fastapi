from config.init import client,profile,connect_error,operate_error

def dict_profile(user_id , password , role , name = None ):
    return {
        "user_id" : user_id.strip(),
        "password" : password.strip(),
        "name" : name,
        "role" : role.lower(),
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







