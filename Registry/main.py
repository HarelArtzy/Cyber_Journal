
import winreg

PATH = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"


def show_history():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PATH) as key:
        order = winreg.QueryValueEx(key, "MRUList")[0]
        history = []

        for name in order:
            try:
                value = winreg.QueryValueEx(key, name)[0]
                history.append((name, value.split("\\1")[0]))
            except FileNotFoundError:
                pass

    for i, (_, command) in enumerate(history, 1):
        print(f"{i}. {command}")

    return history


def delete_history():
    history = show_history()
    index = int(input("Number to delete: ")) - 1

    if not 0 <= index < len(history):
        print("Invalid number")
        return

    name = history[index][0]

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PATH,
                        0, winreg.KEY_READ | winreg.KEY_SET_VALUE) as key:
        order = winreg.QueryValueEx(key, "MRUList")[0]
        winreg.DeleteValue(key, name)
        winreg.SetValueEx(
            key, "MRUList", 0, winreg.REG_SZ,
            order.replace(name, "")
        )

    print("Deleted")


def add_history():
    command = input("Command to add: ").strip()
    if not command:
        return

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PATH,
                        0, winreg.KEY_READ | winreg.KEY_SET_VALUE) as key:
        order = winreg.QueryValueEx(key, "MRUList")[0]

        for name in "abcdefghijklmnopqrstuvwxyz":
            if name not in order:
                break
        else:
            print("History is full")
            return

        winreg.SetValueEx(
            key, name, 0, winreg.REG_SZ, command + "\\1"
        )
        winreg.SetValueEx(
            key, "MRUList", 0, winreg.REG_SZ, name + order
        )

    print("Added")


while True:
    print("\n1. Show history")
    print("2. Delete command")
    print("3. Add command")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_history()
    elif choice == "2":
        delete_history()
    elif choice == "3":
        add_history()
    elif choice == "4":
        break
