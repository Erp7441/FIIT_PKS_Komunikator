from cli.MenuSystem import show_main_menu

# LAB IPs
# 192.168.48.128 - Server
# 192.168.48.129 - Client

if __name__ == "__main__":
    try:
        show_main_menu()
    except KeyboardInterrupt:
        # Exit script gracefully when Ctrl+C is pressed
        exit(0)


