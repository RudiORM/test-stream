import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Streamlit app
st.title("3D Scatter Plot with Animation")

# File uploader for the XLSX
uploaded_file = st.file_uploader("Upload your XLSX file", type="xlsx")

if uploaded_file is not None:
    # Read the uploaded XLSX into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Define a color map for the 'Type' column
    color_map = {
        'Exhibition': '#003f5c',   # Dark Blue
        'Festival': '#374c80',     # Blue
        'Initiative': '#7a5195',   # Purple
        'Film festival': '#bc5090',# Pinkish Purple
        'Multimedia': '#ef5675',   # Red
        'Talk': '#ff764a',         # Orange
        'Film': '#ffa600'          # Yellowish Orange
    }

    # Create a blank figure object
    fig = go.Figure()

    # Add the initial empty trace for the points and lines (to create the base structure)
    fig.add_trace(go.Scatter3d(x=[], y=[], z=[], mode='markers', marker=dict(size=5)))
    fig.add_trace(go.Scatter3d(x=[], y=[], z=[], mode='lines', line=dict(color='black', width=3)))

    # Create frames for both points and lines, but do them independently
    frames = []
    for year in range(2008, 2024):
        # Filter data for points that are active in the current year
        filtered_df = df[(df['Year'] <= year) & (df['End year'] >= year)]
        
        # Filter data for the line, connecting all points up to the current year
        line_df = df[df['Year'] <= year].sort_values(by='Year')  # Sort points by Year for proper line connections
        
        # Map colors based on 'Type' for the filtered points
        point_colors = filtered_df['Type'].map(color_map)

        # Append frame for both points and line
        frames.append(go.Frame(
            data=[
                # Line trace for connecting points
                go.Scatter3d(x=line_df['conventional to conceptual'],
                             y=line_df['confined to autonomous'],
                             z=line_df['Peripheral to Immersive'],
                             mode='lines',
                             hoverinfo='skip',
                             line=dict(color='black', width=3)),
                # Scatter trace for the points with hover text for the 'Title'
                go.Scatter3d(x=filtered_df['conventional to conceptual'],
                             y=filtered_df['confined to autonomous'],
                             z=filtered_df['Peripheral to Immersive'],
                             mode='markers',
                             marker=dict(size=7, color=point_colors),
                             hovertext=filtered_df['Title'],  # Hover text for the Title
                             hoverinfo='text')  # Show only the text on hover
            ],
            name=str(year)
        ))

    # Add the frames to the figure
    fig.frames = frames

    # Set axis limits and labels, ensuring the scales stay fixed and set aspect ratio for a cube
    fig.update_layout(scene=dict(
        xaxis=dict(range=[0, 10], title='conventional to conceptual', autorange=False),
        yaxis=dict(range=[0, 10], title='confined to autonomous', autorange=False),
        zaxis=dict(range=[0, 10], title='Peripheral to Immersive', autorange=False),
        aspectmode="cube"  # Ensures that the x, y, and z axes have equal scaling
    ))

    # Add the animation settings (play/pause buttons and slider)
    fig.update_layout(updatemenus=[dict(type="buttons",
                                        showactive=False,
                                        buttons=[dict(label="Play",
                                                      method="animate",
                                                      args=[None, dict(frame=dict(duration=500, redraw=True), 
                                                                       fromcurrent=True, 
                                                                       mode='immediate')]),
                                                 dict(label="Pause",
                                                      method="animate",
                                                      args=[[None], dict(frame=dict(duration=0, redraw=True), 
                                                                         mode='immediate')])])],
                      title="3D Scatter Plot with Year Slider",
                      sliders=[{
                          'steps': [{'args': [[str(year)],
                                              {'frame': {'duration': 500, 'redraw': True},
                                               'mode': 'immediate'}],
                                     'label': str(year),
                                     'method': 'animate'} for year in range(2008, 2024)],
                          'currentvalue': {'prefix': 'Year: '}
                      }])

    # Show the figure in Streamlit
    st.plotly_chart(fig)

else:
    st.write("Please upload an XLSX file.")
