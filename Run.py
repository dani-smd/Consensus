import matplotlib.pyplot as plt
from os.path import exists
import os

while True:
    os.system("cls")
    print("# --------- This is a simulator of POS --------- #")
    print("# ---------------------------------------------- #")
    print("# ---------- Select one of these items --------- #")
    print("    1- Input Values")
    print("    2- sha256")
    print("    3- BLAKE3")
    print("    4- Plot")
    print("    5- Generate Transaction Pool Dataset")
    print("    6- Exit")

    item = input("Write the number of item you want: ")
    if item == "1":
        if exists('input.txt'):
            os.remove('input.txt')
        # ---
        validators = input("Number of validators: ")
        blocks = input("Number of blocks: ")
        iterations = input("Number of iterations: ")
        watt = input("Average power consumption of a single node in watt: ")
        with open('input.txt', 'a') as the_file:
            the_file.write(f'{validators}\n')
            the_file.write(f'{blocks}\n')
            the_file.write(f'{iterations}\n')
            the_file.write(f'{watt}\n')
        the_file.close()
    elif item == "2":
        while True:
            os.system("cls")
            print("# --------- This is a simulator of POS --------- #")
            print("# --------------------sha256-------------------- #")
            print("# --------- Select one of these Metrics -------- #")
            print("    1- Latency")
            print("    2- Throughput")
            print("    3- Fault Tolerance")
            print("    4- Energy Consumption")
            print("    5- Back To Main Menu")

            item2 = input("Write the number of item you want: ")

            if item2 == "1":
                os.system("cls")
                print("# --- Latency selected for sha256 --- #")
                # C:\Users\Danial\Desktop\Projects\Ms.Zeinab - Iraq\Sybil Attack\.venv\Scripts\python.exe
                os.system("python sha256/POS__Latency.py")
                input("Press Enter to continue...")
            elif item2 == "2":
                os.system("cls")
                print("# --- Throughput selected for sha256 --- #")
                os.system("python sha256/POS__Throughput.py")
                input("Press Enter to continue...")
            elif item2 == "3":
                os.system("cls")
                print("# --- Fault Tolerance selected for sha256 --- #")
                os.system("python sha256/POS__Fault_Tolerance.py")
                input("Press Enter to continue...")
            elif item2 == "4":
                os.system("cls")
                print("# --- Energy Consumption selected for sha256 --- #")
                os.system("python sha256/POS__Energy_Consumption.py")
                input("Press Enter to continue...")
            elif item2 == "5":
                os.system("cls")
                input("Press enter to back to the main menu...")
            break
    elif item == "3":
        while True:
            os.system("cls")
            print("# --------- This is a simulator of POS --------- #")
            print("# --------------------BLAKE3-------------------- #")
            print("# --------- Select one of these Metrics -------- #")
            print("    1- Latency")
            print("    2- Throughput")
            print("    3- Fault Tolerance")
            print("    4- Energy Consumption")
            print("    5- Back To Main Menu")

            item2 = input("Write the number of item you want: ")

            if item2 == "1":
                os.system("cls")
                print("# --- Latency selected for BLAKE3 --- #")
                os.system("python blake3/POS__Latency.py")
                input("Press Enter to continue...")
            elif item2 == "2":
                os.system("cls")
                print("# --- Throughput selected for BLAKE3 --- #")
                os.system("python blake3/POS__Throughput.py")
                input("Press Enter to continue...")
            elif item2 == "3":
                os.system("cls")
                print("# --- Fault Tolerance selected for BLAKE3 --- #")
                os.system("python blake3/POS__Fault_Tolerance.py")
                input("Press Enter to continue...")
            elif item2 == "4":
                os.system("cls")
                print("# --- Energy Consumption selected for BLAKE3 --- #")
                os.system("python blake3/POS__Energy_Consumption.py")
                input("Press Enter to continue...")
            elif item2 == "5":
                os.system("cls")
                input("Press enter to back to the main menu...")
            break
    elif item == "4":
        os.system("cls")
        # --- blake3
        file1 = open('blake3/files/energy_blake3.txt', 'r')
        file2 = open('blake3/files/fault_blake3.txt', 'r')
        file3 = open('blake3/files/throughput_Blake3.txt', 'r')
        file4 = open('blake3/files/latency_blake3.txt', 'r')
        lines1 = file1.readlines()
        lines2 = file2.readlines()
        lines3 = file3.readlines()
        lines4 = file4.readlines()
        blake3 = []
        for line in lines1:
            blake3.append(float(line.strip()))
        file1.close()
        for line in lines2:
            blake3.append(float(line.strip()))
        file2.close()
        for line in lines3:
            blake3.append(float(line.strip()))
        file3.close()
        for line in lines4:
            blake3.append(float(line.strip()))
        file4.close()
        # --- sha256
        file1 = open('sha256/files/energy_sha256.txt', 'r')
        file2 = open('sha256/files/fault_sha256.txt', 'r')
        file3 = open('sha256/files/latency_sha256.txt', 'r')
        file4 = open('sha256/files/throughput_sha256.txt', 'r')
        lines1 = file1.readlines()
        lines2 = file2.readlines()
        lines3 = file3.readlines()
        lines4 = file4.readlines()
        sha256 = []
        for line in lines1:
            sha256.append(float(line.strip()))
        file1.close()
        for line in lines2:
            sha256.append(float(line.strip()))
        file2.close()
        for line in lines3:
            sha256.append(float(line.strip()))
        file3.close()
        for line in lines4:
            sha256.append(float(line.strip()))
        file4.close()
        # --- Latency
        y_latency = [blake3[3], sha256[2]]
        # --- TPS
        y_tps = [blake3[2], sha256[3]]
        # # --- Energy
        y_energy = [blake3[0], sha256[0]]
        # # --- Fault Tolerance
        y_fault = [blake3[1], sha256[1]]
        # --- Show Plot
        x_axis = ['blake3', 'sha256']

        colors = ['purple', 'teal']

        plot1 = plt.subplot2grid((2, 2), (0, 0))
        plot2 = plt.subplot2grid((2, 2), (0, 1))
        plot3 = plt.subplot2grid((2, 2), (1, 0))
        plot4 = plt.subplot2grid((2, 2), (1, 1))

        plot1.bar(x_axis, y_latency, color=colors)
        plot2.bar(x_axis, y_tps, color=colors)
        plot3.bar(x_axis, y_energy, color=colors)
        plot4.bar(x_axis, y_fault, color=colors)

        plot1.set_title("Latency (Second)")
        plot2.set_title("Throughput (TPS)")
        plot3.set_title("Energy Consumption (KWh)")
        plot4.set_title("Fault Tolerance (Percent)")

        plt.tight_layout()
        plt.show()

        input("Press Enter to continue...")
    elif item == "5":
        os.system("cls")
        while True:
            num_trn_pl = input("Enter number of transactions you want to generate: ")
            if num_trn_pl:
                os.system(f"python dataset_generator/transaction_pool.py {num_trn_pl}")
            break
        input("Press Enter to continue...")
    elif item == "6":
        break

    os.system("cls")
