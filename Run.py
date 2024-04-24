import matplotlib.pyplot as plt
from os.path import exists
import time
import os

from sha.POS__Latency import Network as latencyNetwork
from sha.POS__Throughput import Network as throughputNetwork
from sha.POS__Fault_Tolerance import Network as faultNetwork
from sha.POS__Energy_Consumption import Network as energyNetwork

from blake.POS__Latency import Network as blakeLatencyNetwork
from blake.POS__Throughput import Network as blakeThroughputNetwork
from blake.POS__Fault_Tolerance import Network as blakeFaultNetwork
from blake.POS__Energy_Consumption import Network as blakeEnergyNetwork

while True:
    os.system("cls")
    print("# --------- This is a simulator of POS --------- #")
    print("# ---------------------------------------------- #")
    print("# ---------- Select one of these items --------- #")
    print("    1- Input Values")
    print("    2- SHA256")
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
            print("# --------------------SHA256-------------------- #")
            print("# --------- Select one of these Metrics -------- #")
            print("    1- Latency")
            print("    2- Throughput")
            print("    3- Fault Tolerance")
            print("    4- Energy Consumption")
            print("    5- Back To Main Menu")

            item2 = input("Write the number of item you want: ")

            if item2 == "1":
                os.system("cls")
                print("# --- Latency selected for sha --- #")

                input_file = open('input.txt', 'r')
                input_lines = input_file.readlines()
                metrics = []
                for line in input_lines:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # ---
                if exists('sha/latency_sha256.txt'):
                    os.remove('sha/latency_sha256.txt')
                if exists('sha/Latency(sha)_Blockchain.json'):
                    os.remove('sha/Latency(sha)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = latencyNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, status)
                    else:
                        status = False
                        network.simulate(num_blocks, status)
                # ---
                result = open('sha/latency.txt', 'r')
                result_lines = result.readlines()
                result.close()
                # ---
                count = 0
                # Strips the newline character
                for result_line in result_lines:
                    count += float(result_line.strip())
                # ---
                latency = (count / iteration) / 10
                with open('sha/latency_sha256.txt', 'a') as the_file:
                    the_file.write(f'{latency:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Latency per block: {latency:.6f} seconds")
                if exists('sha/latency.txt'):
                    os.remove('sha/latency.txt')
                # os.system("python sha/POS__Latency.py")
                input("Press Enter to continue...")
            elif item2 == "2":
                os.system("cls")
                print("# --- Throughput selected for sha --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # ---
                if exists('sha/throughput_sha256.txt'):
                    os.remove('sha/throughput_sha256.txt')
                if exists('sha/Throughput(sha)_Blockchain.json'):
                    os.remove('sha/Throughput(sha)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = throughputNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, status)
                    else:
                        status = False
                        network.simulate(num_blocks, status)
                # ---
                file1 = open('sha/throughput.txt', 'r')
                lines = file1.readlines()
                file1.close()
                # ---
                count = 0
                # Strips the newline character
                for line in lines:
                    count += float(line.strip())
                # ---
                throughput = count / iteration
                with open('sha/throughput_sha256.txt', 'a') as the_file:
                    the_file.write(f'{throughput:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Throughput: {throughput:.6f} transactions per second")
                if exists('sha/throughput.txt'):
                    os.remove('sha/throughput.txt')
                input("Press Enter to continue...")
            elif item2 == "3":
                os.system("cls")
                print("# --- Fault Tolerance selected for sha --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # ---
                if exists('sha/fault_sha256.txt'):
                    os.remove('sha/fault_sha256.txt')
                if exists('sha/Fault_Tolerance(sha)_Blockchain.json'):
                    os.remove('sha/Fault_Tolerance(sha)_Blockchain.json')
                # ---
                network = faultNetwork(num_validators)
                network.simulate(num_blocks)
                fault_tolerance, f = network.calculate_fault_tolerance()
                with open('sha/fault_sha256.txt', 'a') as the_file:
                    the_file.write(f'{fault_tolerance * 100}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Fault tolerance: {fault_tolerance * 100} %")
                print(
                    f"The Result Of 2F+1 Is Equal = {f}, It Means you Need At Least {f} Node For The POS Consensus To Work!")
                input("Press Enter to continue...")
            elif item2 == "4":
                os.system("cls")
                print("# --- Energy Consumption selected for sha --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # --- Average power consumption of a single node in watts
                avg_power = metrics[3]
                # ---
                if exists('sha/energy_sha256.txt'):
                    os.remove('sha/energy_sha256.txt')
                if exists('sha/Energy_Consumption(sha)_Blockchain.json'):
                    os.remove('sha/Energy_Consumption(sha)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = energyNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, avg_power, num_validators, status)
                    else:
                        status = False
                        network.simulate(num_blocks, avg_power, num_validators, status)
                # ---
                file1 = open('sha/energy.txt', 'r')
                lines = file1.readlines()
                file1.close()
                # ---
                count = 0
                # Strips the newline character
                for line in lines:
                    count += float(line.strip())
                # ---
                energy = count / iteration
                with open('sha/energy_sha256.txt', 'a') as the_file:
                    the_file.write(f'{energy:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Energy Consumption: {energy:.6f} Kwh")
                if exists('sha/energy.txt'):
                    os.remove('sha/energy.txt')
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
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # ---
                if exists('blake/latency_blake3.txt'):
                    os.remove('blake/latency_blake3.txt')
                if exists('blake/Latency(blake)_Blockchain.json'):
                    os.remove('blake/Latency(blake)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = blakeLatencyNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, status)
                    else:
                        status = False
                        network.simulate(num_blocks, status)
                # ---
                file1 = open('blake/latency.txt', 'r')
                lines = file1.readlines()
                file1.close()
                # ---
                count = 0
                # Strips the newline character
                for line in lines:
                    count += float(line.strip())
                # ---
                latency = (count / iteration) / 10
                with open('blake/latency_blake3.txt', 'a') as the_file:
                    the_file.write(f'{latency:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Latency per block: {latency:.6f} seconds")
                if exists('blake/latency.txt'):
                    os.remove('blake/latency.txt')
                input("Press Enter to continue...")
            elif item2 == "2":
                os.system("cls")
                print("# --- Throughput selected for BLAKE3 --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # ---
                if exists('blake/throughput_Blake3.txt'):
                    os.remove('blake/throughput_Blake3.txt')
                if exists('blake/Throughput(blake)_Blockchain.json'):
                    os.remove('blake/Throughput(blake)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = blakeThroughputNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, status)
                    else:
                        status = False
                        network.simulate(num_blocks, status)
                # ---
                file1 = open('blake/throughput.txt', 'r')
                lines = file1.readlines()
                file1.close()
                # ---
                count = 0
                # Strips the newline character
                for line in lines:
                    count += float(line.strip())
                # ---
                throughput = count / iteration
                with open('blake/throughput_Blake3.txt', 'a') as the_file:
                    the_file.write(f'{throughput:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Throughput: {throughput:.6f} transactions per second")
                if exists('blake/throughput.txt'):
                    os.remove('blake/throughput.txt')
                input("Press Enter to continue...")
            elif item2 == "3":
                os.system("cls")
                print("# --- Fault Tolerance selected for BLAKE3 --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # ---
                if exists('blake/fault_blake3.txt'):
                    os.remove('blake/fault_blake3.txt')
                if exists('blake/Fault_Tolerance(blake)_Blockchain.json'):
                    os.remove('blake/Fault_Tolerance(blake)_Blockchain.json')
                # ---
                network = blakeFaultNetwork(num_validators)
                network.simulate(num_blocks)
                fault_tolerance, f = network.calculate_fault_tolerance()
                with open('blake/fault_blake3.txt', 'a') as the_file:
                    the_file.write(f'{fault_tolerance * 100}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Fault tolerance: {fault_tolerance * 100} %")
                print(
                    f"The Result Of 2F+1 Is Equal = {f}, It Means you Need At Least {f} Node For The POS Consensus To Work!")
                input("Press Enter to continue...")
            elif item2 == "4":
                os.system("cls")
                print("# --- Energy Consumption selected for BLAKE3 --- #")
                file1 = open('input.txt', 'r')
                lines1 = file1.readlines()
                metrics = []
                for line in lines1:
                    metrics.append(int(line.strip()))
                # --- Number of validators
                num_validators = metrics[0]
                # --- Number of blocks
                num_blocks = metrics[1]
                # --- Number of iterations
                iteration = metrics[2]
                # --- Average power consumption of a single node in watts
                avg_power = metrics[3]
                # ---
                if exists('blake/energy_blake3.txt'):
                    os.remove('blake/energy_blake3.txt')
                if exists('blake/Energy_Consumption(blake)_Blockchain.json'):
                    os.remove('blake/Energy_Consumption(blake)_Blockchain.json')
                # ---
                for i in range(0, iteration):
                    network = blakeEnergyNetwork(num_validators)
                    if i == 0:
                        status = True
                        network.simulate(num_blocks, avg_power, num_validators, status)
                    else:
                        status = False
                        network.simulate(num_blocks, avg_power, num_validators, status)
                # ---
                file1 = open('blake/energy.txt', 'r')
                lines = file1.readlines()
                file1.close()
                # ---
                count = 0
                # Strips the newline character
                for line in lines:
                    count += float(line.strip())
                # ---
                energy = count / iteration
                with open('blake/energy_blake3.txt', 'a') as the_file:
                    the_file.write(f'{energy:.6f}\n')
                the_file.close()
                print("Processing . . . ")
                time.sleep(2)
                print(f"Energy Consumption: {energy:.6f} Kwh")
                if exists('blake/energy.txt'):
                    os.remove('blake/energy.txt')
                input("Press Enter to continue...")
            elif item2 == "5":
                os.system("cls")
                input("Press enter to back to the main menu...")
            break
    elif item == "4":
        os.system("cls")
        # --- blake
        input_file = open('blake/files/energy_blake3.txt', 'r')
        file2 = open('blake/files/fault_blake3.txt', 'r')
        file3 = open('blake/files/throughput_Blake3.txt', 'r')
        file4 = open('blake/files/latency_blake3.txt', 'r')
        input_lines = input_file.readlines()
        lines2 = file2.readlines()
        lines3 = file3.readlines()
        lines4 = file4.readlines()
        blake3 = []
        for line in input_lines:
            blake3.append(float(line.strip()))
        input_file.close()
        for line in lines2:
            blake3.append(float(line.strip()))
        file2.close()
        for line in lines3:
            blake3.append(float(line.strip()))
        file3.close()
        for line in lines4:
            blake3.append(float(line.strip()))
        file4.close()
        # --- sha
        input_file = open('sha/files/energy_sha256.txt', 'r')
        file2 = open('sha/files/fault_sha256.txt', 'r')
        file3 = open('sha/files/latency_sha256.txt', 'r')
        file4 = open('sha/files/throughput_sha256.txt', 'r')
        input_lines = input_file.readlines()
        lines2 = file2.readlines()
        lines3 = file3.readlines()
        lines4 = file4.readlines()
        sha256 = []
        for line in input_lines:
            sha256.append(float(line.strip()))
        input_file.close()
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
        x_axis = ['blake', 'sha']

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
