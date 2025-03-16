import asyncio
import tkinter as tk


async def run():
    root = tk.Tk()
    root.title("Airope")
    root.title = tk.Label(
        root,
        text="Welcome to the survey",
        font=("Arial 16 bold", 16),
        bg="brown",
        fg="#FF0",
    )
    name_label: tk.Label = tk.Label(root, text="What is your name?")
    name_inp: tk.Entry = tk.Entry(root)

    eater_inp: tk.Checkbutton = tk.Checkbutton(
        root,
        text="Check this box if you eat bananas",
    )

    num_label: tk.Label = tk.Label(
        root,
        text="How many times do you eat bananas?",
    )

    num_inp: tk.Spinbox = tk.Spinbox(
        root,
        from_=0,
        to=1000,
        increment=1,
    )

    color_label: tk.Label = tk.Label(
        root,
        text="What is your favorite color?",
    )

    color_inp: tk.Listbox = tk.Listbox(root, height=1)
    color_choices: tuple[str, ...] = (
        "Any",
        "Green",
        "Green-Yellow",
        "Yellow",
        "Brown Spotted",
        "Black",
    )

    for choice in color_choices:
        color_inp.insert(tk.END, choice)

    root.geometry("640x480+300+300")
    root.resizable(False, False)

    plantain_l = tk.Label(root, text="Do you like plantains?")
    plantain_f = tk.Frame(root)
    plantain_y_inp = tk.Radiobutton(plantain_l, text="Yes")
    plantain_n_inp = tk.Radiobutton(plantain_l, text="No")

    root.mainloop()


if __name__ == "__main__":
    asyncio.run(run())
