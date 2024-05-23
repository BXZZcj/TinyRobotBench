import chainlit as cl
from chainlit.input_widget import Select, Slider
from reasoner.chainlit_reasoner import ChainlitReasoner


chainlit_reasoner = ChainlitReasoner()


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Base Large Language Model",
                values=["Vicuna-13B-v1.5-GPTQ"],
                initial_index=0,
            ),
            Select(
                id="Context",
                label="Context Mode",
                values=["No Context", "Within the Historical Context"],
                initial_index=0,
            ),
            Select(
                id="Mode",
                label="Knowledge Mode",
                values=["Free","KG-based"],
                initial_index=0,
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0,
                min=0,
                max=1,
                step=0.1,
            )
        ]
    ).send()
    await setup_agent(settings)
    cl.user_session.set("response_history", [])


@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("settings", settings)


@cl.on_message
async def main(message: str):
    settings = cl.user_session.get("settings")
    context_mode, knowledge_mode, temperature = settings['Context'], settings['Mode'], settings['Temperature']
    response_history = cl.user_session.get("response_history") if settings['Context'] == "Within the Historical Context" else []
    
    if knowledge_mode == 'Free':
        _, response_history = await chainlit_reasoner.RAG_answer(message, response_history, temperature=temperature)
    elif knowledge_mode == 'KG-based':
        _, response_history = await chainlit_reasoner.reason_answer(message, response_history, knowledge_top_k=1, temperature=temperature)
    
    if settings['Context'] == "Within the Historical Context":
        cl.user_session.set("response_history", response_history)
