import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

audio_path = "https://docs.google.com/uc?export=open&id=16QSvoLWNxeqco_Wb2JvzaReSAw5ow6Cl"
img_path = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-IXnKLBEnPDb34iq3tABlqJvw/user-BeV7GjPCB9dPvbjN14wFUhyb/img-rDFUgojrmsWGAEU2UqEpjurl.png?st=2023-06-28T18%3A01%3A21Z&se=2023-06-28T20%3A01%3A21Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-06-28T00%3A12%3A26Z&ske=2023-06-29T00%3A12%3A26Z&sks=b&skv=2021-08-06&sig=jjSplR/nXVOGsiCpBI6jinpntpXx6jkgEr%2BGtRJnQXw%3D"
youtube_embed = '''
<iframe width="400" height="215" src="https://www.youtube.com/embed/LMQ5Gauy17k" title="YouTube video player" frameborder="0" allow="accelerometer; encrypted-media;"></iframe>
'''

markdown = """
### HTML in markdown is ~quite~ **unsafe**
<blockquote>
  However, if you are in a trusted environment (you trust the markdown). You can use allow_html props to enable support for html.
</blockquote>

* Lists
* [ ] todo
* [x] done

Math:

Lift($L$) can be determined by Lift Coefficient ($C_L$) like the following
equation.

$$
L = \\frac{1}{2} \\rho v^2 S C_L
$$

~~~py
import streamlit as st

st.write("Python code block")
~~~

~~~js
console.log("Here is some JavaScript code")
~~~

"""

table_markdown = '''
A Table:

| Feature     | Support              |
| ----------: | :------------------- |
| CommonMark  | 100%                 |
| GFM         | 100% w/ `remark-gfm` |
'''

st.session_state.setdefault(
    'past', 
    ['plan text with line break',
     'play the song "Dancing Vegetables"', 
     'show me image of cat', 
     'and video of it',
     'show me some markdown sample',
     'table in markdown']
)
st.session_state.setdefault(
    'generated', 
    [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
     {'type': 'normal', 'data': f'<audio controls src="{audio_path}"></audio>'}, 
     {'type': 'normal', 'data': f'<img width="256" height="256" src="{img_path}"/>'}, 
     {'type': 'normal', 'data': f'{youtube_embed}'},
     {'type': 'normal', 'data': f'{markdown}'},
     {'type': 'table', 'data': f'{table_markdown}'}]
)

st.title("Chat placeholder")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(
            st.session_state['generated'][i]['data'], 
            key=f"{i}", 
            allow_html=True,
            is_table=True if st.session_state['generated'][i]['type']=='table' else False
        )

    st.button("Clear message", on_click=on_btn_click)

with st.container():
    st.text_input("User Input:", on_change=on_input_change, key="user_input")