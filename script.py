import os
import json
from openpyxl import Workbook


def run_ansible_playbook(inventory, playbook):
    """Run the Ansible playbook."""
    command = f"ansible-playbook -i {inventory} {playbook}"
    os.system(command)


def read_results(servers):
    """Retrieve results from all servers."""
    results = {}
    for server in servers:
        try:
            os.system(f"scp {server}:/tmp/system_info.json ./")
            with open("system_info.json", "r") as f:
                results[server] = json.load(f)
        except Exception as e:
            print(f"Error retrieving results from {server}: {e}")
    return results


def write_to_excel(data):
    """Write the collected data to an Excel sheet."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "System Info"
    sheet.append(["Server", "CPU Frequency (MHz)", "Number of Cores", "Total Memory", "CPU Factor"])

    for server, info in data.items():
        sheet.append([
            server,
            info.get("cpu_frequency"),
            info.get("num_cores"),
            info.get("total_memory"),
            info.get("cpu_factor"),
        ])

    workbook.save("system_info.xlsx")
    print("Data saved to system_info.xlsx")


if __name__ == "__main__":
    # Step 1: Define the inventory and playbook file paths
    inventory_file = "server-inventory.ini"
    playbook_file = "gather_info.yml"

    # Step 2: Read the list of servers from the inventory file
    with open(inventory_file, "r") as f:
        servers = [
            line.strip() for line in f.readlines() if line.strip() and not line.startswith("[")
        ]

    # Step 3: Run the playbook
    run_ansible_playbook(inventory_file, playbook_file)

    # Step 4: Retrieve results from each server
    results = read_results(servers)

    # Step 5: Write results to an Excel file
    write_to_excel(results)
