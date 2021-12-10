import tweepy


auth = tweepy.OAuthHandler("KHTgJEJT60RFm8K14eq39q06H", "cw2VxeXhLhIEameT1OxVgpuiLoUuzUKbnaZcuywSCQdyGFNJAJ")
auth.set_access_token("1437376736233234433-tR2MmfMyPpkvHHbiWrd9eMoS703uG2", "UGcGGdgLA7ekJX6ct1WTl4SUX6KHlMG3MQtkKIm9bxGNm")

api = tweepy.API(auth)

