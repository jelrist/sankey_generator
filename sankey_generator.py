import sys
import base64
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

#-------------------------------------------#
# set local image as background in streamlit
#import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file) 
    page_bg_img = '''
    <style>
.stApp {
  background-image: url("data:image/png;base64,%s");
  background-size: cover;
}
</style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background1.png')
#--------------------------------------------#

#----TITLE----#
st.markdown('<h1 style="text-align:center;">Sankey diagram generator</h1>', unsafe_allow_html=True)
#-------------#

#----SIDEBAR MENU-----#

expander_bar5 = st.sidebar.expander("PLEASE READ FIRST BEFORE PROCEEDING")
expander_bar2 = st.sidebar.expander("What are Sankey diagrams?")
expander_bar3 = st.sidebar.expander("How to format your data?")
expander_bar4 = st.sidebar.expander("How to change view and save your diagram?")
expander_bar1 = st.sidebar.expander("About")
expander_bar1.markdown("""<p>This project is brought to you by a sankey enthusiast who believes that one sankey is worth a thousand pie charts.</p>
<p>Coded by Jelena Risti&#263;, 2022 <br> <a href="jelenaristic.info" style="text-decoration:none;">jelenaristic.info</a></p>
""", unsafe_allow_html=True)
expander_bar2.markdown("""<p>A Sankey diagram is a graphical representation of flows. Several entities (nodes) are represented by rectangles and / or text. Their links/relationships are represented as ribbons that have a width proportional to the importance of the flow.</p>
<p>Sankey diagrams are named after Irish Captain Matthew Henry Phineas Riall Sankey, who used this type of diagram in 1898 in a classic figure showing the energy efficiency of a steam engine. The original charts in black and white displayed just one type of flow (e.g. steam); using colors for different types of flows lets the diagram express additional variables.</p>
<br><a href="https://upload.wikimedia.org/wikipedia/commons/1/10/JIE_Sankey_V5_Fig1.png" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/1/10/JIE_Sankey_V5_Fig1.png" style="width:280px; height:"auto";"></a><a href="https://en.wikipedia.org/wiki/Sankey_diagram" target="_blank" style="text-decoration:none;">Source: Wikipedia</a></p>
<p>For a successful sankey, opt for rgba colours and avoid overcluttering by dismissing weak or very minor connections.</p>""", unsafe_allow_html=True)
expander_bar3.markdown("""<ul><li>Split your data into 2 files in <b>CSV format</b>;</li>
    <li>One for all the <b>elements</b>. This will be your <b>NODE file</b> with following header (case sensitive): <b>ID, label, color</b></li>
    <li>One for all the <b>relationships</b> between the elements (nodes). This will be your <b>LINKS file</b> with following header (case sensitive): <b>source, target, value, link color</b></li>
    <li>each row in your NODE file with contain a unique ID number (ID), node name (label), node colour (color):
    <ul><li>e.g. if your data is about characters in the book <em>Alice's Adventures in Wonderland</em>, the first row will be: "0, Alice, #dfdfdf", the second will be "1, White Rabbit, #ffffff", and so on.</li></ul></li>
    <li>each row of your LINKS file will contain the relationships between the nodes:
    <ul><li>source: the source node ID number;</li>
    <li>target: the target node ID number;</li>
    <li>value: the value of the link (i.e. an integer or a float);</li>
    <li>link color: the colour in which the link between nodes will be displayed.</li>
    <ul><li>e.g. if the diagram is to represent how many times characters interact with each other over the whole book and if Alice interacted with White Rabbit 36 times, we can fill in a links csv row as such: "0, 1, 36, #fa6cca".</li></ul></ul>
    <li><b>A note about choosing colours:</b> Sometimes too many relations between nodes can make the sankey diagram difficult to read. Opt for rgba and play with the alpha value. The transparency will allow the overlapping links to show better and help with readability.""", unsafe_allow_html=True)
expander_bar4.markdown("""There is a toolbar in the top right corner. Use the select tools (rectangle and lasso tools) to change view and aggregate nodes. Click on the camera icon to download your generated sankey diagram in png format. Click on the house icon to reset view.""", unsafe_allow_html=True)
expander_bar5.markdown("""This app has been created out of pure love of sankeys and python. <br><strong>The app cannot guarantee the safety of your data. Therefore, if your files contain sensitive data, please avoid using this app.</strong> <br>Many thanks for your understanding.""", unsafe_allow_html=True)
#-----------------------------------------------------#


#-----INPUT FORM ORGANISED IN 2 COLUMNS-----#

col1, col2 = st.columns(2)

with col1:
  st.subheader("Nodes dataframe")
  df_nodes = st.file_uploader("Upload your nodes file in csv format: ", "csv")
  st.subheader("Links dataframe")
  df_links = st.file_uploader("Upload your links file in csv format: ", "csv")
  st.subheader("Orientation")
  orientation = st.radio("Choose 'h' for horizontal or 'v' for vertical display: ", ('h', 'v'))
  st.subheader("Link values (decimals and units)")
  valueformat = st.radio("For your values display, opt '.2f' for 2 decimals after floating point, '.1f' for one, or '.0f' for none: ", (".2f", ".1f",".0f"))
  valuesuffix = st.text_input("Input your value unit here (%, $, kg, film/s, chapter/s, etc.):")
  
with col2:
  st.subheader("Diagram title")
  title_diagram = st.text_input("Type in your sankey diagram title: ")
  st.subheader("Diagram height and width ")
  diagram_height = st.text_input("Enter height in px: ")
  diagram_width = st.text_input("Enter width in px: ")
  st.subheader("Diagram background color and font")
  diagram_bg_color = st.color_picker("Pick a background colour: ")
  font_color = st.color_picker("Pick a font colour: ")
  font_size = st.select_slider("Font size:", options=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
#----------------------------------------------------#
sys.tracebacklimit=0

#-----DISPLAY DATAFRAMES-----#
try:
  df_nodes = pd.read_csv(df_nodes)
  df_links = pd.read_csv(df_links)
  st.subheader("Display nodes: ")
  st.write(df_nodes)
  st.subheader("Display links: ")
  st.write(df_links)
except:
  st.markdown("""<h3 style="color:red;">First, please upload your files and</h3>""", unsafe_allow_html=True)

#-----------------------------#

#----PLOT SANKEY------#
try:
  data_trace = dict(
    type='sankey',
    domain = dict(
      x =  [0,1],
      y =  [0,1]
    ),
    orientation = orientation,
    valueformat = valueformat,
    valuesuffix = valuesuffix,
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(
        color = "black",
        width = 0
      ),
      label =  df_nodes['label'].dropna(axis=0, how='any'),
      color = df_nodes['color']
    ),
    link = dict(
      source = df_links['source'].dropna(axis=0, how='any'),
      target = df_links['target'].dropna(axis=0, how='any'),
      value = df_links['value'].dropna(axis=0, how='any'),
      color = df_links['link color'].dropna(axis=0, how='any'),
    )
  )

  layout = dict(
    title = title_diagram,
    height = int(diagram_height),
    width = int(diagram_width),
    hovermode = "x",
    plot_bgcolor= diagram_bg_color,
    paper_bgcolor=diagram_bg_color,
    font = dict(
      family="Helvetica", size = int(font_size), color= font_color),)

  fig = go.Figure(data=[data_trace], layout=layout)
  #---DISPLAY SANKEY IN STREAMLIT-----#
  st.plotly_chart(fig)
  #------------------------------------#
except:
  st.markdown("""<h3 style="color:red;">set the height and width of your diagram. Thank you.</h3>""", unsafe_allow_html=True)

