from cli.MenuSystem import show_main_menu


if __name__ == "__main__":
    try:
        show_main_menu()
    except KeyboardInterrupt:
        # Exit script gracefully when Ctrl+C is pressed
        exit(0)
