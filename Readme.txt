from Cesar Lopez Ramirez <cesarlr@gmail.com>
Here is the script for Linux. The usage is

    rfexplorer /dev/ttyUSB0 0400000 0500000 050 120

where
    1st parameter is linux device,
    2nd is start freq (7 chars)
    3rd is end freq (7 chars)
    4th is amp top (3 chars) (without minus)
    5th is amp bottom (3 chars) (without minus)

The output is a CSV file in the same way as the mac client does.
