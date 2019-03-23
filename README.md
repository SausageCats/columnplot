# ColumnPlot

ColumnPlot is a command-line tool to easily create multiple graphs for each column in a file.
The following figure shows an example of ColumnPlot that reads a data file with 17 columns to plot each of them in different regions in a window.
By clicking on several graphs in the main window, ColumnPlot merges selected graphs and displays them into a new sub window.
In those windows, ColumnPlot provides a simple set of keyboard shortcuts and mouse events to change graph style.
ColumnPlot supports different data types such as numeric, datetime, and alphabetic values.
For more information, see usage section.

![](https://raw.githubusercontent.com/SausageCats/supplements/master/columnplot/columnplot.png)


# Prerequisite

ColumnPlot creates a matplotlib graph that is embedded into a Tkinter window using python3.
This requires the following packages:

- python3\-tk
- Matplotlib >= 2.2.2



# Installation

ColumnPlot can be installed using the following command.

``` bash
$ git clone https://github.com/SausageCats/columnplot.git
$ cd columnplot
$ python3 setup.py install --user
$ columnplot --version # to check the success of the installation
```



# Usage


## Data file notation

A data file format is as follows:

- Each column must be separated by the same delimiter.
A default delimiter is set to multiple white spaces (\"\\s+\") except for a comma delimiter for \".csv\" files.
The default delimiter can be replaced by other characters using \"\-\-delimiter\" option.

- Each column must have the same data type.
Available data type is either numeric values, datetime groups, or strings.
In the case of a string column, however, if it contains many different string values, it takes too long to plot the column data.
For the reason, the number of different string elements must be less than or equal to \"max_strelms\" option value (15 as default).
Otherwise, a string column cannot be plotted.

- Each row must have the same number of delimiters.
A row that contains an empty string (\"\") in a column will be skipped.

- Each row starting at \"#\" or \"\\s+#\" is treated as comment line.
The first row with comment is used for graph titles.
This is disabled by setting \"enable_graphtitle\" option to False.


## Command

ColumnPlot works using the following command.
It creates multiple graphs where horizontal axis is the data number and vertical axis is the column data in a file.

``` bash
$ columnplot DATAFILE [OPTION]...
```

where DATAFILE is the path to a data file described in \"Data file notation\" section.
Each of OPTION is described below.

Option&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Description
:--|:--
\-d, \-\-delimiter DELIMITER | Specify a delimiter to separate columns in DATAFILE
\-D, \-\-datetime FORMAT[ FORMAT...] | Set FORMAT to a datetime format if DATAFILE contains datetime columns. For example, if a column has "2018\-01\-02 03:04:05\", the FORMAT is given \"%Y\-%m\-%d %H:%M:%S\". Without this option, ColumnPlot tries to parse datetime columns automatically, but it may take a long time to parse it. If FORMAT is specified as an empty string (\"\"), ColumnPlot determines that there are no datetime columns in DATAFILE. It is possible to specify multiple formats. For example, "\-\-format %H:%M:%S %Hh%Mm%Ss" matches datetime such as \"01:02:03\" or \"01h02m03s\". For the format codes, refer to [here](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).
\-t, \-\-titleline | Use the first line in DATAFILE as a graph title.
\-h, \-\-help | Display help message and exit.
\-i, \-\-ignore COLUMN[ COLUMN...] | Set COLUMN to a column number. The corresponding data is not plotted in ColumnPlotMain window. The number starts at 1. For example, "\-\-ignore 1 3" does not create graphs for 1st and 3st columns. If this option is given together with \"\-\-limit\" option, this option will be disabled.
\-l, \-\-limit COLUMN[ COLUMN...] | This option is similar to \"\-\-ignore\", but a specified column is plotted.
\-p, \-\-print | Print configuration information.
\-v, \-\-version | Display version.


## Configuration file

ColumnPlot reads a configuration file (columnplot.cfg) that is placed in a directory \"$HOME/.config/columnplot\".
The $COLUMNPLOTCFG environment variable changes the default config path.
The configuration file has several options as shown in below table.
Each option is defined as name\-value pairs separated by an equal sign (=).
The sample config file is stored in this repository.

Option|Type|Default|Description
:--|:--|:--|:--
enable_graphtitle  | boolean      | True  | The first line in a data file is used for graph title.
max_strelms        | int          | 15    | If a column has different strings and the number of them exceeds this option value, ColumnPlot does not create the graph from the string type column.
timefmt            | list[string] | []    | This option is similar to \-\-timefmt option except that this value is set to a list, such as [\"%H:%M:%S\", \"%Hh%Mm%Ss\"]
geometry_plotmain  | string       | 1600x1200+40+50 | Specify the size and location of the ColumnPlotMain window. The format is \"WxH+x+y\" where W and H is the width and height of ColumnPlotMain window, and x and y is a position from the top left of the desktop screen.
geometry_plotsub   | string       | 1000x750+40+50  | Specify the size and location of the ColumnPlotSub window. The format is the same as described above.
linestyle          | string       | \-    | Specify a line style that is used in Matplotlib. A line on a graph is displayed or undisplayed by pressing \"key_linestyle\" value.
marker1            | string       | o     | Specify a marker that is used in Matplotlib. A marker on a graph is displayed or undisplayed by pressing \"key_marker1\" value.
marker2            | string       | .     | This is the same as \"marker1" except for use of \"key_marker2\".
show_grid          | boolean      | False | Show grid lines in ColumnPlotMain at the start if this value is True.
show_marker        | boolean      | False | Show \"marker1\" in ColumnPlotMain at the start if this value is True.
show_msgs          | boolean      | False | Show some messages at an event if this value is True.
show_toolbar       | boolean      | False | Show a toolbar in ColumnPlotMain at the start if this value is True.
key_marker1        | string       | m     | Specify a key to toggle \"marker1\" on or off.
key_marker2        | string       | M     | Specify a key to toggle \"marker2\" on or off.
key_grid           | string       | G     | Specify a key to toggle gird lines on or off.
key_linestyle      | string       | l     | Specify a key to toggle graph lines on or off.
key_quit           | string       | q     | Specify a key to quit a current active window (ColumnPlotMain or ColumnPlotSub).
key_quitall        | string       | Q     | Specify a key to quit both ColumnPlotMain and ColumnPlotSub.
key_plotsub        | string       | s     | Specify a key to enter graph selection mode. In the mode, when you press a numeric key (N), a graph with the number N is created in ColumnPlotSub. For example, pressing 's1' or 's1\<Enter\>' creates graph1 (corresponding to first column). This option is invalid in ColumnPlotSub. Some messages are displayed in the command line if \"show_msgs\" is True.
key_xcoord         | string       | x     | Specify a key to enter x-axis selection mode. In the mode, when you press a numeric key (N), x-axis values in all graphs are changed to the y-axis values of a Nth graph. For example, by pressing 'x1' or 'x1\<Enter\>', x-axis values are changed to y-axis values of graph1. You can return this modification back to the original by pressing the same keys. This option is invalid in ColumnPlotSub. Some messages are displayed if \"show_msgs\" is True.
key_toolbar        | string       | T     | Specify a key to toggle a tool bar on or off.
mouse_plotsub      | int          | 1     | Specify a mouse number to display multiple graphs in ColumnPlotSub. The mouse number 1, 2, and 3 expresses the left, middle, and right button of a mouse, respectively. A graph is selected by single\-clicking or double\-clickng on the mouse number. However, the double\-clicking displays selected graphs into ColumnPlotSub. For example, if you single\-click on graph1 and double\-click on graph2, then the graph1 and graph2 are displayed in ColumnPlotSub. This option is invalid in ColumnPlotSub.
mouse_xcoord       | int          | 2     | Specify a mouse number to change x-axis values. The mouse number is the same as described above, and this option is similar to \"key_xcoord" option. For example, if you click on graph1 with the specified mouse number, x-axis values are changed to the y-axis values of the graph1. This option is invalid in ColumnPlotSub.



## Getting started

Here is a simple tutorial on how to use ColumnPlot.

1. Copy the following test data to a file "functions.txt".
   - column1 shows x coordinate values of function2, 3, and 4.
   - column2 shows y coordinate values of function2: y=x*x.
   - column3 shows y coordinate values of function3: y=sin(x).
   - column4 shows y coordinate values of function4: y=|x|.

```
#[1]x_values [2]y=x*x [3]y=sin(x) [4]y=|x|
-3.00 9.00 -0.14 3.00
-2.43 5.90 -0.65 2.43
-1.92 3.69 -0.94 1.92
-1.47 2.16 -0.99 1.47
-1.08 1.17 -0.88 1.08
-0.75 0.56 -0.68 0.75
-0.48 0.23 -0.46 0.48
-0.27 0.07 -0.27 0.27
-0.12 0.01 -0.12 0.12
-0.03 0.00 -0.03 0.03
0.00 0.00 0.00 0.00
0.03 0.00 0.03 0.03
0.12 0.01 0.12 0.12
0.27 0.07 0.27 0.27
0.48 0.23 0.46 0.48
0.75 0.56 0.68 0.75
1.08 1.17 0.88 1.08
1.47 2.16 0.99 1.47
1.92 3.69 0.94 1.92
2.43 5.90 0.65 2.43
3.00 9.00 0.14 3.00
```

2. Run a command `columnplot functions.txt`.
   - Four Graphs are displayed in a single window (ColumnPlotMain).
   - The x axis shows data numbers starting from 0 to 20.
   - The y axis on graph1 (top left side) shows the column1 values.
   - The y axis on graph2 (top right side) shows the column2 values.
   - The y axis on graph3 (bottom left side) shows the column3 values.
   - The y axis on graph4 (bottom right side) shows the column4 values.

3. Press \'x1\' or middleclick on graph1 to change x-axis values.
   - All of the x-axis values are changed to the y-axis values of the graph1.
   - This transformation results in correct x coordinate values of function2, 3, and 4 at the 2-4th graphs.

4. Press \'m\'
   - Red dots are inserted on the lines of the graphs.

5. Press \'G\'
   - Grid lines are inserted on the graphs.

6. Leftclick on the graph1, 2 and 3, and double leftclick on the graph4.
   - The graphs are merged and displayed into a single window (ColumnPlotSub).

7. Press \'l\' in the ColumnPlotSub.
   - All lines are deleted in the ColumnPlotSub only.

8. Press \'Q\'
   - ColumnPlotMain and ColumnPlotSub are disappeared.


![](https://raw.githubusercontent.com/SausageCats/supplements/master/columnplot/getting_started.png)
