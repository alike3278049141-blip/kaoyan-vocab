# -*- coding: utf-8 -*-
# ============================================================
#  考研英语词汇复习系统（桌面版 · Day 1 词库已内置）
#  本版改动：新词学习改为每批 20 个（BATCH 可调）；
#  每学完一批，立即自动开始该批「即时复习」：看英文选中文义，
#  答错自动重测并附例句；全部过关后可一键继续下一批。
#  艾宾浩斯复习排程不受影响（明天起 +1/+2/+4/+7/+15/+30）。
#  运行：  python kaoyan_vocab.py        （Python 3.8+，无需第三方库）
#  打包：  pip install pyinstaller
#          pyinstaller -F -w --name KaoYanVocab kaoyan_vocab.py
#  数据：  ~\.kaoyan_vocab\vocab_data.json（自动创建）
# ============================================================
import json, os, re, random, datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

BATCH = 20   # 每批学习词数：学完 BATCH 个立即进入本批即时复习
IV = [0, 1, 2, 4, 7, 15, 30, 90]
APP_DIR = os.path.join(os.path.expanduser("~"), ".kaoyan_vocab")
DATA_FILE = os.path.join(APP_DIR, "vocab_data.json")

RAW = [
    ("groundbreaking","adj.","开创性的，突破性的","Groundbreaking research showed that Shakespeare does benefit children's literacy and emotional development.","文章"),
    ("scholarly","adj.","学术性的；博学的","The grammar school boy from Stratford-upon-Avon has landed a scholarly punch.","文章"),
    ("benefit","v.&n.","使受益；好处","Shakespeare does benefit children's literacy and emotional development.","文章"),
    ("literacy","n.","读写能力","...does benefit children's literacy and emotional development.","文章"),
    ("emotional","adj.","情感的；情绪的","...as well as their emotional literacy.","文章"),
    ("drama","n.","戏剧；戏剧艺术","The target group was given a 30-minute drama-based activity.","文章"),
    ("rehearsal","n.","排练，排演","A rehearsal room approach to teaching Shakespeare was tested.","文章"),
    ("approach","n.","方法，方式；接近","The rehearsal room approach broadened children's vocabulary.","文章"),
    ("broaden","v.","拓宽，扩大","The approach broadened children's vocabulary and the complexity of their writing.","文章"),
    ("complexity","n.","复杂性，复杂度","It broadened the complexity of their writing.","文章"),
    ("commission","v.","委托，授权（做研究）；n.佣金","Jacqui O'Hanlon of the RSC, which commissioned the study, said...","文章"),
    ("randomised","adj.","随机化的","The randomised control trial involved hundreds of pupils.","文章"),
    ("trial","n.","试验；（法律）审判","It was a randomised control trial at 45 state primary schools.","文章"),
    ("pupil","n.","小学生，学生","Hundreds of year 5 pupils aged nine and ten took part.","文章"),
    ("previously","adv.","此前，以前","Schools had not been previously exposed to RSC pedagogy.","文章"),
    ("expose","v.","使接触；使暴露","Schools not previously exposed to RSC pedagogy.","文章"),
    ("pedagogy","n.","教学法，教育理论","Schools had not been exposed to RSC pedagogy.","文章"),
    ("target","n.&v.","目标；瞄准","The target group was given a 30-minute drama-based activity.","文章"),
    ("accompany","v.","伴随；陪伴","A drama-based activity to accompany the passage.","文章"),
    ("sophisticated","adj.","复杂精妙的；（词）高级的","Target pupils used words classed as more sophisticated or rarer.","文章"),
    ("reliance","n.","依赖，依靠","Control pupils' reliance on desert island clichés.","文章"),
    ("cliché","n.","陈词滥调，老生常谈","Control pupils relied on clichés such as palm trees.","文章"),
    ("expansive","adj.","广博的；辽阔的","Target pupils were more expansive, giving a broader picture.","文章"),
    ("atmospheric","adj.","大气的；有氛围的","A broader picture of the sky, the sea and the atmospheric conditions.","文章"),
    ("evident","adj.","明显的，清楚的","The emotional literacy was evident in the children's writing.","文章"),
    ("resilient","adj.","有韧性的；坚强乐观的","The target children were more resilient in their writing, more hopeful.","文章"),
    ("embed","v.","使融入；嵌入","The study showed the importance of embedding arts in education.","文章"),
    ("replicate","v.","复现，重现（结果）","But could the results be replicated with any old dramatist?","文章"),
    ("dramatist","n.","剧作家","Could the results be replicated with any old dramatist?","文章"),
    ("massive","adj.","巨大的，大量的","Shakespeare's 20,000 words gave a massive expansion of language.","文章"),
    ("expansion","n.","扩充，扩大","A massive expansion of language into children's lives.","文章"),
    ("involve","v.","涉及；使参与","The trial involved hundreds of year 5 pupils.","文章"),
    ("react","v.","（作出）反应","Control pupils imagine how they themselves would react to being shipwrecked.","文章"),
    ("combine","v.","使结合，联合","This was combined with children using their whole bodies.","文章"),
    ("process","n.","过程，进程","It is probably related to the rehearsal room process.","文章"),
    ("understanding","n.","理解，领悟","The emotional understanding was very evident.","文章"),
    ("character","n.","角色；性格","Children put themselves in the shoes of a literary character.","文章"),
    ("royal","adj.","皇家的","The Royal Shakespeare Company (RSC) commissioned the study.","文章"),
    ("rewrite","v.","重写，改写","[A] rewrite the lines from Shakespeare","选项"),
    ("line","n.","台词；（诗）行","[A] rewrite the lines from Shakespeare","选项"),
    ("performance","n.","演出，表演","[B] watch RSC actors' performances","选项"),
    ("divide","v.","划分，分开","The study divided the pupils into two groups.","选项"),
    ("instruction","n.","教学，指导","whether the change in instruction enhances learning outcomes","选项"),
    ("enhance","v.","提高，增强","whether the change in instruction enhances learning outcomes","选项"),
    ("outcome","n.","结果，成效","whether the change enhances learning outcomes","选项"),
    ("fluency","n.","流利，流畅","whether expanding vocabulary helps develop reading fluency","选项"),
    ("stimulate","v.","激发，刺激","whether the classroom activity stimulates interest in the arts","选项"),
    ("weakness","n.","弱点，不足","Their reliance on clichés shows their weakness in description.","选项"),
    ("description","n.","描写，描述","Their reliance on clichés shows their weakness in description.","选项"),
    ("omission","n.","遗漏，省略","[B] omission of small details","选项"),
    ("casual","adj.","随意的，漫不经心的","[C] casual style of writing","选项"),
    ("preference","n.","偏爱，偏好","[D] preference for big words","选项"),
    ("promote","v.","促进，提升","What can promote children's emotional literacy according to O'Hanlon?","选项"),
    ("inspiration","n.","灵感","[C] Drawing inspiration from nature","选项"),
    ("imaginative","adj.","富于想象力的","[A] Writing in an imaginative manner","选项"),
    ("manner","n.","方式；态度","Writing in an imaginative manner","选项"),
    ("formidable","adj.","难以应对的，令人生畏的","The language of Shakespeare may be formidable for pupils.","选项"),
    ("reluctant","adj.","不情愿的","Pupils may be reluctant to work on other old dramatists.","选项"),
    ("infer","v.","推断，推论","It can be inferred from the last paragraph that...","选项"),
    ("act out","phr.","把……表演出来","Shakespeare benefits children only if you act him out.","短语"),
    ("split into","phr.","分成，划分为","They were split into target and control groups.","短语"),
    ("control group","phr.","对照组","They were split into target and control groups.","短语"),
    ("draw on","phr.","动用，汲取，利用","The target group drew on a wider vocabulary.","短语"),
    ("put oneself in the shoes of","phr.","设身处地，换位体会","Children put themselves in the shoes of a literary character.","短语"),
    ("rely on","phr.","依赖，依靠","Control pupils relied on desert island clichés.","短语"),
    ("identify with","phr.","认同；与……产生共鸣","[B] Identifying with literary characters.","短语"),
    ("draw inspiration from","phr.","从……中获得灵感","[C] Drawing inspiration from nature.","短语"),
    ("concentrate on","phr.","专注于，集中精力于","[D] Concentrating on real-life situations.","短语"),
    ("be reluctant to","phr.","不情愿做……","Pupils may be reluctant to work on other old dramatists.","短语"),
    ("bring ... to life","phr.","使……生动鲜活","Children used their whole bodies to bring words to life.","短语"),
]
SEED = {"date": "2026-09-26", "title": "Day 1 · 莎士比亚“排练室”教学研究（RSC）",
        "words": [{"w": a[0], "pos": a[1], "cn": a[2], "ex": a[3], "tag": a[4]} for a in RAW]}

def today(): return dt.date.today().isoformat()
def add_days(s, n): return (dt.date.fromisoformat(s) + dt.timedelta(days=n)).isoformat()

DB = {"days": {}, "progress": {}}

def load_db():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        DB["days"] = data.get("days", {})
        DB["progress"] = data.get("progress", {})
    except Exception:
        pass
    DB["days"].setdefault(SEED["date"], SEED)

def save_db():
    os.makedirs(APP_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(DB, f, ensure_ascii=False)

def st(key):
    return DB["progress"].setdefault(key, {"box": 0, "due": None, "seen": 0, "wrong": 0})

def all_words():
    out = []
    for day, data in DB["days"].items():
        for w in data["words"]:
            out.append({"day": day, "w": w, "key": day + "::" + w["w"]})
    return out

def due_words():
    t = today(); out = []
    for it in all_words():
        s = st(it["key"])
        if s["box"] > 0 and s["due"] and s["due"] <= t:
            out.append(it)
    return out

def learn_done(key):
    s = st(key)
    if s["box"] == 0:
        s["box"] = 1; s["due"] = add_days(today(), 1)
    s["seen"] += 1; save_db()

def learn_fail(key):
    s = st(key); s["seen"] += 1; save_db()

def apply_result(key, correct):
    s = st(key); t = today()
    if s["box"] == 0: return
    if s["due"] and s["due"] <= t:
        if correct:
            s["box"] = min(s["box"] + 1, len(IV) - 1); s["due"] = add_days(t, IV[s["box"]])
        else:
            s["box"] = 1; s["due"] = add_days(t, 1); s["wrong"] += 1
        save_db()

def status_of(s):
    if s["box"] == 0: return "未学"
    if s["box"] >= 7: return "已掌握"
    if s["box"] >= 5: return "强化中"
    if s["box"] >= 3: return "巩固中"
    return "初记"

def get_options(item):
    pool = [x for x in all_words()
            if x["key"] != item["key"] and x["w"]["w"] != item["w"]["w"] and x["w"]["cn"] != item["w"]["cn"]]
    same = [x for x in pool if x["w"]["tag"] == item["w"]["tag"]]
    rest = [x for x in pool if x["w"]["tag"] != item["w"]["tag"]]
    random.shuffle(same); random.shuffle(rest)
    opts = [item] + same[:3]
    for c in rest:
        if len(opts) >= 4: break
        if c not in opts: opts.append(c)
    random.shuffle(opts)
    return opts

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("考研英语词汇复习系统 · Day 1")
        self.geometry("880x660"); self.minsize(760, 560)
        style = ttk.Style(self)
        try: style.theme_use("clam")
        except Exception: pass

        self.nb = ttk.Notebook(self); self.nb.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabs = {}
        for name in ["今日计划", "新词学习", "识别测验", "例句填空", "词库本", "复习日程", "数据·导入"]:
            frm = ttk.Frame(self.nb); self.nb.add(frm, text=name); self.tabs[name] = frm
        self.nb.bind("<<NotebookTabChanged>>", lambda e: self.on_tab())

        self.learn_q, self.learn_i, self.learn_again, self.learn_total = [], 0, 0, 0
        self.learn_rest = []
        self.quiz_q, self.quiz_i, self.quiz_ok, self.quiz_total = [], 0, 0, 0
        self.quiz_bad, self.quiz_re = [], set()
        self.quiz_first_ok, self.quiz_seen, self.quiz_retry = 0, set(), {}
        self.quiz_mode = None          # None / "due"（到期复习）/ "new"（学后即时复习）
        self.cl_q, self.cl_i, self.cl_ok, self.cl_practice = [], 0, 0, False
        self.learn_active = self.quiz_active = self.cl_active = False
        self._after_id = None

        self._build_plan(); self._build_learn(); self._build_quiz()
        self._build_cloze(); self._build_bank(); self._build_sched(); self._build_data()
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.on_tab()

    def _close(self):
        save_db(); self.destroy()

    def on_tab(self):
        w = self.nb.tab(self.nb.select(), "text")
        if w == "今日计划": self.render_plan()
        elif w == "词库本": self.render_bank()
        elif w == "复习日程": self.render_sched()
        elif w == "新词学习": self.render_learn() if self.learn_active else self.render_learn_idle()
        elif w == "识别测验": self.render_quiz() if self.quiz_active else self.render_quiz_idle()
        elif w == "例句填空": self.render_cloze() if self.cl_active else self.render_cloze_idle()

    # ---------- 今日计划 ----------
    def _build_plan(self):
        f = self.tabs["今日计划"]
        head = ttk.LabelFrame(f, text="📊 概览"); head.pack(fill="x", padx=12, pady=(12, 6))
        self.plan_stats = ttk.Label(head, font=("", 11)); self.plan_stats.pack(anchor="w", padx=10, pady=8)
        b1 = ttk.LabelFrame(f, text="🆕 今日新词（每学完 20 个，自动进入本批即时复习）")
        b1.pack(fill="x", padx=12, pady=6)
        self.plan_new = ttk.Label(b1, wraplength=760, justify="left"); self.plan_new.pack(anchor="w", padx=10, pady=4)
        ttk.Button(b1, text="▶ 开始学习新词（每批 20 词）", command=self.start_learn).pack(anchor="w", padx=10, pady=(0, 8))
        b2 = ttk.LabelFrame(f, text="🔁 到期复习"); b2.pack(fill="x", padx=12, pady=6)
        self.plan_due = ttk.Label(b2, wraplength=760, justify="left"); self.plan_due.pack(anchor="w", padx=10, pady=4)
        r = ttk.Frame(b2); r.pack(anchor="w", padx=10, pady=(0, 8))
        ttk.Button(r, text="▶ 识别测验", command=self.start_quiz).pack(side="left", padx=(0, 8))
        ttk.Button(r, text="▶ 例句填空复习", command=lambda: self.start_cloze(True)).pack(side="left")
        b3 = ttk.LabelFrame(f, text="⏰ 逾期未首学"); b3.pack(fill="x", padx=12, pady=6)
        self.plan_over = ttk.Label(b3, wraplength=760, justify="left"); self.plan_over.pack(anchor="w", padx=10, pady=4)
        b4 = ttk.LabelFrame(f, text="📖 篇章速览与参考答案（Day 1 · Shakespeare 排练室研究）")
        b4.pack(fill="both", expand=True, padx=12, pady=6)
        txt = tk.Text(b4, height=7, wrap="word", relief="flat", background="#f9fafb")
        txt.pack(fill="both", expand=True, padx=10, pady=6)
        gist = ("大意：RSC 委托的随机对照试验发现，“排练室”教学法（让学生入戏扮演角色，如以 Ferdinand 身份写“瓶中信”）"
                "能扩大小学生词汇量、提升写作复杂度与情感素养：实验组能设身处地为文学角色代言、描写更开阔；"
                "对照组则依赖“荒岛陈词滥调”。原因可能是戏剧让学生用整个身体把文字演活，加上莎士比亚 2 万词的庞大词汇量。\n\n"
                "参考答案：21 C ｜ 22 A ｜ 23 A ｜ 24 B ｜ 25 A")
        txt.insert("1.0", gist); txt.config(state="disabled")

    def render_plan(self):
        t = today(); day = DB["days"].get(t)
        new_today = [w for w in day["words"] if st(t + "::" + w["w"])["box"] == 0] if day else []
        overdue = [it for it in all_words() if st(it["key"])["box"] == 0 and it["day"] != t]
        due = due_words()
        aws = all_words(); total = len(aws)
        learned = len([1 for it in aws if st(it["key"])["box"] > 0])
        self.plan_stats.config(text=f"📅 {t}    词库总数 {total}    已启动学习 {learned}    "
                                    f"今日新词 {len(new_today)}    今日待复习 {len(due)}")
        if day:
            self.plan_new.config(text=f"{day.get('title', '')}（待首学 {len(new_today)} / {len(day['words'])} 个 · "
                                      f"每批 {BATCH} 词，学完即测）")
        else:
            self.plan_new.config(text="今天还没有新词单：把新文章+题目截图发给助手 → 拿到 JSON → 到「数据·导入」粘贴即可。")
        if due:
            self.plan_due.config(text=f"今天有 {len(due)} 个词到期（艾宾浩斯节奏），答错过的词明天会更快重现。")
        else:
            self.plan_due.config(text="今天没有到期复习词。学完新词后，明天起按 +1 → +2 → +4 → +7 → +15 → +30 天自动安排。")
        if overdue:
            self.plan_over.config(text=f"有 {len(overdue)} 个之前导入但未首学的词，开始学习时会优先补学。")
        else:
            self.plan_over.config(text="没有积压的未学词 👍")

    # ---------- 新词学习（每批 BATCH 个，学完立即复习本批） ----------
    def _build_learn(self):
        f = self.tabs["新词学习"]
        self.learn_top = ttk.Frame(f); self.learn_top.pack(fill="x", padx=12, pady=(12, 0))
        self.learn_prog = ttk.Label(self.learn_top); self.learn_prog.pack(side="left")
        self.pbar = ttk.Progressbar(self.learn_top, length=300, maximum=100); self.pbar.pack(side="right")
        self.learn_card = ttk.Frame(f); self.learn_card.pack(expand=True, fill="both")
        self.l_word = tk.Label(self.learn_card, font=("Segoe UI", 28, "bold")); self.l_word.pack(pady=(36, 0))
        self.l_meta = tk.Label(self.learn_card, foreground="#6b7280"); self.l_meta.pack()
        self.l_cn = tk.Label(self.learn_card, font=("", 15)); self.l_cn.pack(pady=8)
        self.l_ex = tk.Label(self.learn_card, wraplength=720, justify="left", foreground="#4b5563",
                             background="#f9fafb", padx=12, pady=8)
        self.l_ex.pack(pady=6, padx=24, fill="x")
        row = ttk.Frame(self.learn_card); row.pack(pady=18)
        tk.Button(row, text="😵 没记住", command=lambda: self.learn_answer(False), bg="#fee2e2",
                  relief="flat", padx=14, pady=6, font=("", 12)).pack(side="left", padx=10)
        tk.Button(row, text="🔊 发音", command=self.speak, relief="flat", padx=14, pady=6,
                  font=("", 12)).pack(side="left", padx=10)
        tk.Button(row, text="✅ 认识了", command=lambda: self.learn_answer(True), bg="#dcfce7",
                  relief="flat", padx=14, pady=6, font=("", 12)).pack(side="left", padx=10)
        self.learn_done_lbl = tk.Label(f, text="", font=("", 13), justify="left")

    def speak(self):
        try:
            import pyttsx3
            eng = pyttsx3.init(); eng.say(self.learn_q[self.learn_i]["w"]["w"]); eng.runAndWait()
        except Exception:
            messagebox.showinfo("提示", "朗读需要语音库：pip install pyttsx3（可选）")

    def start_learn(self):
        t = today()
        q = [it for it in all_words() if st(it["key"])["box"] == 0]
        q.sort(key=lambda it: (0 if it["day"] == t else 1, it["day"]))
        if not q:
            messagebox.showinfo("提示", "没有待学的新词。可到「数据·导入」粘贴新词单，或先做到期复习。")
            return
        batch, self.learn_rest = q[:BATCH], q[BATCH:]   # 本批只学 BATCH 个，其余留给下一批
        self.learn_q, self.learn_i, self.learn_again, self.learn_total = batch, 0, 0, len(batch)
        self.learn_active = True
        self.nb.select(self.tabs["新词学习"])
        self.render_learn()

    def render_learn(self):
        self.learn_card.pack(expand=True, fill="both")
        self.learn_top.pack(fill="x", padx=12, pady=(12, 0))
        self.learn_done_lbl.pack_forget()
        if self.learn_i >= len(self.learn_q):
            self.learn_active = False
            self.learn_card.pack_forget(); self.learn_top.pack_forget()
            self.start_new_review(self.learn_q)   # ★ 学完一批（≤BATCH 个），立即复习本批
            return
        it = self.learn_q[self.learn_i]
        self.pbar.config(value=self.learn_i / max(self.learn_total, 1) * 100)
        self.learn_prog.config(text=f"新词学习（本批 {self.learn_total} 词）· 第 {self.learn_i + 1}/{self.learn_total} 个")
        self.l_word.config(text=it["w"]["w"])
        self.l_meta.config(text=f"{it['w']['pos']}    [{it['w']['tag']}]")
        self.l_cn.config(text=it["w"]["cn"])
        self.l_ex.config(text=it["w"]["ex"])

    def render_learn_idle(self):
        self.learn_card.pack_forget(); self.learn_top.pack_forget(); self.learn_done_lbl.pack_forget()
        self.learn_done_lbl.config(text=f"🆕 新词学习（每批 {BATCH} 词）\n\n"
                                        "看词 → 看释义和真题例句 → 自评“认识 / 没记住”（无需拼写）。\n"
                                        f"每学完一批 {BATCH} 词，会自动开始本批「即时复习」：看英文选中文义，\n"
                                        "答错自动重测并给出例句，直到全部过关。\n"
                                        "（若正在复习中，请回「识别测验」页继续）\n"
                                        "点「今日计划」中的「开始学习新词」开始。")
        self.learn_done_lbl.pack(pady=30, padx=20)

    def learn_answer(self, ok):
        if self.learn_i >= len(self.learn_q): return
        it = self.learn_q[self.learn_i]
        if ok:
            learn_done(it["key"])
        else:
            learn_fail(it["key"]); self.learn_q.append(it); self.learn_again += 1
        self.learn_i += 1; self.render_learn()

    # ---------- 识别测验（到期复习） + 学后即时复习 ----------
    def _build_quiz(self):
        f = self.tabs["识别测验"]
        self.quiz_top = ttk.Frame(f); self.quiz_top.pack(fill="x", padx=12, pady=(12, 0))
        self.quiz_prog = ttk.Label(self.quiz_top); self.quiz_prog.pack(side="left")
        self.qbar = ttk.Progressbar(self.quiz_top, length=300, maximum=100); self.qbar.pack(side="right")
        self.quiz_card = ttk.Frame(f); self.quiz_card.pack(expand=True, fill="both")
        self.q_word = tk.Label(self.quiz_card, font=("Segoe UI", 28, "bold")); self.q_word.pack(pady=(40, 0))
        self.q_meta = tk.Label(self.quiz_card, foreground="#6b7280"); self.q_meta.pack()
        self.q_opts = tk.Frame(self.quiz_card); self.q_opts.pack(pady=16, padx=60, fill="x")
        self.q_btns = []
        for _ in range(4):
            b = tk.Button(self.q_opts, anchor="w", relief="flat", padx=12, pady=8, font=("", 12))
            b.pack(fill="x", pady=4); self.q_btns.append(b)
        self.q_fb = tk.Label(self.quiz_card, font=("", 12), wraplength=720, justify="left"); self.q_fb.pack()
        self.quiz_done_lbl = tk.Label(f, text="", font=("", 13), justify="left")
        self.q_next_btn = ttk.Button(f, text="", command=self._next_batch)   # 学完一批后的“下一批”入口

    def _next_batch(self):
        self.q_next_btn.pack_forget()
        self.start_learn()

    def start_quiz(self):
        self.quiz_mode = "due"
        self.quiz_q = due_words(); random.shuffle(self.quiz_q)
        self.quiz_i, self.quiz_ok, self.quiz_total = 0, 0, len(self.quiz_q)
        self.quiz_bad, self.quiz_re = [], set()
        self.quiz_first_ok, self.quiz_seen, self.quiz_retry = 0, set(), {}
        self.quiz_active = True
        self.q_next_btn.pack_forget()
        self.nb.select(self.tabs["识别测验"])
        self.render_quiz()

    def start_new_review(self, items):
        """★ 学完一批新词后立刻复习：看英文选中文义，答错重测（附例句），直到过关。
        即时复习不改 SRS 档位——这批词明天照常进入第 1 轮复习。"""
        if not items: return
        self.quiz_mode = "new"
        self.quiz_q = items[:]; random.shuffle(self.quiz_q)
        self.quiz_i, self.quiz_ok, self.quiz_first_ok = 0, 0, 0
        self.quiz_total = len(self.quiz_q)
        self.quiz_bad, self.quiz_re = [], set()
        self.quiz_seen, self.quiz_retry = set(), {}
        self.quiz_active = True
        self.q_next_btn.pack_forget()
        self.nb.select(self.tabs["识别测验"])
        self.render_quiz()

    def render_quiz(self):
        self.quiz_card.pack(expand=True, fill="both")
        self.quiz_top.pack(fill="x", padx=12, pady=(12, 0))
        self.quiz_done_lbl.pack_forget(); self.q_next_btn.pack_forget()
        if self.quiz_i >= len(self.quiz_q):
            self.quiz_active = False
            self.quiz_card.pack_forget(); self.quiz_top.pack_forget()
            if self.quiz_mode == "new":
                self._render_new_review_done()
                return
            if self.quiz_total == 0 and not self.quiz_q:
                text = "今天没有到期复习词。先去「新词学习」吧！"
            else:
                wrongs = "、".join(self.quiz_bad[:30]) if self.quiz_bad else "无"
                text = f"答对 {self.quiz_ok} / {len(self.quiz_q)}（含错词重排）\n错词：{wrongs}\n错词已降档，明天会再次出现。"
            self.quiz_done_lbl.config(text="🏁 测验完成\n\n" + text)
            self.quiz_done_lbl.pack(pady=30, padx=20)
            self.quiz_mode = None
            return
        it = self.quiz_q[self.quiz_i]
        mode_txt = "即时复习（学后巩固）" if self.quiz_mode == "new" else "识别测验"
        self.qbar.config(value=self.quiz_i / max(len(self.quiz_q), 1) * 100)
        self.quiz_prog.config(text=f"{mode_txt} · 第 {self.quiz_i + 1}/{len(self.quiz_q)} 个 · 答对 {self.quiz_ok}")
        self.q_word.config(text=it["w"]["w"]); self.q_meta.config(text=it["w"]["pos"])
        self.q_fb.config(text="")
        opts = get_options(it); self._q_item = it
        self._q_correct = [i for i, o in enumerate(opts) if o["key"] == it["key"]][0]
        for i, b in enumerate(self.q_btns):
            b.config(text=opts[i]["w"]["cn"], bg="#ffffff", fg="#1f2937",
                     command=lambda i=i: self.quiz_answer(i), state="normal")

    def _render_new_review_done(self):
        wrongs = "、".join(self.quiz_bad[:30]) if self.quiz_bad else "无"
        text = (f"本批 {self.quiz_total} 词 · 首次即答对 {self.quiz_first_ok} 个\n"
                f"需要留意的词：{wrongs}\n\n"
                "这批词已进入艾宾浩斯计划：明天第 1 轮复习（之后 +2/+4/+7/+15/+30 天推进）。")
        rest = self.learn_rest
        if rest:
            text += f"\n\n还剩 {len(rest)} 个新词待学，点下方按钮继续下一批。"
            self.q_next_btn.config(text=f"▶ 继续学习下一批（剩余 {len(rest)} 词）")
            self.q_next_btn.pack(pady=12)
        else:
            text += "\n\n✅ 新词已全部处理完，明天按计划回来复习即可。"
        self.quiz_done_lbl.config(text=f"🎓 本批「学 {BATCH} 词 + 即时复习」完成\n\n" + text)
        self.quiz_done_lbl.pack(pady=30, padx=20)
        self.quiz_mode = None

    def quiz_answer(self, i):
        it = self._q_item; ok = (i == self._q_correct)
        for j, b in enumerate(self.q_btns):
            b.config(state="disabled")
            if j == self._q_correct: b.config(bg="#dcfce7", fg="#166534")
            elif j == i and not ok: b.config(bg="#fee2e2", fg="#991b1b")
        if self.quiz_mode == "new":
            # 即时复习：只统计、不改档位；答错重测直到答对（同一词最多重测 2 次）
            if it["key"] not in self.quiz_seen:
                self.quiz_seen.add(it["key"])
                if ok: self.quiz_first_ok += 1
                else: self.quiz_bad.append(it["w"]["w"])
            if ok:
                self.quiz_ok += 1
                fb = f"✔ 正确　{it['w']['pos']} {it['w']['cn']}"
            else:
                c = self.quiz_retry.get(it["key"], 0)
                if c < 2:
                    self.quiz_retry[it["key"]] = c + 1
                    self.quiz_q.append(it)   # 稍后再次出现
                fb = (f"✘ 正确答案：{it['w']['pos']} {it['w']['cn']}\n"
                      f"例句：{it['w']['ex']}" + ("" if c >= 2 else "\n（稍后会再出现，答对即过）"))
            self.q_fb.config(text=fb, foreground="#16a34a" if ok else "#dc2626")
        else:
            if ok: self.quiz_ok += 1
            else:
                self.quiz_bad.append(it["w"]["w"])
                if it["key"] not in self.quiz_re:
                    self.quiz_re.add(it["key"]); self.quiz_q.append(it)
            apply_result(it["key"], ok)
            self.q_fb.config(text="✔ 正确" if ok else f"✘ 正确答案：{it['w']['cn']}",
                             foreground="#16a34a" if ok else "#dc2626")
        if self._after_id: self.after_cancel(self._after_id)
        self._after_id = self.after(900 if ok else 1800, self._quiz_next)

    def _quiz_next(self):
        self.quiz_i += 1; self.render_quiz()

    def render_quiz_idle(self):
        n = len(due_words())
        self.quiz_card.pack_forget(); self.quiz_top.pack_forget(); self.quiz_done_lbl.pack_forget()
        self.q_next_btn.pack_forget()
        self.quiz_done_lbl.config(text=f"🔁 识别测验\n\n到期复习：看英文选中文义（四选一），答对升档、答错降档并明天重现。\n"
                                       f"每批新词学完后的「即时复习」也在这里自动进行。\n当前到期：{n} 个。")
        self.quiz_done_lbl.pack(pady=30, padx=20)

    # ---------- 例句填空 ----------
    def _build_cloze(self):
        f = self.tabs["例句填空"]
        self.cl_top = ttk.Frame(f); self.cl_top.pack(fill="x", padx=12, pady=(12, 0))
        self.cl_prog = ttk.Label(self.cl_top); self.cl_prog.pack(side="left")
        self.cl_bar = ttk.Progressbar(self.cl_top, length=300, maximum=100); self.cl_bar.pack(side="right")
        self.cl_card = ttk.Frame(f); self.cl_card.pack(expand=True, fill="both")
        self.cl_sent = tk.Label(self.cl_card, wraplength=720, justify="left", font=("", 13),
                                background="#f9fafb", padx=14, pady=10)
        self.cl_sent.pack(pady=(24, 10), padx=24, fill="x")
        self.cl_opts = tk.Frame(self.cl_card); self.cl_opts.pack(padx=60, fill="x")
        self.cl_btns = []
        for _ in range(4):
            b = tk.Button(self.cl_opts, relief="flat", padx=12, pady=8, font=("Consolas", 12, "bold"))
            b.pack(fill="x", pady=4); self.cl_btns.append(b)
        self.cl_fb = tk.Label(self.cl_card, wraplength=720, justify="left", font=("", 12)); self.cl_fb.pack(pady=8)
        self.cl_done_lbl = tk.Label(f, text="", font=("", 13), justify="left")

    def cloze_pool(self):
        out = []
        for it in all_words():
            w = it["w"]
            if w["tag"] == "短语" or not w.get("ex"): continue
            if re.search(r"\b" + re.escape(w["w"]) + r"\b", w["ex"], re.I):
                out.append(it)
        return out

    def start_cloze(self, use_due):
        if use_due:
            t = today(); q = []
            for it in self.cloze_pool():
                s = st(it["key"])
                if s["box"] > 0 and s["due"] and s["due"] <= t: q.append(it)
            self.cl_practice = False
        else:
            q = self.cloze_pool(); random.shuffle(q); q = q[:10]
            self.cl_practice = True
        self.cl_q, self.cl_i, self.cl_ok = q, 0, 0
        self.cl_active = True
        self.nb.select(self.tabs["例句填空"])
        if not q:
            self.cl_active = False
            self.cl_card.pack_forget(); self.cl_top.pack_forget(); self.cl_done_lbl.pack_forget()
            self.cl_done_lbl.config(text="当前没有到期词。可先用「数据·导入」旁的自由练习入口："
                                         "在「今日计划」无到期词时，用「随机练 10 词」（自由练习，不计进度）。")
            self.cl_done_lbl.pack(pady=30, padx=20); return
        self.render_cloze()

    def render_cloze(self):
        self.cl_card.pack(expand=True, fill="both")
        self.cl_top.pack(fill="x", padx=12, pady=(12, 0))
        self.cl_done_lbl.pack_forget()
        if self.cl_i >= len(self.cl_q):
            self.cl_active = False
            self.cl_card.pack_forget(); self.cl_top.pack_forget()
            mode = "自由练习（不计进度）" if self.cl_practice else "到期词已按作答更新复习时间"
            self.cl_done_lbl.config(text=f"📖 填空完成：答对 {self.cl_ok} / {len(self.cl_q)}\n{mode}")
            self.cl_done_lbl.pack(pady=30, padx=20); return
        it = self.cl_q[self.cl_i]
        self.cl_bar.config(value=self.cl_i / max(len(self.cl_q), 1) * 100)
        self.cl_prog.config(text=f"例句填空 · 第 {self.cl_i + 1}/{len(self.cl_q)} 个"
                                 + ("（自由练习）" if self.cl_practice else ""))
        pat = re.compile(r"\b" + re.escape(it["w"]["w"]) + r"\b", re.I)
        self._cl_pat = pat; self._cl_item = it
        self.cl_sent.config(text=pat.sub("______", it["w"]["ex"], count=1))
        self.cl_fb.config(text="")
        pool = [x for x in all_words()
                if x["key"] != it["key"] and x["w"]["w"] != it["w"]["w"] and x["w"]["tag"] != "短语"]
        same = [x for x in pool if x["w"]["tag"] == it["w"]["tag"]]
        rest = [x for x in pool if x["w"]["tag"] != it["w"]["tag"]]
        random.shuffle(same); random.shuffle(rest)
        opts = [it] + same[:3]
        for c in rest:
            if len(opts) >= 4: break
            if c not in opts: opts.append(c)
        random.shuffle(opts)
        self._cl_correct = [i for i, o in enumerate(opts) if o["key"] == it["key"]][0]
        for i, b in enumerate(self.cl_btns):
            b.config(text=opts[i]["w"]["w"], bg="#ffffff", fg="#1f2937",
                     command=lambda i=i: self.cloze_answer(i), state="normal")

    def cloze_answer(self, i):
        it = self._cl_item; ok = (i == self._cl_correct)
        for j, b in enumerate(self.cl_btns):
            b.config(state="disabled")
            if j == i: b.config(bg="#dcfce7" if ok else "#fee2e2")
        if ok: self.cl_ok += 1
        if not self.cl_practice: apply_result(it["key"], ok)
        self.cl_fb.config(text=self._cl_pat.sub(lambda m: "【" + m.group(0) + "】", it["w"]["ex"], count=1))
        if self._after_id: self.after_cancel(self._after_id)
        self._after_id = self.after(1200, self._cl_next)

    def _cl_next(self):
        self.cl_i += 1; self.render_cloze()

    def render_cloze_idle(self):
        self.cl_card.pack_forget(); self.cl_top.pack_forget(); self.cl_done_lbl.pack_forget()
        self.cl_done_lbl.config(text="📖 例句填空\n\n文章原句挖空，点击选词（无需拼写）。\n"
                                     "入口在「今日计划 → 到期复习 → 例句填空复习」。")
        self.cl_done_lbl.pack(pady=30, padx=20)

    # ---------- 词库本 ----------
    def _build_bank(self):
        f = self.tabs["词库本"]
        top = ttk.Frame(f); top.pack(fill="x", padx=12, pady=(12, 4))
        ttk.Label(top, text="搜索：").pack(side="left")
        self.var_q = tk.StringVar(); e = ttk.Entry(top, textvariable=self.var_q, width=26)
        e.pack(side="left", padx=(4, 12)); e.bind("<KeyRelease>", lambda ev: self.render_bank())
        ttk.Label(top, text="分类：").pack(side="left")
        self.var_tag = tk.StringVar(value="全部")
        cb1 = ttk.Combobox(top, textvariable=self.var_tag, values=["全部", "文章", "选项", "短语"],
                           width=7, state="readonly"); cb1.pack(side="left", padx=(4, 12))
        ttk.Label(top, text="状态：").pack(side="left")
        self.var_status = tk.StringVar(value="全部")
        cb2 = ttk.Combobox(top, textvariable=self.var_status,
                           values=["全部", "未学", "初记", "巩固中", "强化中", "已掌握"],
                           width=7, state="readonly"); cb2.pack(side="left", padx=(4, 12))
        ttk.Button(top, text="刷新", command=self.render_bank).pack(side="left")
        cb1.bind("<<ComboboxSelected>>", lambda ev: self.render_bank())
        cb2.bind("<<ComboboxSelected>>", lambda ev: self.render_bank())
        cols = ("word", "cn", "status")
        frame = ttk.Frame(f); frame.pack(fill="both", expand=True, padx=12, pady=6)
        self.bank_tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)
        self.bank_tree.heading("word", text="单词 / 词条")
        self.bank_tree.heading("cn", text="释义")
        self.bank_tree.heading("status", text="状态 / 下次复习")
        self.bank_tree.column("word", width=270); self.bank_tree.column("cn", width=340)
        self.bank_tree.column("status", width=160)
        vs = ttk.Scrollbar(frame, orient="vertical", command=self.bank_tree.yview)
        self.bank_tree.configure(yscrollcommand=vs.set)
        self.bank_tree.pack(side="left", fill="both", expand=True); vs.pack(side="left", fill="y")
        self.bank_tree.bind("<Double-1>", self._bank_detail)

    def render_bank(self):
        q = self.var_q.get().strip().lower()
        tagf, statf = self.var_tag.get(), self.var_status.get()
        self.bank_tree.delete(*self.bank_tree.get_children())
        for it in all_words():
            w, s = it["w"], st(it["key"])
            if tagf != "全部" and w["tag"] != tagf: continue
            lab = status_of(s)
            if statf != "全部" and lab != statf: continue
            if q and q not in w["w"].lower() and q not in w["cn"].lower(): continue
            nxt = f"（下次 {s['due']}）" if s["box"] > 0 and s["box"] < 7 and s["due"] else ""
            self.bank_tree.insert("", "end", values=(f"{w['w']}  [{w['tag']}]",
                                                     f"{w['pos']} {w['cn']}", lab + nxt))

    def _bank_detail(self, _ev):
        sel = self.bank_tree.selection()
        if not sel: return
        word = self.bank_tree.item(sel[0], "values")[0].split("  [")[0].strip()
        for it in all_words():
            if it["w"]["w"] == word:
                messagebox.showinfo(it["w"]["w"],
                                    f"{it['w']['pos']}  {it['w']['cn']}\n[{it['w']['tag']}]\n\n例句：{it['w']['ex']}")
                return

    # ---------- 复习日程 ----------
    def _build_sched(self):
        f = self.tabs["复习日程"]
        self.sched_text = tk.Text(f, wrap="none", font=("Consolas", 11), relief="flat", background="#fafafa")
        self.sched_text.pack(fill="both", expand=True, padx=12, pady=12)

    def render_sched(self):
        t = today()
        lines = [f"📅 未来 15 天复习日程（{t}）", ""]
        for i in range(15):
            d = add_days(t, i); n = 0
            for it in all_words():
                s = st(it["key"])
                if s["box"] > 0 and s["due"] == d: n += 1
            label = "今天" if i == 0 else d[5:]
            lines.append(f"{label}   {'█' * n if n else '·'}   {n}")
        lines += ["", "节奏：学后 1 → 2 → 4 → 7 → 15 → 30 天各复习一次（艾宾浩斯间隔重复）。",
                  "每天打开软件，计划按到期情况自动生成。"]
        self.sched_text.config(state="normal"); self.sched_text.delete("1.0", "end")
        self.sched_text.insert("1.0", "\n".join(lines)); self.sched_text.config(state="disabled")

    # ---------- 数据·导入 ----------
    def _build_data(self):
        f = self.tabs["数据·导入"]
        tip = ttk.LabelFrame(f, text="📥 每日导入流程"); tip.pack(fill="x", padx=12, pady=(12, 6))
        ttk.Label(tip, wraplength=760, justify="left",
                  text="① 把新文章+题目的截图发给助手 → ② 助手整理词单并给你一段 JSON → "
                       "③ 粘贴到下面 → ④ 点“导入并更新计划”，当日计划自动生成。").pack(anchor="w", padx=10, pady=8)
        box = ttk.LabelFrame(f, text="导入新词单 JSON"); box.pack(fill="both", expand=True, padx=12, pady=6)
        self.data_text = tk.Text(box, height=12, font=("Consolas", 10))
        self.data_text.pack(fill="both", expand=True, padx=10, pady=8)
        row = ttk.Frame(box); row.pack(anchor="w", padx=10, pady=(0, 10))
        ttk.Button(row, text="导入并更新计划", command=self.do_import).pack(side="left", padx=(0, 8))
        ttk.Button(row, text="导出备份", command=self.do_export).pack(side="left", padx=(0, 8))
        ttk.Button(row, text="清空学习进度", command=self.do_reset).pack(side="left")
        ttk.Label(f, text=f"数据文件：{DATA_FILE}", foreground="#6b7280").pack(anchor="w", padx=14, pady=(0, 10))

    def do_import(self):
        raw = self.data_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("提示", "请先粘贴 JSON 内容"); return
        try:
            obj = json.loads(raw)
            if "days" in obj:
                DB["days"].update(obj["days"]); DB["progress"].update(obj.get("progress", {}))
            elif "date" in obj and "words" in obj:
                DB["days"][obj["date"]] = {"date": obj["date"],
                                           "title": obj.get("title", "Day " + obj["date"]),
                                           "words": obj["words"]}
            else:
                raise ValueError("需要 {date,title,words} 或完整备份数据")
            save_db(); messagebox.showinfo("成功", "导入成功！今日计划已更新")
            self.nb.select(self.tabs["今日计划"])
        except Exception as e:
            messagebox.showerror("导入失败", str(e))

    def do_export(self):
        p = filedialog.asksaveasfilename(defaultextension=".json",
                                         initialfile="kaoyan_vocab_backup.json",
                                         filetypes=[("JSON 文件", "*.json")])
        if not p: return
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(DB, fh, ensure_ascii=False, indent=1)
        messagebox.showinfo("成功", "已备份到：\n" + p)

    def do_reset(self):
        if messagebox.askyesno("确认", "确定清空所有学习进度吗？（词库保留，进度清零）"):
            DB["progress"] = {}; save_db(); self.nb.select(self.tabs["今日计划"])

def main():
    load_db()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
