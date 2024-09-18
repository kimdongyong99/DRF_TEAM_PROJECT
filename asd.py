from openai import OpenAI
from Big_News.config_key import OPENAI_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY,
)
system_instructions = """
너는 장고 선생님이야 학생이 질문하면 자세하게 알려주고 공식 문서 도 알려줘
 """
print("질문 내용을 입력하세요. 입력을 마치려면 'END'를 입력하세요.")
user_input_lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    user_input_lines.append(line)

user_input = "\n".join(user_input_lines)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": system_instructions,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ],
)

print(completion.choices[0].message)
