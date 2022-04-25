import json
import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
gamemap = ['white']*100
users_timing = []
users_waitings = []
class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        user = str(self.scope['user'])
        block=False
        finded = -1
        for i in users_timing:
            if i[0]==user:
                block=True
        if block==False:
            users_timing.append([user,int(self.scope['client'][1])])
            for j in range(len(users_waitings)):
                if users_waitings[j][0]==str(self.scope['user']):
                    finded=j
            if finded==-1:
                users_waitings.append([str(self.scope['user']),0])
            print(users_timing)
            print(users_waitings)
            self.send(text_data=json.dumps({
                'type':'connection_established',
                'message':gamemap,
                'wait': str(users_waitings[int(finded)][1])
            }))
        else:
            self.send(text_data=json.dumps({
                'type':'disconnect'
            }))
            self.close()
    def disconnect(self,code):
        for j in range(len(users_timing)):
            try:
                if users_timing[j][0]==str(self.scope['user']):
                    users_timing.remove(users_timing[j])
                    print(users_timing)
                    break
            except:
                break
    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type']=='game_message':
            for i in range(len(users_waitings)):
                if users_waitings[i][0]==str(self.scope['user']):
                    timing = users_waitings[i][1]
                    break
            if int(datetime.datetime.now().timestamp())-30>=timing and gamemap[int(text_data_json['id'])]!=text_data_json['color']:
                color = text_data_json['color']
                elemid = text_data_json['id']
                message = text_data_json['message']
                user = text_data_json['user']
                gamemap[int(elemid)] = color
                for j in range(len(users_waitings)):
                    if users_waitings[j][0]==user:
                        if user=="pixeladmin":
                            users_waitings[j][1] = 0
                        else:
                            sec = int(datetime.datetime.now().timestamp())
                            users_waitings[j][1]=sec
                            self.send(text_data=json.dumps({
                                'type':'game_wait',
                                'wait': users_waitings[j][1]
                            }))
                        break
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'game_message',
                        'message': message,
                        'color': color,
                        'id':elemid
                    }
                )
    def game_message(self,event):
        message = event['message']
        mestype = event['type']
        color = event['color']
        elemid = event['id']

        self.send(text_data=json.dumps({
            'type':mestype,
            'message': message,
            'color': color,
            'id':elemid
        }))
