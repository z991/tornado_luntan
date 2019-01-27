import requests

class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    def send_single_sms(self,code, mobile):
        #发送单条短信
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【drf人生记录仪】您购买的{}订单已成功消费，祝您生活愉快！".format(code)
        res = requests.post(url, data={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":text
        })

        return res

if __name__ == "__main__":
    yun_pian = YunPian("57477467cb72b6bac9abc9c327986752")
    res = yun_pian.send_single_sms("梁桂侠", "18033526460")
    print(res.text)

