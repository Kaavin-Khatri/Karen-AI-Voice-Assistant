import streamlit as st
import karen
import time
import threading
# importlib.reload(karen) # Removed to preserve state (TTS process handle)
pass

# Page config
st.set_page_config(page_title="Karen AI", page_icon="🤖", layout="wide")

# Custom CSS for glassmorphism and premium look
# Custom CSS for glassmorphism and premium look
st.markdown("""
<style>
    /* Import Sci-Fi Font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;600&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .stButton {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
    }

    /* Gradient Background - Dark Tech */
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        background-attachment: fixed;
        color: #e0e0e0;
    }

    /* GRID OVERLAY (Simulating HUD) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    /* FORCE SIDEBAR VISIBILITY */
    [data-testid="stSidebarCollapsedControl"] {
        color: #00d4ff !important;
        background-color: rgba(0, 20, 40, 0.8) !important;
        border-radius: 5px;
        border: 1px solid #00d4ff;
        z-index: 999999 !important;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
    ::-webkit-scrollbar-thumb { background: #00d4ff; border-radius: 3px; }

    /* REACTOR CORE ANIMATION (CSS Only) */
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff inset; }
        50% { box-shadow: 0 0 25px #00d4ff, 0 0 50px #00d4ff inset; }
        100% { box-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff inset; }
    }

    .reactor-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }

    .reactor {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 2px solid rgba(0, 212, 255, 0.3);
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        animation: pulse 2s infinite ease-in-out;
        background: rgba(0,0,0,0.2);
    }

    .reactor-inner {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        border: 2px dashed #00d4ff;
        animation: rotate 10s linear infinite;
    }
    
    .reactor-core {
        position: absolute;
        width: 40px;
        height: 40px;
        background: radial-gradient(circle, #fff, #00d4ff);
        border-radius: 50%;
        box-shadow: 0 0 20px #00d4ff;
    }

    /* CHAT BUBBLES - GLASSMORPHISM */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding-bottom: 120px;
    }

    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        max-width: 80%;
        position: relative;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 100, 200, 0.2));
        margin-left: auto;
        border-bottom-right-radius: 2px;
        flex-direction: row-reverse;
        border-left: 3px solid #00d4ff;
    }
    
    .chat-message.bot {
        background: rgba(255, 255, 255, 0.05);
        margin-right: auto;
        border-bottom-left-radius: 2px;
        border-right: 3px solid rgba(255, 255, 255, 0.2);
    }

    .chat-message .avatar {
        width: 40px; height: 40px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem;
        background: rgba(0,0,0,0.3);
        margin: 0 15px;
        border: 1px solid rgba(0, 212, 255, 0.3);
        flex-shrink: 0; /* Prevent squashing */
    }
    
    .chat-message .message {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        line-height: 1.5;
    }

    /* INPUT AREA - FLOATING CAPSULE */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 700px !important;
        z-index: 1000;
    }
    
    .stChatInputContainer {
        border-radius: 50px !important;
        background: rgba(10, 15, 30, 0.95) !important; /* Non-transparent */
        backdrop-filter: blur(20px);
        border: 1px solid #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .stChatInputContainer textarea {
        color: #00d4ff !important;
        caret-color: #00d4ff !important;
    }

    /* BUTTONS - NEON STYLE */
    .stButton > button {
        border-radius: 5px !important;
        border: 1px solid #00d4ff !important;
        background: #0f3460 !important; /* Solid background */
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        opacity: 1 !important;
        z-index: 10000; /* Ensure on top */
    }
    
    .stButton > button:hover {
        background: #00d4ff !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00d4ff;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.95);
        border-right: 1px solid rgba(0, 212, 255, 0.1);
    }

    /* HIDE DEFAULT STREAMLIT MENU */
    #MainMenu, footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting if empty
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am Karen, your virtual assistant. How can I help you?"})

# Monkey Patch Karen's speak function to update UI
# We need to be careful not to double-patch because Streamlit caches modules
if not hasattr(karen, 'original_speak_ref'):
    karen.original_speak_ref = karen.speak

def patched_speak(audio):
    # Only append if we have a session to append to
    if "messages" in st.session_state:
        st.session_state.messages.append({"role": "assistant", "content": audio})
    
    # Run the original speak to get audio
    try:
        # We call the REFERENCE stored in the module, which is the clean, original function
        karen.original_speak_ref(audio)
    except Exception as e:
        print(f"Audio failed in patched speak: {e}")

# Apply patch
karen.speak = patched_speak

# Sidebar
with st.sidebar:
    # Reactor Core Animation
    st.markdown("""
        <div class="reactor-container">
            <div class="reactor">
                <div class="reactor-inner"></div>
                <div class="reactor-core"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("KAREN")
    st.markdown("---")
    st.write("System Status: **ONLINE**")
    
    # Auto-configure from file
    karen.configure_genai()
    
    if karen.genai_client:
        st.success("Brain: Connected")
    else:
        st.warning("Brain: Disconnected (Check gemini_api_key.txt)")

    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.title("Karen Voice Assistant")

# Display Camera if Open
camera_placeholder = st.empty()

# Display Chat History
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        role_class = "user" if message["role"] == "user" else "bot"
        avatar = "👤" if message["role"] == "user" else "🤖"
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <div class="avatar">{avatar}</div>
            <div class="message">{message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Input Area
# Sticky Input Area logic
# Sticky Input Area logic
# Sticky Input Area logic
# Sticky Input Area logic
st.markdown("""
<style>
    /* 
       LAYOUT STRATEGY:
       1. Chat Input: Fixed at bottom ~100px.
       2. Controls: Fixed at bottom ~20px.
    */

    /* Chat Input Container */
    .stChatInput {
        position: fixed !important;
        bottom: 120px !important; /* Moved up for more space */
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important; 
        max-width: 800px !important;
        z-index: 10000001 !important; /* Above everything */
        background: transparent !important;
        pointer-events: auto !important; /* FORCE CLICKS */
    }
    
    /* The actual input box */
    .stChatInputContainer {
        border-radius: 15px !important;
        background-color: #1e1e2f !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        pointer-events: auto !important; /* FORCE CLICKS */
    }
    
    /* Input text color */
    .stChatInputContainer textarea {
        color: white !important;
        caret-color: white !important; /* Cursor color */
    }

    /* 2. Control Buttons Container */
    div[data-testid="stHorizontalBlock"]:last-of-type {
        position: fixed !important;
        bottom: 30px !important; /* Slightly higher base */
        left: 50% !important;
        transform: translateX(-50%) !important;
        right: auto !important;
        width: 100% !important;
        max-width: 700px; /* Wider container for buttons */
        z-index: 999999;
        background-color: transparent;
        pointer-events: none; /* Allow clicks to pass through empty space */
        display: flex;
        justify-content: center;
    }

    /* Target the column holding the buttons */
    div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="column"]:nth-of-type(2) {
        pointer-events: auto; /* Enable clicks on buttons */
        background: transparent;
        padding: 0;
        border: none;
        box-shadow: none;
        
        display: flex;
        flex-direction: row;
        gap: 20px;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    
    /* Hide the empty first column */
    div[data-testid="stHorizontalBlock"]:last-of-type > div[data-testid="column"]:nth-of-type(1) {
        display: none;
    }

    /* 3. Big Buttons */
    /* FORCE INTERACTIVITY */
    .stButton {
        pointer-events: auto !important;
        z-index: 1000000 !important; /* Ensure they are top-most reachable */
    }

    .stButton > button {
        pointer-events: auto !important;
        border-radius: 30px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0 2rem !important; /* Reduced vertical padding */
        height: 55px !important; /* Fixed height for uniformity */
        min-width: 160px !important; /* Slightly wider */
        white-space: nowrap !important; /* PREVENT WRAPPING */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        transition: transform 0.2s, filter 0.2s;
        cursor: pointer !important;
    }
    
    /* Primary (Stop) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff4b4b, #d90429);
        box-shadow: 0 4px 12px rgba(217, 4, 41, 0.4);
    }
    
    /* Secondary (Alert) */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #3a86ff, #2563eb);
        color: white !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        filter: brightness(1.1);
    }

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.chat_input("Type your command here...")

with col2:
    # Use nested columns to put specific buttons side-by-side cleanly
    # Centering trick using columns: [empty, button, button, button, empty]
    c_pad1, c_btn1, c_btn2, c_btn3, c_pad2 = st.columns([0.5, 2, 2, 2, 0.5])
    
    listen_button = False
    
    with c_btn1:
        if st.button("🎤 Speak", type="secondary", use_container_width=True):
            listen_button = True
    
    with c_btn2:
        # Live Chat Toggle
        if "live_chat_active" not in st.session_state:
            st.session_state.live_chat_active = False
            
        if st.session_state.live_chat_active:
            if st.button("💬 Stop Live", type="primary", use_container_width=True):
                st.session_state.live_chat_active = False
                st.rerun()
        else:
            if st.button("💬 Live Chat", type="secondary", use_container_width=True):
                st.session_state.live_chat_active = True
                st.rerun()

    with c_btn3:
        if st.button("🛑 Stop All", type="primary", use_container_width=True):
            karen.stop_speaking()
            st.session_state.live_chat_active = False
            st.rerun()

# Logic Processing
processed = False
query = None

# 1. Standard Speak Button
if listen_button:
    with st.spinner("Listening..."):
        try:
            query = karen.takeCommand()
            if query and query.lower() != "none":
                st.session_state.messages.append({"role": "user", "content": query})
                processed = True
            else:
                st.warning("Did not hear anything.")
        except Exception as e:
            st.error(f"Error listening: {e}")

# 2. Live Chat Logic (Continuous Loop)
if st.session_state.get("live_chat_active", False):
    # Wait for any previous speech to finish before listening
    # This prevents Karen from hearing herself
    karen.wait_until_done()

    with st.spinner("Live Chat Active... Listening..."):
        # Add a small delay to prevent rapid-fire loops if listening fails
        time.sleep(0.5) 
        try:
            query = karen.takeCommand()
            if query and query.lower() != "none":
                # Check for stop command
                if "stop live chat" in query.lower() or "stop listening" in query.lower():
                    st.session_state.live_chat_active = False
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.session_state.messages.append({"role": "assistant", "content": "Stopping live chat."})
                    karen.speak("Stopping live chat.")
                    st.rerun()

                st.session_state.messages.append({"role": "user", "content": query})
                processed = True
            # If nothing heard, we just loop back (rerun)
            else:
                st.rerun()
        except Exception as e:
            # If error, maybe stop live chat to prevent infinite error loop
            # st.session_state.live_chat_active = False
            st.error(f"Live chat error: {e}")
            time.sleep(2)
            st.rerun()

if user_input:
    query = user_input
    st.session_state.messages.append({"role": "user", "content": query})
    processed = True

if processed and query:
    with st.spinner("Processing..."):
        # Process in Karen
        should_continue = karen.process_query(query)
        st.rerun()

# Camera Loop Handler - THIS MUST BE AT THE END OR IN A LOOP
# Camera Loop Handler
# We removed the st.rerun loop as it causes the whole app to glitch/refresh.
# The camera now opens in a native OpenCV window which is smoother.
if karen.camera_open:
    st.info("Camera is running in a separate window. Say 'Close Camera' to stop it.")

