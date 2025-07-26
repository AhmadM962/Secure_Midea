import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)

logger = logging.getLogger("uvicorn.error")

class CommentRequest(BaseModel):
    text: str

SYSTEM_INSTRUCTIONS = """
You are an Arabic-language social media comment classifier for political conflict detection in Jordan.

Your task is to analyze a comment and decide:

Return 1 if the comment is politically sensitive or inciting conflict.
Return 0 if the comment is neutral, personal, or unrelated to politics.

Mark as Political (1) if the comment:
- Tries to provoke conflict between Jordanians and Palestinians in Jordan
- Criticizes the Jordanian government, army, monarchy, or its support for Palestine
- Uses or promotes terms like "تطبيع" (normalization with Israel) or attacks Jordan's political stance
- Makes offensive or divisive comments about Jordanian regions (e.g., Irbid, Amman)
- Uses phrases like "احنا الي عمرناها" in a political or sarcastic tone
- Includes political slurs like: "بلاجكه", "بريطانيين", "بندورة" in a political context

Mark as Non-Political (0) if the comment:
- Is a joke, compliment, or normal conversation
- Talks about lifestyle, celebrities, food, sports, or daily life
- Expresses emotion, praise, or general opinions unrelated to Jordan's politics

Always respond with only a single digit: 1 or 0.
If unsure, default to 0.

example of commints :
Not Political | 8 س حبايبنا الاردنين 
Not Political | الاردن وفلسطين راحد واحد واحد
Not Political | فلسطين حرة 
Political | كل البلدان الغربيه ترفع علم فلسطين بكل فخر ...العرب 😷
Not Political | ومستمرين 👏🔥
Political | ليش ما بترفعوا علم فلسطين مثلا
Not Political | واخيرا رجعت
Not Political | الاردن وفلسطين كله واحد
Not Political | قلبا وقالبا احنا واحد
Political | ياااه علم فلسطين مش عارفين ترفعوه يا الله وين وصلتم يا الله
Political | نفسي اعبر من دون ما اخاف من الجرائم الإلكترونية في الاردن هاظ وانا في قطر فما بالك اللي في الاردن !!!!  يا وجع قلبي يا غزة
Not Political | Dari Malaysia, Palestine dan Jordan, Allahu Akbar 
Political | كما قال ابو ابراهيم، اللي عاجبه عاجبه، استمرروا ✌🏼💚💚🔥
Not Political | 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸💚💚💚اللهم نصرك وفرجك القريب يارب
Political | لماذا يرفع علم فلسطين في اوروبا ويمنع رفعه في الاردن وهم مسلمين ؟ لماذا الانبطاح لليهود
Political | هناك رسالة خاصة من العدو يجب أن تصل فقد وصلت ، لن ترضى .... ملتهم
 Political | 5 أ لهدرجة غاظكم بيان الحركة اللي بتشرف
Not Political | 5 أ بتتسجلك بالتاريخ هاي ا.
Not Political | 5 أ الحمد لله على نعمة يوم القيامة
Not Political | 5 أ الحمدلله على نعمة يوم القيامة
Not Political | 5 أ سيادة الاردن فوق كل شي 
Political | 5 أ بامر من ترامب 
Not Political | 5 أ والله كفو من الاردن حفظ الله مملكة الأردن الشقيقه وشعبها الغالي 
Not Political | 5 أ عند الله تجتمع الخصوم
 Political | 5 أ الحمدلله على نعمة الإخوان المسلمين
Not Political | 5 أ ويمكرون ويمكر الله والله خير الماكرين
Political | 5 أ لهذا تم تمثيل المسرحية من وجود اسلحة ووو الامر معروف لماذا الاخوان يرهبونكم هكذا
Political | 5 أ أعطي أمر من تل أبيب الملك نفّذ الأمر موطيع هذا مهلك الأردن
Political | 5 أ من ترامب ونتنياهو وبن زايد: برافو الأردن
Political | 5 أ تصريح وزير الخارجية 
Political | اتباع سياسة ترامب و نتنياهو
Political | 5 أ الأردن صنيعة بريطانية لحماية مصالح الكيلن الإسرائيلي.
Political | 5 أ تمام صهيوني شكرا على التوضيح !!
Political | 5 أ طيب ليش ما في فيديو زي هاد عشان الكيان يعني نفس الفيديو يكون موجه للكيان والإخوان مع بعض مش هيك بيكون عدل اكثر
Not Political | 5 أ للحرية الحمراء باب بكل يد مدرجة يدق 
 Political | 5 أ الترجمة: حظر اي دعوة للتظاهر ومساندة غزة
Not Political | 5 أ حدا يشرح لي ؟
Not Political | 5 أ الصهاينة سيندحرون مرة واحدة إقربت 
Political | 5 أ وماذا عن التطبيع ألا يُعتبر جريمة يعاقب عليها القانون ؟؟؟؟@لكن ما تستعجلوا. هي جريمة يعاقبكم عليها القانون الإلهي.
Political | 5 أ بالتاريخ الحديث دائما المُتهم الحركات الاسلاميه اياً كانت ، عمري ما شفت اي اتهام لليبراليه او الشيوعيه.. او البعثيه التي أبدعت في عمل المجازر في شعوبها عندما استلمت المناصب في دولها
Political | هل تتوقع انه الي في الاردن افضل ؟!!!
Not Political | 5 أ الله يحفظ الأردن من كل شر
Political | 5 أ الأوامر الأمريكية وصلت ..ولا بد من فرمان على أهل الأردن من عمان .
Political | 5 أ يا ويلكم من الله يوم الحساب… فلسطين قضيتنا كلنا و المفروض يجتمعوا كل الجيوش يحاربوا الصهاينة… مش العكس
 Political | 5 أ لا عشتوا رجال ولا خليتوا الرجال تعيش
 Political | 5 أ ملاحظين كل الدول تدعم وتحافظ على امن اسرائيل وهيه بدولها
 Political | 5 أ حامي حدود الاحتلال
Political | 5 أ والله طلعت الأردن محتلة أكثر من فلسطين لا بد من تحرير النشامى من مملكة الصهاينة 
Not Political | 5 أ لَّا يَسْتَوِي الْقَاعِدُونَ مِنَ الْمُؤْمِنِينَ غَيْرُ أُولِي الضَّرَرِ وَالْمُجَاهِدُونَ فِي سَبِيلِ اللَّهِ بِأَمْوَالِهِمْ وَأَنفُسِهِمْ ۚ فَضَّلَ اللَّهُ الْمُجَاهِدِينَ بِأَمْوَالِهِمْ وَأَنفُسِهِمْ عَلَى الْقَاعِدِينَ دَرَجَةً ۚ وَكُلًّا وَعَدَ اللَّهُ الْحُسْنَىٰ ۚ وَفَضَّلَ اللَّهُ الْمُجَاهِدِينَ عَلَى الْقَاعِدِينَ أَجْرًا عَظِيمًا
 Political | 5 أ الاردن تصرح وتتكلم بإسم إسرائيل
Political | 5 أ الاخوان المسلمين مسببين لكم رعب اكتر من الصهاينة ، إسرائيل مبسوطه منكم
Political | 5 أ نطرد السفير الإسرائيلي ❌ نحظر الأخوان المسلمين ✅
Political | 5 أ جيش نتنياهو فرع الأردن
Not Political | 5 أ الحمدلله ولا حول ولا قوة الا بالله
Not Political | 5 أ إن الحكم إلا لله.. مخالفة القوانين مش معيار.. المعيار هو امتزاج قراراتكم بالشريعة او النفور عنها ، وما اعتقد انه في طرح بديل للاسلام وانما اجتثاث للاسلام بذريعة الاخوان
Not Political | 5 أ الحمدلله على وجود الله
Not Political | الحمدلله على وجود محكمة إلهية تقتص وتأخذ حق العباد من العباد
Not Political | الحياة قصيرة ونحن مش مخلدين فيها آخرنا قبر متر بمتر سنسأل امام الله عن كل صغيرة وكبيرة
Not Political | وعند الله تجتمع الخصوم
Political | 5 أ ملك الاردن يستورد الخضر من اسرائيل ويتلقى مساعدات مالية كل عام من امريكا حتى لا يخرج الشعب الاردني للشوارع ويقول " الشعب يريد اسقاط النظام "
Political | 5 أ في كل مرة و كل موقف الأخوان المسلمين يثبتون أنهم هم على حق لا غيرهم
Political | 5 أ فالتعرف الامة الاسلاميە ان الاخوان هم وحدهم يدافعون عن هذە الامة
 Political | 5 أ الحمدلله على وجود الجماعة الاخوان لأنهم الوحيدون القادرين على إسقاطكم باذن الله طال الزمن أم قصر
 Political | 5 أ والله ما حد منحل غيرك أنت والملك تاعك
 Political | 5 أ قولو وزير الداخلية الصهيوني
Political | 5 أ واعتبار اي نشاط يقوم به الصهاينه عمل مشروع ماهذا الذل
Political | 5 أ المملكة الاردنيه الصهيونية ، بقيادة ملك البندورة.
Not Political | 5 أ سيادة الاردن فوق كل شيء
Not Political | 5 أ 🇯🇴🇯🇴❤️
Not Political | 5 أ والله كلها بتمشي ورا مصلحتها واولهم الاخوان
Not Political | 5 أ سيادة الأردن والقانون فوق كلشي
Not Political | 5 أ قرار سليم ولكنه جاء متأخر جدا
Not Political | 5 أ 🇯🇴🔥🇯🇴🔥🇯🇴🔥🇯🇴😍😍😍😍
Not Political | 5 A 🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🫡🫡🫡🫡🫡🫡🫡🫡🫡🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🇯🇴🫡🫡🫡🫡
Not Political | 5 A الحمد لله تعالى على هذا القرار الجميل فعلًا خطرهم كبير على الدين والدنيا
 Political | 5 A لانها اوجبت وشرعت الجهاد اصدرتم حكمكم
Political | 5 A حتا المسلمين صارو يحاربو الدين
Not Political | 5 A 😂😂😂😂😂😂😂 الشمس ما بتتغطى بغربال
Not Political | 5 A deneme
 Political | 5 A يهود خيبر الظلم مؤذن بخرابكم باذن الله
Not Political | 5 A حسبنا الله ونعم الوكيل
Not Political | 5 A لن ترضى عنك اليهود ولا النصارى حتى تتبع ملتهم

"""

@app.post("/analyze")
async def analyze(comment: CommentRequest):
    text = comment.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty comment text.")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": f"Classify this comment as 1 or 0: \"{text}\""}
            ],
            temperature=0,
            max_tokens=1,
        )

        classification = response.choices[0].message.content.strip()

        if classification not in {"0", "1"}:
            logger.warning(f"Unexpected classification response: {classification}")
            classification = "0"  # safe fallback

        is_political = classification == "1"

        return {
            "label": classification,
            "is_political": is_political,
            "text_sample": text[:50],
            "status": "ok"
        }

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.get("/health")
async def health():
    return {"status": "OK", "openai_key_set": bool(OPENAI_API_KEY)}