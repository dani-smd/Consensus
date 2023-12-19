import subprocess

while True:

    print("# --- This is a simulator of POS with BLAKE3 --- #")
    print("# ---------------------------------------------- #")
    print("# -------- Select one of these metrics --------- #")
    print("    1- Latency")
    print("    2- Throughput")
    print("    3- Fault Tolerance")
    print("    4- Energy Consumption")
    print("    5- Exit")

    item = input("Write the number of item you want: ")

    if item == "1":
        subprocess.run("cls", shell=True)
        print("# --- Latency selected --- #")
        subprocess.run(["python", "POS__Latency.py"], shell=True)
        input("Press Enter to continue...")
    elif item == "2":
        subprocess.run("cls", shell=True)
        print("# --- Throughput selected --- #")
        subprocess.run(["python", "POS__Throughput.py"], shell=True)
        input("Press Enter to continue...")
    elif item == "3":
        subprocess.run("cls", shell=True)
        print("# --- Fault Tolerance selected --- #")
        subprocess.run(["python", "POS__Fault_Tolerance.py"], shell=True)
        input("Press Enter to continue...")
    elif item == "4":
        subprocess.run("cls", shell=True)
        print("# --- Energy Consumption selected --- #")
        subprocess.run(["python", "POS__Energy_Consumption.py"], shell=True)
        input("Press Enter to continue...")
    elif item == "5":
        break

    subprocess.run("cls", shell=True)
