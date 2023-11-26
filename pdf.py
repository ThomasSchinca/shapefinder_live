# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:27:12 2023

@author: thoma
"""

# Since the image has been uploaded, we can now proceed to add it to the PDF.
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd

# Path to your Poppins font .ttf files
poppins_bold_path = 'Poppins/Poppins-Bold.ttf'  # Replace with your font file path
poppins_regular_path = 'Poppins/Poppins-Regular.ttf'  # Replace with your font file path

# Register the Poppins font
pdfmetrics.registerFont(TTFont('Poppins-Bold', poppins_bold_path))
pdfmetrics.registerFont(TTFont('Poppins', poppins_regular_path))

month = datetime.now().strftime("%B")
year = datetime.now().strftime("%Y")
month_s = datetime.now().strftime("%b")
six_months = date.today() + relativedelta(months=+5)
sm_m = six_months.strftime("%b")
sm_y = six_months.strftime("%Y")


# Define the path for the new PDF and the uploaded image
output_pdf_path = 'Report.pdf'
c = canvas.Canvas(output_pdf_path, pagesize=letter)

title_text = f'{month} {year} Newsletter'
title_font = "Poppins-Bold"  
title_font_size = 30
title_color = HexColor("#df2226")
# Add title to the PDF
c.setFont(title_font, title_font_size)
c.setFillColor(title_color)
c.drawCentredString(297.5, 750, title_text)  # Positioning title at the top, center of the page

# Set the subtitle properties
subtitle_text = "Global Risk Prediction Map ("+str(month_s)+' '+str(year)+' - '+str(sm_m)+' '+str(sm_y)+")"
subtitle_font = "Poppins"  # Using a standard sans-serif font
subtitle_font_size = 11
subtitle_color = HexColor("#505050")  # Assuming "gris foncé 3" is a dark grey color
c.setFont(subtitle_font, subtitle_font_size)
c.setFillColor(subtitle_color)
c.drawCentredString(297.5, 730, subtitle_text)  # Positioning subtitle below the title

# Place the image on the PDF
map_image_path = 'Images/map.png'
c.drawImage(map_image_path, x=50, y=470, width=500, height=250, mask='auto')  # Scaled to fit


t_1 = "Most Risky Countries"
c.setFillColor(subtitle_color)
c.drawCentredString(297.5/2, 455, t_1)
t_3 = "Continent Risk"
c.setFillColor(subtitle_color)
c.drawCentredString(297.5*1.5, 455, t_3)
sub_image2 = 'Images/sub2.png'
sub_image3 = 'Images/sub3.png'
c.drawImage(sub_image2, x=50, y=285, width=220,height=160, mask='auto')  # Scaled to fit
c.drawImage(sub_image3, x=325, y=285, width=220,height=160, mask='auto')  # Scaled to fit

t_2 = "Monthly Fatalities based on Historical Patterns"
c.setFillColor(subtitle_color)
c.drawCentredString(297.5, 265, t_2)
sub_image1 = 'Images/sub1_1.png'
c.drawImage(sub_image1, x=25, y=90, width=550,height=160,  mask='auto')  # Scaled to fit

pace_logo = 'Images/PaCE Final.png'
c.drawImage(pace_logo, x=50, y=20, width=100,height=40,  mask='auto')  # Scaled to fit

info_text = "Click here for more info"
info_url = "https://shapefinder.azurewebsites.net/"
c.setFillColor(HexColor("#999999"))  # Blue color for the link text
c.setFont("Poppins", 10)
text_width = c.stringWidth(info_text, "Poppins", 10)
c.drawString((letter[0] - text_width) / 2, 30, info_text)
c.linkURL(info_url, (297.5 - text_width / 2, 30, 297.5 + text_width / 2, 42), relative=1)

# Adding "Twitter" and "Website" links in the bottom right corner
twitter_text = "Twitter"
twitter_url = "https://twitter.com/LabConflict"
website_text = "Website"
website_url = "https://paceconflictlab.wixsite.com/conflict-research-la"
contact = "Contact"


# Calculate the positioning for the text
right_margin = 50
bottom_margin = 20
line_height = 12



c.drawString(letter[0] - right_margin - c.stringWidth('schincat@tcd.ie', "Poppins", 10), bottom_margin + 2*line_height, 'schincat@tcd.ie')
c.drawString(letter[0] - right_margin - c.stringWidth(twitter_text, "Poppins", 10), bottom_margin + line_height, twitter_text)
c.linkURL(twitter_url, (letter[0] - right_margin - c.stringWidth(twitter_text, "Poppins", 10), bottom_margin + line_height, letter[0] - right_margin, bottom_margin + line_height * 2), relative=1)
c.drawString(letter[0] - right_margin - c.stringWidth(website_text, "Poppins", 10), bottom_margin, website_text)
c.linkURL(website_url, (letter[0] - right_margin - c.stringWidth(website_text, "Poppins", 10), bottom_margin, letter[0] - right_margin, bottom_margin + line_height), relative=1)

subtitle_font = "Poppins"  # Using a standard sans-serif font
subtitle_font_size = 11
subtitle_color = HexColor("#505050")  # Assuming "gris foncé 3" is a dark grey color
c.setFont(subtitle_font, subtitle_font_size)
c.setFillColor(subtitle_color)
c.drawString(letter[0] - right_margin - c.stringWidth('Contact', "Poppins", 11), bottom_margin + 3.25*line_height, 'Contact')
c.showPage()

df_best = pd.read_csv('best.csv',index_col=0)

first = df_best.iloc[-1][0]
title_text = f'{first}'
title_font = "Poppins-Bold"  
title_font_size = 13
title_color = HexColor("#df2226")
c.setFont(title_font, title_font_size)
c.setFillColor(title_color)
c.drawCentredString(75, 740, title_text)

images = ['Images/ex1.png', 'Images/ex1_m4.png', 'Images/ex1_barh.png']
titles = ["Last Observed Values", "Mean of Past Futures", "All sequences"]
subtitle_font = "Poppins"  # Using a standard sans-serif font
subtitle_font_size = 11
subtitle_color = HexColor("#505050")  # Assuming "gris foncé 3" is a dark grey color
c.setFont(subtitle_font, subtitle_font_size)
c.setFillColor(subtitle_color)
image_y = 580
text_y = image_y + 130 
x_offset = 50
x_step = 175
for i, (title, image) in enumerate(zip(titles, images)):
    current_x = x_offset + i * x_step
    if i==2:
        c.drawImage(image, current_x-15, image_y, width=200, height=150, preserveAspectRatio=True)
        c.drawString(current_x+50, text_y, title)
    else:
        c.drawImage(image, current_x, image_y, width=150, height=130, preserveAspectRatio=True)
        c.drawString(current_x+25, text_y, title)

c.drawCentredString(297.5, image_y-10, 'Matching sequences')
image_y = 440
images = ['Images/ex1_m0.png', 'Images/ex1_m1.png', 'Images/ex1_m2.png']
for i, (title, image) in enumerate(zip(titles, images)):
    current_x = x_offset + i * x_step
    c.drawImage(image, current_x, image_y, width=150, height=130, preserveAspectRatio=True)

first = df_best.iloc[-2][0]
title_text = f'{first}'
title_font = "Poppins-Bold"  
title_font_size = 13
title_color = HexColor("#df2226")
c.setFont(title_font, title_font_size)
c.setFillColor(title_color)
c.drawCentredString(75, 400, title_text)

images = ['Images/ex2.png', 'Images/ex2_m4.png', 'Images/ex2_barh.png']
titles = ["Last Observed Values", "Mean of Past Futures", "All sequences"]
subtitle_font = "Poppins"  # Using a standard sans-serif font
subtitle_font_size = 11
subtitle_color = HexColor("#505050")  # Assuming "gris foncé 3" is a dark grey color
c.setFont(subtitle_font, subtitle_font_size)
c.setFillColor(subtitle_color)
image_y = 240
text_y = image_y + 130 
x_offset = 50
x_step = 175
for i, (title, image) in enumerate(zip(titles, images)):
    current_x = x_offset + i * x_step
    if i==2:
        c.drawImage(image, current_x-15, image_y, width=200, height=150, preserveAspectRatio=True)
        c.drawString(current_x+50, text_y, title)
    else:
        c.drawImage(image, current_x, image_y, width=150, height=130, preserveAspectRatio=True)
        c.drawString(current_x+25, text_y, title)

c.drawCentredString(297.5, image_y-10, 'Matching sequences')
image_y = 100
images = ['Images/ex2_m0.png', 'Images/ex2_m1.png', 'Images/ex2_m2.png']
for i, (title, image) in enumerate(zip(titles, images)):
    current_x = x_offset + i * x_step
    c.drawImage(image, current_x, image_y, width=150, height=130, preserveAspectRatio=True)

pace_logo = 'Images/PaCE Final.png'
c.drawImage(pace_logo, x=50, y=20, width=100,height=40,  mask='auto')  # Scaled to fit

info_text = "Click here for more info"
info_url = "https://shapefinder.azurewebsites.net/"
c.setFillColor(HexColor("#999999"))  # Blue color for the link text
c.setFont("Poppins", 10)
text_width = c.stringWidth(info_text, "Poppins", 10)
c.drawString((letter[0] - text_width) / 2, 30, info_text)
c.linkURL(info_url, (297.5 - text_width / 2, 30, 297.5 + text_width / 2, 42), relative=1)

# Adding "Twitter" and "Website" links in the bottom right corner
twitter_text = "Twitter"
twitter_url = "https://twitter.com/LabConflict"
website_text = "Website"
website_url = "https://paceconflictlab.wixsite.com/conflict-research-la"
contact = "Contact"


# Calculate the positioning for the text
right_margin = 50
bottom_margin = 20
line_height = 12


c.drawString(letter[0] - right_margin - c.stringWidth('schincat@tcd.ie', "Poppins", 10), bottom_margin + 2*line_height, 'schincat@tcd.ie')
c.drawString(letter[0] - right_margin - c.stringWidth(twitter_text, "Poppins", 10), bottom_margin + line_height, twitter_text)
c.linkURL(twitter_url, (letter[0] - right_margin - c.stringWidth(twitter_text, "Poppins", 10), bottom_margin + line_height, letter[0] - right_margin, bottom_margin + line_height * 2), relative=1)
c.drawString(letter[0] - right_margin - c.stringWidth(website_text, "Poppins", 10), bottom_margin, website_text)
c.linkURL(website_url, (letter[0] - right_margin - c.stringWidth(website_text, "Poppins", 10), bottom_margin, letter[0] - right_margin, bottom_margin + line_height), relative=1)

subtitle_font = "Poppins"  # Using a standard sans-serif font
subtitle_font_size = 11
subtitle_color = HexColor("#505050")  # Assuming "gris foncé 3" is a dark grey color
c.setFont(subtitle_font, subtitle_font_size)
c.setFillColor(subtitle_color)
c.drawString(letter[0] - right_margin - c.stringWidth('Contact', "Poppins", 11), bottom_margin + 3.25*line_height, 'Contact')

c.save()

output_pdf_path



