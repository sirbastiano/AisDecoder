#ENV: py38
import pandas as pd
from shapely.geometry import Point, Polygon
import folium 



def add_my_legend(folium_map):

    legend_html = f"""
      <div id='maplegend' class='maplegend'>
      <div class='legend-title'>Legend:</div>
      <div class='legend-scale'><br>
        <ul class='legend-labels'>
          <i><img src="https://i.ibb.co/YjBZx84/Argo.png" width="20"/> ARGO AIS Receiver </i>
          <i><img src="https://i.ibb.co/8KX0zLx/loc.png" width="15"/> Ship with COG </i>
          <i><img src="https://i.ibb.co/5sXcLbr/nave.png" width="15"/> Other </i>
        </ul>
      </div>
      </div>
    """

    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 25px;
        border: 3px solid #bbb;
        padding: 1px;
        font-size:16px;
        positon: relative;
        vertical-align: top;
      }
      .maplegend .legend-title {
        text-align: center;
        margin-bottom: 0px;
        vertical-align: top;
        font-weight: bold;
        font-size: 100%;
        }
      .maplegend .legend-scale ul {
        position: relative;
        top: -25px;
        width: 300px;
        }

      .maplegend ul.legend-labels i {
        font-size: 15px;
        display: block;
        float:left;
        height: 25px;
        margin-bottom: -4px;
        }
        
      .maplegend .legend-source {
        font-size: 60%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }

  
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


# def plotReceiver(GPS: pd.DataFrame, m: folium.map):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a ReceiverMarker and adds it to your this_map'''

#      # filter position too close each other TBD


#     for idx, point in GPS.iterrows():

#         folium.Marker(location=[point.latitude, point.longitude],
#                             popup=folium.Popup(f"<b>VM XB-6000, time(UTC):{point.timestamp}</b>", sticky=True, show=True), 
#                             # radius=1,
#                             # weight=1,
#                             icon=folium.Icon(
#                                     icon_color='white',
#                                     icon='fa-street-view',    # icon code from above link
#                                     prefix='fa'),
#                             ).add_to(m)

# def plotIcon(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.Marker(location=[point.lat, point.lon],
#                         popup=folium.Popup(f"<b>{point.mmsi}</b>", ), #sticky=True, show=True
#                         # radius=1,
#                         # weight=1,
#                         icon=folium.Icon(
#                                   icon_color='white',
#                                   icon='fa-ship',    # icon code from above link
#                                   prefix='fa'),
#                         ).add_to(m)


# def plotStartIcon(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.Marker(location=[point.lat, point.lon],
#                         popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
#                         # radius=1,
#                         # weight=1,
#                         icon=folium.Icon(
#                                   icon_color='white',
#                                   icon='fa-flag',    # icon code from above link
#                                   prefix='fa'),
#                         ).add_to(m)

# def plotEndIcon(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.Marker(location=[point.lat, point.lon],
#                         popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
#                         # radius=1,
#                         # weight=1,
#                         icon=folium.Icon(
#                                   icon_color='white',
#                                   icon='fa-ship',    # icon code from above link
#                                   prefix='fa'),
#                         ).add_to(m)

# def plotAnchorIcon(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.Marker(location=[point.lat, point.lon],
#                         popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
#                         # radius=1,
#                         # weight=1,
#                         icon=folium.Icon(
#                                   icon_color='white',
#                                   icon='fa-anchor',    # icon code from above link
#                                   prefix='fa'),
#                         ).add_to(m)


# def plotDot(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.CircleMarker(location=[point.lat, point.lon],
#                         popup=folium.Popup(f"<b>mmsi:{point.mmsi}, time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
#                         radius=1,
#                         weight=1,
#                         fill=True,
#                         ).add_to(m)

# def SubsetAis_mmsi(ships_mmsi, ais: pd.DataFrame):
#      """
#      Subset ais signal to get only the relative to the ship mmsi given in input     
#      """
#      df = ais[ais['mmsi']==ships_mmsi]
#      return df

# def PlotPolyline(m: folium.map, SShipAIS: pd.DataFrame):
#      """
#      Plots a polyline on a map from a list of tuple points
#      """
#      points = [(x.lat, x.lon) for x in SShipAIS.iloc]
#      for point in points: 
#           folium.CircleMarker(location=point,
#                         radius=0.5,
#                         weight=3,
#                         fill=True,
#                         ).add_to(m)
#      if len(points) > 1:
#           folium.PolyLine(points, color="black", weight=0.5, opacity=1).add_to(m)
#           plotStartIcon(SShipAIS.iloc[0])
#           plotEndIcon(SShipAIS.iloc[-1])
#      else:
#           plotAnchorIcon(SShipAIS.iloc[0])



def plotReceiver(GPS: pd.DataFrame, m: folium.map):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a ReceiverMarker and adds it to your this_map'''
     # filter position too close each other TBD

    for idx, point in GPS.iterrows():
        url = 'https://i.ibb.co/F74VFJk/Argo.png'
        fake_dic = {'course':'0'}
        angle = pd.Series(fake_dic)
        folium.Marker(location=[point.latitude, point.longitude],
                            popup=folium.Popup(f"<b>VM XB-6000, time(UTC):{point.timestamp}</b>", sticky=True, show=True), 
                            radius=1,
                            weight=10,
                            
                            icon = custom_Icon_Argo(url, angle)
                            # icon=folium.Icon(
                            #         icon_color='white',
                            #         color='black',
                            #         icon='fa-street-view',    # icon code from above link
                            #         prefix='fa'),
                            ).add_to(m)

def plotIcon(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.Marker(location=[point.lat, point.lon],
                        popup=folium.Popup(f"<b>{point.mmsi}</b>", ), #sticky=True, show=True
                        # radius=1,
                        # weight=1,
                        icon=folium.Icon(
                                  icon_color='white',
                                  icon='fa-ship',    # icon code from above link
                                  prefix='fa'),
                        ).add_to(m)


def plotStartIcon(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    try:
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon('https://i.ibb.co/wYjjnGp/Starting.png', point),
                            # icon=folium.Icon(
                            #           icon_color='white',
                            #           icon='fa-flag',    # icon code from above link
                            #           prefix='fa'),
                            ).add_to(m)
    except ValueError:
        # point.course = 0
        point.at['course'] = 0
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon('https://i.ibb.co/s9D6zw1/ship3.png', point),
                            # icon=folium.Icon(
                            #           icon_color='white',
                            #           icon='fa-flag',    # icon code from above link
                            #           prefix='fa'),
                            ).add_to(m)

def plotEndIcon(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    try:
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon('https://i.ibb.co/s9D6zw1/ship3.png', point),
                            # icon=folium.Icon(
                            #           icon_color='white',
                            #           icon='fa-flag',    # icon code from above link
                            #           prefix='fa'),
                            ).add_to(m)
    except ValueError:
        # point.course = 0
        point.at['course'] = 0
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon("https://i.ibb.co/tY8qY8v/ship2.png",point),
                            # icon=folium.Icon(
                            #           icon_color='white',
                            #           icon='fa-flag',    # icon code from above link
                            #           prefix='fa'),
                            ).add_to(m)

def plotLocatorIcon(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a Marker and adds it to your this_map'''
    try:
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon_Loc('https://i.ibb.co/ch3sWbh/loc-blue.png', point),
                            # icon=folium.Icon(
                            #           icon_color='white',
                            #           icon='fa-ship',    # icon code from above link
                            #           prefix='fa'),
                            ).add_to(m)
    except ValueError:
        point.at['course'] = 0
        folium.Marker(location=[point.lat, point.lon],
                            popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                            # radius=1,
                            # weight=1,
                            icon=custom_Icon("https://i.ibb.co/tY8qY8v/ship2.png",point),
                            ).add_to(m)


def plotAnchorIcon(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.Marker(location=[point.lat, point.lon],
                        popup=folium.Popup(f"<b>mmsi:{point.mmsi} time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                        # radius=1,
                        # weight=1,
                        icon=folium.Icon(
                                  icon_color='white',
                                  icon='fa-anchor',    # icon code from above link
                                  prefix='fa'),
                        ).add_to(m)

def custom_Icon(icon_url:str, point):
    # icon = folium.features.CustomIcon(icon_url,
    #                                   icon_size=(7, 14),
    #                                   icon_anchor=(0,0),
    #                                   )
    # style="transform:rotate(90deg);"
    angle=str(int(point.course))
    Html = f'<img src="{icon_url}" width="26" style="transform:rotate({angle}deg);"/>'
    icon = folium.features.DivIcon(html=Html, 
                                        icon_size=None, 
                                        icon_anchor=(13,13), 
                                        popup_anchor=None, 
                                        class_name='empty')

    return icon

def custom_Icon_Argo(icon_url:str, point):
    # icon = folium.features.CustomIcon(icon_url,
    #                                   icon_size=(7, 14),
    #                                   icon_anchor=(0,0),
    #                                   )
    # style="transform:rotate(90deg);"
    angle=str(int(point.course))
    Html = f'<img src="{icon_url}" width="36" style="transform:rotate({angle}deg);"/>'
    icon = folium.features.DivIcon(html=Html, 
                                        icon_size=None, 
                                        icon_anchor=(18,18), 
                                        popup_anchor=None, 
                                        class_name='empty')

    return icon

def custom_Icon_Loc(icon_url:str, point):
    # icon = folium.features.CustomIcon(icon_url,
    #                                   icon_size=(7, 14),
    #                                   icon_anchor=(0,0),
    #                                   )

    angle=str(int(point.course))
    Html = f'<img src="{icon_url}" width="13" style="transform:rotate({angle}deg);"/>'
    icon = folium.features.DivIcon(html=Html, 
                                        icon_size=None, 
                                        icon_anchor=(5,10), 
                                        popup_anchor=None, 
                                        class_name='empty')

    return icon

def plotDot(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.lat, point.lon],
                        popup=folium.Popup(f"<b>mmsi:{point.mmsi}, time(UTC):{point.timestamp}</b>", ), #sticky=True, show=True
                        radius=1,
                        weight=1,
                        fill=True,
                        ).add_to(m)

def SubsetAis_mmsi(ships_mmsi, ais: pd.DataFrame):
     """
     Subset ais signal to get only the relative to the ship mmsi given in input     
     """
     df = ais[ais['mmsi']==ships_mmsi]
     return df

def PlotPolyline(m: folium.map, SShipAIS: pd.DataFrame):
     """
     Plots a polyline on a map from a list of tuple points
     """
     points = [(x.lat, x.lon) for x in SShipAIS.iloc]
     
        #   folium.CircleMarker(location=point,
        #                 radius=0.5,
        #                 weight=3,
        #                 fill=True,
        #                 ).add_to(m)
     if len(points) > 1:
        for idx, row in SShipAIS.iterrows():
            plotLocatorIcon(row) 
        folium.PolyLine(points, color="black", weight=0.5, opacity=1).add_to(m)
        plotStartIcon(SShipAIS.iloc[0])
        #   plotEndIcon(SShipAIS.iloc[-1])
     else:
        plotStartIcon(SShipAIS.iloc[0])
        # plotAnchorIcon(SShipAIS.iloc[0])
        pass


def create_map(location: list, zoom_start: int, tiles: str):
     if len(location) != 2 or zoom_start < 0:
          raise ValueError 
     m = folium.Map(location=location, zoom_start=zoom_start, tiles=tiles)
     return m

loc = [40.75, 14.3]
zs = 11
tiles = 'CartoDB positron'

global m
m = create_map(loc, zs, tiles)

if __name__ == "main":
     pass