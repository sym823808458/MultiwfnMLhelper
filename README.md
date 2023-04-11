# MultiwfnMLhelper
Help you to generate quantum chemical descriptors of Multiwfn easily.


Recently, my work required me to quickly extract Multiwfn molecular descriptors for machine learning analysis. So, I created a Python script tool called "MultiwfnMLhelper - Multiwfn-based Molecular Machine Learning Assistant." It is incredibly easy to use, and I'd like to share it with you all.

【Ingredients】
Any task that can generate Gaussian .fchk files is suitable. After generating the files, place all the .fchk files in a folder.

【How to Use】
Download the entire compressed package MultiwfnMLhelper.zip from GitHub: If you are used to working with Windows and don't want to bother with the Python environment and installation, simply copy all the contents of the compressed package into a folder containing multiple Gaussian output .fchk files. Double-click the .exe file, select the current folder path, click OK, and the program will automatically generate Multiwfn molecular descriptors and save them to a CSV file named "Multwfn_analysis_feature_matrix3.csv".
If you are familiar with Python, you can install the required packages and run MultiwfnMLhelper.py yourself.
   
【File List】
(1) Multiwfn_helper.py: The main Python script for extracting Multiwfn descriptors.
(2) batchspec.bat: A batch file for running Multiwfn analysis.
(3) Step_1.txt1: A parameter file needed for Multiwfn analysis.
(4) settings.ini: Make sure to set isilent=1.

【References】
http://sobereva.com/601  
http://sobereva.com/612

【If you have any suggestions or feedback, please let me know】
