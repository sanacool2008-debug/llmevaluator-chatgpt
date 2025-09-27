import streamlit as st
import requests
import time

run_id = str(int(time.time()))

# ---------------- Config ----------------
LLM_ENDPOINT = "http://localhost:8000/responses"
EVALUATE_ENDPOINT = "http://localhost:8000/evaluate"

DEFAULT_MODELS = {
    "openrouter_deepseek": "deepseek/deepseek-chat-v3.1:free",
    "openrouter_nvidia": "nvidia/nemotron-nano-9b-v2:free",
    "openrouter_openai": "openai/gpt-oss-20b:free",
    "local": "gemma:2b"
}

LLM_PROMPT_TEMPLATE = "prompt_config_llm_test"
EVAL_PROMPT_TEMPLATE = "prompt_config_llm_evaluation"
EVALUATOR_MODEL_ID = "nvidia/nemotron-nano-9b-v2:free"

# ---------------- UI ----------------
st.set_page_config(page_title="Model Evaluator Chatbot", layout="wide")

# Center align the title
st.markdown(
    "<h1 style='text-align: center;'>🧠 Chat Model Evaluator</h1>",
    unsafe_allow_html=True
)
# Center align the caption using st.markdown with CSS
st.markdown(
    "<p style='text-align: center;'>Ask a question, compare 4 LLM responses, and evaluate the winner.</p>",
    unsafe_allow_html=True
)


# ---------------- Session State ----------------
if "last_responses" not in st.session_state:
    st.session_state.last_responses = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None
if "evaluation" not in st.session_state:
    st.session_state.evaluation = None
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ---------------- Input ----------------
with st.form("query_form"):
    question = st.text_area("Enter your question:", height=120)
    submitted = st.form_submit_button("Send")

if submitted and question.strip():
    # Clear previous data and set pending question
    st.session_state.evaluation = None
    st.session_state.last_responses = None
    st.session_state.last_prompt = None
    st.session_state.pending_question = question
    st.rerun()

# Check if we have a pending question to process
if st.session_state.pending_question and st.session_state.last_responses is None:
    question = st.session_state.pending_question
    payload = {
        "models": DEFAULT_MODELS,
        "prompt_template_name": LLM_PROMPT_TEMPLATE,
        "question": question
    }

    with st.spinner("Fetching responses from 4 LLMs..."):
        try:
            res = requests.post(LLM_ENDPOINT, json=payload, timeout=300)
            res.raise_for_status()
            data = res.json()
            st.session_state.last_responses = data.get("llm_responses")
            st.session_state.last_prompt = data.get("prompt")
            st.session_state.pending_question = None  # Clear the pending question
            st.success("Responses received.")
        except requests.Timeout:
            st.error("⏳ The request timed out. Try again or increase timeout.")
            st.session_state.pending_question = None
        except Exception as e:
            st.error(f"⚠️ Failed to fetch responses: {e}")
            st.session_state.pending_question = None

# ---------------- Display Responses ----------------
if st.session_state.last_responses:
    st.markdown("### 📜 LLM Responses")
    cols = st.columns(4)

    for i, resp in enumerate(st.session_state.last_responses):
        with cols[i]:
            st.markdown(f"#### 🤖 {resp['llm']}")
            container = st.empty()

            st.text_area(
                "Response",
                resp["response"],
                height=250,
                key=f"response_box_{i}_{run_id}",
                label_visibility="collapsed"
            )

            st.button(
                "📋 Copy",
                key=f"copy{i}_{run_id}",
                on_click=lambda r=resp: st.session_state.update({"copied": r["response"]})
            )

# ---------------- Evaluation ----------------
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.session_state.last_responses and st.button("⚖️ Evaluate Responses", key="evaluate_button"):
    eval_payload = {
        "model": EVALUATOR_MODEL_ID,
        "prompt_template_name": EVAL_PROMPT_TEMPLATE,
        "llm_responses_model": {
            "prompt": st.session_state.last_prompt,
            "llm_responses": st.session_state.last_responses
        }
    }
    with st.spinner("Evaluating responses..."):
        try:
            eval_res = requests.post(EVALUATE_ENDPOINT, json=eval_payload, timeout=90)
            eval_res.raise_for_status()
            st.session_state.evaluation = eval_res.json()
        except requests.Timeout:
            st.error("⏳ Evaluation request timed out. Try again.")
        except Exception as e:
            st.error(f"⚠️ Evaluation failed: {e}")
st.markdown("</div>", unsafe_allow_html=True)


if st.session_state.evaluation:
    eval_data = st.session_state.evaluation
    st.markdown("---")
    st.subheader("🧾 Evaluation Results")

    results = eval_data.get("results", [])
    if results:
        st.dataframe(
            results,
            column_config={
                "llm": st.column_config.Column(
                    "LLM Name"
                ),
                "score": st.column_config.NumberColumn(
                    "Score",
                    format="%d"
                ),
                "reason": st.column_config.TextColumn(
                    "Reason for the Score"
                ),
            },
            use_container_width=True
        )

    winner = eval_data.get("winner", "Unknown")
    placeholder = st.empty()
    for dots in range(3):
        placeholder.markdown(f"### 🎯 Revealing winner{'.' * (dots+1)}")
        time.sleep(0.6)
    placeholder.success(f"🏆 Winner: **{winner}**")
    st.balloons()