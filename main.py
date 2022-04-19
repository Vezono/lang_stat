from pyrogram import Client
import json
from langdetect import detect
import flag
from codes import codes

stats = dict()
stat_file = open('stats.json')
stats = json.load(stat_file)
stat_file.close()

client = Client('user', api_id=1667361, api_hash='b03621737183984458127e171b219459')

self_id = None

def detect_flag(lang):
    return flag.flag(codes[lang])

def gen_stat():
    global stats
    percentages = {}
    overall_count = sum([stats[lang] for lang in stats])
    for lang in stats:
        percentage = str(stats[lang]/overall_count*100).split('.')
        percentage = float(f'{percentage[0]}.{percentage[1][:1]}')
        percentages.update({
            lang: percentage
        })


    percentages = dict(sorted(percentages.items(),key= lambda x:x[1], reverse = True))
    tts = 'Статистика за мовами:\n'
    
    for lang in percentages:
        tts += f'{detect_flag(lang)} - {percentages[lang]}%'+'\n'
    return tts

@client.on_message()
def handler(c, m):
    global self_id
    if not self_id: 
        self_id = client.get_me().id
    if not m.from_user:
        return
    if m.from_user.id != self_id:
        return
    if not m.text:
        return

    if m.text == '.stat':
        client.edit_message_text(m.chat.id, m.message_id, gen_stat())
        return

    lang = detect(m.text)
    flag_emoji = detect_flag(lang)

    if not lang in stats:
        stats.update({lang: 0})

    stats.update({
        lang: stats[lang]+1
    })

    stat_file = open('stats.json', 'w')
    json.dump(stats, stat_file)
    stat_file.close()
    #client.edit_message_text(m.chat.id, m.message_id, f'{flag_emoji}{m.text}')

print('Скріпт працює!')
client.run()