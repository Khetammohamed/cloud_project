import os
import tkinter as tk
from tkinter import filedialog, messagebox
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
            "-m", str(memory),
            "-smp", f"cpus={cpu}",
            "-hda", disk,
            "-cdrom", iso_path,
            "-boot", "d",
            "-accel","whpx"
        ]
        subprocess.run(cmd, check=True)
        messagebox.showinfo("Success", f"Virtual machine '{name}' created successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error occurred while creating the VM: {e}")

# Docker Functions
def generate_dockerfile(base_image, install_python, additional_files, path):
    try:
        # Generate Dockerfile content
        dockerfile_content = f"FROM {base_image}\n\n"

        if install_python:
            dockerfile_content += "RUN apt-get update && apt-get install -y python3 python3-pip\n"

        if additional_files:
            dockerfile_content += f"COPY {additional_files} /app/\n"

        dockerfile_content += "\nCMD [\"/bin/bash\"]\n"

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

def create_dockerfile():
    path = filedialog.askdirectory(title="Select Directory to Save Dockerfile")
    if not path:
        return

    def save_dockerfile():
        content = dockerfile_text.get("1.0", tk.END)
        try:
            with open(os.path.join(path, "Dockerfile"), "w") as f:
                f.write(content)
            messagebox.showinfo("Success", "Dockerfile created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Dockerfile: {e}")
        dockerfile_window.destroy()

    dockerfile_window = tk.Toplevel()
    dockerfile_window.title("Create Dockerfile")

    tk.Label(dockerfile_window, text="Dockerfile Content:").pack()
    dockerfile_text = tk.Text(dockerfile_window, height=15, width=50)
    dockerfile_text.pack()

    tk.Button(dockerfile_window, text="Save", command=save_dockerfile).pack()