from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from datetime import date

import psycopg2
import random

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)
CORS(app)
# Channel Access Token
line_bot_api = LineBotApi('516KsFfnTZ7zAfSfGUJhTYt4T2PBnRThlzS5LZ5DApqHpHV/eb4ODPT5aXcWiKkpkwVvXBU/c66yG7WGF/2m1HTRZdXIOZiVF1LXBBMEyGulfhuyYXRIMTkWvXA8H0NJM1/rF2P/ILtBkEjKrloqywdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4506bcd2d49c87a004060cae9d223e7e')

INFO_LEVEL = ImageSendMessage(
        original_content_url = 'https://linefresh-tiehua.herokuapp.com/static/images/task_member.png',
        preview_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/task_member.png'
    )
INFO_TIEHUA_GO = ImageSendMessage(
        original_content_url = 'https://linefresh-tiehua.herokuapp.com/static/images/tiehua_go.png',
        preview_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/tiehua_go.png'
    )
INFO_SHOP = TemplateSendMessage(
        alt_text = '商家資訊',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/tiehua_map.jpg',
            title = '商家資訊',
            text = '選擇想查看的商家類型',
            actions = [
                MessageTemplateAction(label = '餐廳', text = '餐廳'),
                MessageTemplateAction(label = '住宿', text = '住宿'),
                MessageTemplateAction(label = '伴手禮', text = '伴手禮')
            ]
        )
    )
INFO_RESTAURANT = TemplateSendMessage(
        alt_text = '餐廳',
        template = ButtonsTemplate(
            thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/restaurent.jpg',
            title = '餐廳類型',
            text = '選擇想查看的餐廳類型',
            actions = [
                MessageTemplateAction(label = '飲料', text = '飲料'),
                MessageTemplateAction(label = '小吃', text = '小吃'),
                MessageTemplateAction(label = '咖啡店/早午餐', text = '咖啡店/早午餐'),
                MessageTemplateAction(label = '餐酒館', text = '餐酒館')
            ]
        )
    )
INFO_DRINK = TemplateSendMessage(
        alt_text = '飲料',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/lao_dong_fang.jpg',
                    title = '老東芳青草茶',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/486249286946791179?utm_campaign=486249286946791179&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/dongfunherbal')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/follow_milk.jpg',
                    title = '花惹蜜 Follow Milk',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/486248109765038421?utm_campaign=486248109765038421&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/FollowMilk.tw')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/ding_go.jpg',
                    title = '叮哥茶飲-台東屈臣氏店',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/484790920194074706?utm_campaign=484790920194074706&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/DING-GO-%E5%8F%AE%E5%93%A5%E8%8C%B6%E9%A3%B2%E5%8F%B0%E6%9D%B1%E5%B1%88%E8%87%A3%E6%B0%8F%E9%96%80%E5%B8%82-328249917829603')
                    ]
                )
            ]
        )
    )
INFO_SNACK = TemplateSendMessage(
        alt_text = '小吃',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/hsiang_chi.jpg',
                    title = '香琪鴨肉',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/572168160510221752?utm_campaign=572168160510221752&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/%E9%A6%99%E7%90%AA%E9%B4%A8%E8%82%89-822868161166378/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/mr_cow.png',
                    title = '烤大爺',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/486251073846121999?utm_campaign=486251073846121999&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/%E7%83%A4%E5%A4%A7%E7%88%BA-%E5%8F%B0%E6%9D%B1%E9%90%B5%E8%8A%B1%E6%96%B0%E8%81%9A%E8%90%BD-139132060117831/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/hang_tien.jpg',
                    title = '韓天食府',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/651192165128475034?utm_campaign=651192165128475034&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/%E9%9F%93%E5%A4%A9%E9%A3%9F%E5%BA%9C-166963530538292/'
                        )
                    ]
                )
            ]
        )
    )
INFO_BRUNCH = TemplateSendMessage(
        alt_text = '咖啡店/早午餐',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/six_inch.jpg',
                    title = '六吋盤早午餐',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/656248336109542165?utm_campaign=656248336109542165&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/%E5%85%AD%E5%90%8B%E7%9B%A4%E6%97%A9%E5%8D%88%E9%A4%90-%E5%8F%B0%E6%9D%B1%E5%BA%97-2177225652311042/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/time_station.jpg',
                    title = '時光車站',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/707009872612300234?utm_campaign=707009872612300234&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/waitingfortimeT/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/toast.jpg',
                    title = '吐司代表',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/486247096979036893?utm_campaign=486247096979036893&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/pnw2043p/'
                        )
                    ]
                )
            ]
        )
    )
INFO_BISTRO = TemplateSendMessage(
        alt_text = '餐酒館',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/love_land.jpg',
                    title = 'LoveLand專情島',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://liff.line.me/1582347558-VdW5GZDw/detail/738502408874761666?utm_campaign=738502408874761666&utm_medium=CopyURL&utm_source=Share'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/LOVELAND-%E5%B0%88%E6%83%85%E5%B3%B6-100776048285302/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/craft_beer.png',
                    title = '溫度釀製所',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/temperaturebrewery/')
                    ]
                )
            ]
        )
    )
INFO_HOTEL = TemplateSendMessage(
        alt_text = '住宿',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/traveller_inn.jpg',
                    title = '旅人驛站鐵花文創館',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/detail/486259086564792106'),
                        URIAction(label = '官方網站', uri = 'http://www.traveler-inn.com/hotel.php?id=27')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/sheraton.jpg',
                    title = '台東桂田喜來登酒店',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/detail/486259092302600073'),
                        URIAction(label = '官方網站', uri = 'https://www.sheraton-taitung.com')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/yes_hotel.png',
                    title = '樂知旅店',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點',uri = 'https://spot.line.me/detail/486259039764747372'),
                        URIAction(label = '官方網站', uri = 'https://www.yeshotel.com.tw/tw/index.html'
                        )
                    ]
                )
            ]
        )
    )
INFO_GIFT = TemplateSendMessage(
        alt_text = '伴手禮',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/wu_ma_ma.jpg',
                    title = '台東吳家媽媽地瓜酥',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/台東吳家媽媽地瓜酥-263410203681032/')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/hong_ding.jpg',
                    title = '鴻鼎記食品行',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/'),
                        URIAction(label = '官方網站', uri = 'http://hongdingji.livetaitung.tw')
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/chin_zei.jpg',
                    title = '青澤琪瑪酥 伴手禮專賣店-鐵花館',
                    text = '商家資訊',
                    actions = [
                        URIAction(label = 'Line 熱點', uri = 'https://spot.line.me/'),
                        URIAction(label = '官方網站', uri = 'https://www.facebook.com/chingtse.tiehua/')
                    ]
                )
            ]
        )
    )
INFO_TASK = TextSendMessage(
        text = '以下是今日任務列表$\n試著點選下方按鈕，完成任務並獲取積分吧！$',
        emojis = [
            {"index": 9,  "productId": "5ac22b23040ab15980c9b44d", "emojiId": "030"},
            {"index": 31, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "088"}
        ]
    )
TASK_LIST = TemplateSendMessage(
        alt_text = '任務列表',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/sign_in.png',
                    title = '每日簽到',
                    text = '點擊簽到按鈕即可獲得10點',
                    actions = [PostbackAction(label = '點擊簽到', data = 'sign_in')]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/line_music.png',
                    title = '聆聽歌單',
                    text = '點選任一歌曲播放5秒即可獲得10點',
                    actions = [URIAction(label = '前往聆聽', uri = 'https://liff.line.me/1656598921-KN0L4QqG')]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/invoice.png',
                    title = '登錄發票',
                    text = '登錄消費發票即可獲得10點',
                    actions = [URIAction(label = '登錄發票', uri = 'https://liff.line.me/1656598921-Xr4AEy3Y')]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/bonus.png',
                    title = '積分寶箱',
                    # text = '完成前三項任務，即可領取寶箱隨機獲得10-50點積分',
                    text = '領取寶箱，隨機獲得10-50點積分',
                    actions = [PostbackAction(label = '領取寶箱', data = 'bonus')]
                )
            ]
        )
    )
COUPON_LIST = TemplateSendMessage(
        alt_text = '積分兌換',
        template = CarouselTemplate(
            columns = [
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/discount.png',
                    title = '商家折扣',
                    text = '以積分10點兌換',
                    actions = [PostbackAction(label = '兌換優惠', data = 'discount')]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/line_points.png',
                    title = 'LINE POINTS 30點',
                    text = '以積分10點兌換',
                    actions = [PostbackAction(label = '兌換優惠', data = 'line_points')]
                ),
                CarouselColumn(
                    thumbnail_image_url = 'https://linefresh-tiehua.herokuapp.com/static/images/draw.png',
                    title = '抽獎券',
                    text = '以積分10點兌換',
                    actions = [PostbackAction(label = '兌換優惠', data = 'draw')]
                )
            ]
        )
    )
USER_LEVELS = {1: "銅花", 2: "銀花", 3: "金花"}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
@handler.add(FollowEvent)
def handle_follow(event):
    # check user
    user_id = event.source.user_id
    print(f"[FOLLOW] {user_id}")
    sql_check_user = f"SELECT FROM users WHERE userid = \'{user_id}\'"
    result = sql_query_fetchall(sql_check_user)
    print(f"[SQL] {sql_check_user} => {result}")
    # if user not added
    if not result:
        # add user
        sql = f"INSERT INTO users VALUES(\'{user_id}\');"
        sql_query(sql)
        print(f"[FOLLOW] {user_id}")
    # reply message
    user_name = line_bot_api.get_profile(user_id).display_name
    # info_follow = TextSendMessage(
    #         text = f"Hi, {user_name}，很開心終於和你在這裡相遇$\n\n從現在起，我們將陪你一起展開「音joy鐵花慢活圈」的奇妙之旅！\n\n點開節目表可以看到鐵花歌手的表演時間，點開商家資訊可以查詢鐵花商圈的餐廳、住宿跟伴手禮店家，也可以連結到他們的 LINE 熱點和官方網站呦～$\n\n最特別的是點進 LINE MUSIC 專區就可以藉由聽音樂得到各種回饋$\n\n現在就來看看有哪些任務，還有你累積了多少積分吧！$",
    #         emojis = [
    #             {"index": len(user_name) + 17,  "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "094"},
    #             {"index": len(user_name) + 123, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "035"},
    #             {"index": len(user_name) + 161, "productId": "5ac22e85040ab15980c9b44f", "emojiId": "033"},
    #             {"index": len(user_name) + 188, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "011"}
    #         ]
    #     )
    info_follow = TextSendMessage(
            text = f"Hi, {user_name}，很開心終於和你在這裡相遇\n\n從現在起，我們將陪你一起展開「音joy鐵花慢活圈」的奇妙之旅！\n\n點開節目表可以看到鐵花歌手的表演時間，點開商家資訊可以查詢鐵花商圈的餐廳、住宿跟伴手禮店家，也可以連結到他們的 LINE 熱點和官方網站呦～\n\n最特別的是點進 LINE MUSIC 專區就可以藉由聽音樂得到各種回饋\n\n現在就來看看有哪些任務，還有你累積了多少積分吧！"
        )
    reply_message = [info_follow, INFO_LEVEL, INFO_TIEHUA_GO]
    line_bot_api.reply_message(event.reply_token, reply_message)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get info
    user_id = event.source.user_id
    message_text = event.message.text
    print(f"[MESSAGE] {user_id} => {message_text}")
    # handle message
    if message_text == '商家資訊':
        reply_message = INFO_SHOP
    elif message_text == '餐廳':
        reply_message = INFO_RESTAURANT
    elif message_text == '飲料':
        reply_message = INFO_DRINK
    elif message_text == '小吃':
        reply_message = INFO_SNACK
    elif message_text == '咖啡店/早午餐':
        reply_message = INFO_BRUNCH
    elif message_text == '餐酒館':
        reply_message = INFO_BISTRO
    elif message_text == '住宿':
        reply_message = INFO_HOTEL
    elif message_text == '伴手禮':
        reply_message = INFO_GIFT
    elif message_text == '任務會員總表':
        reply_message = INFO_LEVEL
    elif message_text == '任務':
        reply_message = [INFO_TASK, TASK_LIST]
    elif message_text == '積分兌換':
        # get user data
        user_name = line_bot_api.get_profile(user_id).display_name
        user = get_user(user_id)
        user_level = user[1]
        user_points = user[2]
        user_totalpoints = user[3]
        # reply_message
        if user_level == '銅花':
            # info_coupon = TextSendMessage(
            #         text= f"Hi, {user_name}，你目前的等級為「銅花$」!\n累積積分為{user_points}點，距離升級銀花會員還需要{30 - user_totalpoints}點\n\n$點選按鈕兌換下列優惠$",
            #         emojis = [
            #             {"index": len(user_name) + 15,  "productId": "5ac218e3040ab15980c9b43c", "emojiId": "204"},
            #             {"index": len(user_name) + len(str(user_points)) + len(str(30 - user_totalpoints)) + 40, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "243"},
            #             {"index": len(user_name) + len(str(user_points)) + len(str(30 - user_totalpoints)) + 51, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "242"}
            #         ]
            #     )
            info_coupon = TextSendMessage(
                    text= f"Hi, {user_name}，你目前的等級為「銅花」!\n累積積分為{user_points}點，距離升級銀花會員還需要{30 - user_totalpoints}點\n\n點選按鈕兌換下列優惠"
                )
        elif user_level == '銀花':
            # info_coupon = TextSendMessage(
            #         text= f"Hi, {user_name}，你目前的等級為「銀花$」!\n累積積分為{user_points}點，距離升級銀花會員還需要{50 - user_totalpoints}點\n\n$點選按鈕兌換下列優惠$",
            #         emojis = [
            #             {"index": len(user_name) + 15,  "productId": "5ac218e3040ab15980c9b43c", "emojiId": "203"},
            #             {"index": len(user_name) + len(str(user_points)) + len(str(50 - user_totalpoints)) + 40, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "243"},
            #             {"index": len(user_name) + len(str(user_points)) + len(str(50 - user_totalpoints)) + 51, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "242"}
            #         ]
            #     )
            info_coupon = TextSendMessage(
                    text= f"Hi, {user_name}，你目前的等級為「銀花」!\n累積積分為{user_points}點，距離升級銀花會員還需要{50 - user_totalpoints}點\n\n點選按鈕兌換下列優惠"
                )
        elif user_level == '金花':
            # info_coupon = TextSendMessage(
            #         text= f"Hi, {user_name}，你目前的等級為「金花$」!\n累積積分為{user_points}點\n\n$點選按鈕兌換下列優惠$",
            #         emojis = [
            #             {"index": len(user_name) + 15,  "productId": "5ac218e3040ab15980c9b43c", "emojiId": "202"},
            #             {"index": len(user_name) + len(str(user_points)) + 27, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "243"},
            #             {"index": len(user_name) + len(str(user_points)) + 38, "productId": "5ac1bfd5040ab15980c9b435", "emojiId": "242"}
            #         ]
            #     )
            info_coupon = TextSendMessage(
                    text= f"Hi, {user_name}，你目前的等級為「金花」!\n累積積分為{user_points}點\n\n點選按鈕兌換下列優惠"
                )
        reply_message = [info_coupon, COUPON_LIST]
    else:
        reply_message = TextSendMessage(text= message_text)
    # reply message
    line_bot_api.reply_message(event.reply_token, reply_message)
@handler.add(PostbackEvent)
def handle_postback(event):
    # get info
    user_id = event.source.user_id
    task = event.postback.data
    print(f"[MESSAGE] {user_id} => {task}")
    # handle task
    if task == 'sign_in':
        reply_message = sign_in(user_id)
    elif task == 'bonus':
        reply_message = bonus(user_id)
    elif task == 'discount':
        reply_message = discount(user_id)
    elif task == 'line_points':
        reply_message = line_points(user_id)
    elif task == 'draw':
        reply_message = draw(user_id)
    # reply message
    line_bot_api.reply_message(event.reply_token, reply_message)

def sign_in(user_id):
    # get info
    today = int(date.today().strftime("%Y%m%d"))
    get_user(user_id)
    # check signIn
    sql_check_sign_in = f"SELECT FROM done WHERE userid = \'{user_id}\' AND taskname = \'signIn\' AND date = {today};"
    result = sql_query_fetchall(sql_check_sign_in)
    print(f"[SQL] CHECK (signIn) => {result}")
    # if signIn not yet done
    if not result:
        # update points
        sql_done_signIn = f"INSERT INTO done (userid, taskname, date) VALUES (\'{user_id}\', \'signIn\', {today});"
        sql_query(sql_done_signIn)
        sql_update_points = f"UPDATE users SET points = points + 10, totalpoints = totalpoints + 10 WHERE userId=\'{user_id}\';"
        sql_query(sql_update_points)
        # update level
        # reply message
        reply_message = update_user_level(user_id, '每日簽到', 10)
    else:
        reply_message = [TextSendMessage(text= "你今日已完成過此任務囉，快去試試其他的！"), TASK_LIST]
    return reply_message
@app.route("/listening", methods = ['POST'])
def listening():
    # get info
    data = request.get_json()
    user_id = data.get('user_id')
    today = int(date.today().strftime("%Y%m%d"))
    get_user(user_id)
    # check listening
    sql_check_listening = f"SELECT FROM done WHERE userid = \'{user_id}\' AND taskname = \'listening\' AND date = {today};"
    result = sql_query_fetchall(sql_check_listening)
    print(f"[SQL] CHECK (listening) => {result}")
    # if listening not yet done
    if not result:
        # update points
        sql_done_listening = f"INSERT INTO done (userid, taskname, date) VALUES (\'{user_id}\', \'listening\', {today});"
        sql_query(sql_done_listening)
        sql_update_points = f"UPDATE users SET points = points + 10, totalpoints = totalpoints + 10 WHERE userId=\'{user_id}\';"
        sql_query(sql_update_points)
        # update level
        # reply message
        reply_message = update_user_level(user_id, '聆聽歌單', 10)
        line_bot_api.push_message(user_id, reply_message)
    return jsonify({'result': 1})
@app.route("/invoice", methods = ["POST"])
def invoice():
    # get info
    data = request.get_json()
    user_id = data.get('user_id')
    invoice_num = data.get('invoice_num')
    today = int(date.today().strftime("%Y%m%d"))
    get_user(user_id)
    # check invoice
    sql_check_invoice = f"SELECT FROM invoice WHERE userid = \'{user_id}\' AND invoicenum = \'{invoice_num}\'"
    result = sql_query_fetchall(sql_check_invoice)
    # if invoice not yet done
    if not result:
        # update points
        sql_done_invoice = f"INSERT INTO done (userid, taskname, date) VALUES (\'{user_id}\', \'invoice\', {today});"
        sql_query(sql_done_invoice)
        sql_invoice = f"INSERT INTO invoice (userid, invoicenum) VALUES (\'{user_id}\', \'{invoice_num}\');"
        sql_query(sql_invoice)
        sql_update_points = f"UPDATE users SET points = points + 10, totalpoints = totalpoints + 10 WHERE userId=\'{user_id}\';"
        sql_query(sql_update_points)
        # update level
        # reply message
        reply_message = update_user_level(user_id, '登錄發票', 10)
        line_bot_api.push_message(user_id, reply_message)
        return jsonify({'result': True})
    else:
        return jsonify({'result': False})
def bonus(user_id):
    # get info
    today = int(date.today().strftime("%Y%m%d"))
    user_name = line_bot_api.get_profile(user_id).display_name
    get_user(user_id)
    # check bonus
    sql_check_bonus = f"SELECT taskname FROM done WHERE userid = \'{user_id}\' AND date = {today};"
    result = [row[0] for row in sql_query_fetchall(sql_check_bonus)]
    print(f"[SQL] CHECK (bonus) => {result}")
    # if bonus not yet done
    if not 'bonus' in result:
        # # if other tasks done
        # if 'signIn' in result and 'listening' in result and 'invoice' in result:
        #     # update points
        #     sql_done_bonus = f"INSERT INTO done (userid, taskname, date) VALUES (\'{user_id}\', \'bonus\', {today});"
        #     sql_query(sql_done_bonus)
        #     random_points = random.randint(1, 5) * 10
        #     sql_update_points = f"UPDATE users SET points = points + {random_points}, totalpoints = totalpoints + {random_points} WHERE userId=\'{user_id}\';"
        #     sql_query(sql_update_points)
        #     # update level
        #     # reply message
        #     reply_message = [
        #             update_user_level(user_id, '領取寶箱', random_points), 
        #             TextSendMessage(
        #                 text= f"Hi, {user_name}，你已完成今天所有任務了喔$\n明天再回來繼續完成任務吧！$$\n我們在「音joy鐵花慢活圈」等你喔$",
        #                 emojis = [
        #                     {"index": len(user_name) + 17,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
        #                     {"index": len(user_name) + 32, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"},
        #                     {"index": len(user_name) + 33, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"},
        #                     {"index": len(user_name) + 52, "productId": "5ac21ae3040ab15980c9b440", "emojiId": "133"}
        #                 ]
        #             )
        #         ]
        # else:
        #     reply_message = TextSendMessage(
        #             text= f"先去完成前面三項任務，再來領取寶箱吧$",
        #             emojis = [{"index": 18,  "productId": "5ac21ae3040ab15980c9b440", "emojiId": "073"},]
        #         )

        # if other tasks done
        if 'signIn' in result or 'listening' in result or 'invoice' in result:
            # update points
            sql_done_bonus = f"INSERT INTO done (userid, taskname, date) VALUES (\'{user_id}\', \'bonus\', {today});"
            sql_query(sql_done_bonus)
            random_points = random.randint(1, 5) * 10
            sql_update_points = f"UPDATE users SET points = points + {random_points}, totalpoints = totalpoints + {random_points} WHERE userId=\'{user_id}\';"
            sql_query(sql_update_points)
            # update level
            # reply message
            reply_message = update_user_level(user_id, '領取寶箱', random_points)
        else:
            reply_message = TextSendMessage(
                    text= f"先去完成前面三項任務，再來領取寶箱吧$",
                    emojis = [{"index": 18,  "productId": "5ac21ae3040ab15980c9b440", "emojiId": "073"},]
                )

    else:
        # reply_message = TextSendMessage(
        #         text= f"Hi, {user_name}，你已完成今天所有任務了喔$\n明天再回來繼續完成任務吧！$$\n我們在「音joy鐵花慢活圈」等你喔$",
        #         emojis = [
        #             {"index": len(user_name) + 17, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
        #             {"index": len(user_name) + 32, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"},
        #             {"index": len(user_name) + 33, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"},
        #             {"index": len(user_name) + 52, "productId": "5ac21ae3040ab15980c9b440", "emojiId": "133"}
        #         ]
        #     )
        reply_message = [TextSendMessage(text= "你今日已完成過此任務囉，快去試試其他的！"), TASK_LIST]
    return reply_message
def discount(user_id):
    # get info
    user = get_user(user_id)
    user_points = user[2]
    # if points enough
    if user_points >= 10:
        # update points
        sql_exchange = f"UPDATE users SET points = points - 10 WHERE userId = \'{user_id}\';"
        sql_query(sql_exchange)
        # TODO 圖片存進來
        # reply message
        qrcode_img = ImageSendMessage(
                original_content_url='https://i.ibb.co/zhzhWVk/0-YS2-Y28-DZP.png',
                preview_image_url='https://i.ibb.co/zhzhWVk/0-YS2-Y28-DZP.png'
            )
        reply_message = [TextSendMessage(text= f"[兌換成功] 商家折扣\n剩餘點數：{user_points - 10}點"), qrcode_img]
    else:
        reply_message = [TextSendMessage(text= "積分不足，去完成任務吧"), TASK_LIST]
    return reply_message
def line_points(user_id):
    # get info
    user = get_user(user_id)
    user_points = user[2]
    # if points enough
    if user_points >= 10:
        # update points
        sql_exchange = f"UPDATE users SET points = points - 10 WHERE userId = \'{user_id}\';"
        sql_query(sql_exchange)
        # reply message
        serial_number = random_serial()
        reply_message = TextSendMessage(text= f"[兌換成功] Line points 30 點\n兌換序號： {serial_number}\n剩餘點數：{user_points-10}點")
    else:
        reply_message = [TextSendMessage(text= "積分不足，去完成任務吧"), TASK_LIST]
    return reply_message
def draw(user_id):
    # get info
    user = get_user(user_id)
    user_points = user[2]
    # if points enough
    if user_points >= 10:
        # update points
        sql_exchange = f"UPDATE users SET points = points - 10 WHERE userId = \'{user_id}\';"
        sql_query(sql_exchange)
        sql_max_couponnum = f"SELECT MAX(couponnum) FROM coupon;"
        result = sql_query_fetchall(sql_max_couponnum)[0][0]
        couponnum = 0 if result == None else result
        sql_coupon = f"INSERT INTO coupon (couponnum, userid) VALUES ({couponnum + 1}, \'{user_id}\');"
        sql_query(sql_coupon)
        # reply message
        reply_message = TextSendMessage(text= f"[兌換成功] 抽獎券\n抽獎序號： {couponnum + 1:03}\n剩餘點數：{user_points-10}點")
    else:
        reply_message = [TextSendMessage(text= "積分不足，去完成任務吧"), TASK_LIST]
    return reply_message

def get_user(user_id):
    sql_get_user = f"SELECT userid, userlevel, points, totalpoints FROM users WHERE userid = \'{user_id}\';"
    result = sql_query_fetchall(sql_get_user)
    print(f"[SQL] {sql_get_user} => {result}")
    if not result:
        sql_new_user = f"INSERT INTO users VALUES(\'{user_id}\');"
        sql_query(sql_new_user)
        user_level = USER_LEVELS[1]
        user_points = 0
        user_totalpoints = 0
    else:
        user = result[0]
        user_level = user[1]
        user_level = USER_LEVELS[user_level]
        user_points = user[2]
        user_totalpoints = user[3]
    user = [user_id, user_level, user_points, user_totalpoints]
    return user
def update_user_level(user_id, task, task_points):
    # get info
    user = get_user(user_id)
    user_level = user[1]
    user_points = user[2]
    user_totalpoints = user[3]
    # check update level
    if task == '領取寶箱':
        if user_level == '銅花':
            if user_totalpoints >= 30 and user_totalpoints < 50:
                sql_update_level = f"UPDATE users SET userlevel = 2 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為銀花會員！\n距離金花會員還需要{50 - user_totalpoints}點",
                        emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                    )
            elif user_totalpoints >= 50:
                sql_update_level = f"UPDATE users SET userlevel = 3 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為金花會員！",
                        emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                    )
            else:
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n距離銀花會員還需要{30 - user_totalpoints}點",
                        emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                    )
        elif user_level == '銀花':
            if user_totalpoints >= 50:
                sql_update_level = f"UPDATE users SET userlevel = 3 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為金花會員！",
                        emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                    )
            else:
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n距離金花會員還需要{50 - user_totalpoints}點",
                        emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                    )
        elif user_level == '金花':
            reply_message =     TextSendMessage(
                    text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$",
                    emojis = [{"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"}]
                )
    else:
        if user_level == '銅花':
            if user_totalpoints >= 30 and user_totalpoints < 50:
                sql_update_level = f"UPDATE users SET userlevel = 2 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為銀花會員！\n距離金花會員還需要{50 - user_totalpoints}點\n繼續完成下一個任務吧！$",
                        emojis = [
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + len(str(50 - user_totalpoints)) + 53, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                        ]
                    )
            elif user_totalpoints >= 50:
                sql_update_level = f"UPDATE users SET userlevel = 3 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為金花會員！\n繼續完成下一個任務吧！$",
                        emojis = [
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 42, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                        ]
                    )
            else:
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n距離銀花會員還需要{30 - user_totalpoints}點\n繼續完成下一個任務吧！$",
                        emojis = [
                                {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                                {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + len(str(30 - user_totalpoints)) + 42, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                            ]
                    )
        elif user_level == '銀花':
            if user_totalpoints >= 50:
                sql_update_level = f"UPDATE users SET userlevel = 3 WHERE userId=\'{user_id}\';"
                sql_query(sql_update_level)
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n成功升級為金花會員！\n繼續完成下一個任務吧！$",
                        emojis = [
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 42, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                        ]
                    )
            else:
                reply_message = TextSendMessage(
                        text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n距離金花會員還需要{50 - user_totalpoints}點\n繼續完成下一個任務吧！$",
                        emojis = [
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                            {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + len(str(50 - user_totalpoints)) + 42, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                        ]
                    )
        elif user_level == '金花':
            reply_message = TextSendMessage(
                    text= f"[任務完成] {task}\n你的積分：{user_points - task_points} -> {user_points}點$\n繼續完成下一個任務吧！$",
                    emojis = [
                        {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 18,  "productId": "5ac223c6040ab15980c9b44a", "emojiId": "038"},
                        {"index": len(task) + len(str(user_points - task_points)) + len(str(user_points)) + 31, "productId": "5ac223c6040ab15980c9b44a", "emojiId": "072"}
                    ]
                )
    return reply_message
def sql_query(sql):
    conn = psycopg2.connect(
            database='d31hmkqi1b3i6l',
            user='eteltzscugyzlf',
            password='d997aff8600c2f245977b12c1729500a6a84577b2f7f99244d1c8557947f230c',
            host='ec2-54-159-244-207.compute-1.amazonaws.com',
            port='5432')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
def sql_query_fetchall(sql):
    conn = psycopg2.connect(
            database='d31hmkqi1b3i6l',
            user='eteltzscugyzlf',
            password='d997aff8600c2f245977b12c1729500a6a84577b2f7f99244d1c8557947f230c',
            host='ec2-54-159-244-207.compute-1.amazonaws.com',
            port='5432')
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    return result

def random_serial():
    code_list = [] 
    for i in range(10):
        code_list.append(str(i))
    for i in range(65, 91):
        code_list.append(chr(i))
    serial_number = ''.join(random.sample(code_list, 16))
    print(f"[SERIAL] {serial_number}")
    return serial_number

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
