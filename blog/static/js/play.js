let user = document.querySelector('.user').textContent 
function waiting(){
    interval = setInterval(function (){
        towait = Math.floor(new Date().getTime() / 1000 ) - time
        if (towait>20){
            document.querySelector('.time').innerHTML = "00:0"+(30-towait)
        }
        if (towait<21){
            document.querySelector('.time').innerHTML = "00:"+(30-towait)
        }
        if (towait>=30){
            document.querySelector('.time').style = 'opacity:0'
            clearInterval(interval)
        }
    },1000)
}
document.querySelector('.user').remove()
let url = `ws://${window.location.host}/ws/socket-server/`
const gameSocket = new WebSocket(url)
mapall = []
gameSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    console.log('Data:',data)
    if (data['type']=='connection_established'){
        for(let i=0;i<=99;i++){
            document.getElementById(i).style = 'background:'+data['message'][i]
            mapall.push(data['message'][i])
        }
        if (30-(Math.floor(new Date().getTime() / 1000 ) - data['wait'])>0){
            time = data['wait']
            document.querySelector('.time').innerHTML = "00:"+(30-(Math.floor(new Date().getTime() / 1000 ) - time))
            document.querySelector('.time').style = 'color:white;opacity:1'
            waiting()
            console.log(time)
        }
    }
    if (data['type']=='game_message'){
        document.getElementById(data['id']).style = 'background:'+data['color']
        mapall[data['id']]=data['color']
    }
    if (data['type']=='game_wait'){
        time = data['wait']
        document.querySelector('.time').innerHTML = "00:"+(30-(Math.floor(new Date().getTime() / 1000 ) - time))
        document.querySelector('.time').style = 'color:white;opacity:1'
        waiting()
    }
    if (data['type']=='disconnect'){
        gameSocket.close()
        document.querySelector('.disconnect').style = 'display:inline'
        document.querySelector('.colors').remove()
        document.querySelector('.table').remove()
        document.querySelector('.pos').remove()
    }
}
for(let i=0; i<=8; i++){
    document.querySelectorAll('.choose-color')[i].style = 'background:'+document.querySelectorAll('.choose-color')[i].classList[0]
}
towait = 30
last = ''
tocolor = 'white'
document.querySelector('.table').addEventListener('mousemove',function(element){
    if (last!=''){
        last.style='background:'+lastback
    }
    lastback = element.path[0].style.background
    last = element.path[0]
    element.path[0].style='background: '+tocolor
    idel = element.path[0].id
    xel = idel%10+1
    yel = Math.floor(idel/10)+1
    document.querySelector('.pos').innerHTML = 'x:'+xel+' y:'+yel
})
document.querySelector('.table').addEventListener('mouseout',function(){
    document.getElementById(last.id).style = 'background:'+mapall[last.id]
    lastback = mapall[last.id]
    document.querySelector('.pos').innerHTML = 'x:'+0+' y:'+0
})
function changecolor(color) {
    document.querySelector('.colors').style = "border-top: 1px solid "+color
    tocolor = color
}
function change(elem){
    lastback = tocolor
    if (towait>=30){
        if (mapall[elem]!=tocolor){
            gameSocket.send(JSON.stringify({
                'message':'Changing area',
                'type':'game_message',
                'color':tocolor,
                'id':elem,
                'user':user
            }))
        }
        else {
            document.querySelector('.warning').innerHTML = 'Клетка уже закрашена этим цветом!'
            document.querySelector('.warning').style = 'opacity:1;z-index:1;'
            setTimeout(()=>document.querySelector('.warning').style = 'opacity:0;z-index;-1',1000)
        }
    }
    else {
        document.querySelector('.warning').innerHTML = 'Вы недавно уже закрасили клетку!'
        document.querySelector('.warning').style = 'opacity:1;z-index:1;'
        setTimeout(()=>document.querySelector('.warning').style = 'opacity:0;z-index;-1',1000)
    }
}