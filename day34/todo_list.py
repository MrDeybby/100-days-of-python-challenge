import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Todo List")
    root.geometry("420x520")
    root.resizable(False, False)

    frame_top = tk.Frame(root, padx=10, pady=10)
    frame_top.pack(fill="x")

    task_var = tk.StringVar()
    entry = tk.Entry(frame_top, textvariable=task_var, width=30)
    entry.pack(side="left", fill="x", expand=True)
    entry.focus_set()

    def add_task() -> None:
        task = task_var.get().strip()
        if task:
            listbox.insert(tk.END, task)
            task_var.set("")

    add_btn = tk.Button(frame_top, text="Add", width=8, command=add_task)
    add_btn.pack(side="left", padx=(8, 0))

    frame_list = tk.Frame(root, padx=10, pady=10)
    frame_list.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame_list, orient="vertical")
    listbox = tk.Listbox(
        frame_list,
        height=18,
        yscrollcommand=scrollbar.set,
        selectmode=tk.SINGLE,
    )
    scrollbar.config(command=listbox.yview)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_bottom = tk.Frame(root, padx=10, pady=10)
    frame_bottom.pack(fill="x")

    def delete_task() -> None:
        selection = listbox.curselection()
        if selection:
            listbox.delete(selection[0])

    def clear_tasks() -> None:
        listbox.delete(0, tk.END)

    del_btn = tk.Button(frame_bottom, text="Delete", width=10, command=delete_task)
    del_btn.pack(side="left", padx=(0, 8))

    clear_btn = tk.Button(frame_bottom, text="Clear All", width=10, command=clear_tasks)
    clear_btn.pack(side="left")

    exit_btn = tk.Button(frame_bottom, text="Exit", width=10, command=root.destroy)
    exit_btn.pack(side="right")

    root.bind("<Return>", lambda _event: add_task())
    root.mainloop()


if __name__ == "__main__":
    main()
