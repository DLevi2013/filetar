from database import init_db

init_db()

print("================================")
print(" FileTár - Monkersoft Development")
print("================================")
print("www.monkersoft.hu\n")

mode = input("1 = CLI | 2 = GUI: ")

if mode == "2":
    from gui import start_gui
    start_gui()

else:
    from cli import run_cli
    run_cli()