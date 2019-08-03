from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from jsonschema import validate
import base64
import os 
from datetime import datetime



def cr_log(in_date, in_ip, in_status):
   with open('access.logs', 'a+') as fl:
       fl.write(in_date + "::" + in_ip + "::" + in_status + '\n')


def cr_dir(dir_name):
   if not os.path.exists(dir_name):
    os.makedirs(dir_name)
   return 0
    

def save_img(in_img, in_path):
    decoded_img = base64.b64decode(in_img)
    with open(in_path + '/three_bear.jpg', 'wb') as cnkd:
        cnkd.write(decoded_img)
    return 0

@api_view(['POST'])

def img_saver(request):

   
    """
       POST TO SAVE some .img file
		
    
    """


    schema  = {
      "type" : "object",
      "properties" : {
         "title" : {"type" : "string"},
         "img" : {"type" : "string"},
     },
    }

    ip = request.META['REMOTE_ADDR']
    str_time = datetime.now().strftime('%Y-%m-%d %H:%m:%S')
    print(str_time)
    f = request.data  
    title = f['title']
    img = f['img']
    

    try:
        validate(instance={"title" : title, "img" : img}, schema=schema)
        assert 0 == cr_dir(title)
        assert 0 == save_img(img,title)
        cr_log(str_time, ip, "200")
        return Response(status=200)

    except Exception as error:
        cr_log(str_time, ip, "400")
        return Response(status=400)
       

    
    
     	    

    
