# Theater Booking Script
```
     _____              _       
  __|___  |_ _  ___ ___| |_   _ 
 / _ \ / / _` |/ _ \_  / | | | |
|  __// / (_| |  __// /| | |_| |
 \___/_/ \__, |\___/___|_|\__, |
         |___/            |___/ 
         By Michael Wagdy©
```
This script automates the booking process for shows in the Egyptian National Theater Festival.

## How Does It Work?

1. **Requirements**: Ensure you have a Python environment set up.
2. **Running the Script**: Use the following command to run the script:

   ```bash
   python theater.py <day_number> "<show_name_1>, <show_name_2>"

### Input Details

- The first input (`<day_number>`) is a number from **1 to 7**:
  - **1** represents **Sunday**
  - **2** represents **Monday**
  - …and so on up to **7** for **Saturday**.

- The second input is a comma-separated list of show names you want to book. If you have multiple shows, enclose the names in quotes and separate them by commas. You only need to provide one keyword from each show's name, not the entire title.
### Example Usage

  ```bash
python theater.py 1 "Hamlet, Macbeth"
```
This command will book shows with keywords "Hamlet" and "Macbeth" on Sunday.
### Script Behavior

- The script will attempt to book each show **up to three times**. If it does not find the show on the first try, it will try two more times before stopping.
- If a show exists and has available seats, the script will save the link to the QR code in a text file named `qr_code_info.txt`.

### Automating the Process

To automate the process and run the script at a specific time, follow these steps:

1. Open the `run_once_at_time.sh` file.
2. Edit the file to set your desired time and input parameters.
3. The script will execute at the specified time.

This can be done on any environment that supports Python, including Android phones. To run the script on an Android device:
- Download **Termux**.
- Install **Python** within Termux.
- Run the bash script as explained, and it will run in the background at the specified time.

![Example Image](https://github.com/michael-wagdy-l/e7gezly/blob/main/android%20example.jpg)
note: You can modify the booking parameters, such as your name, directly within the script code.


