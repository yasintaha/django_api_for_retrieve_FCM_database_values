from django.shortcuts import render
from rest_framework.response import  Response
from rest_framework import status
from rest_framework.views import APIView
import pyrebase

#FCM credentials
config = {
    "apiKey" : "<api_key>",
    "authDomain" : "<auth_Domain>",
    "databaseURL" : "<database_URL>",
    "projectId" : "<project_Id>",
    "storageBucket" : "<storage_Bucket>",
    "messagingSenderId" : "<messaging_SenderId>"
  }


# firebase = pyrebase.initialize_app(config)
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()

database = firebase.database()

class get_FCM_data_view(APIView):
    def get(slef,request):
        # Here i am takiing manual email,password you can get this by IsAuthenticated user request to get the user FCM token
        email = 'abc@gmail.com'
        password = '123456789'

        try:
            # signing in the user for idToken of FCM
            user = authe.sign_in_with_email_and_password(email,password)
            user_fcm_token = user['idToken']
            print(user_fcm_token)
        except:
            print("unable to login")   

        # getting the user localID
        id_user = authe.get_account_info(user_fcm_token)
        user_dict = id_user['users']   #users FCM dictonary values
        user_index_for_localId = user_dict[0] #initalizing the index[0] value to get only localId
        user_localId = user_index_for_localId['localId'] #users localId initialization
        b = user_localId

        #getting the value from  FCM database 
        from_fcm_database = database.child('users').child(b).child('reports').shallow().get().val()

        # empty list to append 
        list_items = []

        for i in from_fcm_database:

            list_items.append(i) #appending each value of from_fcm_database in a list_items 

        list_items.sort(reverse=True) #sorting the values to get the latest value first
        print(list_items)

        # empty list varibales for apped
        work = [] 
        progress = []

        for i in list_items:

            wor = database.child('users').child(b).child('reports').child(i).child('work_assigned').get().val() 
            pro = database.child('users').child(b).child('reports').child(i).child('progress').get().val()  

            work.append(wor)    
            progress.append(pro)  

        comb_list = zip(work,progress) #zipping the appended list    

        content = {'message':comb_list}
        return Response(content,status=status.HTTP_200_OK)