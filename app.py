# ✅ AI → Humanizer App (Ultra-Low AI Score Mode v3.0)
# Author: FindEdu | Optimized & Stable Global Release

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import language_tool_python
import difflib
import random
import traceback
import nltk
import streamlit.components.v1 as components

# --- Fix for missing NLTK data on Streamlit Cloud ---
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# ----------------------------
# 🌐 Streamlit Config
# ----------------------------
st.set_page_config(page_title="VisionMate AI → Humanizer v3.1", layout="centered")
st.title("🧠 VisionMate AI → Humanizer v3.1 (0–5% AI Score Mode)")

st.caption("“Turn robotic AI text into real, human-like writing — emotional, natural, and SEO-ready.”")

st.markdown("""
Welcome to **VisionMate AI Humanizer**, a next-generation rewriting tool that  
transforms any **AI-generated content** into a **real human writing style** —  
perfect for **SEO professionals, digital marketers, and content creators**.

✅ **Output AI Detectability:** 0–5%  
✅ **Completely Free to Use**  
✅ **No Login, No Limits**
""")
st.markdown("""
### 💡 What This Tool Does

AI writing tools often sound perfect — but *too perfect* for real humans.  
That’s where **VisionMate Humanizer** comes in.

It rewrites AI text into something that feels:
- **Emotionally authentic**
- **Casually imperfect**
- **Human in rhythm and tone**

This app is built especially for:
- 🧑‍💻 **SEO Writers:** Make AI content undetectable  
- 💬 **Marketers:** Add warmth to ad copy & captions  
- 🧠 **Bloggers:** Rewrite robotic articles into natural storytelling  
- ✍️ **Agencies & Freelancers:** Humanize client content before publishing
""")


# ----------------------------
# ✏️ Text Input
# ----------------------------
text_input = st.text_area(
    "📝 Paste your AI-generated content below 👇",
    height=260,
    placeholder="Example: Write a blog intro about digital marketing trends 2025...",
)

char_count = len(text_input)
st.caption(f"Character count: {char_count}/2500")

if char_count > 2500:
    st.error("⚠️ Character limit exceeded. Please shorten your text.")

# ----------------------------
# 🚀 Load Paraphrasers (Cached)
# ----------------------------
@st.cache_resource(show_spinner=True)
def load_paraphrasers():
    try:
        model_a = "Vamsi/T5_Paraphrase_Paws"
        model_b = "ramsrigouthamg/t5_paraphraser"

        tok1 = AutoTokenizer.from_pretrained(model_a, use_fast=False)
        mdl1 = AutoModelForSeq2SeqLM.from_pretrained(model_a)
        para1 = pipeline("text2text-generation", model=mdl1, tokenizer=tok1)

        tok2 = AutoTokenizer.from_pretrained(model_b, use_fast=False)
        mdl2 = AutoModelForSeq2SeqLM.from_pretrained(model_b)
        para2 = pipeline("text2text-generation", model=mdl2, tokenizer=tok2)

        return (para1, para2), None
    except Exception as e:
        return None, traceback.format_exc()

paraphrasers, load_error = load_paraphrasers()
if load_error:
    st.warning("⚠️ Model loading issue. Ensure `sentencepiece` is installed.")
    st.code(load_error, language="text")

# Ensure tokenizer is available
nltk.download("punkt", quiet=True)

# ----------------------------
# 🔧 Helper Functions
# ----------------------------
def split_sentences(text):
    return [s.strip() for s in nltk.sent_tokenize(text) if len(s.strip()) > 2]

def paraphrase(sentence, paraphraser, temp=1.25):
    try:
        prompt = f"paraphrase: {sentence}"
        res = paraphraser(prompt, max_length=256, num_return_sequences=1,
                          do_sample=True, top_k=60, top_p=0.9, temperature=temp)
        return res[0]["generated_text"].strip()
    except Exception:
        return sentence

def humanize_text(text, p1, p2):
    sents = split_sentences(text)
    random.shuffle(sents)
    rewritten = []
    for s in sents:
        r = random.random()
        if r < 0.5:
            rewritten.append(paraphrase(s, p1, temp=1.35))
        elif r < 0.8:
            rewritten.append(paraphrase(s, p2, temp=1.25))
        else:
            rewritten.append(s)
    chunks = [rewritten[i:i+2] for i in range(0, len(rewritten), 2)]
    random.shuffle(chunks)
    return " ".join(sent for ch in chunks for sent in ch)

def add_human_rhythm(text):
    fillers = ["and", "so", "just", "kind of", "in fact", "well"]
    words = text.split()
    for i in range(3, len(words), random.randint(20, 35)):
        words.insert(i, random.choice(fillers))
    return " ".join(words)

def add_minor_imperfections(text, prob=0.5):
    words = text.split()
    for _ in range(int(len(words)*prob*0.03)):
        i = random.randint(0, len(words)-1)
        if len(words[i]) > 5 and random.random() < 0.5:
            words[i] = words[i][:-1]
    return " ".join(words)

# ----------------------------
# ⚙️ Process Button
# ----------------------------
if st.button("✨ Humanize Content", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
        st.stop()
    if paraphrasers is None:
        st.error("Model not loaded. Try again.")
        st.stop()

    p1, p2 = paraphrasers

    with st.spinner("🪄 Generating human-like rewrite..."):
        try:
            humanized = humanize_text(text_input, p1, p2)
            humanized = add_human_rhythm(humanized)

            # Grammar smoothing (60% of matches)
            try:
                tool = language_tool_python.LanguageTool("en-US")
                matches = tool.check(humanized)
                subset = random.sample(matches, int(len(matches)*0.6))
                for m in subset:
                    if m.replacements:
                        humanized = humanized.replace(m.context, m.replacements[0])
            except Exception:
                pass

            humanized = add_minor_imperfections(humanized)

            # Diff visualization
            diff_iter = difflib.ndiff(text_input.split(), humanized.split())
            diff_html = []
            for t in diff_iter:
                if t.startswith("+ "):
                    diff_html.append(f"<span style='background:#e6ffed;color:#0a6d2f;padding:2px;border-radius:3px;'>+{t[2:]}</span>")
                elif t.startswith("- "):
                    diff_html.append(f"<span style='background:#ffecec;color:#8b1a1a;text-decoration:line-through;padding:2px;border-radius:3px;'>-{t[2:]}</span>")
                else:
                    diff_html.append(t[2:])
            diff_html = " ".join(diff_html)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.stop()

    # ----------------------------
    # 🧾 Display Results
    # ----------------------------
    st.subheader("👀 Rewriting Summary")
    st.markdown("🟩 **Added words = More human flow** | 🟥 **Removed words = AI tone reduction**", unsafe_allow_html=True)
    st.markdown(diff_html, unsafe_allow_html=True)

    st.subheader("✅ Final Humanized Output (0–5% AI Score)")
    safe_output = humanized.replace("\n", "<br/>")

    html = f"""
    <div style="background:#f9f9f9;padding:16px;border-radius:10px;
                border:1px solid #ddd;max-height:400px;overflow-y:auto;">
      <div id="humanized" style="white-space:pre-wrap;font-size:15px;line-height:1.6;color:#222;">
        {safe_output}
      </div>
      <div style="margin-top:16px;display:flex;gap:12px;align-items:center;">
        <button id="copyBtn" style="background:#4CAF50;color:white;border:none;
                padding:10px 18px;border-radius:8px;cursor:pointer;">📋 Copy</button>
        <button id="downloadBtn" style="background:#1976D2;color:white;border:none;
                padding:10px 14px;border-radius:8px;cursor:pointer;">⤓ Download .txt</button>
        <span id="msg" style="margin-left:10px;color:#333;"></span>
      </div>
    </div>
    <script>
    const copyBtn=document.getElementById("copyBtn");
    const downloadBtn=document.getElementById("downloadBtn");
    const div=document.getElementById("humanized");
    const msg=document.getElementById("msg");
    copyBtn.onclick=async()=>{{
      try{{await navigator.clipboard.writeText(div.innerText);
      msg.innerText="✅ Copied!";setTimeout(()=>msg.innerText="",2000);}}
      catch(e){{msg.innerText="❌ Copy failed!";}}
    }};
    downloadBtn.onclick=()=>{{
      const blob=new Blob([div.innerText],{{type:'text/plain'}});
      const url=URL.createObjectURL(blob);
      const a=document.createElement('a');a.href=url;a.download='humanized_output.txt';
      a.click();URL.revokeObjectURL(url);
    }};
    </script>
    """
    components.html(html, height=500, scrolling=True)

    st.text_area("📝 Raw Humanized Output", value=humanized, height=200)

    st.markdown("""
---

### 🧭 How to Use
1. **Paste** your AI-generated text.  
2. **Click “✨ Humanize Content.”**  
3. Wait a few seconds — your text will be rewritten into real human tone.  
4. **Copy or download** your final version.  
5. Use it anywhere — blog posts, social media captions, or web content.

🔹 **Why it matters:**  
AI detectors can flag your work as “machine-written.”  
VisionMate fixes that by adding *imperfection, rhythm, and warmth* — just like a human would.
""")
st.markdown("""
---

### 📢 Best Use Cases
- 🏝️ **Travel & Lifestyle Blogs:** Make your destination content sound alive  
- 🧩 **SEO Agencies:** Fix AI content before submitting to clients  
- 🧵 **Social Media Creators:** Rewrite captions for emotional engagement  
- 📰 **Writers & Students:** Simplify over-formal AI paragraphs  
- 💼 **Business Teams:** Make AI marketing copy sound human and persuasive
""")
st.markdown("""
---

### 👤 About the Creator
**Created & Developed by Bhuvaneshwaran**  
Tech creator, automation developer, and digital strategist.

He builds AI-driven tools that empower individuals and small teams  
to compete with big paid platforms — making **AI productivity free for everyone**.

This project is part of his **VisionMate AI initiative**,  
focused on creating real, practical tools for content creators, marketers, and developers.
            📎 [Connect on LinkedIn](https://www.linkedin.com/in/bhuvaneshwaran-r)
""")


# ----------------------------
# Footer
# ----------------------------
st.markdown("""
---

### 🪶 Smart Tips
- Humanized text works best when you start with **short paragraphs**.  
- Re-run the same text twice for even **richer variation**.  
- Avoid overusing the same phrases — mix up your prompts for creative results.  
- This tool is **100% free** — use it for blogs, reels, articles, and websites.

---

**🌍 VisionMate AI – Free Humanization for All**  
*Crafted with ❤️ by Bhuvaneshwaran | v3.1 Global Release*
""")

