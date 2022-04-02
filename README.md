

# README.py

Python 3.8.10

Written by two student: 
Student1 : xxxxxxxx xxxxxxxx
Student2 : xxxxxxxx xxxxxxxx


Before running the programe, we need make sure there is a file that need to be sent, the python file $sender.py$ on sender side and the python file $receiver.py$ on receiver side


---

Firstly, set up the receiver at a server at $ubuntu2004-008.student.cs.uwaterloo.ca$ as following: 
```
python receiver.py 9994 0.1 Rec_File.txt

# 9994            --  is the port that used to receive the file package  
# 0.1             --  is the drop probability
# Rec_File.txt    --  is the file name that will store the received file.

```

---

Waiting few second for receiver.py to set up...

Secondly, we could send the file at $ubuntu2004-008.student.cs.uwaterloo.ca$

```
python sender.py ubuntu2004-008.student.cs.uwaterloo.ca 9994 9992 1 Send_file.txt

# ubuntu2004-008.student.cs.uwaterloo.ca
#                 --  is the name of the server that the file will be sent to.
# 9994            --  is the port that used to send the file package
# 9992            --  is the port that used to receive the ack package 
# Send_file.txt   --  is the file name that need to transfer

```

---


The following are some possible problem.

* P : The file need to send does not exist
S : The sender window will show "< file > does not exist " and then exit properly.

* P : The port is occupied.
S : The receiver.py cannot set up. The solution is to run the above step by using different port.

* P : The receiver would receive some duplicate text file
S :  Change the timeout of sender to try again, due to the internet delay, sender may treat the delay as drop by receiver, then it would send again.

