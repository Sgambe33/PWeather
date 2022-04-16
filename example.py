import plotly.graph_objects as G
import numpy as N
 
 
n = 100
 
figure = G.Figure(data=[G.Mesh3d(x=(55*N.random.randn(n)),
                   y=(50*N.random.randn(n)),
                   z=(25*N.random.randn(n)),
                   opacity=0.8,
                   color='rgba(244,22,100,0.6)'
                  )])
 
 
 
figure.show()