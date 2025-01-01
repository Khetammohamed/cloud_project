import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
from functions import create_disk_image, create_vm, generate_dockerfile, build_docker_image, list_docker_images, list_running_containers, stop_container, search_local_image, search_dockerhub_image, pull_docker_image, create_dockerfile

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
        additional_files_var = tk.StringVar()
        dockerfile_path_var = tk.StringVar()
        docker_image_name_var = tk.StringVar()

        ttk.Label(docker_tab, text="Base Image:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Combobox(docker_tab, textvariable=base_image_var, values=["ubuntu:latest", "python:3.9", "node:16"]).grid(row=0, column=1, padx=5, pady=5)

        ttk.Checkbutton(docker_tab, text="Install Python", variable=install_python_var).grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(docker_tab, text="Additional Files:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=additional_files_var).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Browse", command=lambda: browse_file(additional_files_var)).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Dockerfile Path:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=dockerfile_path_var).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Save As", command=lambda: save_file(dockerfile_path_var)).grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Image Name:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(docker_tab, textvariable=docker_image_name_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(docker_tab, text="Generate Dockerfile", command=lambda: generate_dockerfile(
            base_image_var.get(),
            install_python_var.get(),
            additional_files_var.get(),
            dockerfile_path_var.get()
        )).grid(row=5, column=0, padx=5, pady=10)

        ttk.Button(docker_tab, text="Build Docker Image", command=lambda: build_docker_image(
            dockerfile_path_var.get(),
            docker_image_name_var.get()
        )).grid(row=5, column=1, padx=5, pady=10)
        ttk.Button(docker_tab, text="List Docker Images", command=list_docker_images).grid(row=6, column=0, padx=5, pady=10)
        ttk.Button(docker_tab, text="List Running Containers", command=list_running_containers).grid(row=6, column=1, padx=5, pady=10)

        ttk.Label(docker_tab, text="Container ID:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        container_id_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=container_id_var).grid(row=7, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Stop Container", command=lambda: stop_container(container_id_var.get())).grid(row=7, column=2, padx=5, pady=5)

        ttk.Label(docker_tab, text="Search Image Name:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        search_image_name_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=search_image_name_var).grid(row=8, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Search Local Image", command=lambda: search_local_image(search_image_name_var.get())).grid(row=8, column=2, padx=5, pady=5)
        ttk.Button(docker_tab, text="Search DockerHub Image", command=lambda: search_dockerhub_image(search_image_name_var.get())).grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(docker_tab, text="Pull Image Name:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
        pull_image_name_var = tk.StringVar()
        ttk.Entry(docker_tab, textvariable=pull_image_name_var).grid(row=10, column=1, padx=5, pady=5)
        ttk.Button(docker_tab, text="Pull Docker Image", command=lambda: pull_docker_image(pull_image_name_var.get())).grid(row=10, column=2, padx=5, pady=5)

        ttk.Button(docker_tab, text="Create Dockerfile", command=create_dockerfile).grid(row=11, column=0, columnspan=3, padx=5, pady=10)

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