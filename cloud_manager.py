import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

# VM Functions
def create_disk_image(path, size):
    try:
        cmd = ["qemu-img", "create", "-f", "qcow2", path, size]
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Disk image created at {path} with size {size}.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error occurred while creating the disk image: {e}")

def create_vm(name, cpu, memory, disk, iso_path):
    try:
        cmd = [
            "qemu-system-x86_64",
            "-name", name,
            "-m", memory,
            "-smp", f"cpus={cpu}",
            "-hda", disk,
            "-cdrom", iso_path,
            "-boot", "d",
            "-accel", "tcg",  # Use TCG accelerator
            "-serial", "file:vm_log.txt"  # Log output to a file
        ]
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Virtual machine '{name}' created successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error occurred while creating the VM: {e}")

# Docker Functions
def generate_dockerfile(base_image, install_python, copy_vm_disk, vm_disk_path, additional_files, path):
    try:
        # Generate Dockerfile content
        dockerfile_content = f"FROM {base_image}\n\n"

        if install_python:
            dockerfile_content += "RUN apt-get update && apt-get install -y python3 python3-pip\n"

        if copy_vm_disk and vm_disk_path:
            dockerfile_content += f"COPY {vm_disk_path} /app/vm-disk.img\n"  # Use .img extension

        if additional_files:
            dockerfile_content += f"COPY {additional_files} /app/\n"

        dockerfile_content += "\nCMD [\"bin/bash\"]\n"

        # Save Dockerfile
        with open(path, "w") as f:
            f.write(dockerfile_content)
        messagebox.showinfo("Success", f"Dockerfile created at {path}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create Dockerfile: {e}")

def build_docker_image(dockerfile, image_name):
    try:
        cmd = ["docker", "build", "-t", image_name, "-f", dockerfile, "."]
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Docker image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error occurred while building the Docker image: {e}")

# Additional Docker Utilities
def list_docker_images():
    try:
        result = subprocess.run(["docker", "images"], text=True, capture_output=True)
        messagebox.showinfo("Docker Images", result.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to list Docker images: {e}")

def list_running_containers():
    try:
        result = subprocess.run(["docker", "ps"], text=True, capture_output=True)
        messagebox.showinfo("Running Containers", result.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to list running containers: {e}")

def stop_container(container_id):
    try:
        subprocess.run(["docker", "stop", container_id], check=True)
        messagebox.showinfo("Success", f"Container {container_id} stopped successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to stop container {container_id}: {e}")

def search_local_image(image_name):
    try:
        result = subprocess.run(["docker", "images", image_name], text=True, capture_output=True)
        messagebox.showinfo("Search Results", result.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to search for image: {e}")

def search_dockerhub_image(image_name):
    try:
        result = subprocess.run(["docker", "search", image_name], text=True, capture_output=True)
        messagebox.showinfo("DockerHub Search Results", result.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to search on DockerHub: {e}")

def pull_docker_image(image_name):
    try:
        subprocess.run(["docker", "pull", image_name], check=True)
        messagebox.showinfo("Success", f"Image {image_name} pulled successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to pull image: {e}")

# GUI Functions
def main():
    
    
    def browse_file(var):
        var.set(filedialog.askopenfilename())

    def save_file(var):
        var.set(filedialog.asksaveasfilename(defaultextension=".Dockerfile"))

    # VM Tab
    def vm_tab_ui(vm_tab):
        ttk.Label(vm_tab, text="VM Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        vm_name = tk.Entry(vm_tab)
        vm_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(vm_tab, text="CPU Cores:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        cpu_cores = tk.Entry(vm_tab)
        cpu_cores.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(vm_tab, text="Memory (MB):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        memory_size = tk.Entry(vm_tab)
        memory_size.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(vm_tab, text="Disk Path:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        file_path = tk.StringVar()
        ttk.Entry(vm_tab, textvariable=file_path).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(vm_tab, text="Browse", command=lambda: save_file(file_path)).grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(vm_tab, text="Disk Size (e.g., 10G):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        disk_size = tk.Entry(vm_tab)
        disk_size.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(vm_tab, text="ISO Path:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        iso_path = tk.StringVar()
        ttk.Entry(vm_tab, textvariable=iso_path).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(vm_tab, text="Browse", command=lambda: browse_file(iso_path)).grid(row=5, column=2, padx=5, pady=5)

        ttk.Button(vm_tab, text="Create Disk", command=lambda: create_disk_image(file_path.get(), disk_size.get())).grid(row=6, column=0, padx=5, pady=10)
        ttk.Button(vm_tab, text="Create VM", command=lambda: create_vm(vm_name.get(), cpu_cores.get(), memory_size.get(), file_path.get(), iso_path.get())).grid(row=6, column=1, padx=5, pady=10)

    # Docker Tab
    def docker_tab_ui(docker_tab):
        base_image_var = tk.StringVar(value="ubuntu:latest")
        install_python_var = tk.BooleanVar()
        copy_vm_disk_var = tk.BooleanVar()
        vm_disk_path_var = tk.StringVar()
        additional_files_var = tk.StringVar()
        dockerfile_path_var = tk.StringVar()
        docker_image_name_var = tk.StringVar()

        ttk.Label(docker_tab, text="Base Image:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Combobox(docker_tab, textvariable=base_image_var, values=["ubuntu:latest", "python:3.9", "node:16"]).grid(row=0, column=1, padx=5, pady=5)

        ttk.Checkbutton(docker_tab, text="Install Python", variable=install_python_var).grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(docker_tab, text="Copy VM Disk", variable=copy_vm_disk_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(docker_tab, text="VM Disk Path:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=vm_disk_path_var).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Browse", command=lambda: browse_file(vm_disk_path_var)).grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Additional Files:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=additional_files_var).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Browse", command=lambda: browse_file(additional_files_var)).grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Dockerfile Path:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=dockerfile_path_var).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Save As", command=lambda: save_file(dockerfile_path_var)).grid(row=5, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Image Name:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=docker_image_name_var).grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(docker_tab, text="Generate Dockerfile", command=lambda: generate_dockerfile(
            base_image_var.get(),
            install_python_var.get(),
            copy_vm_disk_var.get(),
            vm_disk_path_var.get(),
            additional_files_var.get(),
            dockerfile_path_var.get()
        )).grid(row=7, column=0, padx=5, pady=10)

        ttk.Button(docker_tab, text="Build Docker Image", command=lambda: build_docker_image(
            dockerfile_path_var.get(),
            docker_image_name_var.get()
        )).grid(row=7, column=1, padx=5, pady=10)
        ttk.Button(docker_tab, text="List Docker Images", command=list_docker_images).grid(row=8, column=0, padx=5, pady=10)
        ttk.Button(docker_tab, text="List Running Containers", command=list_running_containers).grid(row=8, column=1, padx=5, pady=10)

        ttk.Label(docker_tab, text="Container ID:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        container_id_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=container_id_var).grid(row=9, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Stop Container", command=lambda: stop_container(container_id_var.get())).grid(row=9, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Search Image Name:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
        search_image_name_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=search_image_name_var).grid(row=10, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Search Local Image", command=lambda: search_local_image(search_image_name_var.get())).grid(row=10, column=2, padx=5, pady=5)
        ttk.Button(docker_tab, text="Search DockerHub Image", command=lambda: search_dockerhub_image(search_image_name_var.get())).grid(row=11, column=1, padx=5, pady=5)

        ttk.Label(docker_tab, text="Pull Image Name:").grid(row=12, column=0, padx=5, pady=5, sticky="e")
        pull_image_name_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=pull_image_name_var).grid(row=12, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Pull Docker Image", command=lambda: pull_docker_image(pull_image_name_var.get())).grid(row=12, column=2, padx=5, pady=5)

    # Main Window
    root = tk.Tk()
    root.title("Cloud Management System")
    root.configure(bg="#f0f0f0")  # Set the background color

    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")  # Use a modern theme
    style.configure("TLabel", background="#f0f0f0", foreground="#333333", font=("Helvetica", 12))
    style.configure("TButton", background="#0078d7", foreground="white", font=("Helvetica", 10, "bold"))
    style.configure("TEntry", font=("Helvetica", 10))

    # Header
    header = tk.Label(root, text="Cloud Management System", bg="#0078d7", fg="white", font=("Helvetica", 16, "bold"))
    header.pack(fill="x", pady=10)

    notebook = ttk.Notebook(root)
    vm_tab = ttk.Frame(notebook)
    docker_tab = ttk.Frame(notebook)

    vm_tab_ui(vm_tab)
    docker_tab_ui(docker_tab)

    notebook.add(vm_tab, text="VM Management")
    notebook.add(docker_tab, text="Docker Management")
    notebook.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
