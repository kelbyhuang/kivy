from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import re,requests
class MyGrid(GridLayout):
    def __init__(self,**kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.inside =GridLayout()
        self.inside.cols = 2
        self.inside.add_widget(Label(text ='请输入抖音分享链接：',font_name='SimHei.ttf'))
        self.name = TextInput(font_name='SimHei.ttf')
        self.inside.add_widget(self.name)
        self.add_widget(self.inside)
        self.cols = 1
        self.submit = Button(text = '点击下载',font_size = 40,font_name='SimHei.ttf')
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)
    

    def pressed(self,instance):
        share = self.name.text
        pat = '(https://v.douyin.com/.*?/)' 
        url = re.compile(pat).findall(share)[0]  #正则匹配分享链接
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3904.108 Safari/537.36'}
        response = requests.get(url, headers=headers,allow_redirects=True)
        pat = 'video/(.*?)\/\?'
        item_id = re.findall(pat,response.url)[0]
        item_link = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}'
        response = requests.get(item_link,headers = headers)
        play_url = response.json()['item_list'][0]['video']['play_addr']['url_list'][0]
        dlink = play_url.replace('playwm','play')
        headers = {'user-agent':'Mozilla/5.0 (Android5.1.1) AppleWebKit/537. 36 (KHTML, like Gecko) Chrome/41. 0.2225.0 Safari/537. 36'}
        r = requests.get(dlink, headers=headers)
        with open(item_id+".mp4", 'wb')as file:
            file.write(r.content)
        print("===>视频下载完成！")



class MyApp(App):
    def build(self):
        return MyGrid()
if __name__=='__main__':
    MyApp().run()
