# 20230407苏禹铭编写用于提取multiwfn的分子描述符
import os
import re
from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import subprocess

# bat_file_path = 'C:/Users/YumingSu/Sym_Python_codes/MATLAB2python/batchspec.bat'
root = Tk()
root.withdraw()  

folder_name = filedialog.askdirectory()
os.chdir(folder_name)
bat_file_name = 'batchspec.bat'
bat_file_path = os.path.join(folder_name, bat_file_name)
# Run the .bat file
subprocess.run([bat_file_path], shell=True)

file_list = [file for file in os.listdir(folder_name) if file.endswith('.txt')]

data = []
odi_values = []
for file in file_list:
    with open(file, 'r') as f:
        content = f.read()
        lines = content.splitlines()
    
    sample_name = file[:-4]
    
    pattern = r'Orbital delocalization index:\s*([\d.]+)'
    odi_values = [float(value) for value in re.findall(pattern, content)]
    odi_homo_1, odi_homo, odi_lumo, odi_lumoadd1 = odi_values[:4]
    odi_mean = sum(odi_values) / len(odi_values)
    odi_std = (sum((x - odi_mean) ** 2 for x in odi_values) / len(odi_values)) ** 0.5

    for line in lines:
        if ' Atoms:  ' in line:
            new_str = line.split(': ')[1]
            new_str = new_str.split(',')[0]
            atom_num = int(new_str)
        elif ' Molecule weight:      ' in line:
            new_str = line.split(': ')[1]
            new_str = new_str.split(' Da')[0]
            weight = float(new_str)
        elif 'Orbital' in line and 'HOMO' in line:
            homo = float(re.search(r'energy:\s+([\d.-]+)', line).group(1))
            homo_number = int(re.search(r'Orbital\s+(\d+)', line).group(1))
        elif 'Orbital' in line and 'LUMO' in line:
            lumo = float(re.search(r'energy:\s+([\d.-]+)', line).group(1))
        elif 'HOMO-LUMO gap:' in line:
            homo_lumo_gap = float(re.search(r'gap:\s+([\d.-]+)', line).group(1))
        elif 'Farthest distance:' in line:
            farthest_distance = float(re.search(r'---\s+([\d.]+)', line).group(1))
        elif ' Radius of the system:' in line:
            mol_radius = float(re.search(r'system:\s+([\d.]+)', line).group(1))
        elif ' Length of the three sides:' in line:
            mol_size = list(map(float, re.findall(r'([\d.]+)', line)))
            sorted_mol_size = sorted(mol_size)
            mol_size_short = sorted_mol_size[0]
            mol_size_2 = sorted_mol_size[1]
            mol_size_l = sorted_mol_size[2]
            length_ratio = mol_size_l / sum(mol_size)
            len_div_diameter = mol_size_l / (2 * mol_radius)
        elif 'Molecular planarity parameter (MPP) is' in line:
            mpp = float(re.search(r'is\s+([\d.]+)', line).group(1))
        elif ' Span of deviation from plane (SDP) is' in line:
            sdp = float(re.search(r'is\s+([\d.]+)', line).group(1))   
        elif "Magnitude of dipole moment:" in line:
            dipole_moment = float(re.search(r'a.u.\s+([\d.]+)', line).group(1))
        elif "Magnitude: |Q_2|=" in line:
            quadrupole_moment = float(re.search(r'\|Q_2\|=\s+([\d.]+)', line).group(1))
        elif "Magnitude: |Q_3|=" in line:
            octopole_moment = float(re.search(r'\|Q_3\|=\s+([\d.]+)', line).group(1))

    partindex=0 
    for idx, line in enumerate(lines):
        if '       ================= Summary of surface analysis =================' in line:
            partindex+=1
            if partindex == 1:
                start_idx = idx + 2
                print(start_idx)           
                line = lines[start_idx]
                new_str = line.split('Volume: ')[1]
                new_str = new_str.split('Bohr^3')[0]
                volume = float(new_str)
                line = lines[start_idx+1]
                new_str = line.split('(M/V):')[1]
                new_str = new_str.split('g/cm^3')[0]
                density = float(new_str)
                line = lines[start_idx+2]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('kcal/mol   Maximal')[0]
                espmin = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('kcal/mol')[0]
                espmax = float(new_str)

                line = lines[start_idx+3]
                new_str = line.split('Overall surface area:')[1]
                new_str = new_str.split('Bohr^2 ')[0]
                overall_surf_area = float(new_str)
                line = lines[start_idx+4]
                new_str = line.split('area:')[1]
                new_str = new_str.split('Bohr^2 ')[0]
                pos_surf_area = float(new_str)
                line = lines[start_idx+5]
                new_str = line.split('area:')[1]
                new_str = new_str.split('Bohr^2 ')[0]
                neg_surf_area = float(new_str)
                line = lines[start_idx+6]

                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                overall_ave = float(new_str)
                line = lines[start_idx+7]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                pos_ave = float(new_str)
                line = lines[start_idx+8]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u.')[0]
                neg_ave = float(new_str)

                line = lines[start_idx+9]
                new_str = line.split(':')[1]
                new_str = new_str.split('a.u.')[0]
                Over_var = float(new_str)
                line = lines[start_idx+12]
                new_str = line.split(':')[1]
                nu = float(new_str)
                line = lines[start_idx+14]
                new_str = line.split(':')[1]
                new_str = new_str.split('a.u.')[0]
                Pi = float(new_str)
                line = lines[start_idx+15]
                new_str = line.split(':')[1]
                new_str = new_str.split('eV')[0]
                MPI = float(new_str)
                line = lines[start_idx+16]
                new_str = line.split('Angstrom^2  (')[1]
                new_str = new_str.split('%)')[0]
                nonpolar_area = float(new_str)
                line = lines[start_idx+17]
                new_str = line.split('Angstrom^2  (')[1]
                new_str = new_str.split('%)')[0]
                polar_area = float(new_str)
            elif partindex == 2:
                start_idx = idx + 4
                print(start_idx)           
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('eV,  ')[0]
                aliemin = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('eV')[0]
                aliemax = float(new_str)
                line = lines[start_idx+4]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                alie_ave = float(new_str)
                line = lines[start_idx+5]
                new_str = line.split(':')[1]
                new_str = new_str.split('a.u.')[0]
                alie_var = float(new_str)
            elif partindex == 3:
                start_idx = idx + 4
                print(start_idx)           
                line = lines[start_idx]
                new_str = line.split(' Minimal value:  ')[1]
                new_str = new_str.split('eV,  ')[0]
                leamin = float(new_str)
                new_str = line.split('Maximal value: ')[1]
                new_str = new_str.split('eV')[0]
                leamax = float(new_str)
                line = lines[start_idx+4]
                new_str = line.split('value:')[1]
                new_str = new_str.split('a.u. ')[0]
                lea_ave = float(new_str)
                line = lines[start_idx+7]
                new_str = line.split(':')[1]
                new_str = new_str.split('a.u.')[0]
                lea_var = float(new_str)

    data.append([sample_name, odi_homo_1, odi_homo, odi_lumo, odi_lumoadd1,odi_mean, odi_std, atom_num, weight, homo, homo_number, lumo, homo_lumo_gap, farthest_distance, mol_radius, 
                 mol_size_short, mol_size_2, mol_size_l, length_ratio, len_div_diameter, mpp, sdp, dipole_moment,quadrupole_moment,
                 octopole_moment,volume,density,espmin,espmax, 
                 overall_surf_area,pos_surf_area,neg_surf_area,overall_ave,pos_ave,neg_ave,Over_var,nu,Pi,MPI,nonpolar_area,
                 polar_area,aliemin,aliemax,alie_ave,alie_var,leamin,leamax,lea_ave,lea_var
                 ])
print(data)
df = pd.DataFrame(data, columns=['SampleName',  'ODI_HOMO_1', 'ODI_HOMO', 'ODI_LUMO', 'ODI_LUMO_Add1', 'ODI_Mean', 'ODI_Std','AtomNum', 
                                 'Weight', 'HOMO', 'HOMO_number', 'LUMO', 'HOMO_LUMO_Gap', 'Farthest_Distance', 'Mol_Radius',
                                 'Mol_Size_Short', 'Mol_Size_2', 'Mol_Size_L', 'Length_Ratio', 'Len_Div_Diameter', 'MPP', 'SDP', 
                                 'Dipole_Moment', 'Quadrupole_Moment','Octopole_Moment', 'Volume', 'Density', 'ESPmin', 'ESPmax', 
                                 'Overall_Surface_Area', 'Pos_Surface_Area', 'Neg_Surface_Area', 'Overall_Average', 'Pos_Average', 
                                 'Neg_Average', 'Overall_Variance', 'Nu', 'Pi', 'MPI', 'Nonpolar_Area',
                                 'Polar_Area', 'ALIEmin', 'ALIEmax', 'ALIE_Ave', 'ALIE_Var', 'LEAmin', 'LEAmax', 'LEA_Ave', 'LEA_Var'])
df.to_csv('Multwfn_analysis_feature_matrix3.csv', index=False)
    # atom_list_found = False
    # xyz = np.zeros((atom_num, 4))

    # for idx, line in enumerate(lines):
    #     if ' Atom list:' in line:
    #         atom_list_found = True
    #         start_idx = idx + 1
    #         break

    # if atom_list_found:
    #     for j in range(atom_num):
    #         line = lines[start_idx + j]
    #         charge_str = line.split('Charge:')[1].split('x,y,z(Bohr):')[0]
    #         xyz[j, 0] = float(charge_str)
    #         coords_str = line.split('x,y,z(Bohr): ')[1]
    #         coords = [float(val) for val in coords_str.split()]
    #         xyz[j, 1] = coords[0]
    #         xyz[j, 2] = coords[1]
    #         xyz[j, 3] = coords[2]
    #     print(xyz)
        