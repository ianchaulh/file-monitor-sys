# File Monitoring System on Windows

## Key Features
- Automatic reconfiguration of the application based on the updated configuration settings `config.json`.
- Real-time monitoring of directory paths for file creation, modification, and deletion leverageing the watchdog library.
- Event-driven design to prompt system notification.

## Installation
```bash
git clone https://github.com/ianchaulh/file-monitor-sys
cd file-monitor-sys
pip install -r requirements.txt
```

## Limitations 
- The system can currently be run from either an **IDE** or the **command line**, but it is unable to run in the background. To have it run in the background, users can run it as a Windows service.
- The path to the configuration file is constrained. Please do not move the `config.json` file.
- The configuration file must be in the correct format (see `parse_config.py` file.), and the specified directory must exist.

## Assumptions
The system is designed to handle moderate I/O workloads, and can effectively monitor directories with varying levels of activity.

## Optimization
- Concurrency Control with Locking
- Selective Monitoring: The system ignores temporary files start with `~$`

## Trade-offs
I have choosen to use multi-threading to achieve concurrency because it is a more intuitive programming model combine with Watchdog. I maintain a dictionary `directory_threads` to keep track of the threads associated with each directory. It allows me to easier reference and interact with the threads later.

However, as the system scales to handle a larger number of directories or higher volumes of file events, the overhead and complexity of managing multiple threads may become a limitation.

To address this potential issue, a future iteration of the system could explore an asynchronous programming.

## Improvements
Enable batch processing approach.

## TODO
Users can find TODO items by searching the codebase.