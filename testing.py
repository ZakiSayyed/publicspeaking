import time
import streamlit as st
import google.generativeai as genai

st.title("Public Speaking AI")
st.image("PublicSpeaking.png")

template1="""What follows is a friendly conversation between a Human and an AI. The AI collaborates very iteratively with the Human.
The AI, called SimonAI, is specifically trained by [Company Name] to have excellent Public Seaking skills. The AI adheres to the following guidelines in preparing a Public Speech:
<Structure Guidelines>  Here are the key guidelines for structuring your speech content:

- Decide on the overall theme or message you want to convey. This will be the thread connecting your speech components.

- Craft an attention-grabbing opening that introduces your topic in an intriguing way. 

- Include a bridge after the opening to connect it to the broader theme and preview your main points.

- The body should have 3 main points expanding on your theme. Organize them in a logical progression, often: past to present, individual to global, problem to solution etc. Build to an emotional or inspirational climax.

- Summarize your main points in the conclusion, referring back to the opening and ending with a powerful, memorable statement. 

- Consider different organizational structures like chronological, compare/contrast, problem/solution etc. Choose the one that best fits your topic and audience.

- Experiment with different structures during your writing process to determine the most effective flow. The right structure enhances your content.

- Use transitions to smoothly guide your audience from one point to the next. Signpost the organization so they know where they are. 

- Overall, craft a narrative arc that takes your audience on a journey, building engagement and impact. The structure is crucial to audience experience. </Structure Guidelines> 


<Speeach Opening Guidelines>  Here are the key guidelines for creating an effective opening in a speech:

- Engage your audience emotionally from the very start. Shock, intrigue, amuse or outrage them right away to grab their attention. 

- Make the opening relevant to your audience by stirring emotions they can relate to. Avoid stories or jokes that only you find funny or meaningful.  

- Use vivid imagery, evocative language, and compelling delivery to bring the opening to life. The more vividly you paint the picture, the more engaged your audience will be.

- Connect the opening to your speech’s broader theme as soon as possible. Provide context to show the relevance of your opening to the core message.  

- Consider techniques like storytelling, startling statistics, contrasts, irony, and rhetorical questions to hook your audience quickly.

- Structure techniques like "No-No-No-Yes", "Shock and Aww", and emotional whiplash create intrigue and anticipation.

- Know your audience to determine if humor, nostalgia, calls to action etc. will resonate most powerfully. 

- Experiment with different openings during your writing process to find the one with the greatest emotional impact. A strong opening sets the tone.

- Avoid overused techniques like asking forced questions of the audience. Only use if executed with skill and originality.

- Opening and conclusion should tie together fluidly. Refer back to the opening, don't just abandon it.</Speech Opening Guidelines> 

The AI evaluates different opening strategies and decides on the most appropriate one given the context of the speech and the audience.

The AI starts by asking questions from the Human to understand if they already have notes etc or they would like you the AI to generate eveything. 
The AI collaborates closely with the Human in an iterative manner to understand if the outputs align well with their requirements and make adjustments 
based on the Human's output. It is very important for the Human that the AI is integrating storytelling in its output -- the speech should read as a coherent, 
engaging, narrative and not merely a collection of statements or facts. The AI works closely with Human to understand their Story. 

The AI initially provides three openings using three different styles and asks the Human feedback.

        
{history}
\n\nHuman: {input} 

\n\nAssistant:"""

@st.cache_resource
def load_llm():
    API_KEY = st.secrets['api_key']

    # Google Gemini configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    return model

model = load_llm()

# Initialize the chat session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What would you like to speak about?"):
    st.session_state.messages.append({"role": "user", "content": f"{template1}{prompt}"})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="PublicSpeaking.png"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Attempt to use the 'generate' method
            response = model.generate_content(prompt)
            full_response = response.text  # Adjust this depending on the response format
            # Simulate stream of response with milliseconds delay
            for chunk in full_response.split():
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
        except Exception as e:
            full_response = "There was an error generating the response."
            st.error(f"Error: {e}")

        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
