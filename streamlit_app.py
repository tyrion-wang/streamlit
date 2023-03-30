import openai
import streamlit as st
# import pyperclip

# Step 1: Obtain OpenAI API key
openai.api_key = st.secrets["API_Key"]
# openai.api_key = ""


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
	openai.ChatCompletion.create(
  		model=model,
	  	messages=[
	        {"role": "system", "content": "You are a helpful assistant."},
	        {"role": "user", "content": "Who won the world series in 2020?"},
	        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
	        {"role": "user", "content": "Where was it played?"}
	    ]
	)
	message = completions.choices[0].text
    return message

def main():
    st.set_page_config(page_title="作文灵感生成器", page_icon=":guardsman:", layout="wide")
    st.title("OpenAI GPT 作文小助手\nOpenAI GPT Cover Letter Generator")
    st.markdown("根据你的作文要求，由 OpenAI GPT 帮助你生成一篇文章。")
    
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