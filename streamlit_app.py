import openai
import os
import streamlit as st

from parse_hh import get_html, extract_resume_data, extract_vacancy_data

client = openai.Client(
    api_key = os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет прояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка
должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens = 1000,
        temperature = 0
    )
    return response.choices[0].message.content

st.title('CV Scorinng App')

job_description_url = st.text_area('Enter tho job description url')

cv_url = st.text_area('Enter the CV url')

if st.button('Score CV'):
    with st.spinner('Scoring CV...'):
        try:
            job_html = get_html(job_description_url).text
            resume_html = get_html(cv_url).text
            job_text = extract_vacancy_data(job_html)
            resume_text = extract_resume_data(resume_html)
            prompt = f"# ВАКАНСИЯ\n{job_text}\n\n# РЕЗЮМЕ\n{resume_text}"
            response = request_gpt(SYSTEM_PROMPT, prompt)
            st.subheader("📊 Результат анализа:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")