# main.py
import os
import streamlit as st
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langchain.callbacks.tracers.run_collector import RunCollectorCallbackHandler
from langchain.memory import ConversationBufferMemory, StreamlitChatMessageHistory
from langchain.schema.runnable import RunnableConfig
from langsmith import Client
from streamlit_feedback import streamlit_feedback
from claude_chain import ClaudeChain  # Import the new claude_chain module
import json

# Define a helper function to get secrets
def get_secret(key):
    try:
        return st.secrets[key]
    except AttributeError:
        return os.getenv(key)

# Set environment variables
os.environ["OPENAI_API_KEY"] = get_secret("api_keys")["OPENAI_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Streamlit Demo"
os.environ["LANGCHAIN_API_KEY"] = get_secret("api_keys")["LANGSMITH_API_KEY"]
os.environ['AWS_ACCESS_KEY_ID'] = get_secret("api_keys")["AWS_ACCESS_KEY_ID"]
os.environ['AWS_SECRET_ACCESS_KEY'] = get_secret("api_keys")["AWS_SECRET_ACCESS_KEY"]

from essential_chain import initialize_chain
from vanilla_chain import get_llm_chain

st.set_page_config(
    page_title="Chat with nav.no via LangChain, Collect user feedback via Trubrics and LangSmith!",
    page_icon="💙💛",
)

use_secret_key = st.sidebar.toggle(label="Demo LangSmith API key", value=True)

if use_secret_key:
    os.environ["LANGCHAIN_PROJECT"] = "Streamlit Demo"
else:
    project_name = st.sidebar.text_input(
        "Name your LangSmith Project:", value="Streamlit Demo"
    )
    os.environ["LANGCHAIN_PROJECT"] = project_name

if use_secret_key:
    langchain_api_key = st.secrets["api_keys"]["LANGSMITH_API_KEY"]
else:
    langchain_api_key = st.sidebar.text_input(
        "👇 Add your LangSmith Key",
        value="",
        placeholder="Your_LangSmith_Key_Here",
        label_visibility="collapsed",
    )
if langchain_api_key is not None:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

if "last_run" not in st.session_state:
    st.session_state["last_run"] = "some_initial_value"

langchain_endpoint = "https://api.smith.langchain.com"

col1, col2, col3 = st.columns([0.6, 3, 1])

with col2:
    st.image("images/ukraineflag.png", width=460)

st.write("")
st.markdown("**💙💛 Chat with the NAV docs via [:blue[LangChain]](https://www.nav.com/)** 🪄 **Collect user feedback via [:orange[Trubrics]](https://github.com/trubrics/streamlit-feedback) and [:green[LangSmith]](https://www.langchain.com/langsmith)**")
st.markdown("___")
st.write("👇  Ask a question about the [NAV](https://nav.no/) or 💡 App template was built using this tutorial [blog post](https://blog.streamlit.io/how-in-app-feedback-can-increase-your-chatbots-performance/)")

if not langchain_api_key or langchain_api_key.strip() == "Your_LangSmith_Key_Here":
    st.info("⚠️ Add your [LangSmith API key](https://python.langchain.com/docs/guides/langsmith/walkthrough) to continue, or switch to the Demo key")
else:
    client = Client(api_url=langchain_endpoint, api_key=langchain_api_key)

if "trace_link" not in st.session_state:
    st.session_state.trace_link = None
if "run_id" not in st.session_state:
    st.session_state.run_id = None

_DEFAULT_SYSTEM_PROMPT = ""
system_prompt = _DEFAULT_SYSTEM_PROMPT = ""
system_prompt = system_prompt.strip().replace("{", "{{").replace("}", "}}")

chain_type = st.sidebar.radio(
    "Choose your LLM:",
    ("Classic `GPT 3.5` LLM", "RAG LLM for nav.no", "Claude Sonnet"),
    index=1,
)

memory = ConversationBufferMemory(
    chat_memory=StreamlitChatMessageHistory(key="langchain_messages"),
    return_messages=True,
    memory_key="chat_history",
)

if chain_type == "Classic `GPT 3.5` LLM":
    chain = get_llm_chain(system_prompt, memory)
elif chain_type == "RAG LLM for nav.no":
    chain = initialize_chain(system_prompt, _memory=memory)
elif chain_type == "Claude Sonnet":
    claude_chain = ClaudeChain(memory)

if st.sidebar.button("Clear message history"):
    print("Clearing message history")
    memory.clear()
    if chain_type == "Claude Sonnet":
        claude_chain.clear_memory()
    st.session_state.trace_link = None
    st.session_state.run_id = None

def _get_openai_type(msg):
    if msg.type == "human":
        return "user"
    if msg.type == "ai":
        return "assistant"
    if msg.type == "chat":
        return msg.role
    return msg.type

for msg in st.session_state.langchain_messages:
    streamlit_type = _get_openai_type(msg)
    avatar = "🦜" if streamlit_type == "assistant" else None
    with st.chat_message(streamlit_type, avatar=avatar):
        st.markdown(msg.content)

run_collector = RunCollectorCallbackHandler()
runnable_config = RunnableConfig(
    callbacks=[run_collector],
    tags=["Streamlit Chat"],
)
if st.session_state.trace_link:
    st.sidebar.markdown(
        f'<a href="{st.session_state.trace_link}" target="_blank"><button>Latest Trace: 🛠️</button></a>',
        unsafe_allow_html=True,
    )

def _reset_feedback():
    st.session_state.feedback_update = None
    st.session_state.feedback = None

MAX_CHAR_LIMIT = 500  # Adjust this value as needed

if prompt := st.chat_input(placeholder="Ask a question about nav.no!"):

    if len(prompt) > MAX_CHAR_LIMIT:
        st.warning(f"⚠️ Your input is too long! Please limit your input to {MAX_CHAR_LIMIT} characters.")
        prompt = None  # Reset the prompt so it doesn't get processed further
    else:
        st.chat_message("user").write(prompt)
        _reset_feedback()
        with st.chat_message("assistant", avatar="🦜"):
            message_placeholder = st.empty()
            full_response = ""

            input_structure = {"input": prompt}

            if chain_type == "RAG LLM for nav.no":
                input_structure = {
                    "question": prompt,
                    "chat_history": [
                        (msg.type, msg.content)
                        for msg in st.session_state.langchain_messages
                    ],
                }

            if chain_type == "Classic `GPT 3.5` LLM":
                message_placeholder.markdown("thinking...")
                full_response = chain.invoke(input_structure, config=runnable_config)[
                    "text"
                ]

            elif chain_type == "Claude Sonnet":
                try:
                    full_response = claude_chain.call_api(prompt)
                except ValueError as e:
                    full_response = f"Error calling Claude API: {e}"

            else:
                for chunk in chain.stream(input_structure, config=runnable_config):
                    full_response += chunk["answer"]
                    message_placeholder.markdown(full_response + "▌")
                memory.save_context({"input": prompt}, {"output": full_response})

            message_placeholder.markdown(full_response)

            run = run_collector.traced_runs[0] if run_collector.traced_runs else None
            if run:
                run_collector.traced_runs = []
                st.session_state.run_id = run.id
                wait_for_all_tracers()
                url = client.read_run(run.id).url
                st.session_state.trace_link = url

has_chat_messages = len(st.session_state.get("langchain_messages", [])) > 0

if has_chat_messages:
    feedback_option = (
        "faces" if st.toggle(label="`Thumbs` ⇄ `Faces`", value=False) else "thumbs"
    )
else:
    pass

if st.session_state.get("run_id"):
    feedback = streamlit_feedback(
        feedback_type=feedback_option,
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{st.session_state.run_id}",
    )

    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }

    scores = score_mappings[feedback_option]

    if feedback:
        score = scores.get(feedback["score"])

        if score is not None:
            feedback_type_str = f"{feedback_option} {feedback['score']}"
            feedback_record = client.create_feedback(
                st.session_state.run_id,
                feedback_type_str,
                score=score,
                comment=feedback.get("text"),
            )
            st.session_state.feedback = {
                "feedback_id": str(feedback_record.id),
                "score": score,
            }
        else:
            st.warning("Invalid feedback score.")
