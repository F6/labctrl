print("Testing support for 8 colors mode")

print("Regular:")
test_color = "\x1b[{foreground};{background}m"
reset = "\x1b[0m"
foreground_codes = ["30", "31", "32", "33", "34", "35", "36", "37", "39"]
background_codes = ["40", "41", "42", "43", "44", "45", "46", "47", "49"]
for i in foreground_codes:
    for j in background_codes:
        colored_string = test_color.format(
            foreground=i, background=j) + "ESC[{};{}m".format(i, j) + reset
        print(colored_string, end=' ')
    print()

print("Bold:")
test_color = "\x1b[1;{foreground};{background}m"
reset = "\x1b[0m"
foreground_codes = ["30", "31", "32", "33", "34", "35", "36", "37", "39"]
background_codes = ["40", "41", "42", "43", "44", "45", "46", "47", "49"]
for i in foreground_codes:
    for j in background_codes:
        colored_string = test_color.format(
            foreground=i, background=j) + "ESC[{};{}m".format(i, j) + reset
        print(colored_string, end=' ')
    print()

print("Dimmed:")
test_color = "\x1b[2;{foreground};{background}m"
reset = "\x1b[0m"
foreground_codes = ["30", "31", "32", "33", "34", "35", "36", "37", "39"]
background_codes = ["40", "41", "42", "43", "44", "45", "46", "47", "49"]
for i in foreground_codes:
    for j in background_codes:
        colored_string = test_color.format(
            foreground=i, background=j) + "ESC[{};{}m".format(i, j) + reset
        print(colored_string, end=' ')
    print()

print("Bright:")
test_color = "\x1b[2;{foreground};{background}m"
reset = "\x1b[0m"
foreground_codes = ["90", "91", "92", "93", "94", "95", "96", "97"]
background_codes = ["100", "101", "102", "103", "104", "105", "106", "107"]
for i in foreground_codes:
    for j in background_codes:
        colored_string = test_color.format(
            foreground=i, background=j) + "ESC[{};{}m".format(i, j) + reset
        print(colored_string, end=' ')
    print()

print("Bright on regular background:")
test_color = "\x1b[2;{foreground};{background}m"
reset = "\x1b[0m"
foreground_codes = ["90", "91", "92", "93", "94", "95", "96", "97"]
background_codes = ["40", "41", "42", "43", "44", "45", "46", "47", "49"]
for i in foreground_codes:
    for j in background_codes:
        colored_string = test_color.format(
            foreground=i, background=j) + "ESC[{};{}m".format(i, j) + reset
        print(colored_string, end=' ')
    print()


print("Testing support for 256-color mode")

print("Default Background")
test_color = "\x1b[38;5;{}m"
reset = "\x1b[0m"
for i in range(256):
    if i == 16:
        print()
    if (i-16) % 6 == 0:
        print()
    colored_string = test_color.format(i) + str(i).rjust(4) + reset
    print(colored_string, end='')
print()

print("White Background")
test_color = "\x1b[38;5;{}m\x1b[48;5;15m"
reset = "\x1b[0m"
for i in range(256):
    if i == 16:
        print()
    if (i-16) % 6 == 0:
        print()
    colored_string = test_color.format(i) + str(i).rjust(4) + reset
    print(colored_string, end='')
print()

print("Testing support for RGB colors")

test_foreground_color = "\x1b[38;2;{r};{g};{b}m"
test_background_color = "\x1b[48;2;{r};{g};{b}m"
reset = "\x1b[0m"
for i in range(0, 256, 16):
    for j in range(0, 256, 16):
        colored_string = test_foreground_color.format(
            r=255, g=i, b=j) + "0xff{:02x}{:02x}".format(i, j).rjust(4) + reset
    print()

test_foreground_color = "\x1b[38;2;{r};{g};{b}m"
test_background_color = "\x1b[48;2;{r};{g};{b}m"
reset = "\x1b[0m"
for i in range(0, 256, 16):
    for j in range(0, 256, 16):
        colored_string = test_foreground_color.format(
            r=i, g=255, b=j) + "0x{:02x}ff{:02x}".format(i, j).rjust(4) + reset
    print()

test_foreground_color = "\x1b[38;2;{r};{g};{b}m"
test_background_color = "\x1b[48;2;{r};{g};{b}m"
reset = "\x1b[0m"
for i in range(0, 256, 16):
    for j in range(0, 256, 16):
        colored_string = test_foreground_color.format(
            r=i, g=j, b=255) + "0x{:02x}{:02x}ff".format(i, j).rjust(4) + reset
    print()


print("Done testing")