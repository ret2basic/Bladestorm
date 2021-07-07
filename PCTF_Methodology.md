# PCTF Methodology

## To-Do

### Step 1: Backup

**Tar:**

```shell
# from remote machine
$ tar -zcvf /home/ctf/services.tar.gz /opt/ictf/services
$ sudo iptables-save > /home/ctf/iptables.bak
```

**Download the backup of services to your local machine:**

```shell
# from your local machine
$ scp -i key ctf@52.53.200.1:/home/ctf/services.tar.gz .
```

**If need to revert:**

```shell
# from you local machine
$ scp -i key services.tar.gz ctf@52.53.200.1:/home/ctf

# from remote machine
$ cd /
$ sudo tar -zxvf /home/ctf/services.tar.gz /opt/ictf/services
```

### Step 2: Install Tools

```shell
$ cd
$ sudo apt update

# swpag_client
$ sudo pip3 install swpag_client

# Pwntools
$ sudo apt install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade pwntools

# For compiling x86 binaries
$ sudo apt install gcc-multilib

# File monitor
$ sudo pip install pyinotify

# Oh My Tmux
$ git clone https://github.com/gpakosz/.tmux.git
$ ln -s -f .tmux/.tmux.conf
$ cp .tmux/.tmux.conf.local .

# Automation
$ git clone https://github.com/ret2basic/Bladestorm
```

### Step 3: Deploy WAF (Be Careful, may block game box)

**Edit `php.ini`:**

```shell
$ sudo nano php.ini
```

**Append the following line:**

```php
auto_append_file = "/home/ctf/Bladestorm/waf/a_simpler_waf/waf.php"
```

### Step 4: Backup Again (if WAF was deployed)

**Tar:**

```shell
$ tar -zcvf /home/ctf/services_with_waf.tar.gz /opt/ictf/services
```

**Download the backup of services to your local machine:**

```shell
# from your local machine
$ scp -i key ctf@52.53.200.1:/home/ctf/services_with_waf.tar.gz .
```

**If need to revert:**

```shell
# from you local machine
$ scp -i key services_with_waf.tar.gz ctf@52.53.200.1:/home/ctf

# from remote machine
$ cd /
$ sudo tar -zxvf /home/ctf/services_with_waf.tar.gz /opt/ictf/services
```

## Patching

### Restart Services

**The service will be running as root by default. To lower its privilege, modify the `user` parameter from `/opt/ictf/services/<service_name>/ro/xinetd.conf`:**

![xinetd.conf](https://raw.githubusercontent.com/ret2basic/Basement-of-Writeup/master/Notes/Software_Security/xinetd_conf.png)

**Rebuild the docker image:**

```shell
$ sudo docker-compose build
```

**Restart the services:**

```shell
$ sudo docker-compose down
$ sudo docker-compose up -d
```

### C

**General user input sanitizer:**

```c
for (int i=0; i < strlen(input); i++)
{
      if((name[i] >= 'a' && name[i] <= 'z') || (name[i] >= 'A' && name[i] <= 'Z') || (name[i] >= '0' && name[i] <= '9'))
      {
            printf("\n");
      }
      else
      {
            printf("GG. No points for you.\n");
            fflush(stdout);
            exit(0);
      }
   }
   
printf("\n");
```

**Whenever the program asks for user input, modify variable names and copy and paste this code.**

**Recompile with all security mechanisms on:**

```shell
$ gcc <service_name>.c \
-m32 \
-fPIE \
-fstack-protector-strong \
-D_FORTIFY_SOURCE=2 \
-Wformat \
-Wformat-security \
-Wl,-z,relro \
-Wl,-z,now \
-o <service_name>
```

**If source code is not given, download the binary to local machine and modify bytes with IDA (let me do this part).**

### PHP

**If PHP source code is encoded, decode it at https://www.unphp.net/.**

**A general user input sanitizer is stored at `/home/ctf/Bladestorm/patch/php_patch.php`. Include it in the target PHP file and call those sanitizing functions after each user input:**

```php
<?php require_once "/home/ctf/Bladestorm/patch/php_patch.php";?>
```

## Attack

### Exploit Thrower

**To run exploit thrower in the background:**

```shell
$ nohup ./bladestorm.py <service_name> > <service_name>.log 2 > <service_name>_error.log &
# Example: nohup ./bladestorm.py simplecalc > simplecalc.log 2>simplecalc_error.log &
```

The command `nohup` stands for **"no hangup"**. It executes another program and ignores all the `SIGHUP` signals. Don't forget to append the `&` sign at the end so that the program truly runs in the background.

### Debug

**Check processes that are running in the background:**

```shell
$ jobs
```

**To kill any of them:**

```shell
$ kill %<id>
# Example: kill %1
```

**Make sure all the available exploit throwers are running in the background at any time!**

## Defense

**Check users that are currently logged in:**

```shell
$ sudo w
```

**Kick malicious user:**

```shell
$ pkill -kill -t <tty_id>
# Example: pkill -kill -t pts/0
```

**Check processes that are currently running:**

```shell
$ ps aux
```

**Check network connections:**

```shell
$ netstat -antulp
# Example: netstat -antulp | grep EST
```

**Check a certain port:**

```shell
$ lsof -i:<port>
# or
$ netstat -tunlp | grep <port>
```

**Kill a process:**

```shell
$ kill <pid>
# or
$ killall <process_name>
# or
$ kill - <pid>
```

**Check `iptables` rules:**

```shell
$ sudo iptables -L
```

**Revert `iptables` rules:**

```shell
$ sudo iptables-restore < /home/ctf/iptables.bak
```

**Check all active TCP connections:**

```shell
$ netstat -ant|awk  |grep |sed -e  -e |sort|uniq -c|sort -rn
```

**Check top 10 most visited URL:**

```shell
$ cat /var/log/apache2/access.log | cut -f4 -d   | sort | uniq -c | sort -k  -r | head -
```
