import asyncio
import tkinter as tk


async def run():
    root = tk.Tk()
    label = tk.Label(root, text="Hello, world!")
    label.pack()
    root.mainloop()


if __name__ == "__main__":
    asyncio.run(run())
