What is cron?
The name "cron" comes from the Greek word "chronos" meaning time.

Cron is a time-based job scheduler in Unix-like operating systems. It allows users to schedule tasks or scripts to run automatically at specific times, dates, or intervals.

In Kubernetes CronJob, we use the same cron expressions for scheduling.

Also, cron expressions are used in Jenkins as build triggers, Apache Airflow DAGs, Gitlab scheduled pipelines, in programming languages etc.

Here is how it works,

The cron daemon continuously monitors the system time. It does this by periodically checking the current time against the scheduled job times.
When a scheduled time matches the current system time, cron uses the fork and exec system calls to create a new process and run the job.
The cron daemon runs as a background process, constantly active and waiting to execute jobs at their specified times.
For example, lets say a cron job is scheduled to run backup.sh at midnight.

Here's what happens:

At midnight, the cron daemon detects a match between the system time and the scheduled time.
Cron uses fork to create a new process.
The new process uses exec to run backup.sh.
While backup.sh runs, the main cron daemon continues monitoring the system for other scheduled tasks.
Understanding Cron Job Expression
Irrespective of where we use the cron expressions, the cron syntax remains the same. So, if you understand the expression, you can use it in Linux, Kubernetes, Python, etc.

A cron expression is made up of five fields separated by spaces

![image](https://github.com/user-attachments/assets/18d637dd-0599-4fa9-8826-a87de69224f1)


So, * * * * * as a complete cron expression would mean run the task every minute of every hour, every day of every month, every month, and every day of the week

This cron expression is essentially the same as writing:

0/1 * * * *
❗
While * * * * * is a valid cron expression, it's generally not recommended to use it for most tasks, as it can put a significant load on the system and potentially impact performance.
Using Ranges and Lists
Ranges and lists are commonly used in cron expressions to specify multiple values for a particular field. Here's how you can use them

Ranges allow you to specify a sequence of values for a field. The syntax is start-end, where start and end are the beginning and ending values of the range, respectively.

For example:

0-4 in the hour field means "at every hour from 0 through 4."
1-15 in the day of the month field means "every day from the 1st through the 15th of the month."
Lists allow you to specify multiple individual values for a field, separated by commas. For example:

1,3,5 in the day of the week field means "Monday, Wednesday, and Friday."
10,20,30 in the minute field means "at the 10th, 20th, and 30th minutes of the hour."
You can also combine ranges and lists in the same field. For example:

0-4,8 in the hour field means "at every hour from 0 through 4, and also at 8."
1-10,20-25 in the day of the month field means "every day from the 1st through the 10th, and also from the 20th through the 25th of the month."
Using Step Values
A step value is used in conjunction with a range to specify a frequency or interval at which the task should run within that range.

For example,

start-end/step
Where:

start is the starting value of the range.
end is the ending value of the range.
step is the interval or frequency at which the task should run within that range.
For example, consider the following cron expression

0 0-23/2 * * *
In this expression, the second field 0-23/2 represents a range from 0 to 23 with a step value of 2. This means that the task will run every 2 hours, starting at 0 (midnight), and then at 2 AM, 4 AM, 6 AM, and so on, up to 10 PM (22).

Cron Expression Practical Examples
Lets look at some practical examples of cron expressions.

Description	Cron Expression	Explanation
Run every 2 minutes	*/2 * * * *	*/2 in the minute field means
every 2 minutes.
Run every 2 minutes
between 8 AM and 5 PM	*/2 8-17 * * *	*/2 in the minute field means every
2 minutes. 8-17 in the hour field
specifies between 8 AM and 5 PM.
Every 5 minutes
between 5 PM and 7 PM
on weekends	*/5 17-19 * * 6,7	*/5 in the minute field means every 5 minutes.
17-19 in the hour field specifies
between 5 PM and 7 PM.
6,7 in the day of week field specifies
Saturday and Sunday.
Run at midnight and
noon every day	0 0,12 * * *	0 in the minute field, 0,12 in the hour
field means at midnight and noon.
Run every 2 hours
starting at midnight	0 0-23/2 * * *	0 in the minute field, 0-23/2 in the hour
field means every 2nd hour from
midnight.
Run at midnight on the
1st and 15th
of every month	0 0 1,15 * *	0 in the minute and hour fields, 1,15
in the day of month field means
at midnight on the 1st and 15th.
In addition to cron expressions, you can use predefined shortcuts for common schedules. These make it easier to specify frequently used patterns without needing to remember the full syntax.

Definition	Equivalent Cron Expression	Description
@reboot	N/A	Runs the job once after the system starts up.
@yearly or @annually	0 0 1 1 *	Runs the job once a year (at midnight, Jan 1).
@monthly	0 0 1 * *	Runs the job once a month (at midnight, 1st day).
@weekly	0 0 * * 0	Runs the job once a week (at midnight, Sunday).
@daily or @midnight	0 0 * * *	Runs the job once a day (at midnight).
@hourly	0 * * * *	Runs the job once an hour (at the start of the hour).
Creating a cron job in Linux
Follow the steps given below to create and test a cron job in Linux.

Step 1: Create a shell script
First lest create a simple shell script that we want to run as a cron job.

Let's create a script called script.sh

sudo vi /opt/script.sh
Copy the following script. It creates a temporary file with the timestamp and echos the current date.

#!/bin/bash

printf '%(%Y-%m-%d %H:%M:%S)T [INFO] The current date and time is: %(%Y-%m-%d %H:%M:%S)T\n' -1
Make the script executable.

sudo chmod +x /opt/script.sh
Step 2: Create a log file
Now create a log file and change permissions to allow writing

sudo touch script.log

sudo chmod 666 /opt/script.log
Step 3: Add Script to Crontab
Open the cron table for editing using the crontab -e command. It opens the cron table (crontab) file for the current user, allowing you to edit that user's scheduled cron jobs.

crontab -e
In the cron table file, add a new line with the desired schedule and the command to run your script. For example, lets run our script every two minutes.

*/2 * * * * /opt/script.sh
After adding the cron job entry, save the file and exit the text editor.

With this configuration, the script.sh script will be executed every two minutes by the cron daemon.

Step 3: Validate the script execution
Now we can validate the script execution by check the script.log file which should have the print message in the script.

tail -f script.log
System-wide cron jobs
You can check all the users using cron jobs from the following folder.

$ cd /var/spool/cron/crontabs

$ ls

root  vagrant

$ cat vagrant
As you can see only root and varant

The /etc/crontab file contains system-wide cron jobs that apply to all users. To view these jobs, you can use:

cat /etc/crontab
Also there are system wide cron folder. You can list them using the following command

$ ls /etc | grep cron

cron.d
cron.daily
cron.hourly
cron.monthly
crontab
cron.weekly
The /etc/cron.d/ directory contains additional system-wide cron jobs.
cron.daily, cron.hourly, cron.weekly, cron.monthly - Scripts placed in these directories are executed at their respective intervals. You can list the scripts in each directory:
Troubleshooting Cron In Linux
Lets look at ways troubleshoot cron jobs.

1. Test the script manually
Run the script or command manually from the command line to ensure it executes correctly without any errors. This will help you identify if the issue is with the script itself or with the cron job configuration.

2. Check cron service status
Ensure that the cron service is running

sudo service cron status  
sudo systemctl status cron  
3. Check Script/file permissions
Check the script or file used in the cron has respective execute and write permissions.

4. Write the script output to a log file
Write the script logs to a dedicated log file using the timestamp to ensure it is executed as per the cron expression.

Cron Real World Use Cases
Cron is widely used in real-world projects and production environments for scheduling and automating various tasks. Here are some common use cases of cron in real projects:

In Kubernetes, cron expressions are used in CronJob deployments
In Jenkins & Gitlab CI, cron expressions are used for scheduling jobs.
In airflow, cron expressions are used for scheduling DAG's.
In linux system, cron is used to schedule regular backups of databases, files, or entire systems.
Tasks like system updates, package upgrades, log file rotation, disk cleanup, and database optimizations are commonly scheduled using cron jobs.
In data-intensive applications or analytics platforms, cron jobs can be used to run data processing scripts, generate reports, or execute ETL (Extract, Transform, Load) processes on a regular schedule.
Cron jobs can be used to send scheduled emails.
In DevOps workflows, cron jobs can be used to schedule builds or perform other automation tasks as part of the CI/CD pipeline.
