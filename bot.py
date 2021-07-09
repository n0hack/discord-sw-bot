import discord
from discord.ext import tasks
import asyncio
import os
from datetime import datetime
import time
from pytz import timezone

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# time_variables
doom_time_1 = datetime(2021, 1, 1, 12, 50, 0).strftime("%H:%M:%S")
doom_time_2 = datetime(2021, 1, 1, 20, 50, 0).strftime("%H:%M:%S")
league_raid_time = datetime(2021, 1, 1, 0, 0, 0).strftime("%H:%M:%S")
KST = timezone('Asia/Seoul')


@tasks.loop(seconds=1)
async def contents_notify():
    now = datetime.now().astimezone(KST).strftime("%H:%M:%S")
    now_week = datetime.now().astimezone(KST).weekday()

    # doom time_1 (01:00 pm)
    if now == doom_time_1:
        await client.get_guild(int(os.environ["server"])).get_channel(int(os.environ["channel"])).send('10분 뒤(오후 1시) 월드보스 둠 출현 예정!\n잊지 말고 참여해서 처치 후 보상을 획득해 주세요!')
    # doom time_2 (09:00 pm)
    elif now == doom_time_2:
        await client.get_guild(int(os.environ["server"])).get_channel(int(os.environ["channel"])).send('10분 뒤(오후 9시) 월드보스 둠 출현 예정!\n잊지 말고 참여해서 처치 후 보상을 획득해 주세요!')

    # league raid time (Weekend 10:00 pm)
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

    if message.content == "!안녕":
        await message.channel.send(message.author.nick + "님 안녕하세요!")
    elif message.content == "!리그파티":
        embed = discord.Embed(
            title="아스테라 리그 파티/포스 시간표입니다!", description="`1. 루나폴 (오후 9시 둠 이후 자율 구성)`\n`2. 바이올런트 선 (오후 9시 둠 이후 자율 구성)`\n`3. 브로큰 세이비어 (오후 9시 둠 이후 자율 구성)`\n`4. 리그 레이드 - 리젼 인베이더 (목/토 0시 오픈, 48시간 유지)`\n\n모든 컨텐츠는 편하게 9시 이후 자율적으로 구성하면 됩니다.\n서로가 주도해서 서로를 챙겨 주시면 감사하겠습니다!\n\n리그 컨텐츠는 모두 7채널에서 함께 진행합니다 😆", color=0x00aaaa)
        await message.channel.send(embed=embed)
    elif message.content == "!명령어":
        embed = discord.Embed(
            title="안녕하세요! 오퍼레이터 클로이입니다!", description="리그원 분들께 도움을 드리고자, 여러 기능을 제공하고 있습니다.\n사용 가능한 명령어는 아래에서 확인 가능합니다.\n\n좋은 하루 되세요  💕", color=0x00aaaa)
        embed.add_field(name="클로이와 인사", value="`!안녕`", inline=True)
        embed.add_field(name="함께 하는 컨텐츠", value="`!리그파티`", inline=True)
        embed.add_field(
            name="뉴비 가이드", value="`!육성`, `!행동력`, `!프리셋`, `!메모리얼`, `!신용도`, `!파부`, `!주의사항`", inline=False)
        embed.add_field(
            name="캐릭터 공략", value="`!하루`, `!어윈`, `!스텔라`, `!릴리`, `!진`, `!이리스`\n`!치이`, `!에프넬`, `!이나비`", inline=False)
        embed.add_field(
            name="심화 정보", value="`!파밍순서`, `!소켓`, `!제련`, `!브로치`, `!아카식`, `!칭호`, `!적중도`, `!레이드`\n`!도핑`, `!무적기`, `!재화`, `!퀘스트`, `!코스튬`, `!최적화`, `!프리카메라`", inline=False)
        await message.channel.send(embed=embed)
    elif message.content == "!육성":
        embed = discord.Embed(title="현재 준비된 육성 가이드입니다!",
                              description="아래 링크를 눌러서 순서대로 따라가시면 됩니다.\n그리고 좌측의 뉴비 가이드에 좋은 내용이 많으니 함께 읽어 보세요 😆\n\n[뉴비 분들께 드리고 싶은 말](https://discord.com/channels/857371775683133480/857381320497168425/857690179833823232)\n[Lv 01-30 가이드](https://discord.com/channels/857371775683133480/857381320497168425/857884667167637545)\n[Lv 30-55 가이드](https://discord.com/channels/857371775683133480/857381320497168425/857922926020001803)\n[Lv 55-60 가이드](https://discord.com/channels/857371775683133480/857381320497168425/857926264802639873)\n[Lv 60-68 가이드](https://discord.com/channels/857371775683133480/857381320497168425/857928642885713920)\n[Lv 68-72 가이드](https://discord.com/channels/857371775683133480/857381320497168425/857929416834809856)\n[Lv 72-76 가이드](https://discord.com/channels/857371775683133480/857381320497168425/859260616942026802)\n[자주 하시는 질문 모음](https://discord.com/channels/857371775683133480/857381320497168425/857929753503334400)")
        await message.channel.send(embed=embed)
    elif message.content == "!행동력":
        embed = discord.Embed(
            title="행동력과 관련된 정보입니다!", description="[행동력 회복하는 방법](https://discord.com/channels/857371775683133480/857889672504279060/857905830808780811)\n[행동력 누적 시스템](https://discord.com/channels/857371775683133480/857889672504279060/857930601445326848)")
        await message.channel.send(embed=embed)
    elif message.content == "!프리셋":
        embed = discord.Embed(
            title="프리셋과 관련된 정보입니다!", description="스킬 프리셋은 콤보를 만드는 시스템입니다. 초반에는 크게 신경 쓸 필요가 없지만, 나중에는 어떻게 구성했는지에 따라 데미지 포텐셜에서 많은 차이가 있으므로 꼭 짚고 넘어가야 합니다 👏\n\n[뉴비가 꼭 알아야 하는 프리셋 사용법](https://arca.live/b/soulworkers/22180131)\n[프리셋과 스킬 단계별 보너스에 대한 이해](https://arca.live/b/soulworkers/16863763)")
        await message.channel.send(embed=embed)
    elif message.content == "!메모리얼":
        embed = discord.Embed(
            title="메모리얼과 관련된 정보입니다!", description="메모리얼은 일종의 수집 시스템입니다. (단축키 B)\n메이즈의 EP.1을 클리어하면, 메모리얼 수집이 개방됩니다.\n\n[메모리얼 아이템 좌표 (로코타운~루인포트리스)](https://namu.wiki/w/소울워커/시스템/메모리얼)\n[잔디이불 캠프 메모리얼 좌표](https://discord.com/channels/857371775683133480/857889672504279060/857902345907994634)")
        await message.channel.send(embed=embed)
    elif message.content == "!신용도":
        embed = discord.Embed(
            title="신용도와 관련된 정보입니다!", description="몇몇 NPC는 신용도를 높이면, 그에 따른 혜택을 제공합니다.\n이후 메리트가 많기 때문에 육성 초반부터 꾸준히 하는 것을 권장합니다!\n\n[NPC 신용도 높이기(신용도작)](https://discord.com/channels/857371775683133480/857889672504279060/857918314343563274)")
        await message.channel.send(embed=embed)
    elif message.content == "!파부":
        embed = discord.Embed(
            title="파티 부활 장치와 관련된 정보입니다!", description="부활 가능 횟수를 전부 소진하면,\n파티원이 [파티 부활 장치, 파부]를 사용해 줘야 합니다.\n\n[레이드를 하다 부활 제한 횟수를 전부 사용했을 때](https://discord.com/channels/857371775683133480/857889672504279060/857932688152068096)")
        await message.channel.send(embed=embed)
    elif message.content == "!주의사항":
        embed = discord.Embed(
            title="주의사항과 관련된 정보입니다!", description="뉴비 시절에는 잘 모를 수 있지만,\n몇몇 행동은 비매너로 보일 수 있으므로 주의해야 합니다! 😱\n\n[소울워커 주의사항 (비매너 행위)](https://discord.com/channels/857371775683133480/857889672504279060/857941350217416735)")
        await message.channel.send(embed=embed)
    elif message.content == "!파밍순서":
        embed = discord.Embed(
            title="파밍순서와 관련된 정보입니다!", description="소울워커는 컨텐츠 진입이 상대적으로 쉬운 게임입니다.\n천천히 즐기는 것을 추천드립니다! ⭐️\n\n[장비 종류와 강화, 그리고 파밍 순서](https://discord.com/channels/857371775683133480/857381375279759360/857559855938142219)")
        await message.channel.send(embed=embed)
    elif message.content == "!소켓":
        embed = discord.Embed(
            title="소켓과 관련된 정보입니다!", description="무기(웨폰)와 방어구(기어)에는 소켓이 있습니다.\n소켓에 착용 가능한 아이템은 아래 링크를 확인해 주세요!\n\n[장비에 착용 가능한 소울스톤과 갈망, 그리고 성순](https://discord.com/channels/857371775683133480/857381375279759360/857568686985838592)")
        await message.channel.send(embed=embed)
    elif message.content == "!제련":
        embed = discord.Embed(
            title="제련과 관련된 정보입니다!", description="트리샤 NPC에게서 가능한 제련은 장비를 가공하여 능력치를 높이거나, 원하는 옵션으로 변경할 수 있는 시스템입니다. 레이드 커트라인을 맞추거나, 스펙업을 위해 이용하는 시스템이므로 알아 두면 좋습니다 😊\n\n[등급 제련 (등급작)](https://discord.com/channels/857371775683133480/857381375279759360/857579024603021322)\n[옵션 제련 (옵션작)](https://discord.com/channels/857371775683133480/857381375279759360/857583377117085707)\n[태그 제련 (태그작)](https://discord.com/channels/857371775683133480/857381375279759360/857586213262065695)")
        await message.channel.send(embed=embed)
    elif message.content == "!브로치":
        embed = discord.Embed(
            title="브로치와 관련된 정보입니다!", description="브로치는 코스튬에 장착 가능하며,\n세트 옵션을 통해 캐릭터의 능력치를 상승 시킵니다.\n\n[추천 브로치(글)](https://discord.com/channels/857371775683133480/857381375279759360/857620146550341662)\n[추천 브로치(사진)](https://sw-astera.tistory.com/2)\n[브로치 합성 팁](https://discord.com/channels/857371775683133480/857381375279759360/857621097952575529)")
        await message.channel.send(embed=embed)
    elif message.content == "!아카식":
        embed = discord.Embed(
            title="아카식과 관련된 정보입니다!", description="아카식 레코드는 캐릭터의 능력치를 높여 주거나, 사냥에 도움을 주는 카드 장비 시스템입니다. 주로 사용하는 아카식 리스트가 정해져 있기 때문에, 이 위주로 세팅하는 것이 좋습니다.\n\n[추천 아카식 레코드](https://discord.com/channels/857371775683133480/857381375279759360/857662100285161492)\n[4, 5성 추천 아카식 레코드](https://sw-astera.tistory.com/3)\n[아카식 레코드 합성, 결합 팁](https://discord.com/channels/857371775683133480/857381375279759360/857668257074774044)")
        await message.channel.send(embed=embed)
    elif message.content == "!칭호":
        embed = discord.Embed(
            title="칭호와 관련된 정보입니다!", description="칭호는 캐릭터 닉네임 위를 꾸며주는 요소이면서,\n능력치까지 있는 중요한 장비 아이템입니다 ✨\n\n[종결 칭호 얻는 방법](https://discord.com/channels/857371775683133480/857381375279759360/857687909556682763)\n[능력치는 그대로 받으면서, 다른 칭호 이름 보여주기](https://discord.com/channels/857371775683133480/857381375279759360/858012783429419028)")
        await message.channel.send(embed=embed)
    elif message.content == "!적중도":
        embed = discord.Embed(
            title="적중도와 관련된 정보입니다!", description="적중도는 소울워커에서 중요한 능력치입니다 🔥\n적중도가 낮으면 몬스터에게 데미지가 들어가지 않습니다. (빗나감)\n\n그리고 적중도가 높으면 치명타 확률이 추가 증가합니다.\n\n[적중도와 치명타 확률의 관계](https://discord.com/channels/857371775683133480/857381375279759360/857670942096490527)")
        await message.channel.send(embed=embed)
    elif message.content == "!레이드":
        embed = discord.Embed(
            title="레이드와 관련된 정보입니다!", description="레이드 던전은 많이 있지만,\n여기서는 대표적인 파티/포스 레이드 위주를 소개합니다.\n\n[히든 하이드아웃 커트라인/공략](https://discord.com/channels/857371775683133480/857381625172328478/857527264735920158)\n[루나폴 커트라인/공략](https://discord.com/channels/857371775683133480/857381625172328478/857530277886165042)\n[바이올런트 선 커트라인/공략](https://discord.com/channels/857371775683133480/857381625172328478/857533226855956480)\n[브로큰 세이비어 커트라인/공략](https://discord.com/channels/857371775683133480/857381625172328478/858013749210644532)")
        await message.channel.send(embed=embed)
    elif message.content == "!도핑":
        embed = discord.Embed(
            title="도핑과 관련된 정보입니다!", description="도핑은 캐릭터의 능력치를 일시적으로 높여 주는 아이템입니다 🍎\n퍼퓸이 있으며, 이벤트나 부커TV 상점에서 구할 수 있습니다.\n\n또한 생존이나 유틸에 도움이 되는 포션도 함께 소개합니다!\n\n[캐릭터를 강화하는 물약(도핑)](https://discord.com/channels/857371775683133480/857381375279759360/857874272990134322)\n[생존이나 유틸 확보에 도움이 되는 포션 정리](https://discord.com/channels/857371775683133480/857381375279759360/858082426122141756)")
        await message.channel.send(embed=embed)
    elif message.content == "!무적기":
        embed = discord.Embed(
            title="무적기와 관련된 정보입니다!", description="캐릭터마다 무적 효과가 있는 스킬이 있습니다.\n이런 특성을 파악하면, 패턴 중에도 안정적인 딜링이 가능합니다.\n\n그리고 체력을 홀수로 만들면, 생존에 많은 도움이 됩니다.\n\n[무적기를 이용한 딜링](https://discord.com/channels/857371775683133480/857381375279759360/857700466829295637)\n[콤보의 중요성](https://discord.com/channels/857371775683133480/857381375279759360/857881578218979339)\n[회피 기술과 회피도](https://discord.com/channels/857371775683133480/857381375279759360/857671628301271070)\n[홀수 체력(HP) 만드는 방법](https://discord.com/channels/857371775683133480/857381375279759360/857876713596911636)")
        await message.channel.send(embed=embed)
    elif message.content == "!숙제":
        embed = discord.Embed(
            title="숙제와 관련된 정보입니다!", description="매일 하면 좋은 숙제를 정리했습니다.\n\n[공통 숙제 정리](https://discord.com/channels/857371775683133480/857381576794832906/857495964176875530)")
        await message.channel.send(embed=embed)
    elif message.content == "!재화":
        embed = discord.Embed(
            title="재화 수급과 관련된 정보입니다!", description="소울워커 기본 재화는 제니, B.P, 에텔, 그루톤 코인이 있습니다.\n이 외에도 스펙업에 필요한 재료들이 있으며, 수급 방법이 다양합니다 💎\n\n[기본 재화 종류와 설명](https://discord.com/channels/857371775683133480/857382076432121856/857501264858578966)\n[데이드림 시리즈 (제니, 에너지 컨버터 등)](https://discord.com/channels/857371775683133480/857382076432121856/857505405542596609)\n[히든 하이드아웃/루나폴 레이드(제니, B.P, 에텔 등)](https://discord.com/channels/857371775683133480/857382076432121856/857507028837859328)\n[스카이클락 팰리스 하드(그루톤 코인, 태그 등)](https://discord.com/channels/857371775683133480/857382076432121856/857507874338373655)\n[월드보스 더 둠 (성순, B.P 등)](https://discord.com/channels/857371775683133480/857382076432121856/857509397114388480)\n[독서 (B.P, 에너지 컨버터 부품)](https://discord.com/channels/857371775683133480/857382076432121856/857510422956343337)\n[티끌런 (티끌 = 바이올런트 선 장비 제작 재료)](https://discord.com/channels/857371775683133480/857382076432121856/857511069865869333)\n[테네런 (제니)](https://discord.com/channels/857371775683133480/857382076432121856/857512933738676225)\n[점유작, 점유율작 (부캐로 점유율 보상 챙기기)](https://discord.com/channels/857371775683133480/857382076432121856/857515582336663562)\n[파방냥이 (부캐로 강화 파괴 방지 장치 수급)](https://discord.com/channels/857371775683133480/857382076432121856/857516969065447454)\n[리그 레이드 (리그 레이드 코인)](https://discord.com/channels/857371775683133480/857382076432121856/857518054106464296)\n[주간 랭킹 (B.P, 에너지 컨버터)](https://discord.com/channels/857371775683133480/857382076432121856/857518820649861120)")
        await message.channel.send(embed=embed)
    elif message.content == "!퀘스트":
        embed = discord.Embed(
            title="퀘스트와 관련된 정보입니다!", description="메인 퀘스트가 막혔을 때, 보상이 좋은 퀘스트가 궁금할 때 등\n도움이 될 수 있도록 퀘스트를 정리했습니다 📖\n\n[퀘스트 종류와 구분하는 방법](https://discord.com/channels/857371775683133480/857889654892134420/857892483693412372)\n[메인 퀘스트가 끊겼을 때 (경험치용 퀘스트)](https://discord.com/channels/857371775683133480/857889654892134420/857892055509368864)\n[권장하는 서브 퀘스트 목록 I](https://discord.com/channels/857371775683133480/857889654892134420/857895925229158400)\n[권장하는 서브 퀘스트 목록 II](https://discord.com/channels/857371775683133480/857889654892134420/857896735039684608)\n[레이드 입장을 위한 선행 퀘스트](https://discord.com/channels/857371775683133480/857889654892134420/857899874619490334)\n[데자이어 각성 퀘스트](https://discord.com/channels/857371775683133480/857889654892134420/857910534531579915)")
        await message.channel.send(embed=embed)
    elif message.content == "!코스튬":
        embed = discord.Embed(
            title="코스튬과 관련된 정보입니다!", description="[코스튬 염색](https://discord.com/channels/857371775683133480/857381375279759360/857674732835831869)\n[코스튬 포장 (재판매하는 방법)](https://discord.com/channels/857371775683133480/857381375279759360/857676655195586580)\n[거래소 이용 팁](https://discord.com/channels/857371775683133480/857381375279759360/857677183736479754)")
        await message.channel.send(embed=embed)
    elif message.content == "!최적화":
        embed = discord.Embed(
            title="최적화 설정과 관련된 정보입니다!", description="소울워커는 최적화가 미흡한 편입니다 😢\n아래 링크의 게임 설정을 참고하면, 렉을 줄일 수 있습니다.\n\n[소울워커 최적화를 위한 게임 설정](https://discord.com/channels/857371775683133480/857381785570770953/857524020521074709)")
        await message.channel.send(embed=embed)
    elif message.content == "!프리카메라":
        embed = discord.Embed(
            title="프리 카메라와 관련된 정보입니다!", description="소울워커는 캐릭터 스크린샷을\n예쁘게 촬영할 수 있도록 재밌는 기능을 제공하고 있습니다 🎀\n\n[자유로운 카메라 시점(프리카메라)](https://discord.com/channels/857371775683133480/857381375279759360/857678070756147210)")
        await message.channel.send(embed=embed)
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
