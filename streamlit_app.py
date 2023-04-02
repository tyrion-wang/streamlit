import openai
import streamlit as st
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil

# import pyperclip

# Step 1: Obtain OpenAI API key
openai.api_key = st.secrets["API_Key"]

# 嵌入HTML代码
html_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1734224087399502"
     crossorigin="anonymous"></script>
<!-- 测试 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-1734224087399502"
     data-ad-slot="1628847602"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
<p style='font-size: 18px;'>这是一个广告位</p >
"""

def inject_ga():
    GA_ID = "G-XXXXXXXXXX"

    # Note: Please replace the id from G-XXXXXXXXXX to whatever your
    # web application's id is. You will find this in your Google Analytics account
    
    GA_JS = """
    <p style='font-size: 18px;'>插入谷歌广告</p >
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1734224087399502"
     crossorigin="anonymous"></script>
    <script>
        gtag('config', 'G-XXXXXXXXXX');
    </script>
    """

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    logging.info(f'editing {index_path}')
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    logging.info(f'editing {soup}')
    if not soup.find(id=GA_ID):  # if cannot find tag
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  # recover from backup
        else:
            shutil.copy(index_path, bck_index)  # keep a backup
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_JS)
        index_path.write_text(new_html)


def generate_cover_letter(prompt, model, temperature, max_tokens):
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = completions.choices[0].text
    return message

def generate_3(prompt, model, temperature, max_tokens):
	completions = openai.ChatCompletion.create(
  		model=model,
  		temperature=temperature,
        max_tokens=2000,
        top_p=1,
	  	messages=[
	        {"role": "system", "content": "你是一个作文写作者."},
	        {"role": "user", "content": prompt},
	    ]
	)
	message = completions.choices[0].message.content
	return message

def main():
    st.set_page_config(page_title="作文灵感生成器", page_icon=":guardsman:", layout="wide")
    st.title("OpenAI GPT 作文小助手\nOpenAI GPT Cover Letter Generator")
    st.markdown("根据你的作文要求，由 OpenAI GPT 帮助你生成一篇文章。")
    st.write(html_code, unsafe_allow_html=True)
    if 'API_Key' in os.environ:
        st.write("找到"+ st.secrets)
    
    inject_ga()
    # Get user input
    user_profile = st.text_area("输入你的作文标题:")
    job_description = st.text_area("输入你的作文字数、语言等要求:")
    prompt = (f"写一篇小作文:\n{job_description}\n\n作文要求:\n{user_profile}")
    # prompt = (f"请用中文帮我写一封求职信，我的能力描述以及工作经验：\n{user_profile}\n\n职位描述：\n{job_description}")
    model = "gpt-3.5-turbo"
    temperature = st.slider("选择随机值 Choose Temperature:", 0.0, 1.0, 0.7)
    max_tokens = st.slider("选择作文字数 Choose Max Tokens:", 50, 500, 1000)

    if st.button("生成作文 Generate"):
        cover_letter = generate_3(prompt, model, temperature, max_tokens)
        st.success("大功告成！作文已经生成了！\n Success! Your Cover Letter is Ready")
        st.markdown(cover_letter)
        st.markdown("**点击以下按钮下载作文 Click the Button to Download**")
        
        st.download_button(
            label="下载作文 Download",
            data=cover_letter,
            file_name='cover_letter.md',
        )
        
        # if st.button("Download"):
        #     with open("cover_letter.txt", "w") as f:
        #         f.write(cover_letter)
        #         f.close()
        #         st.markdown("Your cover letter saved as **cover_letter.txt**")
        #         st.markdown("You can also find the cover letter in the **Downloads** folder")

if __name__== "__main__":
    main()