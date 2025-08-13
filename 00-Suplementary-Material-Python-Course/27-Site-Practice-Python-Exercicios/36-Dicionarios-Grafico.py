# !/usr/bin/python3.4   # Scripts executaveis em python (shebang)
# https://www.practicepython.org/exercise/2017/04/02/36-birthday-plots.html
# http://bokeh.pydata.org/en/latest/docs/user_guide.html
# bokeh.pydata.org/en/latest/docs/user_guide/plotting.html

import sys
print(sys.version)
##########################################################################
# Birthday Plots
#
# This exercise is Part 4 of 4 of the birthday data exercise series.
# The other exercises are: Part 1, Part 2, and Part 3.
#
# In the previous exercise we counted how many birthdays there are in each
# month in our dictionary of birthdays.
#
# In this exercise, use the bokeh Python library to plot a histogram of which
# months the scientists have birthdays in! Because it would take a long time
# for you to input the months of various scientists, you can use my scientist
# birthday JSON file. Just parse out the months (if you don’t know how, I
# suggest looking at the previous exercise or its solution) and draw your
# histogram.
#
# It requires installing the bokeh Python package.
#
# Plotting libraries in Python
#
# If you are looking for a plotting library in Python, you have two main options: matplotlib and bokeh. Today I want to discuss bokeh, because I think it will become more popular in years to come.
#
# Many Python developers (and especially data scientists and researchers) will tell you that the most commonly used plotting library in Python is matplotlib. I myself was a matplotlib user for many years - the integrations with Python data libraries are great, and migrating from the MATLAB plotting environment to matplotlib is easy. But a friend introduced me to bokeh and I was hooked ever since. Because it is based on D3.js, the visualizations look smooth and professional.
#
# There is no one “best” plotting library - you should use whichever one feels and looks better for you. But for the rest of this post, I’ll talk about how to use bokeh to make a basic plot.
#
# Installing bokeh
#
# In the Windows command prompt or the bash shell.
#
# On OSX or GNU / Linux, just type
#
# pip3 install bokeh
#
# Using bokeh
#
# The basic idea of any plotting package is simple:
#
#     Load the data
#     Display the data
#
# So the first thing you have to do is prepare some data. Usually, when you are plotting data you have two axes, or groups of data, an x-axis (or horizontal axis) and a y-axis (or vertical axis). The x variable is your input (independent) variable and the y variable is your output (dependent) variable.
#
# For use in bokeh, your data should be loaded into two separate lists, one for the x-axis and one for the y-axis. The basic format of a bokeh (in this case histogram) looks like this:
#
# # need to import at least 3 things to make your
# # bokeh plots work
# from bokeh.plotting import figure, show, output_file
#
# # we specify an HTML file where the output will go
# output_file("plot.html")
#
# # load our x and y data
# x = [10, 20, 30]
# y = [4, 5, 6]
#
# # create a figure
# p = figure()
#
# # create a histogram
# p.vbar(x=x, top=y, width=0.5)
#
# # render (show) the plot
# show(p)
#
# The way bokeh outputs plots is really cool: when you run a piece of bokeh code, it outputs the result into an HTML file that you can then save and display in a web browser on it’s own. After you run this segment on top, it will automatically open a web browser and show you a plot.
#
# One awesome feature of Bokeh is that it gives you a toolbar you can use to play with the graph - moving it around, zooming out, saving it, etc. Plus, you can put it directly into am HTML page!
#
# The example above works when x is a numerical value. But, in the exercise, we are dealing with months, which is called a “categorical” variable (i.e. it belongs to a category, and is not continuous). To make sure bokeh draws the axis correctly, you need to specify a special call to figure() to pass an x_range, like so:
#
# from bokeh.plotting import figure, show, output_file
#
# output_file("plot.html")
# x_categories = ["a", "b", "c", "d", "e"]
# x = ["a", "d", "e"]
# y = [4, 5, 6]
#
# p = figure(x_range=x_categories)
# p.vbar(x=x, top=y, width=0.5)
#
# show(p)

# import dicmes
# from dicmes import main, num_to_string
from dicmes import *

from bokeh.plotting import figure, show, output_file
from bokeh.models import Title

output_file("plot.html")

# main()
# dicmes.main()

# x_categorias = list(num_to_string.items())
# print(x_categorias)
# x_categorias = list(num_to_string.keys())
# print(x_categorias)
# x_categorias = list(num_to_string.values())
# print(x_categorias)

# x = list(dicmes.num_to_string.values())

eixo_x = list(num_to_string.values())
# print("x = ", x)
dic_json = apresenta_dados()
# print(dic_json)
# y = list(dic_json.values())
# print("y = ", y)
#
dic2 = {}
for i in eixo_x:
    dic2[i] = 0
    for j in dic_json.keys():
        if i in j:
            dic2[i] = dic_json[j]
# print(dic2)

x = list(dic2.keys())
# print("x = ", x)

y = list(dic2.values())
# print("y = ", y)

# p = figure(plot_width=400, plot_height=400)
# p = figure(title="Frenquência de aniversários", toolbar_location="above", x_range=eixo_x, plot_height=400)
p = figure(toolbar_location="above", x_range=eixo_x, plot_height=400)
p.vbar(x=x, top=y, width=0.7, bottom=0, color="firebrick", legend="Aniversários")

# configure visual properties on a plot's title attribute
p.title.text = "Número de aniversários ao longo dos meses"
p.title.align = "left"
p.title.text_color = "black"
p.title.text_font_size = "15px"
# Hex color: https://htmlcolorcodes.com/
p.title.background_fill_color = "#f7eeec"

# add extra titles with add_layout(...)
p.add_layout(Title(text="Ano 2019", align="center"), "below")
# Eixos
p.xaxis[0].axis_label = 'Meses'
p.yaxis[0].axis_label = 'Qde'

show(p)
