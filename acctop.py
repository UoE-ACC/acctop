"""
This script provides a real-time system resource monitoring tool that displays various system metrics in the terminal.
It uses the `psutil` library to gather system information and the `tabulate` library to format the output in a readable manner.

Features:
- Disk Usage: Displays total, used, and free disk space along with a colored usage bar.
- Memory Usage: Shows total, used, and available memory with a colored usage bar.
- CPU Usage: Dynamically adjusts the number of columns based on terminal width and displays per-core CPU usage with colored bars.
- User Usage: Aggregates CPU and memory usage by user and displays the process count for each user.
- Network Usage: (Commented out) Displays network statistics including bytes sent/received and packets sent/received per network interface.
- Load Average: (Commented out) Shows the system load average for the past 1, 5, and 15 minutes.
- System Info: (Commented out) Displays system uptime and kernel version.

The script uses ANSI escape codes to add color to the terminal output, making it easier to read and interpret the data.

Functions:
- get_usage_color(percentage): Returns an ANSI color code based on the CPU usage percentage.
- create_cpu_usage_bar(percentage, bar_length=10): Returns a string representing an ASCII bar chart of CPU usage with color.
- create_memory_usage_bar(percentage, bar_length=30): Returns a string representing an ASCII bar chart of memory usage with color.
- create_disk_usage_bar(percentage, bar_length=30): Returns a string representing an ASCII bar chart of disk usage with color.
- display_disk_usage(): Displays disk usage statistics with a colored usage bar.
- display_memory_usage(): Displays memory usage statistics with a colored usage bar.
- get_cpu_columns(): Determines the number of columns to use for CPU usage display based on terminal width.
- display_cpu_usage_in_columns(): Displays per-core CPU usage in dynamically adjusted columns with colored bars.
- display_user_usage(): Displays cumulative CPU, memory usage, and process count for each user.
- display_network_usage(): (Commented out) Displays network usage statistics with aligned columns and colored headers.
- display_load_average(): (Commented out) Displays the system load average for the past 1, 5, and 15 minutes.
- display_system_info(): (Commented out) Displays system uptime and kernel version.
- clear_console(): Clears the terminal screen.
- main(): Main loop that updates the display every 2.5 seconds.

Usage:
Run the script in a terminal to start real-time monitoring. Press Ctrl+C to exit.
"""
import os
import psutil
import time
from collections import defaultdict
from tabulate import tabulate

# ANSI escape codes for colors
HEADER_COLOR    = "\033[1;34m"  # Bold Blue
CPU_COLOR       = "\033[1;35m"  # Bold Magenta"
MEMORY_COLOR    = "\033[1;35m"  # Bold Magenta"
DISK_COLOR      = "\033[1;35m"  # Bold Magenta"
NETWORK_COLOR   = "\033[1;35m"  # Bold Magenta
USER_COLOR      = "\033[1;35m"  # Bold Magenta"
LOAD_COLOR      = "\033[1;35m"  # Bold Magenta"
RESET_COLOR     = "\033[0m"     # Reset to default

# Additional ANSI escape codes for CPU and memory usage bars
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"

def get_usage_color(percentage):
    """Returns an ANSI color code based on the CPU usage percentage."""
    if percentage < 50:
        return GREEN
    elif percentage < 80:
        return YELLOW
    else:
        return RED

def create_cpu_usage_bar(percentage, bar_length=10):
    """Returns a string representing an ASCII bar chart of CPU usage with color."""
    color = get_usage_color(percentage)
    num_bars = int((percentage / 100) * bar_length)
    return f"{color}[{'#' * num_bars}{' ' * (bar_length - num_bars)}] {percentage:6.2f}%{RESET_COLOR}"

def create_memory_usage_bar(percentage, bar_length=30):
    """Returns a string representing an ASCII bar chart of memory usage with color."""
    color = get_usage_color(percentage)
    num_bars = int((percentage / 100) * bar_length)
    return f"{color}[{'#' * num_bars}{' ' * (bar_length - num_bars)}] {percentage:6.2f}%{RESET_COLOR}"

def create_disk_usage_bar(percentage, bar_length=30):
    """Returns a string representing an ASCII bar chart of disk usage with color."""
    color = get_usage_color(percentage)
    num_bars = int((percentage / 100) * bar_length)
    return f"{color}[{'#' * num_bars}{' ' * (bar_length - num_bars)}] {percentage:6.2f}%{RESET_COLOR}"

def display_disk_usage():
    disk_usage = psutil.disk_usage('/')
    print(f"{DISK_COLOR}=== Disk Usage ==={RESET_COLOR}")
    usage_percentage = disk_usage.percent
    print(f"Total: {disk_usage.total / (1024 ** 3):.2f} GB | "
          f"Used: {disk_usage.used / (1024 ** 3):.2f} GB | "
          f"Free: {disk_usage.free / (1024 ** 3):.2f} GB | "
          f"{create_disk_usage_bar(usage_percentage)}")
    print("")

def display_memory_usage():
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()

    # Determine the width of each column
    total_width = max(len(f"{memory_info.total / (1024 ** 3):.2f} GB"), len(f"{swap_info.total / (1024 ** 3):.2f} GB")) + 2
    used_width = max(len(f"{memory_info.used / (1024 ** 3):.2f} GB"), len(f"{swap_info.used / (1024 ** 3):.2f} GB")) + 2
    available_width = len(f"{memory_info.available / (1024 ** 3):.2f} GB") + 2
    percent_width = max(len(f"{memory_info.percent}%"), len(f"{swap_info.percent}%")) + 2

    # Print Memory Usage
    print(f"{MEMORY_COLOR}=== Memory Usage ==={RESET_COLOR}")
    print(f"Total: {f'{memory_info.total / (1024 ** 3):.2f} GB'} | "
          f"Used: {f'{memory_info.used / (1024 ** 3):.2f} GB'} | "
          f"Available: {f'{memory_info.available / (1024 ** 3):.2f} GB'} | "
          f"{f'{create_memory_usage_bar(memory_info.percent)}'}")

    # Print bars
    # print(f"{create_memory_usage_bar(memory_info.percent)}")
    # print(f"{create_memory_usage_bar(swap_info.percent)}")
    print("")

def get_cpu_columns():
    try:
        terminal_width = os.get_terminal_size().columns
        if terminal_width < 50:
            return 1  # Narrow terminal, use 1 column
        elif 50 <= terminal_width < 100:
            return 2  # Medium terminal, use 2 columns
        elif 100 <= terminal_width < 150:
            return 3  # Wide terminal, use 3 columns
        elif 150 <= terminal_width < 200:
            return 4  # Extra wide terminal, use 4 columns
        else:
            return 5  # Extra extra wide terminal, use 5 columns
    except OSError:
        return 2  # Default to 2 columns if terminal size cannot be determined

def display_cpu_usage_in_columns():
    print(f"{CPU_COLOR}=== CPU Usage (Dynamic Columns) ==={RESET_COLOR}")

    cpu_percentages = psutil.cpu_percent(percpu=True)

    # Determine the number of columns based on terminal width
    columns = get_cpu_columns()

    # Determine the width needed for the core labels, bars, and percentages
    num_cores = len(cpu_percentages)
    # print(num_cores)
    # input()


    core_label_width = len(f"Core {num_cores}")-2
    max_bar_length = max(len(create_cpu_usage_bar(p).rstrip()) for p in cpu_percentages)
    max_percentage_width = max(len(f"{p:6.2f}%") for p in cpu_percentages)

    # Total column width (bar + percentage + spacing)
    column_width = max_bar_length + max_percentage_width + 5  # Extra space for spacing and formatting

    # Prepare rows for display based on the number of columns
    row_format = "".join([f"{{:<{column_width}}}" for _ in range(columns)])

    # Prepare the data to be displayed in rows
    row_data = []
    for i, percentage in enumerate(cpu_percentages):
        bar = create_cpu_usage_bar(percentage)
        entry = f"Core {i:<{core_label_width}}: {bar}  "
        row_data.append(entry)

        # When we have enough data for a full row or it's the last core, print the row
        if (i + 1) % columns == 0 or i == len(cpu_percentages) - 1:
            # Pad the row if necessary (if not enough columns are filled)
            while len(row_data) < columns:
                row_data.append(" " * column_width)  # Add empty string to fill the columns
            print(row_format.format(*row_data))
            row_data = []  # Reset for the next row
    print(f"Overall CPU Usage: {get_usage_color(psutil.cpu_percent())}{psutil.cpu_percent()}%{RESET_COLOR}")
    print("")

def display_user_usage():
    print(f"{USER_COLOR}=== Cumulative User CPU, Memory Usage, and Process Count ==={RESET_COLOR}")

    # Define thresholds
    cpu_threshold = 0.01  # CPU usage threshold in percent
    memory_threshold = 0.01  # Memory usage threshold in percent

    # Dictionary to store cumulative CPU, memory usage, and process count for each user
    user_usage = defaultdict(lambda: {'cpu': 0.0, 'memory': 0.0, 'processes': 0})

    # Get the number of CPUs (cores)
    num_cpus = psutil.cpu_count()

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            # Get process information
            proc_info = proc.info
            username = proc_info['username']
            if username:  # Ensure the process has a valid username
                # Accumulate the CPU and memory usage for each user
                user_data = user_usage[username]
                user_data['cpu'] += proc_info['cpu_percent']
                user_data['memory'] += proc_info['memory_percent']
                # Increment the process count for the user
                user_data['processes'] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Filter users based on the thresholds
    filtered_user_data = [
        {
            'Username': user,
            'CPU Usage (%)': f"{get_usage_color((usage['cpu'] / num_cpus))}{(usage['cpu'] / num_cpus):.2f}{RESET_COLOR}",
            'Memory Usage (%)': f"{get_usage_color(usage['memory'])}{usage['memory']:.2f}{RESET_COLOR}",
            'Process Count': usage['processes']
        }
        for user, usage in user_usage.items()
        if (usage['cpu'] / num_cpus) > cpu_threshold or usage['memory'] > memory_threshold
    ]

    # Display the filtered data in a table
    if filtered_user_data:
        print(tabulate(filtered_user_data, headers='keys', tablefmt='pretty'))
    else:
        print("No users exceed the specified thresholds.")
    print("")

def display_network_usage():
    print(f"{NETWORK_COLOR}=== Network Usage ==={RESET_COLOR}")
    net_io = psutil.net_io_counters(pernic=True)

    # Determine the width of each column
    iface_width = max(len(iface) for iface in net_io.keys()) + 2
    sent_width = 20
    recv_width = 20
    packets_sent_width = 15
    packets_recv_width = 15

    # Header row with colored titles
    header = (f"{HEADER_COLOR}{'Interface'.ljust(iface_width)} | "
              f"{'Bytes Sent'.rjust(sent_width)} | "
              f"{'Bytes Received'.rjust(recv_width)} | "
              f"{'Packets Sent'.rjust(packets_sent_width)} | "
              f"{'Packets Received'.rjust(packets_recv_width)}{RESET_COLOR}")
    print(header)
    print("-" * len(header))

    # Data rows
    for interface, stats in net_io.items():
        print(f"{interface.ljust(iface_width)} | "
              f"{stats.bytes_sent / (1024 ** 2):.2f} MB".rjust(sent_width) + " | "
              f"{stats.bytes_recv / (1024 ** 2):.2f} MB".rjust(recv_width) + " | "
              f"{stats.packets_sent}".rjust(packets_sent_width) + " | "
              f"{stats.packets_recv}".rjust(packets_recv_width))

def display_load_average():
    print(f"{LOAD_COLOR}=== Load Average ==={RESET_COLOR}")
    load_avg = os.getloadavg()  # Returns a tuple of (1min, 5min, 15min load averages)
    print(f"1 min: {load_avg[0]:.2f} | "
          f"5 min: {load_avg[1]:.2f} | "
          f"15 min: {load_avg[2]:.2f}")

def display_system_info():
    print(f"{HEADER_COLOR}=== System Info ==={RESET_COLOR}")
    uptime_seconds = time.time() - psutil.boot_time()
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    kernel_version = os.uname().release
    print(f"Uptime: {uptime}")
    print(f"Kernel Version: {kernel_version}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        while True:
            clear_console()  # Clear the screen
            print(f"{HEADER_COLOR}=== Real-Time System Resource Usage for {os.uname().nodename.capitalize()} ==={RESET_COLOR}")
            display_disk_usage()  # Disk usage with a bar
            display_memory_usage()  # Memory usage with a bar
            display_cpu_usage_in_columns()  # Dynamically set number of columns based on terminal width
            display_user_usage()  # Cumulative user usage with CPU normalized by number of cores
            # display_network_usage()  # Network usage with aligned columns and colored headers
            # display_load_average()  # Load average
            # display_system_info()  # System uptime and kernel version
            print(f"{HEADER_COLOR}========================================{RESET_COLOR}")
            print('Press ctrl+c to exit...')
            time.sleep(2.5)  # Update every 2.5 seconds
    except KeyboardInterrupt:
        print("\nExiting real-time monitoring.")

if __name__ == "__main__":
    main()
