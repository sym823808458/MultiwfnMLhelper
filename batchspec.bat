for /f %%i in ('dir *.fchk /b') do (
Multiwfn %%i < Step_1.txt1 > orbana_1_3.txt
rename orbana_1_3.txt %%~ni.txt
)
