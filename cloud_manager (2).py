import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def create_vm():
    def submit_vm():
        vm_name = vm_name_entry.get()
        cpu = cpu_entry.get()
        memory = memory_entry.get()
        disk = disk_entry.get()
        try:
            subprocess.run(["qemu-img", "create", "-f", "qcow2", f"{vm_name}.qcow2", disk])
            subprocess.run(["qemu-system-x86_64", "-m", memory, "-smp", cpu, "-hda", f"{vm_name}.qcow2"])
            messagebox.showinfo("Success", "Virtual Machine created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create VM: {e}")
        vm_window.destroy()

    vm_window = tk.Toplevel()
    vm_window.title("Create Virtual Machine")

    tk.Label(vm_window, text="VM Name:").grid(row=0, column=0)
    vm_name_entry = tk.Entry(vm_window)
    vm_name_entry.grid(row=0, column=1)

    tk.Label(vm_window, text="CPUs:").grid(row=1, column=0)
    cpu_entry = tk.Entry(vm_window)
    cpu_entry.grid(row=1, column=1)

    tk.Label(vm_window, text="Memory (MB):").grid(row=2, column=0)
    memory_entry = tk.Entry(vm_window)
    memory_entry.grid(row=2, column=1)

    tk.Label(vm_window, text="Disk Size (e.g., 10G):").grid(row=3, column=0)
    disk_entry = tk.Entry(vm_window)
    disk_entry.grid(row=3, column=1)

    tk.Button(vm_window, text="Create", command=submit_vm).grid(row=4, columnspan=2)

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

def build_docker_image():
    dockerfile_path = filedialog.askopenfilename(title="Select Dockerfile")
    if not dockerfile_path:
        return

    def submit_image():
        image_name = image_name_entry.get()
        try:
            subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])
            messagebox.showinfo("Success", "Docker image built successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to build image: {e}")
        image_window.destroy()

    image_window = tk.Toplevel()
    image_window.title("Build Docker Image")

    tk.Label(image_window, text="Image Name (e.g., my_image:latest):").grid(row=0, column=0)
    image_name_entry = tk.Entry(image_window)
    image_name_entry.grid(row=0, column=1)

    tk.Button(image_window, text="Build", command=submit_image).grid(row=1, columnspan=2)

def list_docker_images():
    try:
        output = subprocess.check_output(["docker", "images"]).decode()
        messagebox.showinfo("Docker Images", output)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list images: {e}")

def list_running_containers():
    try:
        output = subprocess.check_output(["docker", "ps"]).decode()
        messagebox.showinfo("Running Containers", output)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list containers: {e}")

def stop_container():
    container_id = simple_input_dialog("Stop Container", "Enter the container ID or name to stop:")
    if container_id:
        try:
            subprocess.run(["docker", "stop", container_id])
            messagebox.showinfo("Success", "Container stopped successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop container: {e}")

def search_docker_image():
    image_name = simple_input_dialog("Search Docker Image", "Enter the image name/tag to search for:")
    if image_name:
        try:
            output = subprocess.check_output(["docker", "images", "--format", f"{{{{.Repository}}}}:{{{{.Tag}}}}", "|", "grep", image_name], shell=True).decode()
            messagebox.showinfo("Search Results", output)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search image: {e}")

def search_dockerhub():
    image_name = simple_input_dialog("Search DockerHub", "Enter the image name to search for:")
    if image_name:
        try:
            output = subprocess.check_output(["docker", "search", image_name]).decode()
            messagebox.showinfo("Search Results", output)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search DockerHub: {e}")

def pull_docker_image():
    image_name = simple_input_dialog("Pull Docker Image", "Enter the image name to pull from DockerHub:")
    if image_name:
        try:
            subprocess.run(["docker", "pull", image_name])
            messagebox.showinfo("Success", "Image pulled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pull image: {e}")

def simple_input_dialog(title, prompt):
    dialog = tk.Toplevel()
    dialog.title(title)
    
    tk.Label(dialog, text=prompt).pack()
    entry = tk.Entry(dialog)
    entry.pack()

    def submit():
        dialog.result = entry.get()
        dialog.destroy()

    tk.Button(dialog, text="Submit", command=submit).pack()
    dialog.wait_window()
    return getattr(dialog, "result", None)

def main():
    root = tk.Tk()
    root.title("Cloud Management System")

    tk.Button(root, text="Create Virtual Machine", command=create_vm).pack(fill=tk.X)
    tk.Button(root, text="Create Dockerfile", command=create_dockerfile).pack(fill=tk.X)
    tk.Button(root, text="Build Docker Image", command=build_docker_image).pack(fill=tk.X)
    tk.Button(root, text="List Docker Images", command=list_docker_images).pack(fill=tk.X)
    tk.Button(root, text="List Running Containers", command=list_running_containers).pack(fill=tk.X)
    tk.Button(root, text="Stop Container", command=stop_container).pack(fill=tk.X)
    tk.Button(root, text="Search Docker Image Locally", command=search_docker_image).pack(fill=tk.X)
    tk.Button(root, text="Search DockerHub", command=search_dockerhub).pack(fill=tk.X)
    tk.Button(root, text="Pull Docker Image", command=pull_docker_image).pack(fill=tk.X)
    tk.Button(root, text="Exit", command=root.destroy).pack(fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
