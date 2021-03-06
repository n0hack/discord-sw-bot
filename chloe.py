import discord
import asyncio
import os
import time
from discord.ext import tasks
from datetime import datetime
from pytz import timezone

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# 시간 변수 선언
doom_time_1 = datetime(2021, 1, 1, 12, 50, 0).strftime("%H:%M:%S")
doom_time_2 = datetime(2021, 1, 1, 20, 50, 0).strftime("%H:%M:%S")
league_raid_time = datetime(2021, 1, 1, 0, 0, 0).strftime("%H:%M:%S")
KST = timezone('Asia/Seoul')


# 컨텐츠 알림
@tasks.loop(seconds=1)
async def contents_notify():
    now = datetime.now().astimezone(KST).strftime("%H:%M:%S")
    now_week = datetime.now().astimezone(KST).weekday()

    # 월드보스 안내 (오후 1시)
    if now == doom_time_1:
        await client.get_guild(int(os.environ["server"])).get_channel(int(os.environ["channel"])).send('10분 뒤(오후 1시) 월드보스 둠 출현 예정!\n잊지 말고 참여해서 처치 후 보상을 획득해 주세요!')
    # 월드보스 안내 (오후 9시)
    elif now == doom_time_2:
        await client.get_guild(int(os.environ["server"])).get_channel(int(os.environ["channel"])).send('10분 뒤(오후 9시) 월드보스 둠 출현 예정!\n잊지 말고 참여해서 처치 후 보상을 획득해 주세요!')

    # 리그레이드 안내 (자정)
    if (now_week == 3 or now_week == 4 or now_week == 5 or now_week == 6) and now == league_raid_time:
        await client.get_guild(int(os.environ["server"])).get_channel(int(os.environ["channel"])).send('목-금/토-일은 리그 레이드가 오픈되어 있습니다.\n리그원들과 함께 15만점을 달성해서, 리그 레이드 코인 20개를 획득해 주세요!\n\n획득한 보상으로 세레스(길드 NPC) 상점에서 다양한 아이템 구매가 가능합니다!')


@client.event
async def on_ready():
    print('아스테라 클로이 봇 로그인이 완료되었습니다.')
    print('Bot Name: ' + client.user.name)
    print('Bot ID: ' + str(client.user.id))
    print('-------------------------------------------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("아스테라 리그 업무"))

    # run background task
    contents_notify.start()


@ client.event
async def on_member_join(member):
    # time.sleep(1)
    await member.guild.get_channel(int(os.environ["channel"])).send(member.mention + "님 아스테라 디스코드에 오신 것을 환영합니다.\n서버 좌측에 공지사항이 있으니 꼭 확인해 주세요!")


@ client.event
async def on_message(message):
    if message.author.bot:
        return

    # 명령어 리스트
    if message.content == "!명령어":
        embed = discord.Embed(
            title="안녕하세요! 오퍼레이터 클로이입니다!", description="여러분께 도움을 드리고자, 여러 기능을 제공하고 있습니다.\n사용 가능한 명령어는 아래에서 확인 가능합니다.\n\n좋은 하루 되세요 💕\nㅤ", color=0x00aaaa)
        embed.add_field(name="클로이와 인사", value="`!안녕`", inline=True)
        embed.add_field(
            name="뉴비 가이드", value="`!육성`, `!뉴비`", inline=True)
        embed.add_field(
            name="캐릭터 공략", value="`!하루`, `!어윈`, `!릴리`, `!스텔라`, `!진`, `!이리스`\n`!치이`, `!에프넬`, `!이나비`", inline=False)
        embed.add_field(
            name="유용한 정보", value="`!ASTERA`, `!NPC`, `!거래`, `!경험치`, `!도핑`, `!레이드`, `!만치`\n`!메모리얼`, `!브로치`, `!소켓`, `!숙제`, `!아카식`, `!장비`, `!재화`\n`!적중도`, `!제련`, `!칭호`, `!캐레`, `!캐쉬`, `!코스튬`, `!파밍`\n`!포션`, `!프리셋`, `!프리카메라`, `!행감`, `!행동력`", inline=False)
        await message.channel.send(embed=embed)
    # 클로이와 인사
    elif message.content == "!안녕":
        await message.channel.send(message.author.nick + "님 안녕하세요!")
    # 뉴비 가이드
    elif message.content == "!육성":
        embed = discord.Embed(title="리그 마스터가 직접 작성한 가이드입니다!",
                              description="아래 링크를 눌러서 순서대로 따라가시면 됩니다.\n그리고 <가이드-기초정보>에 좋은 내용이 많으니 함께 읽어 보세요 😆\n\n[🎀 시작에 앞서 드리고 싶은 말](https://page.onstove.com/soulworker/kr/view/7313632)\n[🎀 LV 01-30 (최적화/아카식/기초)](https://page.onstove.com/soulworker/kr/view/7313665)\n[🎀 LV 30-55 (칭호/브로치)](https://page.onstove.com/soulworker/kr/view/7314159)\n[🎀 LV 55-60 (소울스톤/승급)](https://page.onstove.com/soulworker/kr/view/7314368)\n[🎀 LV 60-68 (데자이어 각성)](https://page.onstove.com/soulworker/kr/view/7314505)\n[🎀 LV 68-72 (루나폴/강화/제련)](https://page.onstove.com/soulworker/kr/view/7314929)\n[🎀 LV 72-76 (만렙/유용한정보)](https://page.onstove.com/soulworker/kr/view/7314931)\n[🎀 소울워커 플레이 시 주의해야 하는 것](https://page.onstove.com/soulworker/kr/view/7314935)")
        await message.channel.send(embed=embed)
    elif message.content == "!뉴비":
        embed = discord.Embed(title="뉴비분들에게 유용한 정보입니다!",
                              description="아래 소개하는 정보 외에도 준비된 자료가 많습니다.\n가이드의 <기초정보>, <심화정보>를 참고해 주세요!\n\n[교본 아이템 정리](https://discord.com/channels/857371775683133480/864500194077966407/864758762827808809)\n[인벤토리 확장/정리 방법](https://discord.com/channels/857371775683133480/864500194077966407/864764550343950336)\n[장비 내구도 관리의 중요성](https://discord.com/channels/857371775683133480/864500194077966407/864760857857359902)\n[보너스 카드키 사용처](https://discord.com/channels/857371775683133480/864500194077966407/864764223350112257)\n[클리어 랭크 산정 방식](https://discord.com/channels/857371775683133480/864168723174653952/864813229652705310)\n[콤보의 중요성](https://discord.com/channels/857371775683133480/864168723174653952/864813734904201257)\n[회피기의 중요성](https://discord.com/channels/857371775683133480/864500194077966407/864762135976738816)\n[무적기를 이용한 데미지 딜링](https://discord.com/channels/857371775683133480/864168723174653952/864814737351114813)\n[부활 관련 팁](https://discord.com/channels/857371775683133480/864500194077966407/864763405105627176)\n[체력(HP)을 홀수로 만들면 좋은 이유](https://discord.com/channels/857371775683133480/864168723174653952/864806904538333184)\n[공격속도가 스킬에 미치는 영향](https://discord.com/channels/857371775683133480/864168723174653952/865154870528180234)\n[지역 이동 시간 아끼는 방법](https://discord.com/channels/857371775683133480/864500194077966407/864768341905113118)\n[소울워커 이벤트 알리미 구독](https://discord.com/channels/857371775683133480/864500194077966407/864773161165127701)\n[소울워커에서 지켜주시면 좋은 것](https://discord.com/channels/857371775683133480/864500194077966407/864774040241963048)")
        await message.channel.send(embed=embed)
    # 캐릭터 공략
    elif message.content == "!하루":
        embed = discord.Embed(
            title="하루 에스티아 공략입니다!", description="복수의 소울럼소드\n운용 난이도: ★★☆☆☆", color=0xffa500)
        embed.set_image(url="https://i.imgur.com/tAAWsWO.jpg")
        embed.add_field(
            name="별명", value="`하루룽`, `하구리`", inline=False)
        embed.add_field(
            name="장점", value="`1. 딜링 안정성`\n`2. 빠르고 원활한 스킬 연계`\n`3. 높은 일반 메이즈 사냥 능력`", inline=False)
        embed.add_field(
            name="단점", value="`1. 부족한 생존력`\n`2. 낮은 콤보 축적 속도`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[하루 첫 걸음부터 끝 걸음까지 육성 (2020.12.06)](https://page.onstove.com/soulworker/kr/view/6438215)\n[하루 기본적인 딜사이클과 프리셋 (2020.12.09)](https://arca.live/b/soulworkers/10297441)\n[하루 솔로 히든 하이드아웃 영상 (2021.06.01)](https://www.youtube.com/watch?v=FrhjCLFr0G8)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!어윈":
        embed = discord.Embed(
            title="어윈 아크라이트 공략입니다!", description="쾌락의 건재즈\n운용 난이도: ★★★☆☆", color=0x0000ff)
        embed.set_image(url="https://i.imgur.com/A4WdTAF.jpg")
        embed.add_field(
            name="별명", value="`어가놈`, `어송이`, `어원`", inline=False)
        embed.add_field(
            name="장점", value="`1. 강력한 스킬 난사 능력`\n`2. 강력하고, 안정적인 보스전 능력`\n`3. 높은 콤보수와 상시 방어 관통 보정`", inline=False)
        embed.add_field(
            name="단점", value="`1. 승급 전 광역기 부재로 인한 높은 육성 난이도`\n`2. 까다로운 운용과 높은 방관 대신 낮은 계수`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[뉴비가 보면 좋은 어윈 공략 (2020.12.06)](https://page.onstove.com/soulworker/kr/view/6440896)\n[어윈 기본적인 딜사이클과 프리셋 (2020.12.30)](https://arca.live/b/soulworkers/19181173)\n[어윈 솔로 히든 하이드아웃 영상 (2021.06.06)](https://www.youtube.com/watch?v=I49or0vi1Sg)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!릴리":
        embed = discord.Embed(
            title="릴리 블룸메르헨 공략입니다!", description="광기의 미스트사이드\n운용 난이도: ★★★☆☆", color=0x871b4d)
        embed.set_image(url="https://i.imgur.com/ThCDoti.png")
        embed.add_field(
            name="별명", value="`닌니`, `광기 조무사`, `릴퀴`, `러블리 릴리`", inline=False)
        embed.add_field(
            name="장점", value="`1. 평타와 주력기의 넓은 범위`\n`2. 퓨리 마하를 통한 빠른 누킹`\n`3. 아카식의 높은 효율`", inline=False)
        embed.add_field(
            name="단점", value="`1. 높은 재사용 대기 시간 감소 의존도`\n`2. 최종 세팅의 어려움 (재사용 대기 시간 감소)`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[찐뉴비 릴리들을 위한 기초 공략 (2021.05.21)](https://arca.live/b/soulworkers/26634805)\n[데스 그라인더 채용 프리셋 (2021.06.07)](https://arca.live/b/soulworkers/27711486)\n[릴리 솔로 히든 하이드아웃 영상 (2020.12.13)](https://www.youtube.com/watch?v=o4qrUgqWeQ4)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!스텔라":
        embed = discord.Embed(
            title="스텔라 유니벨 공략입니다!", description="슬픔의 하울링기타\n운용 난이도: ★★★★★", color=0x7f00ff)
        embed.set_image(url="https://i.imgur.com/akx07jC.png")
        embed.add_field(
            name="별명", value="`댕라`", inline=False)
        embed.add_field(
            name="장점", value="`1. 높은 딜량`\n`2. 압도적인 시너지`", inline=False)
        embed.add_field(
            name="단점", value="`1. 회복 플레이 시 난이도`\n`2. 시너지가 공격속도에 치중되어 있음`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[스텔라 기본적인 공략글 (2021.03.14)](https://arca.live/b/soulworkers/22769925)\n[스텔라 솔로 히든 하이드아웃 영상 (2021.05.24)](https://www.youtube.com/watch?v=PRkjk-emAmM)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!진":
        embed = discord.Embed(
            title="진 세이파츠 공략입니다!", description="열정의 스피릿암즈\n운용 난이도: ★★★★☆", color=0xffff00)
        embed.set_image(url="https://i.imgur.com/cZY3qeF.jpg")
        embed.add_field(
            name="별명", value="`진따`, `진시황제`, `진붕이`", inline=False)
        embed.add_field(
            name="장점", value="`1. 개성적이고 공/방일체 스킬인 카운터의 존재`\n`2. 우월한 유틸성을 기반으로 한 다재다능함`\n`3. 매우 뛰어난 탱킹`\n`4. 안정적인 SG, SV 수급력`", inline=False)
        embed.add_field(
            name="단점", value="`1. 피지컬에 따라 요동치는 성능과 높은 난이도`\n`2. 카운터에 종속된 딜링 성능과 낮은 포텐셜`\n`3. 낮은 연타수로 인한 손해`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[움짤로 보는 진 세이파츠 공략 (2020.12.04)](https://page.onstove.com/soulworker/kr/view/6428693)\n[진 세이파츠 개편 공략 완전판 (2021.01.29)](https://arca.live/b/soulworkers/20544731)\n[진 솔로 히든 하이드아웃 영상 (2021.06.02)](https://www.youtube.com/watch?v=-nuqW6RmLdk)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!이리스":
        embed = discord.Embed(
            title="이리스 유마 공략입니다!", description="분노의 해머스톨\n운용 난이도: ★★★★☆", color=0xff0000)
        embed.set_image(url="https://i.imgur.com/Msg9nu6.jpg")
        embed.add_field(
            name="별명", value="`지민이`, `분노 주머니`", inline=False)
        embed.add_field(
            name="장점", value="`1. 강력한 광역 딜링`\n`2. 폭딜과 지속딜링 양면에서 모두 강력한 편`\n`3. 준수한 파티 시너지`", inline=False)
        embed.add_field(
            name="단점", value="`1. 대부분 스킬이 채널링과 차징`\n`2. 이동형 보스에게 취약한 상성`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[이리스 뉴비를 위한 공략 (2020.12.21)](https://page.onstove.com/soulworker/kr/view/6518214)\n[지민이 범용 프리셋 (2021.05.19)](https://arca.live/b/soulworkers/26512753)\n[이리스 솔로 히든 하이드아웃 영상 (2021.06.13)](https://www.youtube.com/watch?v=7vxcYp0guro)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!치이":
        embed = discord.Embed(
            title="치이 아루엘 공략입니다!", description="열망의 데스퍼로어\n운용 난이도: ★★★★☆", color=0xdc143c)
        embed.set_image(url="https://i.imgur.com/rO2nK06.jpg")
        embed.add_field(
            name="별명", value="`코양이`", inline=False)
        embed.add_field(
            name="장점", value="`1. 고성능 자버프 스킬 보유`\n`2. 빠른 스킬 연계`\n`3. 수월한 SG 운용과 뛰어난 회복 능력`", inline=False)
        embed.add_field(
            name="단점", value="`1. 상당한 HP 소모`\n`2. 짧은 사거리와 난이도 있는 운용`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[치이 육성, 스킬트리/프리셋, 운영법 (2020.12.04)](https://page.onstove.com/soulworker/kr/view/6427627)\n[치이 솔로 히든 하이드아웃 영상 (2021.03.11)](https://www.youtube.com/watch?v=cIqCHeECTDE)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!에프넬":
        embed = discord.Embed(
            title="에프넬 공략입니다!", description="불굴의 바밍스피어\n운용 난이도: ★★★★☆", color=0x008000)
        embed.set_image(url="https://i.imgur.com/ahMKFwZ.jpg")
        embed.add_field(
            name="별명", value="`마리`", inline=False)
        embed.add_field(
            name="장점", value="`1. 강력한 데미지 포텐셜`\n`2. 매우 빠른 스킬 연계`\n`3. 여유로운 캔슬 판정`", inline=False)
        embed.add_field(
            name="단점", value="`1. 높은 운용 피로도`\n`2. 최악의 파티 버프 효과`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[뉴비분들을 위한 에프넬 공략 (2020.12.21)](https://page.onstove.com/soulworker/kr/view/6518340)\n[에프넬 프리셋 새로 짜봤습니다 (2021.03.30)](https://arca.live/b/soulworkers/23635542)\n[에프넬 솔로 히든 하이드아웃 영상 (2021.04.14)](https://www.youtube.com/watch?v=vthbsATbJ4c)", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!이나비":
        embed = discord.Embed(
            title="이나비 공략입니다!", description="충심의 로열라이플\n운용 난이도: ★★★★★", color=0x008080)
        embed.set_image(url="https://i.imgur.com/oH9Va6Y.jpg")
        embed.add_field(
            name="별명", value="`빅나비`", inline=False)
        embed.add_field(
            name="장점", value="`1. 무지막지한 딜량`\n`2. 고효율 개인 버프`\n`3. 긴 사거리`", inline=False)
        embed.add_field(
            name="단점", value="`1. 높은 운용 난이도`\n`2. 매우 높은 재사용 대기시간 감소 의존도`\n`3. 근접전의 어려움`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="[뉴비분들을 위한 이나비 공략 (2020.12.26)](https://page.onstove.com/soulworker/kr/view/6536545)\n[이나비 힛앤런 쓰는 프리셋 (2021.04.22)](https://arca.live/b/soulworkers/24915730)\n[이나비 솔로 히든 하이드아웃 영상 (2021.05.23)](https://www.youtube.com/watch?v=5xMsDmSzkvg)", inline=False)
        await message.channel.send(embed=embed)
    # 유용한 정보
    elif message.content == "!ASTERA" or message.content == "!astera" or message.content == "!공지":
        embed = discord.Embed(
            title="아스테라 오신 것을 환영합니다!", description="공지사항에 있는 내용이지만,\n중요하기 때문에 추가로 가져왔습니다!\n\n[리그 규칙](https://discord.com/channels/857371775683133480/857379819923046401/857383497663381505)\n[리그 컨텐츠 시간표 (고정X)](https://discord.com/channels/857371775683133480/857379819923046401/864151420332277771)\n[디스코드 참여 후 체크사항](https://discord.com/channels/857371775683133480/857379819923046401/864150320045097000)")
        await message.channel.send(embed=embed)
    elif message.content == "!npc" or message.content == "!NPC":
        embed = discord.Embed(
            title="소울워커 NPC에 대한 정보입니다!", description="일반적으로 많이 이용하는 NPC 위주로 정리했습니다.\n고객등급이 있는 NPC는 꼭 등급을 높여서 혜택을 받으세요!\n\n[NPC 소개 - 자이트(무기상인)](https://discord.com/channels/857371775683133480/864500194077966407/864740674921300039)\n[NPC 소개 - 요미(잡화상인)](https://discord.com/channels/857371775683133480/864500194077966407/864743549307060244)\n[NPC 소개 - 트리샤(강화)](https://discord.com/channels/857371775683133480/864500194077966407/864744422418808892)\n[NPC 소개 - 제니스(제작)](https://discord.com/channels/857371775683133480/864500194077966407/864744920496603137)\n[NPC 소개 - 막심(제작)](https://discord.com/channels/857371775683133480/864500194077966407/864746392009179177)\n[NPC 소개 - 세레스(길드)](https://discord.com/channels/857371775683133480/864500194077966407/864748338040406078)\n[NPC 소개 - 이오(아카식)](https://discord.com/channels/857371775683133480/864500194077966407/864750206040801281)\n[NPC 소개 - 부커TV(퍼퓸/컨버터)](https://discord.com/channels/857371775683133480/864500194077966407/864751948589957160)\n[NPC 신용도 높이기 (신용도작)](https://discord.com/channels/857371775683133480/864500194077966407/864752447654592534)")
        await message.channel.send(embed=embed)
    elif message.content == "!거래":
        embed = discord.Embed(
            title="거래와 관련된 정보입니다!", description="불필요한 물건을 정리하거나, 제니가 필요할 때\n도움이 될 수 있는 정보를 준비했습니다!\n\n[거래 관련 팁 (거래소 / 캐쉬구매)](https://discord.com/channels/857371775683133480/864500194077966407/864772051105480705)")
        await message.channel.send(embed=embed)
    elif message.content == "!경험치":
        embed = discord.Embed(
            title="경험치와 관련된 정보입니다!", description="육성 단계에서는 경험치가 중요하기 때문에,\n추가 수급 방법과 버프 종류에 대해 소개합니다!\n\n[경험치 버프 종류](https://discord.com/channels/857371775683133480/864500194077966407/864756535632855080)\n[경험치 추가 수급 방법](https://discord.com/channels/857371775683133480/864500194077966407/864758639842295809)")
        await message.channel.send(embed=embed)
    elif message.content == "!도핑":
        embed = discord.Embed(
            title="도핑과 관련된 정보입니다!", description="도핑은 능력치를 일시적으로 높여 주는 아이템입니다.\n소울워커의 도핑 아이템을 소개합니다!\n\n[도핑(퍼퓸) 소개/수급처](https://discord.com/channels/857371775683133480/864168723174653952/864812711102513172)")
        await message.channel.send(embed=embed)
    elif message.content == "!레이드":
        embed = discord.Embed(
            title="소울워커 레이드에 대한 정보입니다!", description="레이드는 파티원들과 함께 하는 컨텐츠이므로,\n공략 숙지는 기본이고, 커트라인도 충족해야 합니다.\n\n[[LV65] 히든 하이드아웃](https://discord.com/channels/857371775683133480/864168661992472586/864385362289491979)\n[[LV68] 루나폴](https://discord.com/channels/857371775683133480/864168661992472586/864389836220006421)\n[[LV72] 바이올런트 선](https://discord.com/channels/857371775683133480/864168661992472586/864394927538700298)\n[[LV76] 브로큰 세이비어](https://discord.com/channels/857371775683133480/864168661992472586/864399902893539358)")
        await message.channel.send(embed=embed)
    elif message.content == "!만치":
        embed = discord.Embed(
            title="캐릭터별 만치에 대한 정보입니다!", description="캐릭터별 만치는 아래와 같습니다.\n밸런스 패치에 의해 언제든 변경될 수 있으니 유의해 주세요!\n\n- 하루: 70%\n- 어윈: 70%\n- 릴리: 55% [포스리전 +15%]\n- 스텔라: 60% [비즈플레이 +10%]\n- 진: 70%\n- 이리스: 70%\n- 치이: 60% [승급패시브 +10%]\n- 에프넬: 70%\n- 이나비: 60% [허니비 +10%]\n※ 위 치명타 확률을 맞추고, 퍼퓸을 사용하면 됩니다.")
        await message.channel.send(embed=embed)
    elif message.content == "!메모리얼":
        embed = discord.Embed(
            title="메모리얼과 관련된 정보입니다!", description="메모리얼은 일종의 수집 시스템입니다. [단축키 B]\n메이즈의 EP.1을 클리어하면, 메모리얼 수집이 개방됩니다.\n\n[메모리얼 아이템 좌표 (로코 타운 ~ 그레이스 시티)](https://page.onstove.com/soulworker/kr/view/7315659)\n[메모리얼 아이템 좌표 (루인 포트리스 ~ 잔디이불 캠프)](https://page.onstove.com/soulworker/kr/view/7315806)")
        await message.channel.send(embed=embed)
    elif message.content == "!브로치":
        embed = discord.Embed(
            title="브로치와 관련된 정보입니다!", description="브로치는 코스튬에 장착 가능하며,\n세트 옵션을 통해 캐릭터의 능력치를 상승 시킵니다.\n\n[브로치 (추천 옵션 / 합성 팁)](https://discord.com/channels/857371775683133480/864168723174653952/864801053349117954)\n[사진으로 보는 추천 브로치](https://sw-astera.tistory.com/2)\n[모든 브로치 옵션 정리](https://namu.wiki/w/소울워커/아이템/브로치)")
        await message.channel.send(embed=embed)
    elif message.content == "!소켓":
        embed = discord.Embed(
            title="소켓과 관련된 정보입니다!", description="무기(웨폰)와 방어구(기어)에는 소켓이 있습니다.\n소켓에 착용 가능한 패밀리어와 관련 아이템을 소개합니다!\n\n[패밀리어 (갈망/성순)](https://discord.com/channels/857371775683133480/864168723174653952/864793294768832512)\n[소켓 확장/추출 아이템 획득처](https://discord.com/channels/857371775683133480/864500194077966407/864767049624059924)")
        await message.channel.send(embed=embed)
    elif message.content == "!숙제":
        embed = discord.Embed(
            title="소울워커 숙제에 대한 정보입니다!", description="행동력을 필요로 하지 않고,\n공통적으로 하기 좋은 숙제 위주로 가져왔습니다 :)\n\n[📚 소울워커 일일 숙제](https://discord.com/channels/857371775683133480/864167531433951242/864402081012121611)")
        await message.channel.send(embed=embed)
    elif message.content == "!아카식":
        embed = discord.Embed(
            title="아카식과 관련된 정보입니다!", description="아카식은 캐릭터의 능력치를 높여 주거나,\n사냥에 도움을 주는 카드 장비 시스템입니다!\n\n[아카식 레코드 선택권 추천](https://discord.com/channels/857371775683133480/864500194077966407/864756121553338398)\n[아카식 레코드 (추천세팅/적폐/팁)](https://arca.live/b/soulworkers/29489527)\n[모든 아카식 레코드 옵션 정리](https://namu.wiki/w/소울워커/아카식%20레코드)\n")
        await message.channel.send(embed=embed)
    elif message.content == "!장비":
        embed = discord.Embed(
            title="장비와 관련된 정보입니다!", description="소울워커 장비 종류에 대한 설명과\n강화/계승 방법에 대해 준비했습니다!\n\n[장비 종류 (스탠다드/익스텐드)](https://discord.com/channels/857371775683133480/864168723174653952/864788438872227840)\n[장비 강화 (장비 고유의 능력치를 높이는 시스템)](https://discord.com/channels/857371775683133480/864168723174653952/864791867119239208)\n[장비 계승 (강화 수치와 옵션의 일부를 옮기는 시스템)](https://discord.com/channels/857371775683133480/864168723174653952/864792010618830868)")
        await message.channel.send(embed=embed)
    elif message.content == "!재화":
        embed = discord.Embed(
            title="소울워커 재화에 대한 정보입니다!", description="[💎 소울워커 재화 종류](https://discord.com/channels/857371775683133480/864167531433951242/864411974355910666)\n[💎 재화 수급 메이즈 <데이드림>](https://discord.com/channels/857371775683133480/864167531433951242/864414754960441344)\n[💎 재화 수급 메이즈 <스카이클락 팰리스>](https://discord.com/channels/857371775683133480/864167531433951242/864416920454692874)\n[💎 재화 수급 메이즈 <티끌런>](https://discord.com/channels/857371775683133480/864167531433951242/864420007350108200)\n[💎 재화 수급 메이즈 <테네런/자살런>](https://discord.com/channels/857371775683133480/864167531433951242/864421469610311690)\n[💎 재화 수급 메이즈 <레이드>](https://discord.com/channels/857371775683133480/864167531433951242/864424764738109470)\n[💎 재화 수급 메이즈 <리그 레이드>](https://discord.com/channels/857371775683133480/864167531433951242/864426401742848030)\n[💎 재화 수급 메이즈 <월드보스>](https://discord.com/channels/857371775683133480/864167531433951242/864427385453281290)\n[💎 재화 수급 방법 <독서>](https://discord.com/channels/857371775683133480/864167531433951242/864429376829784097)\n[💎 재화 수급 방법 <점유작/점유율작>](https://discord.com/channels/857371775683133480/864167531433951242/864431611684585482)\n[💎 재화 수급 방법 <컨버터작/버터나비>](https://discord.com/channels/857371775683133480/864167531433951242/864432693689450516)\n[💎 재화 수급 방법 <파방냥이/강파방냥이>](https://discord.com/channels/857371775683133480/864167531433951242/864433494452076564)\n[💎 재화 수급 방법 <랭킹>](https://discord.com/channels/857371775683133480/864167531433951242/864434222419410964)\n[💎 재화, 유용한 아이템 수급 방법 정리](https://discord.com/channels/857371775683133480/864167531433951242/864727411857162290)")
        await message.channel.send(embed=embed)
    elif message.content == "!적중도":
        embed = discord.Embed(
            title="적중도와 관련된 정보입니다!", description="적중도와 치명타 확률은 중요한 능력치입니다.\n커트라인에 직결되는 만큼, 많은 신경을 써야 합니다!\n\n[적중도와 치명타 확률의 관계](https://discord.com/channels/857371775683133480/864168723174653952/864800408282988554)")
        await message.channel.send(embed=embed)
    elif message.content == "!제련":
        embed = discord.Embed(
            title="제련과 관련된 정보입니다!", description="제련은 장비를 가공하여 능력치를 높이거나,\n원하는 옵션으로 변경할 수 있는 시스템입니다.\n\n[등급 제련 (등급작)](https://discord.com/channels/857371775683133480/864168723174653952/864795517707223070)\n[옵션 제련 (옵션작)](https://discord.com/channels/857371775683133480/864168723174653952/864796973609254943)\n[태그 제련 (태그작)](https://discord.com/channels/857371775683133480/864168723174653952/864799063744184351)")
        await message.channel.send(embed=embed)
    elif message.content == "!칭호":
        embed = discord.Embed(
            title="칭호와 관련된 정보입니다!", description="칭호는 캐릭터 닉네임 위를 꾸며주는 요소이면서,\n능력치까지 높일 수 있는 중요한 장비 아이템입니다!\n\n[종결 칭호 얻는 방법](https://discord.com/channels/857371775683133480/864168723174653952/864815148568936478)\n[보여지는 칭호 다르게 하기](https://discord.com/channels/857371775683133480/864500194077966407/864768195565715466)\n[모든 칭호 옵션/얻는법 정리](https://namu.wiki/w/소울워커/칭호)")
        await message.channel.send(embed=embed)
    elif message.content == "!캐레":
        embed = discord.Embed(
            title="캐주얼 레이드와 관련된 정보입니다!", description="캐주얼 레이드는 승급 시 주로 찾는 메이즈입니다.\n메이즈의 속성이 매일 변경되기 때문에, 요일별로 정리했습니다!\n\n[캐주얼 레이드 속성과 속성간 상성](https://discord.com/channels/857371775683133480/864168723174653952/864815853290782750)")
        await message.channel.send(embed=embed)
    elif message.content == "!캐쉬":
        embed = discord.Embed(
            title="캐쉬 충전과 관련된 정보입니다!", description="에그머니 상품권을 이용하면,\n좀 더 저렴한 가격으로 캐쉬를 충전할 수 있습니다!\n\n[캐쉬충전 Tip](https://discord.com/channels/857371775683133480/864500194077966407/864773793908785162)")
        await message.channel.send(embed=embed)
    elif message.content == "!코스튬":
        embed = discord.Embed(
            title="코스튬과 관련된 정보입니다!", description="캐릭터의 외형을 꾸밀 수 있는 코스튬에 관해\n궁금할 법한 내용을 정리해 가져왔습니다!\n\n[코스튬 염색/재판매 방법](https://discord.com/channels/857371775683133480/864500194077966407/864769493288484875)\n[코스튬 재판 날짜 확인](https://soulworker.game.onstove.com/Costume/List)\n[역대 코스튬 정보 보기](https://namu.wiki/w/소울워커/코스튬)")
        await message.channel.send(embed=embed)
    elif message.content == "!퀘스트":
        embed = discord.Embed(
            title="소울워커 퀘스트에 대한 정보입니다!", description="메인 퀘스트가 끊겼거나, 좋은 보상을 주는 퀘스트가 궁금할 때!\n도움이 될 수 있도록 퀘스트를 최대한 정리했습니다~★\n\n[📖 퀘스트 종류와 구분하는 방법](https://discord.com/channels/857371775683133480/857889654892134420/857892483693412372)\n[📖 메인 퀘스트가 끊겼을 때](https://discord.com/channels/857371775683133480/857889654892134420/857892055509368864)\n[📖 권장하는 서브 / 반복 퀘스트 목록 I](https://discord.com/channels/857371775683133480/857889654892134420/857895925229158400)\n[📖 권장하는 서브 / 반복 퀘스트 목록 II](https://discord.com/channels/857371775683133480/857889654892134420/857896735039684608)\n[📖 캔더스 시티 서브 퀘스트 TIP](https://discord.com/channels/857371775683133480/857889654892134420/860795469957562409)\n[📖 레이드 입장을 위한 선행 퀘스트](https://discord.com/channels/857371775683133480/857889654892134420/857899874619490334)\n[📖 레이드 일일 퀘스트](https://discord.com/channels/857371775683133480/857889654892134420/857900029220880394)\n[📖 데자이어 각성 퀘스트 정리](https://discord.com/channels/857371775683133480/857889654892134420/857910534531579915)\n[📖 LV 72-76 퀘스트 정리](https://discord.com/channels/857371775683133480/857889654892134420/864444675040346122)")
        await message.channel.send(embed=embed)
    elif message.content == "!파밍":
        embed = discord.Embed(
            title="아이템 파밍에 대한 정보입니다!", description="소울워커는 컨텐츠 장벽이 낮고, 파밍이 쉬운 편입니다.\n게임을 가볍게, 천천히 즐기는 것을 추천 드려요!\n\n[장비 파밍 순서 (루나폴 ~ 바이올런트 선)](https://discord.com/channels/857371775683133480/864168723174653952/864791153119592458)")
        await message.channel.send(embed=embed)
    elif message.content == "!포션":
        embed = discord.Embed(
            title="포션과 관련된 정보입니다!", description="포션은 생존과 유틸 확보에 많은 도움을 주기 때문에,\n주로 사용하는 포션과 수급 방법에 대해 소개합니다!\n\n[자주 사용하는 포션](https://discord.com/channels/857371775683133480/864168723174653952/864812401210949662)")
        await message.channel.send(embed=embed)
    elif message.content == "!프리셋":
        embed = discord.Embed(
            title="프리셋과 관련된 정보입니다!", description="스킬 프리셋은 콤보를 만드는 시스템입니다.\n초반에는 괜찮지만, 이후에는 꼭 짚고 넘어가야 합니다!\n\n[뉴비가 꼭 알아야 하는 프리셋 사용법](https://arca.live/b/soulworkers/22180131)\n[프리셋과 스킬 단계별 보너스에 대한 이해](https://arca.live/b/soulworkers/16863763)")
        await message.channel.send(embed=embed)
    elif message.content == "!프리카메라":
        embed = discord.Embed(
            title="프리 카메라와 관련된 정보입니다!", description="소울워커는 캐릭터를 예쁘게 촬영할 수 있도록\n프리 카메라라는 재밌는 기능을 제공하고 있습니다!\n\n[예쁘게 스크린샷 찍는 방법 (프리 카메라)](https://discord.com/channels/857371775683133480/864500194077966407/864773020207939614)")
        await message.channel.send(embed=embed)
    elif message.content == "!행감":
        embed = discord.Embed(
            title="행동력과 관련된 정보입니다!", description="소울워커는 주말마다 랜덤한 메이즈의 요구 행동력이 감소합니다.\n이를 행감이라 부르며, 감소되는 행동력은 아래에서 확인하세요!\n\n[메이즈 행동력 감소 버프 시스템)](https://discord.com/channels/857371775683133480/864168723174653952/864816346193985546)")
        await message.channel.send(embed=embed)
    elif message.content == "!행동력":
        embed = discord.Embed(
            title="행동력과 관련된 정보입니다!", description="소울워커는 행동력 시스템이 있으며, 오전 9시에 초기화됩니다.\n중요한 시스템이기 때문에 채우는 법과 누적 시스템을 소개합니다!\n\n[행동력 (채우는 방법 / 누적 시스템)](https://discord.com/channels/857371775683133480/864500194077966407/864759379092570122)")
        await message.channel.send(embed=embed)
    # 테스트 명령
    elif message.content == "!시간테스트":
        now = datetime.now().astimezone(KST).strftime("%H:%M:%S")
        now_week = datetime.now().astimezone(KST).weekday()
        await message.channel.send("현재 시간은 " + now + ", 둠 타임은 " + doom_time_1 + ", " + doom_time_2 + ", 요일: " + str(now_week) + ", 리레: " + league_raid_time)

        if now_week == 5 or now_week == 6:
            await message.channel.send("조건 테스트 케이스 1!")
        else:
            await message.channel.send("조건 테스트 케이스 2!")


# 클로이 실행
client.run(os.environ["token"])
