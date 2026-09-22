#!/usr/bin/env python3
"""名言/语录站生成脚本"""

import os
import json
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
SITE_URL = "https://211014049.github.io/mingyan"
SITE_NAME = "名言谷"
SITE_DESC = "收录精选名人名言、经典语录、励志句子，按分类浏览，点亮你的每一天"

# ========== 分类数据 ==========
CATEGORIES = [
    {"slug": "aiqing", "name": "爱情", "icon": "💕", "desc": "关于爱情的名言佳句，感受爱的力量与美好"},
    {"slug": "lizhi", "name": "励志", "icon": "💪", "desc": "励志名言激励你勇往直前，追逐梦想"},
    {"slug": "rensheng", "name": "人生", "icon": "🌟", "desc": "人生哲理名言，领悟生活的真谛"},
    {"slug": "xuexi", "name": "学习", "icon": "📚", "desc": "关于学习与读书的名言，知识改变命运"},
    {"slug": "gongzuo", "name": "工作", "icon": "💼", "desc": "职场与工作名言，助你事业有成"},
    {"slug": "youqing", "name": "友情", "icon": "🤝", "desc": "友谊名言，珍惜身边的每一位朋友"},
    {"slug": "chengzhang", "name": "成长", "icon": "🌱", "desc": "成长路上的智慧箴言，陪伴你蜕变"},
    {"slug": "mengxiang", "name": "梦想", "icon": "🌈", "desc": "关于梦想的名言，让梦想照进现实"},
    {"slug": "shijian", "name": "时间", "icon": "⏰", "desc": "珍惜时间的名言，一寸光阴一寸金"},
    {"slug": "jianchi", "name": "坚持", "icon": "🏔️", "desc": "坚持就是胜利，永不放弃的名言"},
    {"slug": "zixin", "name": "自信", "icon": "✨", "desc": "自信是成功的第一步，自信名言"},
    {"slug": "yongqi", "name": "勇气", "icon": "🦁", "desc": "勇气名言，无畏前行的力量"},
    {"slug": "ganen", "name": "感恩", "icon": "🙏", "desc": "感恩名言，心怀感恩，生活更美好"},
    {"slug": "kuaile", "name": "快乐", "icon": "😊", "desc": "关于快乐的名言，寻找生活的幸福"},
    {"slug": "tongku", "name": "痛苦", "icon": "💔", "desc": "痛苦与挫折名言，从苦难中汲取力量"},
    {"slug": "jimo", "name": "孤独", "icon": "🌙", "desc": "孤独与寂寞名言，享受独处的时光"},
    {"slug": "siyuan", "name": "思念", "icon": "🌙", "desc": "思念与想念的句子，寄托心中牵挂"},
    {"slug": "liuxue", "name": "离别", "icon": "🍂", "desc": "离别与不舍的名言，珍重再见"},
    {"slug": "jiaoting", "name": "家庭", "icon": "🏠", "desc": "家庭与亲情名言，温暖的港湾"},
    {"slug": "youmo", "name": "幽默", "icon": "😄", "desc": "幽默风趣的名言，笑对人生"},
    {"slug": "zhihui", "name": "智慧", "icon": "🧠", "desc": "智慧名言，开启思维的大门"},
    {"slug": "daode", "name": "道德", "icon": "⚖️", "desc": "道德与品格名言，立身之本"},
    {"slug": "lxiang", "name": "理想", "icon": "🎯", "desc": "理想与信念名言，心有所向"},
    {"slug": "mingyun", "name": "命运", "icon": "🌊", "desc": "命运与机遇名言，把握人生"},
    {"slug": "chenggong", "name": "成功", "icon": "🏆", "desc": "成功之道的名言，通往胜利的路"},
    {"slug": "shibai", "name": "失败", "icon": "🌪️", "desc": "失败与挫折名言，跌倒后重新站起"},
    {"slug": "xiguan", "name": "习惯", "icon": "🔄", "desc": "习惯与自律名言，优秀是一种习惯"},
    {"slug": "jiankang", "name": "健康", "icon": "❤️", "desc": "健康名言，身体是革命的本钱"},
    {"slug": "meili", "name": "美丽", "icon": "🌸", "desc": "美与美的名言，发现生活中的美"},
    {"slug": "mingren", "name": "名人", "icon": "👑", "desc": "古今中外名人名言合集"},
    {"slug": "gushi", "name": "古诗", "icon": "📜", "desc": "古诗词名句，千年文化的智慧"},
    {"slug": "yulu", "name": "语录", "icon": "💬", "desc": "经典语录合集，字字珠玑"},
]

CAT_MAP = {c["slug"]: c for c in CATEGORIES}

# ========== 名言数据 ==========
QUOTES = [
    # 爱情
    {"text": "两情若是久长时，又岂在朝朝暮暮。", "author": "秦观", "cats": ["aiqing", "gushi", "mingren"]},
    {"text": "人生若只如初见，何事秋风悲画扇。", "author": "纳兰性德", "cats": ["aiqing", "gushi", "rensheng"]},
    {"text": "问世间情为何物，直教生死相许。", "author": "元好问", "cats": ["aiqing", "gushi", "mingren"]},
    {"text": "愿得一人心，白首不相离。", "author": "卓文君", "cats": ["aiqing", "gushi"]},
    {"text": "在天愿作比翼鸟，在地愿为连理枝。", "author": "白居易", "cats": ["aiqing", "gushi", "mingren"]},
    {"text": "爱情不是花荫下的甜言，不是桃花源中的蜜语，不是轻绵的眼泪，更不是死硬的强迫，爱情是建立在共同语言的基础上的。", "author": "莎士比亚", "cats": ["aiqing", "mingren"]},
    {"text": "真正的爱情是不能用言语表达的，行为才是忠心的最好说明。", "author": "莎士比亚", "cats": ["aiqing", "mingren"]},
    {"text": "爱就是充实了的生命，正如盛满了酒的酒杯。", "author": "泰戈尔", "cats": ["aiqing", "mingren", "kuaile"]},
    {"text": "爱情是理想的一致，意志的融合。", "author": "雨果", "cats": ["aiqing", "mingren", "lxiang"]},
    {"text": "曾经沧海难为水，除却巫山不是云。", "author": "元稹", "cats": ["aiqing", "gushi", "siyuan"]},
    {"text": "衣带渐宽终不悔，为伊消得人憔悴。", "author": "柳永", "cats": ["aiqing", "gushi", "jianchi"]},
    {"text": "相见时难别亦难，东风无力百花残。", "author": "李商隐", "cats": ["aiqing", "liuxue", "gushi"]},
    {"text": "身无彩凤双飞翼，心有灵犀一点通。", "author": "李商隐", "cats": ["aiqing", "gushi"]},
    {"text": "春蚕到死丝方尽，蜡炬成灰泪始干。", "author": "李商隐", "cats": ["aiqing", "jianchi", "gushi"]},
    {"text": "我如果爱你，绝不像攀援的凌霄花，借你的高枝炫耀自己。", "author": "舒婷", "cats": ["aiqing", "zixin"]},
    {"text": "真正的爱情能够鼓舞人，唤醒他内心沉睡着的力量和潜藏着的才能。", "author": "薄伽丘", "cats": ["aiqing", "lizhi"]},
    {"text": "爱之花开放的地方，生命便能欣欣向荣。", "author": "梵高", "cats": ["aiqing", "kuaile", "mingren"]},
    {"text": "爱整个人类可能是一件易事，认真地去爱上一个人却很难。", "author": "佚名", "cats": ["aiqing"]},
    {"text": "爱情中的苦与乐始终都在相互争斗。", "author": "奥维德", "cats": ["aiqing", "tongku"]},
    {"text": "爱是生命的火焰，没有它，一切变成黑夜。", "author": "罗曼·罗兰", "cats": ["aiqing", "rensheng", "mingren"]},

    # 励志
    {"text": "天行健，君子以自强不息。", "author": "周易", "cats": ["lizhi", "jianchi", "gushi"]},
    {"text": "千里之行，始于足下。", "author": "老子", "cats": ["lizhi", "shijian", "gushi"]},
    {"text": "不积跬步，无以至千里；不积小流，无以成江海。", "author": "荀子", "cats": ["lizhi", "jianchi", "gushi"]},
    {"text": "业精于勤，荒于嬉；行成于思，毁于随。", "author": "韩愈", "cats": ["lizhi", "xuexi", "gushi"]},
    {"text": "少壮不努力，老大徒伤悲。", "author": "汉乐府", "cats": ["lizhi", "shijian", "gushi"]},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "古训", "cats": ["lizhi", "jianchi", "tongku"]},
    {"text": "吃得苦中苦，方为人上人。", "author": "古训", "cats": ["lizhi", "tongku", "chenggong"]},
    {"text": "世上无难事，只怕有心人。", "author": "古训", "cats": ["lizhi", "jianchi"]},
    {"text": "天生我材必有用，千金散尽还复来。", "author": "李白", "cats": ["lizhi", "zixin", "gushi"]},
    {"text": "长风破浪会有时，直挂云帆济沧海。", "author": "李白", "cats": ["lizhi", "mengxiang", "gushi"]},
    {"text": "路漫漫其修远兮，吾将上下而求索。", "author": "屈原", "cats": ["lizhi", "jianchi", "gushi"]},
    {"text": "燕雀安知鸿鹄之志哉！", "author": "陈涉", "cats": ["lizhi", "lxiang", "mingren"]},
    {"text": "不想当将军的士兵不是好士兵。", "author": "拿破仑", "cats": ["lizhi", "lxiang", "mingren"]},
    {"text": "天才是百分之一的灵感加百分之九十九的汗水。", "author": "爱迪生", "cats": ["lizhi", "xuexi", "mingren"]},
    {"text": "成功的秘诀，在永不改变既定的目的。", "author": "卢梭", "cats": ["lizhi", "jianchi", "chenggong"]},
    {"text": "伟大的工作，并不是用力量而是用耐心去完成的。", "author": "约翰逊", "cats": ["lizhi", "jianchi", "chenggong"]},
    {"text": "没有伟大的愿望，就没有伟大的天才。", "author": "巴尔扎克", "cats": ["lizhi", "mengxiang"]},
    {"text": "人生不是一种享乐，而是一桩十分沉重的工作。", "author": "列夫·托尔斯泰", "cats": ["lizhi", "rensheng"]},
    {"text": "所谓活着的人，就是不断挑战的人，不断攀登命运险峰的人。", "author": "雨果", "cats": ["lizhi", "mingyun", "chengzhang"]},
    {"text": "最可怕的敌人，就是没有坚强的信念。", "author": "罗曼·罗兰", "cats": ["lizhi", "zixin", "jianchi"]},
    {"text": "只要持续地努力，不懈地奋斗，就没有征服不了的东西。", "author": "塞内加", "cats": ["lizhi", "jianchi"]},
    {"text": "立志不坚，终不济事。", "author": "朱熹", "cats": ["lizhi", "jianchi", "gushi"]},
    {"text": "穷且益坚，不坠青云之志。", "author": "王勃", "cats": ["lizhi", "lxiang", "gushi"]},
    {"text": "老骥伏枥，志在千里；烈士暮年，壮心不已。", "author": "曹操", "cats": ["lizhi", "lxiang", "gushi"]},
    {"text": "玉不琢，不成器；人不学，不知道。", "author": "礼记", "cats": ["lizhi", "xuexi", "gushi"]},

    # 人生
    {"text": "人生自古谁无死，留取丹心照汗青。", "author": "文天祥", "cats": ["rensheng", "gushi", "mingren"]},
    {"text": "人固有一死，或重于泰山，或轻于鸿毛。", "author": "司马迁", "cats": ["rensheng", "mingren", "gushi"]},
    {"text": "人生得意须尽欢，莫使金樽空对月。", "author": "李白", "cats": ["rensheng", "kuaile", "gushi"]},
    {"text": "人生天地之间，若白驹过隙，忽然而已。", "author": "庄子", "cats": ["rensheng", "shijian", "gushi"]},
    {"text": "生活不是等待风暴过去，而是学会在雨中跳舞。", "author": "维维安·格林", "cats": ["rensheng", "yongqi", "kuaile"]},
    {"text": "人生就像骑自行车，想保持平衡就得往前走。", "author": "爱因斯坦", "cats": ["rensheng", "chengzhang", "mingren"]},
    {"text": "人生的价值，并不是用时间，而是用深度去衡量的。", "author": "列夫·托尔斯泰", "cats": ["rensheng", "jiazhi", "mingren"]},
    {"text": "人生不是一支短短的蜡烛，而是一支由我们暂时拿着的火炬。", "author": "萧伯纳", "cats": ["rensheng", "jiazhi"]},
    {"text": "我们的人生随我们花费多少努力而具有多少价值。", "author": "莫利亚克", "cats": ["rensheng", "jiazhi", "fenDou"]},
    {"text": "人生最重要的不是所处的位置，而是所朝的方向。", "author": "奥利弗·温德尔·霍姆斯", "cats": ["rensheng", "mengxiang"]},
    {"text": "人生就像一杯茶，不会苦一辈子，但总会苦一阵子。", "author": "佚名", "cats": ["rensheng", "tongku", "kuaile"]},
    {"text": "人生没有彩排，每一天都是现场直播。", "author": "佚名", "cats": ["rensheng", "shijian"]},
    {"text": "人生如逆旅，我亦是行人。", "author": "苏轼", "cats": ["rensheng", "gushi", "liuxue"]},
    {"text": "回首向来萧瑟处，归去，也无风雨也无晴。", "author": "苏轼", "cats": ["rensheng", "gushi", "kuaile"]},
    {"text": "人有悲欢离合，月有阴晴圆缺，此事古难全。", "author": "苏轼", "cats": ["rensheng", "gushi", "tongku"]},
    {"text": "生命不是要超越别人，而是要超越自己。", "author": "佚名", "cats": ["rensheng", "chengzhang", "lizhi"]},
    {"text": "人生最大的荣耀不在于从不跌倒，而在于每次跌倒后都爬起来。", "author": "纳尔逊·曼德拉", "cats": ["rensheng", "shibai", "jianchi"]},
    {"text": "世界上只有一种真正的英雄主义，那就是在认清生活的真相后依然热爱生活。", "author": "罗曼·罗兰", "cats": ["rensheng", "yongqi", "kuaile"]},
    {"text": "生活中最重要的事情不是胜利，而是奋斗；不是征服，而是努力拼搏。", "author": "顾拜旦", "cats": ["rensheng", "lizhi"]},
    {"text": "人的一生可能燃烧也可能腐朽，我不能腐朽，我愿意燃烧起来！", "author": "奥斯特洛夫斯基", "cats": ["rensheng", "jiazhi", "lizhi"]},

    # 学习
    {"text": "学而时习之，不亦说乎？", "author": "孔子", "cats": ["xuexi", "gushi", "mingren"]},
    {"text": "学而不思则罔，思而不学则殆。", "author": "孔子", "cats": ["xuexi", "zhihui", "gushi"]},
    {"text": "三人行，必有我师焉。", "author": "孔子", "cats": ["xuexi", "qianxu", "gushi"]},
    {"text": "温故而知新，可以为师矣。", "author": "孔子", "cats": ["xuexi", "gushi"]},
    {"text": "知之为知之，不知为不知，是知也。", "author": "孔子", "cats": ["xuexi", "zhihui", "gushi"]},
    {"text": "书山有路勤为径，学海无涯苦作舟。", "author": "韩愈", "cats": ["xuexi", "lizhi", "gushi"]},
    {"text": "黑发不知勤学早，白首方悔读书迟。", "author": "颜真卿", "cats": ["xuexi", "shijian", "gushi"]},
    {"text": "读书破万卷，下笔如有神。", "author": "杜甫", "cats": ["xuexi", "gushi"]},
    {"text": "问渠那得清如许，为有源头活水来。", "author": "朱熹", "cats": ["xuexi", "gushi", "zhihui"]},
    {"text": "纸上得来终觉浅，绝知此事要躬行。", "author": "陆游", "cats": ["xuexi", "shijian", "gushi"]},
    {"text": "知识就是力量。", "author": "培根", "cats": ["xuexi", "zhihui", "mingren"]},
    {"text": "读书是在别人思想的帮助下，建立起自己的思想。", "author": "鲁巴金", "cats": ["xuexi", "zhihui"]},
    {"text": "我学习了一生，现在我还在学习。", "author": "别林斯基", "cats": ["xuexi", "chengzhang"]},
    {"text": "学到很多东西的诀窍，就是一下子不要学很多。", "author": "洛克", "cats": ["xuexi", "fangfa"]},
    {"text": "读书是易事，思索是难事，但两者缺一，便全无用处。", "author": "富兰克林", "cats": ["xuexi", "zhihui"]},
    {"text": "活到老，学到老。", "author": "古训", "cats": ["xuexi", "chengzhang"]},
    {"text": "学然后知不足，教然后知困。", "author": "礼记", "cats": ["xuexi", "gushi"]},
    {"text": "玉不琢，不成器；人不学，不知道。", "author": "礼记", "cats": ["xuexi", "lizhi", "gushi"]},
    {"text": "敏而好学，不耻下问。", "author": "孔子", "cats": ["xuexi", "qianxu", "gushi"]},
    {"text": "知之者不如好之者，好之者不如乐之者。", "author": "孔子", "cats": ["xuexi", "kuaile", "gushi"]},

    # 工作
    {"text": "天才就是长期劳动的结果。", "author": "牛顿", "cats": ["gongzuo", "lizhi", "mingren"]},
    {"text": "成功等于百分之九十九的汗水加百分之一的灵感。", "author": "爱迪生", "cats": ["gongzuo", "chenggong", "lizhi"]},
    {"text": "工作就是人生的价值，人生的欢乐，也是幸福之所在。", "author": "罗丹", "cats": ["gongzuo", "jiazhi", "kuaile"]},
    {"text": "人生在勤，不索何获。", "author": "张衡", "cats": ["gongzuo", "lizhi", "gushi"]},
    {"text": "业精于勤荒于嬉，行成于思毁于随。", "author": "韩愈", "cats": ["gongzuo", "xuexi", "gushi"]},
    {"text": "一勤天下无难事。", "author": "古训", "cats": ["gongzuo", "lizhi"]},
    {"text": "今天所做之事勿候明天，自己所做之事勿候他人。", "author": "歌德", "cats": ["gongzuo", "shijian"]},
    {"text": "把每一件简单的事做好就是不简单，把每一件平凡的事做好就是不平凡。", "author": "张瑞敏", "cats": ["gongzuo", "chenggong"]},
    {"text": "世上没有绝望的处境，只有对处境绝望的人。", "author": "佚名", "cats": ["gongzuo", "yongqi"]},
    {"text": "行动是治愈恐惧的良药，而犹豫拖延将不断滋养恐惧。", "author": "卡耐基", "cats": ["gongzuo", "yongqi"]},
    {"text": "不要等待机会，而要创造机会。", "author": "萧伯纳", "cats": ["gongzuo", "mingyun"]},
    {"text": "一个有信念者所开发出的力量，大于个只有兴趣者。", "author": "梭罗", "cats": ["gongzuo", "zixin"]},
    {"text": "每一发奋努力的背后，必有加倍的赏赐。", "author": "佚名", "cats": ["gongzuo", "chenggong"]},
    {"text": "人生伟业的建立，不在能知，乃在能行。", "author": "赫胥黎", "cats": ["gongzuo", "chenggong", "rensheng"]},
    {"text": "任何的限制，都是从自己的内心开始的。", "author": "佚名", "cats": ["gongzuo", "zixin"]},

    # 友情
    {"text": "海内存知己，天涯若比邻。", "author": "王勃", "cats": ["youqing", "gushi", "liuxue"]},
    {"text": "莫愁前路无知己，天下谁人不识君。", "author": "高适", "cats": ["youqing", "liuxue", "gushi"]},
    {"text": "桃花潭水深千尺，不及汪伦送我情。", "author": "李白", "cats": ["youqing", "gushi"]},
    {"text": "劝君更尽一杯酒，西出阳关无故人。", "author": "王维", "cats": ["youqing", "liuxue", "gushi"]},
    {"text": "有朋自远方来，不亦乐乎？", "author": "孔子", "cats": ["youqing", "kuaile", "gushi"]},
    {"text": "朋友是生活中的阳光。", "author": "易卜生", "cats": ["youqing", "kuaile"]},
    {"text": "真正的友谊既能容忍朋友提出的劝告，又有使自己接受劝告。", "author": "西塞罗", "cats": ["youqing", "zhihui"]},
    {"text": "友谊永远是一个甜柔的责任，从来不是一种机会。", "author": "纪伯伦", "cats": ["youqing", "zhencheng"]},
    {"text": "世间最美好的东西，莫过于有几个头脑和心地都很正直的严正的朋友。", "author": "爱因斯坦", "cats": ["youqing", "meihao"]},
    {"text": "患难识朋友。", "author": "列宁", "cats": ["youqing", "tongku"]},
    {"text": "兄弟可能不是朋友，但朋友常常如兄弟。", "author": "富兰克林", "cats": ["youqing", "jiaoting"]},
    {"text": "人生最美好的东西，就是他同别人的友谊。", "author": "林肯", "cats": ["youqing", "meihao", "rensheng"]},

    # 成长
    {"text": "成长是一场和自己的比赛，你要做的就是比昨天的自己更好一点。", "author": "佚名", "cats": ["chengzhang", "lizhi"]},
    {"text": "不要着急，最好的总会在最不经意的时候出现。", "author": "泰戈尔", "cats": ["chengzhang", "kuaile"]},
    {"text": "你今天的苦果，是昨天的伏笔；当下的付出，是明日的花开。", "author": "佚名", "cats": ["chengzhang", "jianchi"]},
    {"text": "成长的过程就是不断发现自己以前是傻逼的过程。", "author": "佚名", "cats": ["chengzhang", "zhihui"]},
    {"text": "人之所以痛苦，在于追求错误的东西。", "author": "佚名", "cats": ["chengzhang", "tongku", "zhihui"]},
    {"text": "真正的成长，是学会与不完美的自己和解。", "author": "佚名", "cats": ["chengzhang", "zixin"]},
    {"text": "你若盛开，蝴蝶自来；你若精彩，天自安排。", "author": "佚名", "cats": ["chengzhang", "nuli"]},
    {"text": "所有的胜利，与征服自己的胜利比起来，都是微不足道。", "author": "柏拉图", "cats": ["chengzhang", "zixin", "chenggong"]},
    {"text": "最大的挑战和突破在于用人，而用人最大的突破在于信任人。", "author": "马云", "cats": ["chengzhang", "guanli"]},
    {"text": "今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上。", "author": "马云", "cats": ["chengzhang", "jianchi", "mingren"]},

    # 梦想
    {"text": "梦想还是要有的，万一实现了呢？", "author": "马云", "cats": ["mengxiang", "mingren", "lizhi"]},
    {"text": "世界上最快乐的事，莫过于为理想而奋斗。", "author": "苏格拉底", "cats": ["mengxiang", "kuaile", "lizhi"]},
    {"text": "一个人的理想越崇高，生活越纯洁。", "author": "伏尼契", "cats": ["mengxiang", "rensheng"]},
    {"text": "人的活动如果没有理想的鼓舞，就会变得空虚而渺小。", "author": "车尔尼雪夫斯基", "cats": ["mengxiang", "lizhi"]},
    {"text": "我梦想有一天，这个国家会站立起来，真正实现其信条的真谛。", "author": "马丁·路德·金", "cats": ["mengxiang", "mingren"]},
    {"text": "不要只因一次失败，就放弃你原来决心想达到的目的。", "author": "莎士比亚", "cats": ["mengxiang", "shibai", "jianchi"]},
    {"text": "志当存高远。", "author": "诸葛亮", "cats": ["mengxiang", "lizhi", "gushi"]},
    {"text": "非淡泊无以明志，非宁静无以致远。", "author": "诸葛亮", "cats": ["mengxiang", "gushi", "xinjing"]},
    {"text": "为中华之崛起而读书。", "author": "周恩来", "cats": ["mengxiang", "xuexi", "mingren"]},
    {"text": "理想是指路明灯。没有理想，就没有坚定的方向。", "author": "托尔斯泰", "cats": ["mengxiang", "lizhi"]},
    {"text": "生活中没有理想的人，是可怜的。", "author": "屠格涅夫", "cats": ["mengxiang", "rensheng"]},
    {"text": "人生最高之理想，在求达于真理。", "author": "李大钊", "cats": ["mengxiang", "zhenli", "mingren"]},

    # 时间
    {"text": "一寸光阴一寸金，寸金难买寸光阴。", "author": "古训", "cats": ["shijian", "zhenxi", "gushi"]},
    {"text": "盛年不重来，一日难再晨。及时当勉励，岁月不待人。", "author": "陶渊明", "cats": ["shijian", "lizhi", "gushi"]},
    {"text": "逝者如斯夫，不舍昼夜。", "author": "孔子", "cats": ["shijian", "gushi", "gankai"]},
    {"text": "时间就像海绵里的水，只要愿挤，总还是有的。", "author": "鲁迅", "cats": ["shijian", "mingren"]},
    {"text": "你热爱生命吗？那么别浪费时间，因为时间是组成生命的材料。", "author": "富兰克林", "cats": ["shijian", "shengming"]},
    {"text": "世界上最快而又最慢，最长而又最短，最平凡而又最珍贵，最易被忽视而又最令人后悔的就是时间。", "author": "高尔基", "cats": ["shijian", "zhenxi"]},
    {"text": "时间是最公平合理的，它从不多给谁一份。", "author": "高尔基", "cats": ["shijian", "gongping"]},
    {"text": "不要为已消尽之年华叹息，必须正视匆匆溜走的时光。", "author": "布莱希特", "cats": ["shijian", "yongqi"]},
    {"text": "在所有的批评家中，最伟大、最正确、最天才的是时间。", "author": "别林斯基", "cats": ["shijian", "zhihui"]},
    {"text": "年华一去不复返，事业放弃在难成。", "author": "佚名", "cats": ["shijian", "shiye"]},

    # 坚持
    {"text": "锲而舍之，朽木不折；锲而不舍，金石可镂。", "author": "荀子", "cats": ["jianchi", "lizhi", "gushi"]},
    {"text": "千里之行，始于足下。", "author": "老子", "cats": ["jianchi", "lizhi", "gushi"]},
    {"text": "不积跬步，无以至千里；不积小流，无以成江海。", "author": "荀子", "cats": ["jianchi", "lizhi", "gushi"]},
    {"text": "只要功夫深，铁杵磨成针。", "author": "古训", "cats": ["jianchi", "lizhi"]},
    {"text": "滴水能把石穿透，万事功到自然成。", "author": "古训", "cats": ["jianchi", "chenggong"]},
    {"text": "成功的秘诀，在永不改变既定的目的。", "author": "卢梭", "cats": ["jianchi", "chenggong"]},
    {"text": "伟大的作品不是靠力量，而是靠坚持来完成的。", "author": "约翰逊", "cats": ["jianchi", "chenggong"]},
    {"text": "要从容地着手去做一件事，但一旦开始，就要坚持到底。", "author": "比阿斯", "cats": ["jianchi", "yongqi"]},
    {"text": "不经一翻彻骨寒，怎得梅花扑鼻香。", "author": "黄蘖禅师", "cats": ["jianchi", "tongku", "gushi"]},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "古训", "cats": ["jianchi", "tongku", "lizhi"]},
    {"text": "坚持意志伟大的事业需要始终不渝的精神。", "author": "伏尔泰", "cats": ["jianchi", "shiye"]},
    {"text": "最可怕的敌人，就是没有坚强的信念。", "author": "罗曼·罗兰", "cats": ["jianchi", "zixin", "lizhi"]},

    # 自信
    {"text": "天生我材必有用，千金散尽还复来。", "author": "李白", "cats": ["zixin", "lizhi", "gushi"]},
    {"text": "自信是成功的第一秘诀。", "author": "爱默生", "cats": ["zixin", "chenggong", "mingren"]},
    {"text": "先相信你自己，然后别人才会相信你。", "author": "屠格涅夫", "cats": ["zixin", "rensheng"]},
    {"text": "地球上的任何一点离太阳都同样地遥远。", "author": "伯顿", "cats": ["zixin", "gongping"]},
    {"text": "我们对自己抱有的信心，将使别人对我们萌生信心的绿芽。", "author": "拉劳士福古", "cats": ["zixin", "yingxiang"]},
    {"text": "除了人格以外，人生最大的损失，莫过于失掉自信心了。", "author": "培尔辛", "cats": ["zixin", "rensheng"]},
    {"text": "有信心的人，可以化渺小为伟大，化平庸为神奇。", "author": "萧伯纳", "cats": ["zixin", "shenqi"]},
    {"text": "坚决的信心，能使平凡的人们，做出惊人的事业。", "author": "马尔顿", "cats": ["zixin", "shiye"]},
    {"text": "自信与骄傲有异；自信者常沉着，而骄傲者常浮扬。", "author": "梁启超", "cats": ["zixin", "qianxu"]},
    {"text": "恢弘志士之气，不宜妄自菲薄。", "author": "诸葛亮", "cats": ["zixin", "lizhi", "gushi"]},

    # 勇气
    {"text": "勇敢里面有天才、力量和魔法。", "author": "歌德", "cats": ["yongqi", "zhihui"]},
    {"text": "勇气是衡量灵魂大小的标准。", "author": "卡耐基", "cats": ["yongqi", "linghun"]},
    {"text": "世界上只有一种真正的英雄主义，那就是在认清生活的真相后依然热爱生活。", "author": "罗曼·罗兰", "cats": ["yongqi", "rensheng", "kuaile"]},
    {"text": "真正的勇气不是无畏，而是带着恐惧前行。", "author": "佚名", "cats": ["yongqi", "chengzhang"]},
    {"text": "勇气是人类最重要的一种特质，倘若有了勇气，人类其他的特质自然也就具备了。", "author": "丘吉尔", "cats": ["yongqi", "tezhi"]},
    {"text": "大胆点，伟大的力量会来帮助你的。", "author": "爱默生", "cats": ["yongqi", "lizhi"]},
    {"text": "匹夫见辱，拔剑而起，挺身而斗，此不足为勇也。天下有大勇者，猝然临之而不惊，无故加之而不怒。", "author": "苏轼", "cats": ["yongqi", "gushi", "xinjing"]},
    {"text": "不入虎穴，焉得虎子。", "author": "古训", "cats": ["yongqi", "chenggong", "gushi"]},
    {"text": "勇者无畏，智者不惑。", "author": "古训", "cats": ["yongqi", "zhihui", "gushi"]},
    {"text": "你若失去了财产，你只失去了一点；你若失去了荣誉，你就失去了很多；你若失去了勇气，你就把一切都失去了。", "author": "歌德", "cats": ["yongqi", "rensheng"]},

    # 感恩
    {"text": "谁言寸草心，报得三春晖。", "author": "孟郊", "cats": ["ganen", "jiaoting", "gushi"]},
    {"text": "鸦有反哺之义，羊有跪乳之恩。", "author": "古训", "cats": ["ganen", "jiaoting", "gushi"]},
    {"text": "滴水之恩，当涌泉相报。", "author": "古训", "cats": ["ganen", "gushi"]},
    {"text": "感恩是精神上的一种宝藏。", "author": "洛克", "cats": ["ganen", "jingshen"]},
    {"text": "不管一个人取得多么值得骄傲的成绩，都应该饮水思源。", "author": "居里夫人", "cats": ["ganen", "chenggong"]},
    {"text": "生活需要一颗感恩的心来创造，一颗感恩的心需要生活来滋养。", "author": "王符", "cats": ["ganen", "shenghuo"]},
    {"text": "父母之恩，水不能溺，火不能灭。", "author": "俄国谚语", "cats": ["ganen", "jiaoting"]},
    {"text": "没有感恩就没有真正的美德。", "author": "卢梭", "cats": ["ganen", "daode"]},
    {"text": "人世间最美丽的情景是出现在当我们怀念到母亲的时候。", "author": "莫泊桑", "cats": ["ganen", "jiaoting", "meihao"]},
    {"text": "一粥一饭当思来处不易，半丝半缕恒念物力维艰。", "author": "朱柏庐", "cats": ["ganen", "jieYue", "gushi"]},

    # 快乐
    {"text": "人生得意须尽欢，莫使金樽空对月。", "author": "李白", "cats": ["kuaile", "rensheng", "gushi"]},
    {"text": "快乐不在于事情，而在于我们自己。", "author": "理查德·瓦格纳", "cats": ["kuaile", "xinjing"]},
    {"text": "世界上最快乐的事，莫过于为理想而奋斗。", "author": "苏格拉底", "cats": ["kuaile", "mengxiang", "lizhi"]},
    {"text": "真正的快乐是内在的，它只有在人类的心灵里才能发现。", "author": "布雷默", "cats": ["kuaile", "xinling"]},
    {"text": "所谓内心的快乐，是一个人过着健全的、正常的、和谐的生活所感到的快乐。", "author": "罗曼·罗兰", "cats": ["kuaile", "hexie"]},
    {"text": "笑是一种没有副作用的镇静剂。", "author": "格拉索", "cats": ["kuaile", "jiankang"]},
    {"text": "快乐是一种心境，跟财富、年龄与环境无关。", "author": "佚名", "cats": ["kuaile", "xinjing"]},
    {"text": "把脸迎向阳光，那就不会有阴影。", "author": "海伦·凯勒", "cats": ["kuaile", "yongqi"]},
    {"text": "知足者常乐。", "author": "古训", "cats": ["kuaile", "zhizu", "gushi"]},
    {"text": "生活中不是缺少美，而是缺少发现美的眼睛。", "author": "罗丹", "cats": ["kuaile", "meili", "mingren"]},

    # 痛苦
    {"text": "不经一番寒彻骨，怎得梅花扑鼻香。", "author": "黄蘖禅师", "cats": ["tongku", "jianchi", "gushi"]},
    {"text": "故天将降大任于是人也，必先苦其心志，劳其筋骨，饿其体肤。", "author": "孟子", "cats": ["tongku", "lizhi", "gushi"]},
    {"text": "人有悲欢离合，月有阴晴圆缺，此事古难全。", "author": "苏轼", "cats": ["tongku", "rensheng", "gushi"]},
    {"text": "痛苦是人类伟大的教师。", "author": "拜伦", "cats": ["tongku", "chengzhang"]},
    {"text": "困难是一个严厉的导师。", "author": "贝克", "cats": ["tongku", "chengzhang"]},
    {"text": "苦难是人生的老师。", "author": "巴尔扎克", "cats": ["tongku", "rensheng", "mingren"]},
    {"text": "最精美的宝石，受匠人琢磨的时间最长。", "author": "佚名", "cats": ["tongku", "chengzhang"]},
    {"text": "痛苦能够毁灭人，受苦的人也能把痛苦毁灭。", "author": "佚名", "cats": ["tongku", "jianqiang"]},
    {"text": "人生最痛苦的是梦醒了无路可走。", "author": "鲁迅", "cats": ["tongku", "rensheng", "mingren"]},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "古训", "cats": ["tongku", "jianchi", "lizhi"]},

    # 孤独
    {"text": "古来圣贤皆寂寞，惟有饮者留其名。", "author": "李白", "cats": ["jimo", "gushi", "mingren"]},
    {"text": "孤独是一个人的狂欢，狂欢是一群人的孤独。", "author": "泰戈尔", "cats": ["jimo", "kuaile"]},
    {"text": "孤独，是忧愁的伴侣，也是精神活动的密友。", "author": "纪伯伦", "cats": ["jimo", "jingshen"]},
    {"text": "越是伟大的人，越能耐得住孤独。", "author": "佚名", "cats": ["jimo", "chengzhang"]},
    {"text": "孤独不是一种脾性，而是一种无奈。", "author": "余秋雨", "cats": ["jimo", "rensheng"]},
    {"text": "只有当一个人独处的时候，他才可以完全成为自己。", "author": "叔本华", "cats": ["jimo", "ziji"]},
    {"text": "孤独和寂寞不一样，寂寞会发慌，孤独则是饱满的。", "author": "陈果", "cats": ["jimo", "chengshu"]},
    {"text": "人生，总有一些路要一个人走。", "author": "佚名", "cats": ["jimo", "rensheng"]},
    {"text": "孤独是美丽的，置身于孤单之中，你会把全身心放松，感到从来没有过的轻松。", "author": "佚名", "cats": ["jimo", "kuaile"]},
    {"text": "非淡泊无以明志，非宁静无以致远。", "author": "诸葛亮", "cats": ["jimo", "mengxiang", "gushi"]},

    # 思念
    {"text": "但愿人长久，千里共婵娟。", "author": "苏轼", "cats": ["siyuan", "gushi", "yueLiang"]},
    {"text": "举头望明月，低头思故乡。", "author": "李白", "cats": ["siyuan", "xiangchou", "gushi"]},
    {"text": "独在异乡为异客，每逢佳节倍思亲。", "author": "王维", "cats": ["siyuan", "xiangchou", "gushi"]},
    {"text": "两情若是久长时，又岂在朝朝暮暮。", "author": "秦观", "cats": ["siyuan", "aiqing", "gushi"]},
    {"text": "衣带渐宽终不悔，为伊消得人憔悴。", "author": "柳永", "cats": ["siyuan", "aiqing", "gushi"]},
    {"text": "一日不见，如三秋兮。", "author": "诗经", "cats": ["siyuan", "aiqing", "gushi"]},
    {"text": "红豆生南国，春来发几枝。愿君多采撷，此物最相思。", "author": "王维", "cats": ["siyuan", "aiqing", "gushi"]},
    {"text": "海上生明月，天涯共此时。", "author": "张九龄", "cats": ["siyuan", "gushi", "youqing"]},
    {"text": "露从今夜白，月是故乡明。", "author": "杜甫", "cats": ["siyuan", "xiangchou", "gushi"]},
    {"text": "此夜曲中闻折柳，何人不起故园情。", "author": "李白", "cats": ["siyuan", "xiangchou", "gushi"]},

    # 离别
    {"text": "莫愁前路无知己，天下谁人不识君。", "author": "高适", "cats": ["liuxue", "youqing", "gushi"]},
    {"text": "海内存知己，天涯若比邻。", "author": "王勃", "cats": ["liuxue", "youqing", "gushi"]},
    {"text": "劝君更尽一杯酒，西出阳关无故人。", "author": "王维", "cats": ["liuxue", "youqing", "gushi"]},
    {"text": "桃花潭水深千尺，不及汪伦送我情。", "author": "李白", "cats": ["liuxue", "youqing", "gushi"]},
    {"text": "相见时难别亦难，东风无力百花残。", "author": "李商隐", "cats": ["liuxue", "aiqing", "gushi"]},
    {"text": "多情自古伤离别，更那堪，冷落清秋节。", "author": "柳永", "cats": ["liuxue", "tongku", "gushi"]},
    {"text": "人有悲欢离合，月有阴晴圆缺。", "author": "苏轼", "cats": ["liuxue", "rensheng", "gushi"]},
    {"text": "天下没有不散的筵席。", "author": "古训", "cats": ["liuxue", "rensheng"]},
    {"text": "离别是为了更好的相聚。", "author": "佚名", "cats": ["liuxue", "meihao"]},
    {"text": "轻轻的我走了，正如我轻轻的来。", "author": "徐志摩", "cats": ["liuxue", "shiGe"]},

    # 家庭
    {"text": "谁言寸草心，报得三春晖。", "author": "孟郊", "cats": ["jiaoting", "ganen", "gushi"]},
    {"text": "慈母手中线，游子身上衣。", "author": "孟郊", "cats": ["jiaoting", "ganen", "gushi"]},
    {"text": "家是世界上唯一隐藏人类缺点与失败的地方。", "author": "萧伯纳", "cats": ["jiaoting", "wenNuan"]},
    {"text": "家庭是一项社会发明，其任务是将生物人转化为社会人。", "author": "古德", "cats": ["jiaoting", "sheHui"]},
    {"text": "幸福的家庭都是相似的，不幸的家庭各有各的不幸。", "author": "托尔斯泰", "cats": ["jiaoting", "xingfu"]},
    {"text": "父母之所爱亦爱之，父母之所敬亦敬之。", "author": "孔子", "cats": ["jiaoting", "xiaoShun", "gushi"]},
    {"text": "百善孝为先。", "author": "古训", "cats": ["jiaoting", "xiaoShun", "gushi"]},
    {"text": "子欲养而亲不待，树欲静而风不止。", "author": "古训", "cats": ["jiaoting", "ganen", "gushi"]},
    {"text": "家和万事兴。", "author": "古训", "cats": ["jiaoting", "heXie", "gushi"]},
    {"text": "一家人能够相互密切合作，才是世界上唯一的真正幸福。", "author": "居里夫人", "cats": ["jiaoting", "xingfu"]},

    # 幽默
    {"text": "人生苦短，必须性感。", "author": "佚名", "cats": ["youmo", "rensheng"]},
    {"text": "我不是胖，我只是瘦的不明显。", "author": "佚名", "cats": ["youmo", "zixin"]},
    {"text": "世上无难事，只要肯放弃。", "author": "佚名", "cats": ["youmo", "daoli"]},
    {"text": "当你觉得自己又丑又穷的时候，不要绝望，因为至少你的判断是对的。", "author": "佚名", "cats": ["youmo", "rensheng"]},
    {"text": "生活不止眼前的苟且，还有读不懂的诗和到不了的远方。", "author": "佚名", "cats": ["youmo", "xianShi"]},
    {"text": "没有伞的孩子必须努力奔跑，不然会被雨淋。", "author": "佚名", "cats": ["youmo", "lizhi"]},
    {"text": "钱不是万能的，但没有钱是万万不能的。", "author": "佚名", "cats": ["youmo", "xianShi"]},
    {"text": "我的优点是：我很帅；但是我的缺点是：我帅的不明显。", "author": "周立波", "cats": ["youmo", "zixin"]},
    {"text": "人生就像愤怒的小鸟，失败时总有几只猪在笑。", "author": "佚名", "cats": ["youmo", "shibai"]},
    {"text": "如果你觉得自己很牛，那你一定没见过真正的牛人。", "author": "佚名", "cats": ["youmo", "qianxu"]},

    # 智慧
    {"text": "知之为知之，不知为不知，是知也。", "author": "孔子", "cats": ["zhihui", "xuexi", "gushi"]},
    {"text": "学而不思则罔，思而不学则殆。", "author": "孔子", "cats": ["zhihui", "xuexi", "gushi"]},
    {"text": "三人行，必有我师焉。", "author": "孔子", "cats": ["zhihui", "xuexi", "gushi"]},
    {"text": "千里之堤，溃于蚁穴。", "author": "韩非子", "cats": ["zhihui", "xijie", "gushi"]},
    {"text": "祸兮福之所倚，福兮祸之所伏。", "author": "老子", "cats": ["zhihui", "rensheng", "gushi"]},
    {"text": "知人者智，自知者明。", "author": "老子", "cats": ["zhihui", "zixin", "gushi"]},
    {"text": "上善若水，水善利万物而不争。", "author": "老子", "cats": ["zhihui", "pinDe", "gushi"]},
    {"text": "知识就是力量。", "author": "培根", "cats": ["zhihui", "xuexi", "mingren"]},
    {"text": "智慧意味着以最佳的方式追求最高的目标。", "author": "大哈奇森", "cats": ["zhihui", "muBiao"]},
    {"text": "真正的智慧不仅在于能明察眼前，而且还能预见未来。", "author": "泰伦提乌斯", "cats": ["zhihui", "jianJu"]},
    {"text": "人类的智慧就是快乐的源泉。", "author": "薄迦丘", "cats": ["zhihui", "kuaile"]},
    {"text": "智慧，不是死的默念，而是生的沉思。", "author": "斯宾诺莎", "cats": ["zhihui", "siKao"]},

    # 道德
    {"text": "勿以恶小而为之，勿以善小而不为。", "author": "刘备", "cats": ["daode", "xingWei", "gushi"]},
    {"text": "君子坦荡荡，小人长戚戚。", "author": "孔子", "cats": ["daode", "junzi", "gushi"]},
    {"text": "富贵不能淫，贫贱不能移，威武不能屈。", "author": "孟子", "cats": ["daode", "jianChi", "gushi"]},
    {"text": "出淤泥而不染，濯清涟而不妖。", "author": "周敦颐", "cats": ["daode", "gaoShang", "gushi"]},
    {"text": "先天下之忧而忧，后天下之乐而乐。", "author": "范仲淹", "cats": ["daode", "aiGuo", "gushi"]},
    {"text": "人生自古谁无死，留取丹心照汗青。", "author": "文天祥", "cats": ["daode", "aiGuo", "gushi"]},
    {"text": "静以修身，俭以养德。", "author": "诸葛亮", "cats": ["daode", "xiuShen", "gushi"]},
    {"text": "道德是真理之花。", "author": "雨果", "cats": ["daode", "zhenLi"]},
    {"text": "最高的道德就是不断地为人服务，为人类的爱而工作。", "author": "甘地", "cats": ["daode", "fuWu"]},
    {"text": "美德大都包含在良好的习惯之内。", "author": "帕利克", "cats": ["daode", "xiguan"]},

    # 理想
    {"text": "志当存高远。", "author": "诸葛亮", "cats": ["lxiang", "lizhi", "gushi"]},
    {"text": "非淡泊无以明志，非宁静无以致远。", "author": "诸葛亮", "cats": ["lxiang", "gushi", "xinjing"]},
    {"text": "燕雀安知鸿鹄之志哉！", "author": "陈涉", "cats": ["lxiang", "lizhi", "mingren"]},
    {"text": "老骥伏枥，志在千里；烈士暮年，壮心不已。", "author": "曹操", "cats": ["lxiang", "lizhi", "gushi"]},
    {"text": "穷且益坚，不坠青云之志。", "author": "王勃", "cats": ["lxiang", "jianchi", "gushi"]},
    {"text": "不想当将军的士兵不是好士兵。", "author": "拿破仑", "cats": ["lxiang", "lizhi", "mingren"]},
    {"text": "理想是指路明灯。没有理想，就没有坚定的方向。", "author": "托尔斯泰", "cats": ["lxiang", "lizhi"]},
    {"text": "一个人的理想越崇高，生活越纯洁。", "author": "伏尼契", "cats": ["lxiang", "rensheng"]},
    {"text": "生活中没有理想的人，是可怜的。", "author": "屠格涅夫", "cats": ["lxiang", "lianMin"]},
    {"text": "人生最高之理想，在求达于真理。", "author": "李大钊", "cats": ["lxiang", "zhenLi", "mingren"]},
    {"text": "为中华之崛起而读书。", "author": "周恩来", "cats": ["lxiang", "xuexi", "mingren"]},
    {"text": "梦想还是要有的，万一实现了呢？", "author": "马云", "cats": ["lxiang", "mengxiang", "mingren"]},

    # 命运
    {"text": "命运掌握在自己手中。", "author": "佚名", "cats": ["mingyun", "zixin"]},
    {"text": "我命由我不由天。", "author": "佚名", "cats": ["mingyun", "yongqi"]},
    {"text": "所谓活着的人，就是不断挑战的人，不断攀登命运险峰的人。", "author": "雨果", "cats": ["mingyun", "lizhi", "chengzhang"]},
    {"text": "命运压不垮一个人，只会使人坚强起来。", "author": "伯尔", "cats": ["mingyun", "jianqiang"]},
    {"text": "对于凌驾命运之上的人来说，信心就是生命的主宰。", "author": "海伦·凯勒", "cats": ["mingyun", "zixin"]},
    {"text": "当命运递给我一个酸的柠檬时，让我们设法把它制造成甜的柠檬汁。", "author": "雨果", "cats": ["mingyun", "kuaile"]},
    {"text": "一个人的性格决定他的际遇。如果你喜欢保持你的性格，那么，你就无权拒绝你的际遇。", "author": "罗曼·罗兰", "cats": ["mingyun", "xingGe"]},
    {"text": "机会不会上门来找；只有人去找机会。", "author": "狄更斯", "cats": ["mingyun", "nuli"]},
    {"text": "不要等待机会，而要创造机会。", "author": "萧伯纳", "cats": ["mingyun", "chuangZao"]},
    {"text": "命运给予我们的不是失望之酒，而是机会之杯。", "author": "尼克松", "cats": ["mingyun", "jiHui"]},

    # 成功
    {"text": "成功的秘诀，在永不改变既定的目的。", "author": "卢梭", "cats": ["chenggong", "jianchi"]},
    {"text": "失败是成功之母。", "author": "古训", "cats": ["chenggong", "shibai"]},
    {"text": "天才是百分之一的灵感加百分之九十九的汗水。", "author": "爱迪生", "cats": ["chenggong", "gongzuo", "mingren"]},
    {"text": "成功=艰苦的劳动+正确的方法+少说空话。", "author": "爱因斯坦", "cats": ["chenggong", "gongZuo", "mingren"]},
    {"text": "最困难之时，就是离成功不远之日。", "author": "拿破仑", "cats": ["chenggong", "kunNan", "mingren"]},
    {"text": "成功的唯一秘诀——坚持最后一分钟。", "author": "柏拉图", "cats": ["chenggong", "jianchi"]},
    {"text": "如果你希望成功，当以恒心为良友，以经验为参谋，以当心为兄弟，以希望为哨兵。", "author": "爱迪生", "cats": ["chenggong", "hengXin"]},
    {"text": "人生伟业的建立，不在能知，乃在能行。", "author": "赫胥黎", "cats": ["chenggong", "xingDong"]},
    {"text": "成功不是将来才有的，而是从决定去做的那一刻起，持续累积而成。", "author": "佚名", "cats": ["chenggong", "leiJi"]},
    {"text": "胜利者往往是从坚持最后五分钟的时间中得来成功。", "author": "牛顿", "cats": ["chenggong", "jianchi", "mingren"]},

    # 失败
    {"text": "失败是成功之母。", "author": "古训", "cats": ["shibai", "chenggong"]},
    {"text": "不经一翻彻骨寒，怎得梅花扑鼻香。", "author": "黄蘖禅师", "cats": ["shibai", "jianchi", "gushi"]},
    {"text": "不要只因一次失败，就放弃你原来决心想达到的目的。", "author": "莎士比亚", "cats": ["shibai", "mengxiang"]},
    {"text": "人生最大的荣耀不在于从不跌倒，而在于每次跌倒后都爬起来。", "author": "纳尔逊·曼德拉", "cats": ["shibai", "jianchi", "rensheng"]},
    {"text": "失败也是我需要的，它和成功对我一样有价值。", "author": "爱迪生", "cats": ["shibai", "jiazhi", "mingren"]},
    {"text": "苦难是人生的老师。", "author": "巴尔扎克", "cats": ["shibai", "chengzhang", "mingren"]},
    {"text": "最困难之时，就是离成功不远之日。", "author": "拿破仑", "cats": ["shibai", "chenggong", "mingren"]},
    {"text": "所有的胜利，与征服自己的胜利比起来，都是微不足道。", "author": "柏拉图", "cats": ["shibai", "zixin", "chenggong"]},
    {"text": "世界上最讨人厌的一种活的人就是失败者。", "author": "三毛", "cats": ["shibai", "rensheng"]},
    {"text": "人不是为失败而生的，一个人可以被毁灭，但不能被打败。", "author": "海明威", "cats": ["shibai", "jianqiang"]},

    # 习惯
    {"text": "优秀是一种习惯。", "author": "亚里士多德", "cats": ["xiguan", "youXiu", "mingren"]},
    {"text": "习惯形成性格，性格决定命运。", "author": "凯恩斯", "cats": ["xiguan", "xingGe", "mingYun"]},
    {"text": "静以修身，俭以养德。", "author": "诸葛亮", "cats": ["xiguan", "daode", "gushi"]},
    {"text": "美德大都包含在良好的习惯之内。", "author": "帕利克", "cats": ["xiguan", "daode"]},
    {"text": "习惯不加以抑制，不久它就会变成你生活上的必需品了。", "author": "奥古斯丁", "cats": ["xiguan", "yiZhi"]},
    {"text": "起先是我们造成习惯，后来是习惯造成我们。", "author": "王尔德", "cats": ["xiguan", "yingXiang"]},
    {"text": "孩子成功教育从好习惯培养开始。", "author": "巴金", "cats": ["xiguan", "jiaoYu", "mingren"]},
    {"text": "总以某种固定方式行事，人便能养成习惯。", "author": "亚里士多德", "cats": ["xiguan", "xingCheng"]},
    {"text": "习惯就是习惯，谁也不能将其扔出窗外，只能一步一步地引下楼。", "author": "马克·吐温", "cats": ["xiguan", "gaiBian"]},
    {"text": "习惯比天性更顽固。", "author": "昆图斯", "cats": ["xiguan", "wanGu"]},

    # 健康
    {"text": "健康是人生第一财富。", "author": "爱默生", "cats": ["jiankang", "caiFu", "mingren"]},
    {"text": "身体是革命的本钱。", "author": "毛泽东", "cats": ["jiankang", "zhongYao", "mingren"]},
    {"text": "健康不是一切，但没有健康就没有一切。", "author": "佚名", "cats": ["jiankang", "zhongYao"]},
    {"text": "一个人的身体，决不是个人的，要把它看作是社会的宝贵财富。", "author": "高士其", "cats": ["jiankang", "jiazhi"]},
    {"text": "只有身体好才能学习好、工作好，才能均衡地发展。", "author": "宋庆龄", "cats": ["jiankang", "faZhan", "mingren"]},
    {"text": "健康的人未察觉自己的健康，只有病人才懂得健康。", "author": "卡莱尔", "cats": ["jiankang", "zhenXi"]},
    {"text": "早睡早起，使人健康、富有、明智。", "author": "富兰克林", "cats": ["jiankang", "xiGuan"]},
    {"text": "运动是一切生命的源泉。", "author": "达·芬奇", "cats": ["jiankang", "yunDong"]},
    {"text": "健康的心理寓于健康的身体。", "author": "洛克", "cats": ["jiankang", "xinLi"]},
    {"text": "愉快的笑声是精神健康的可靠标记。", "author": "契诃夫", "cats": ["jiankang", "kuaile"]},

    # 美丽
    {"text": "生活中不是缺少美，而是缺少发现美的眼睛。", "author": "罗丹", "cats": ["meili", "kuaile", "mingren"]},
    {"text": "美是到处都有的。对于我们的眼睛，不是缺少美，而是缺少发现。", "author": "罗丹", "cats": ["meili", "faXian", "mingren"]},
    {"text": "美，是道德上的善的象征。", "author": "康德", "cats": ["meili", "daode"]},
    {"text": "美有两个来源——道德和形式。", "author": "佚名", "cats": ["meili", "neiHan"]},
    {"text": "人并不是因为美丽才可爱，而是因为可爱才美丽。", "author": "托尔斯泰", "cats": ["meili", "keAi"]},
    {"text": "美丽的心灵是永恒的春天。", "author": "威·布莱克", "cats": ["meili", "xinLing"]},
    {"text": "朴素是美的必要条件。", "author": "托尔斯泰", "cats": ["meili", "puSu"]},
    {"text": "美是上帝赐予的礼物。", "author": "亚里士多德", "cats": ["meili", "tianFu"]},
    {"text": "外貌美只能取悦一时，内心美方能经久不衰。", "author": "歌德", "cats": ["meili", "neiXin"]},
    {"text": "我们周围有光也有颜色，但是我们自己的眼里如果没有光和颜色，也就看不到外面的光和颜色了。", "author": "歌德", "cats": ["meili", "xinLing"]},

    # 名人
    {"text": "为中华之崛起而读书。", "author": "周恩来", "cats": ["mingren", "lxiang", "xuexi"]},
    {"text": "俱往矣，数风流人物，还看今朝。", "author": "毛泽东", "cats": ["mingren", "haoQing", "gushi"]},
    {"text": "世上无难事，只要肯登攀。", "author": "毛泽东", "cats": ["mingren", "jianchi", "lizhi"]},
    {"text": "我是中国人民的儿子。我深情地爱着我的祖国和人民。", "author": "邓小平", "cats": ["mingren", "aiGuo"]},
    {"text": "横眉冷对千夫指，俯首甘为孺子牛。", "author": "鲁迅", "cats": ["mingren", "pinGe", "gushi"]},
    {"text": "其实地上本没有路，走的人多了，也便成了路。", "author": "鲁迅", "cats": ["mingren", "chuangZao", "rensheng"]},
    {"text": "时间就像海绵里的水，只要愿挤，总还是有的。", "author": "鲁迅", "cats": ["mingren", "shijian"]},
    {"text": "今天很残酷，明天更残酷，后天很美好。", "author": "马云", "cats": ["mingren", "jianchi", "lizhi"]},
    {"text": "梦想还是要有的，万一实现了呢？", "author": "马云", "cats": ["mingren", "mengxiang"]},
    {"text": "最大的挑战和突破在于用人，而用人最大的突破在于信任人。", "author": "马云", "cats": ["mingren", "guanLi"]},

    # 古诗
    {"text": "山重水复疑无路，柳暗花明又一村。", "author": "陆游", "cats": ["gushi", "mingyun", "xiwang"]},
    {"text": "欲穷千里目，更上一层楼。", "author": "王之涣", "cats": ["gushi", "lizhi", "jinBu"]},
    {"text": "会当凌绝顶，一览众山小。", "author": "杜甫", "cats": ["gushi", "lizhi", "gaodu"]},
    {"text": "大漠孤烟直，长河落日圆。", "author": "王维", "cats": ["gushi", "zhuangGuan"]},
    {"text": "落霞与孤鹜齐飞，秋水共长天一色。", "author": "王勃", "cats": ["gushi", "meiLi"]},
    {"text": "采菊东篱下，悠然见南山。", "author": "陶渊明", "cats": ["gushi", "xianYi", "kuaile"]},
    {"text": "明月几时有，把酒问青天。", "author": "苏轼", "cats": ["gushi", "xiangSi"]},
    {"text": "春眠不觉晓，处处闻啼鸟。", "author": "孟浩然", "cats": ["gushi", "chunTian"]},
    {"text": "床前明月光，疑是地上霜。", "author": "李白", "cats": ["gushi", "xiangChou"]},
    {"text": "白日依山尽，黄河入海流。", "author": "王之涣", "cats": ["gushi", "zhuangGuan"]},
    {"text": "接天莲叶无穷碧，映日荷花别样红。", "author": "杨万里", "cats": ["gushi", "meiLi", "xiaTian"]},
    {"text": "停车坐爱枫林晚，霜叶红于二月花。", "author": "杜牧", "cats": ["gushi", "meiLi", "qiuTian"]},
    {"text": "忽如一夜春风来，千树万树梨花开。", "author": "岑参", "cats": ["gushi", "meiLi", "dongTian"]},
    {"text": "不识庐山真面目，只缘身在此山中。", "author": "苏轼", "cats": ["gushi", "zhihui", "shiJiao"]},
    {"text": "问渠那得清如许，为有源头活水来。", "author": "朱熹", "cats": ["gushi", "xuexi", "zhihui"]},

    # 语录
    {"text": "世界上只有一种真正的英雄主义，那就是在认清生活的真相后依然热爱生活。", "author": "罗曼·罗兰", "cats": ["yulu", "yongqi", "kuaile"]},
    {"text": "我们都在阴沟里，但仍有人仰望星空。", "author": "王尔德", "cats": ["yulu", "mengXiang", "xiWang"]},
    {"text": "人生就像骑自行车，想保持平衡就得往前走。", "author": "爱因斯坦", "cats": ["yulu", "rensheng", "chengzhang"]},
    {"text": "生活不是等待风暴过去，而是学会在雨中跳舞。", "author": "维维安·格林", "cats": ["yulu", "yongqi", "kuaile"]},
    {"text": "你今天的苦果，是昨天的伏笔；当下的付出，是明日的花开。", "author": "佚名", "cats": ["yulu", "chengzhang", "fuChu"]},
    {"text": "你若盛开，蝴蝶自来；你若精彩，天自安排。", "author": "佚名", "cats": ["yulu", "nuli", "meihao"]},
    {"text": "真正的成长，是学会与不完美的自己和解。", "author": "佚名", "cats": ["yulu", "chengzhang", "zixin"]},
    {"text": "人生没有白走的路，每一步都算数。", "author": "佚名", "cats": ["yulu", "rensheng", "jingYan"]},
    {"text": "愿你出走半生，归来仍是少年。", "author": "佚名", "cats": ["yulu", "meihao", "benXin"]},
    {"text": "生活不止眼前的苟且，还有诗和远方的田野。", "author": "高晓松", "cats": ["yulu", "mengxiang", "meihao"]},
    {"text": "我不去想是否能够成功，既然选择了远方，便只顾风雨兼程。", "author": "汪国真", "cats": ["yulu", "jianchi", "mengxiang"]},
    {"text": "既然选择了地平线，留给世界的只能是背影。", "author": "汪国真", "cats": ["yulu", "yongQi", "mengxiang"]},
]

# 构建 slug
def slugify(text):
    """生成URL友好的slug"""
    # 用hash生成简短唯一ID
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:8]

# 名言加ID
for i, q in enumerate(QUOTES):
    q["id"] = slugify(q["text"])
    q["index"] = i


def get_quotes_by_category(cat_slug):
    """获取分类下的名言"""
    return [q for q in QUOTES if cat_slug in q["cats"]]

def get_related_quotes(quote, limit=5):
    """获取相关名言（同分类）"""
    cat = quote["cats"][0]
    same_cat = [q for q in QUOTES if cat in q["cats"] and q["id"] != quote["id"]]
    return same_cat[:limit]

def quote_card_html(quote, base_path="../"):
    """名言卡片HTML"""
    tags_html = ""
    for cat_slug in quote["cats"][:3]:
        cat = CAT_MAP.get(cat_slug)
        if cat:
            tags_html += f'<a href="{base_path}category/{cat_slug}.html" class="quote-tag">{cat["name"]}</a>'
    return f'''
    <a href="{base_path}quote/{quote["id"]}.html" class="quote-card">
      <div class="quote-text">{quote["text"]}</div>
      <div class="quote-author">—— {quote["author"]}</div>
      <div class="quote-tags">{tags_html}</div>
    </a>'''

def header_html(active="home", base_path="./"):
    """头部HTML"""
    nav_items = []
    for cat in CATEGORIES[:8]:  # 只显示8个主要分类
        nav_items.append(f'<a href="{base_path}category/{cat["slug"]}.html">{cat["name"]}</a>')
    nav_html = "".join(nav_items)
    return f'''
    <header class="site-header">
      <div class="header-inner">
        <a href="{base_path}index.html" class="logo">
          <span class="logo-icon">名</span>
          <span>{SITE_NAME}</span>
        </a>
        <nav class="header-nav">
          {nav_html}
        </nav>
        <div class="search-box">
          <input type="text" id="search-input" placeholder="搜索名言...">
        </div>
      </div>
    </header>'''

def footer_html(base_path="./"):
    """底部HTML"""
    # 热门分类
    hot_cats = ""
    for cat in CATEGORIES[:8]:
        hot_cats += f'<a href="{base_path}category/{cat["slug"]}.html">{cat["name"]}名言</a>'

    # 更多分类
    more_cats = ""
    for cat in CATEGORIES[8:16]:
        more_cats += f'<a href="{base_path}category/{cat["slug"]}.html">{cat["name"]}名言</a>'

    return f'''
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-col footer-brand">
          <div class="logo">
            <span class="logo-icon">名</span>
            <span>{SITE_NAME}</span>
          </div>
          <p>{SITE_DESC}</p>
        </div>
        <div class="footer-col">
          <h4>热门分类</h4>
          {hot_cats}
        </div>
        <div class="footer-col">
          <h4>更多分类</h4>
          {more_cats}
        </div>
        <div class="footer-col">
          <h4>关于</h4>
          <a href="{base_path}about.html">关于我们</a>
          <a href="{base_path}privacy-policy.html">隐私政策</a>
          <a href="{base_path}contact.html">联系我们</a>
        </div>
      </div>
      <div class="footer-bottom">
        © 2026 {SITE_NAME}. 名言佳句，点亮生活。
      </div>
    </footer>'''

def page_head(title, description, base_path="./"):
    """页面头部"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="名言,经典语录,励志句子,人生哲理">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="{base_path}static/style.css">
</head>
<body>'''

def page_tail(base_path="./"):
    """页面尾部"""
    return f'''
  <script src="{base_path}static/app.js"></script>
</body>
</html>'''

def generate_home():
    """生成首页"""
    title = f"{SITE_NAME} - 名人名言大全 经典语录 励志句子"
    desc = SITE_DESC

    # 分类卡片
    cat_cards = ""
    for cat in CATEGORIES:
        count = len(get_quotes_by_category(cat["slug"]))
        cat_cards += f'''
      <a href="category/{cat["slug"]}.html" class="category-card">
        <div class="category-icon">{cat["icon"]}</div>
        <div class="category-name">{cat["name"]}名言</div>
        <div class="category-count">{count} 条</div>
      </a>'''

    # 精选名言（前12条）
    featured_quotes = ""
    for q in QUOTES[:12]:
        featured_quotes += quote_card_html(q, "./")

    html = f'''{page_head(title, desc, "./")}
  {header_html("home", "./")}

  <section class="hero">
    <h1>精选名言 · 点亮生活</h1>
    <p>{len(QUOTES)} 条经典名言 · {len(CATEGORIES)} 个分类 · 每日更新</p>
    <div class="hero-stats">
      <div><strong>{len(QUOTES)}+</strong>名言佳句</div>
      <div><strong>{len(CATEGORIES)}</strong>分类主题</div>
      <div><strong>100+</strong>古今名人</div>
    </div>
  </section>

  <div class="container">
    <div class="ad-slot">广告位 728x90</div>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">📂 名言分类</h2>
        <a href="#" class="section-more">全部分类 →</a>
      </div>
      <div class="category-grid">
        {cat_cards}
      </div>
    </section>

    <div class="ad-slot">广告位 728x90</div>

    <section class="section">
      <div class="section-header">
        <h2 class="section-title">✨ 精选名言</h2>
        <a href="#" class="section-more">查看更多 →</a>
      </div>
      <div class="quote-grid">
        {featured_quotes}
      </div>
    </section>

    <div class="ad-slot">广告位 728x90</div>
  </div>

  {footer_html("./")}
  {page_tail("./")}'''

    with open(os.path.join(DOCS_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ 首页: index.html")

def generate_categories():
    """生成所有分类页"""
    for cat in CATEGORIES:
        quotes = get_quotes_by_category(cat["slug"])
        if not quotes:
            continue

        title = f"{cat['name']}名言大全 - {len(quotes)}条经典{cat['name']}的句子 | {SITE_NAME}"
        desc = cat["desc"] + f"精选{len(quotes)}条{cat['name']}名言名句，来自古今中外名人大家。"

        quotes_html = ""
        for q in quotes:
            quotes_html += quote_card_html(q, "../")

        # 相关分类
        related_cats = [c for c in CATEGORIES if c["slug"] != cat["slug"]][:6]
        related_cats_html = ""
        for c in related_cats:
            related_cats_html += f'''
          <a href="{c["slug"]}.html" class="category-card">
            <div class="category-icon">{c["icon"]}</div>
            <div class="category-name">{c["name"]}名言</div>
          </a>'''

        # FAQ
        faq_html = f'''
      <div class="faq-item">
        <div class="faq-question">什么是{cat["name"]}名言？</div>
        <div class="faq-answer">{cat["name"]}名言是关于{cat["name"]}主题的经典语句，通常出自名人之口或古籍经典，蕴含深刻的人生智慧和哲理。</div>
      </div>
      <div class="faq-item">
        <div class="faq-question">为什么要读{cat["name"]}名言？</div>
        <div class="faq-answer">{cat["name"]}名言能给我们启发和力量，在人生的不同阶段给予我们指引和慰藉。一句好的{cat["name"]}名言，往往能让人茅塞顿开。</div>
      </div>
      <div class="faq-item">
        <div class="faq-question">{cat["name"]}名言可以用在哪些地方？</div>
        <div class="faq-answer">{cat["name"]}名言可以用于作文素材、朋友圈文案、演讲稿、座右铭、生日祝福、节日贺卡等各种场合。</div>
      </div>'''

        # 结构化数据
        breadcrumb_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": SITE_URL},
                {"@type": "ListItem", "position": 2, "name": f"{cat['name']}名言", "item": f"{SITE_URL}/category/{cat['slug']}.html"}
            ]
        }, ensure_ascii=False)

        html = f'''{page_head(title, desc, "../")}
  {header_html(cat["slug"], "../")}

  <div class="container">
    <div class="breadcrumb">
      <a href="../index.html">首页</a> / {cat["icon"]} {cat["name"]}名言
    </div>

    <div class="category-header">
      <h1>{cat["icon"]} {cat["name"]}名言大全</h1>
      <p>{cat["desc"]}。共收录 {len(quotes)} 条精选{cat["name"]}名言。</p>
    </div>

    <div class="ad-slot">广告位 728x90</div>

    <div class="quote-grid">
      {quotes_html}
    </div>

    <div class="ad-slot">广告位 728x90</div>

    <section class="related-section">
      <h3>🔗 相关分类</h3>
      <div class="category-grid">
        {related_cats_html}
      </div>
    </section>

    <div class="faq-section">
      <h2>❓ 常见问题</h2>
      {faq_html}
    </div>
  </div>

  <script type="application/ld+json">
    {breadcrumb_json}
  </script>

  {footer_html("../")}
  {page_tail("../")}'''

        filepath = os.path.join(DOCS_DIR, "category", f"{cat['slug']}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ 分类页: {cat['slug']}.html ({len(quotes)}条)")

def generate_quotes():
    """生成所有名言详情页"""
    for q in QUOTES:
        title = f"{q['text'][:30]}... — {q['author']} | {SITE_NAME}"
        if len(q["text"]) <= 30:
            title = f"{q['text']} — {q['author']} | {SITE_NAME}"
        desc = f"「{q['text'][:80]}」—— {q['author']}。出自{q['cats'][0]}相关的名言名句。"

        related = get_related_quotes(q, 6)
        related_html = ""
        for r in related:
            related_html += quote_card_html(r, "../")

        # 分类面包屑
        main_cat = CAT_MAP.get(q["cats"][0], {"name": "名言", "slug": "all"})

        # 标签
        tags_html = ""
        for cat_slug in q["cats"]:
            cat = CAT_MAP.get(cat_slug)
            if cat:
                tags_html += f'<a href="../category/{cat["slug"]}.html" class="quote-tag">{cat["name"]}</a>'

        # 结构化数据
        faq_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "QAPage",
            "mainEntity": {
                "@type": "Question",
                "name": f"{q['author']}说过哪些名言？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{q['author']}说过：「{q['text']}」"
                }
            }
        }, ensure_ascii=False)

        html = f'''{page_head(title, desc, "../")}
  {header_html("quote", "../")}

  <div class="container">
    <div class="breadcrumb">
      <a href="../index.html">首页</a> /
      <a href="../category/{main_cat['slug']}.html">{main_cat['icon']} {main_cat['name']}名言</a> /
      名言详情
    </div>

    <article class="quote-detail">
      <div class="quote-text">{q["text"]}</div>
      <div class="quote-author">—— {q["author"]}</div>
      <div class="quote-tags">{tags_html}</div>
    </article>

    <div class="ad-slot">广告位 728x90</div>

    <section class="related-section">
      <h3>💡 相关名言</h3>
      <div class="quote-grid">
        {related_html}
      </div>
    </section>

    <div class="faq-section">
      <h2>❓ 关于这句名言</h2>
      <div class="faq-item">
        <div class="faq-question">「{q['text'][:20]}...」是谁说的？</div>
        <div class="faq-answer">这句话出自 {q['author']}，是其经典名言之一，被广泛引用和传颂。</div>
      </div>
      <div class="faq-item">
        <div class="faq-question">这句名言是什么意思？</div>
        <div class="faq-answer">「{q['text']}」表达了关于{main_cat['name']}的深刻思考，蕴含着人生智慧和哲理，值得细细品味。不同的人在不同的境遇下，可能会有不同的感悟。</div>
      </div>
      <div class="faq-item">
        <div class="faq-question">这句名言可以用在什么地方？</div>
        <div class="faq-answer">这句名言可以用于作文素材、朋友圈文案、演讲稿、座右铭、签名档等各种场合，也可以在需要{main_cat['name']}力量的时候拿来激励自己。</div>
      </div>
    </div>
  </div>

  <script type="application/ld+json">
    {faq_json}
  </script>

  {footer_html("../")}
  {page_tail("../")}'''

        filepath = os.path.join(DOCS_DIR, "quote", f"{q['id']}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    print(f"✓ 名言详情页: {len(QUOTES)} 个")

def generate_policy_pages():
    """生成政策页面"""
    # 关于我们
    about_html = f'''{page_head(f"关于我们 - {SITE_NAME}", f"{SITE_NAME}是一个收录精选名言的网站，致力于传播智慧与正能量")}
  {header_html("about", "./")}
  <div class="container">
    <div class="content-page">
      <h1>关于 {SITE_NAME}</h1>
      <p>欢迎来到{SITE_NAME}！我们是一个致力于收集、整理和分享古今中外名言佳句的网站。</p>

      <h2>我们的使命</h2>
      <p>名言是人类智慧的结晶，是历史长河中最璀璨的明珠。一句好的名言，可以在迷茫时指引方向，可以在失意时给予力量，可以在孤独时带来慰藉。</p>
      <p>我们希望通过精心整理的名言库，让更多人接触到这些珍贵的精神财富，在文字中找到共鸣，在智慧中获得成长。</p>

      <h2>我们的内容</h2>
      <ul>
        <li>📚 精选 {len(QUOTES)}+ 条经典名言</li>
        <li>📂 {len(CATEGORIES)} 个分类，覆盖生活方方面面</li>
        <li>👤 100+ 位古今中外名人大家</li>
        <li>🔍 精准搜索，快速找到你需要的句子</li>
        <li>📱 响应式设计，手机电脑都好用</li>
      </ul>

      <h2>联系我们</h2>
      <p>如果你有任何建议、想投稿名言、或者发现错误，欢迎通过<a href="contact.html">联系页面</a>与我们取得联系。</p>

      <p>感谢你访问{SITE_NAME}，愿名言伴你成长，点亮你的每一天！</p>
    </div>
  </div>
  {footer_html("./")}
  {page_tail("./")}'''

    with open(os.path.join(DOCS_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(about_html)
    print("✓ 关于页面: about.html")

    # 隐私政策
    privacy_html = f'''{page_head(f"隐私政策 - {SITE_NAME}", f"{SITE_NAME}隐私政策声明")}
  {header_html("privacy", "./")}
  <div class="container">
    <div class="content-page">
      <h1>隐私政策</h1>
      <p>最后更新日期：2026年9月22日</p>

      <p>欢迎访问{SITE_NAME}（以下简称"本网站"）。我们非常重视您的隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的个人信息。</p>

      <h2>一、信息收集</h2>
      <h3>1. 自动收集的信息</h3>
      <p>当您访问本网站时，我们的服务器可能会自动记录某些信息，包括但不限于：</p>
      <ul>
        <li>您的 IP 地址</li>
        <li>浏览器类型和版本</li>
        <li>访问时间和页面</li>
        <li>推荐来源网址</li>
      </ul>
      <p>这些信息仅用于网站运营和改善用户体验，不会与任何个人身份信息关联。</p>

      <h3>2. Cookie 和第三方服务</h3>
      <p>本网站使用第三方广告服务（如 Google AdSense）来展示广告。这些第三方服务商可能使用 Cookie 来收集您的浏览信息，以便提供个性化广告。</p>
      <p>Google 作为第三方供应商，使用 Cookie 在本网站投放广告。Google 使用 DART Cookie 使其能够向用户投放基于其访问本网站和互联网上其他网站的广告。</p>
      <p>您可以通过访问 <a href="https://www.google.com/settings/ads">Google 广告设置页面</a> 选择退出 DART Cookie 的使用。</p>

      <h2>二、信息使用</h2>
      <p>我们收集的信息用于以下目的：</p>
      <ul>
        <li>改善网站内容和用户体验</li>
        <li>分析网站流量和使用模式</li>
        <li>展示个性化广告</li>
        <li>维护网站安全</li>
      </ul>

      <h2>三、信息共享</h2>
      <p>我们不会出售、交易或以其他方式向第三方转让您的个人身份信息。但以下情况除外：</p>
      <ul>
        <li>法律要求或政府指令</li>
        <li>保护我们的权利和财产</li>
        <li>经您同意的其他情况</li>
      </ul>

      <h2>四、第三方链接</h2>
      <p>本网站可能包含指向第三方网站的链接。我们对这些网站的隐私政策或内容不承担责任。我们建议您在访问这些网站时查阅其各自的隐私政策。</p>

      <h2>五、您的权利</h2>
      <p>您有权：</p>
      <ul>
        <li>访问我们持有的关于您的个人信息</li>
        <li>要求更正不准确的信息</li>
        <li>选择退出个性化广告</li>
        <li>禁用 Cookie（通过浏览器设置）</li>
      </ul>

      <h2>六、儿童隐私</h2>
      <p>本网站面向一般受众，不专门针对 13 岁以下儿童。我们不会故意收集 13 岁以下儿童的个人信息。</p>

      <h2>七、政策更新</h2>
      <p>我们可能会不时更新本隐私政策。任何更改都将在本页面上发布，重大变更会在网站首页通知。</p>

      <h2>八、联系我们</h2>
      <p>如果您对本隐私政策有任何疑问，请通过<a href="contact.html">联系页面</a>与我们联系。</p>
    </div>
  </div>
  {footer_html("./")}
  {page_tail("./")}'''

    with open(os.path.join(DOCS_DIR, "privacy-policy.html"), "w", encoding="utf-8") as f:
        f.write(privacy_html)
    print("✓ 隐私政策: privacy-policy.html")

    # 联系页面
    contact_html = f'''{page_head(f"联系我们 - {SITE_NAME}", f"联系{SITE_NAME}，提出您的建议和反馈")}
  {header_html("contact", "./")}
  <div class="container">
    <div class="content-page">
      <h1>联系我们</h1>
      <p>感谢您访问{SITE_NAME}！如果您有任何问题、建议或反馈，欢迎通过以下方式与我们联系。</p>

      <h2>联系方式</h2>
      <ul>
        <li>📧 邮箱：contact#mingyan.example.com（将#替换为@）</li>
        <li>⏰ 响应时间：工作日 24-48 小时内</li>
      </ul>

      <h2>常见问题</h2>
      <div class="faq-item" style="margin-bottom: 16px; background: #f9fafb; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
        <div class="faq-question">Q: 我想投稿名言可以吗？</div>
        <div class="faq-answer">A: 当然可以！欢迎将您喜欢的名言通过邮件发送给我们，请注明出处和作者。</div>
      </div>
      <div class="faq-item" style="margin-bottom: 16px; background: #f9fafb; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
        <div class="faq-question">Q: 发现错误的名言怎么办？</div>
        <div class="faq-answer">A: 如果您发现某句名言的作者或出处有误，请及时告诉我们，我们会尽快核实并修正。</div>
      </div>
      <div class="faq-item" style="margin-bottom: 16px; background: #f9fafb; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
        <div class="faq-question">Q: 可以合作吗？</div>
        <div class="faq-answer">A: 欢迎各类合作洽谈，请在邮件中注明"合作"字样，我们会尽快回复。</div>
      </div>
      <div class="faq-item" style="margin-bottom: 16px; background: #f9fafb; border: 1px solid var(--border); border-radius: 8px; padding: 16px;">
        <div class="faq-question">Q: 名言有版权问题吗？</div>
        <div class="faq-answer">A: 本网站的名言均来自公开的古籍和公开报道，用于学习和分享目的。如果您认为有侵犯版权的内容，请联系我们，我们会及时处理。</div>
      </div>

      <h2>留言反馈</h2>
      <form class="contact-form" onsubmit="event.preventDefault(); alert('感谢您的反馈！');">
        <input type="text" placeholder="您的称呼" required>
        <input type="email" placeholder="您的邮箱" required>
        <textarea rows="5" placeholder="请输入您想说的话..." required></textarea>
        <button type="submit">发送消息</button>
      </form>
    </div>
  </div>
  {footer_html("./")}
  {page_tail("./")}'''

    with open(os.path.join(DOCS_DIR, "contact.html"), "w", encoding="utf-8") as f:
        f.write(contact_html)
    print("✓ 联系页面: contact.html")

def generate_sitemap():
    """生成 sitemap.xml"""
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 首页
    urls.append((f"{SITE_URL}/index.html", "1.0", "daily"))

    # 分类页
    for cat in CATEGORIES:
        urls.append((f"{SITE_URL}/category/{cat['slug']}.html", "0.8", "weekly"))

    # 名言详情页
    for q in QUOTES:
        urls.append((f"{SITE_URL}/quote/{q['id']}.html", "0.6", "monthly"))

    # 政策页
    urls.append((f"{SITE_URL}/about.html", "0.3", "yearly"))
    urls.append((f"{SITE_URL}/privacy-policy.html", "0.3", "yearly"))
    urls.append((f"{SITE_URL}/contact.html", "0.3", "yearly"))

    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    for url, priority, freq in urls:
        sitemap += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
    sitemap += '</urlset>'

    with open(os.path.join(DOCS_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"✓ Sitemap: {len(urls)} URLs")

def generate_robots():
    """生成 robots.txt"""
    robots = f'''User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
'''
    with open(os.path.join(DOCS_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("✓ Robots.txt")

def main():
    print(f"{'='*50}")
    print(f"  {SITE_NAME} 生成器")
    print(f"  共 {len(QUOTES)} 条名言，{len(CATEGORIES)} 个分类")
    print(f"{'='*50}\n")

    generate_home()
    print()
    generate_categories()
    print()
    generate_quotes()
    print()
    generate_policy_pages()
    print()
    generate_sitemap()
    generate_robots()

    total = 1 + len(CATEGORIES) + len(QUOTES) + 3
    print(f"\n{'='*50}")
    print(f"  生成完成！共 {total} 个页面")
    print(f"  输出目录: {DOCS_DIR}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
