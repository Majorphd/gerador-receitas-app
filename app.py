import streamlit as st
import google.generativeai as genai

# Configuração da chave da API Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Título do App
st.title("🍽️ Gerador de Receitas com IA Gemini")

# 1. Ingredientes
ingredientes = st.text_area(
    "Ingredientes principais que você possui:",
    placeholder="Ex: frango, tomate, cebola, arroz"
)

# 2. Tipo de culinária
tipo_culinaria = st.selectbox(
    "Escolha o tipo de culinária desejado:",
    ["Italiana", "Brasileira", "Asiática", "Mexicana", "Qualquer uma"]
)

# 3. Nível de dificuldade
nivel_dificuldade = st.slider(
    "Nível de dificuldade da receita:",
    min_value=1,
    max_value=5,
    value=3
)

# 4. Restrição alimentar
possui_restricao = st.checkbox("Possui restrição alimentar?")
restricao = ""
if possui_restricao:
    restricao = st.text_input(
        "Informe a restrição alimentar (ex: sem glúten, vegetariana, sem lactose):")

# 5. Geração da receita
if st.button("Sugerir Receita"):
    restricao_str = f"Considere a seguinte restrição alimentar: {restricao}." if possui_restricao and restricao else ""

    # Monta o prompt
    prompt = (
        f"Sugira uma receita {tipo_culinaria.lower()} com nível de dificuldade {nivel_dificuldade} "
        f"(sendo 1 muito fácil e 5 desafiador). Deve usar principalmente os seguintes ingredientes: '{ingredientes}'. "
        f"{restricao_str} Apresente o nome da receita, uma lista de ingredientes adicionais se necessário, "
        f"e um breve passo a passo."
    )

    with st.spinner("🔍 Gerando sugestão de receita com IA..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = model.generate_content(prompt)
            st.markdown("### 🍳 Receita Sugerida:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Ocorreu um erro ao chamar a IA: {e}")
