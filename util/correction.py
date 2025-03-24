from doped.analysis import DefectsParser
dielectric = 9.9

dp = DefectsParser(
    output_path="MgO/Defects/",  # directory containing the defect calculation folders
    dielectric=dielectric,  # dielectric needed for charge corrections
    # processes=1,  # Can set the number of processes to 1 if you're having issues with multiprocessing
)

defect_entry = dp.defect_dict["Mg_O_+4"]
print(f"Charge: {defect_entry.charge_state:+} at site: {defect_entry.defect_supercell_site.frac_coords}")
print(f"Finite-size charge corrections: {defect_entry.corrections}")