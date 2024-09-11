from zhipuai import ZhipuAI
import datetime
import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    speak("你好")
    Hour = datetime.datetime.now().hour
    if Hour >= 6 and Hour < 12:
        speak("早上好！")
    elif Hour >= 12 and Hour < 18:
        speak("下午好！")
    else:
        speak("晚上好！")
    speak("人工智能为您服务，请问有什么需要的么")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n录音中...")
        r.pause_threshold = 3
        audio = r.listen(source)
        # print(audio)
    try:
        print("辨认中...")
        query = r.recognize_google(audio, language='zh-CN')
        print(query)
    except Exception as e:
        speak("辨认失败，请重说。")
        return "None"

    return query


def get_ai_response(prompt_text,chat_history):
    client = ZhipuAI(api_key="2b2a20ea8b0288528d6903b9c43e87cc.mGCTxCAZwrhSSX61")
    # api_key换成自己的api_key即可
    chat_history.append({
                "role": "user",
                "content": prompt_text
            })

    response = client.chat.completions.create(
        model="glm-4",
        messages=chat_history,
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        stream=True,
    )
    # 打印用户的提问
    # print(prompt_text)
    # 在循环中逐次打印回复内容，并在每条回复后面添加换行符
    model_response = ''
    for chunk in response:
        for choice in chunk.choices:
            choice_content = choice.delta.content
            print(choice_content, end="", flush=True)  # 移除换行符，使得内容连在一起
            model_response+=choice_content
    speak(model_response)
    print("\n")  # 在所有回复结束后添加一个换行符
    chat_history.append({
        "role": "user",
        "content": model_response
    })
    return chat_history


def main():
    chat_history = []
    wish()
    wake = "你好"
    while True:
        que = takeCommand().lower()
        if que.count(wake) > 0:
            speak("开始")
            prompt_text = takeCommand().lower()
            if prompt_text.lower() == "退出":
                print("再见")
                speak("再见")
                break
            chat_history = get_ai_response(prompt_text, chat_history)

if __name__ == "__main__":
    main()