# SlackAssociation
# Setup
This project uses Virtual Environments for the execution.
To configure the environment execute the following step: 
- Create a folder that will host the virtual environment:
```
mkdir slackassociation
cd slackassociation
```
- Create the virtual environment
```
python3.6 -m venv v_slack_association
cd v_slack_association
. bin/activate
```
- Add libraries
```
pip install networkx
pip install requests
pip install PyGithub
pip install jupyter
pip install numpy
pip install pyaml
pip install gitpython
cd ..
```
- project clone:
```
git clone 'https://github.com/GiovanniLanotte/SlackAssociation.git'
cd SlackAssociation
```
# Execution
- Create the files where it contains all the Tokens, where each line contains the various GitHub Tokens;

- Program execution command:
```
python3.6 main.py organization "path/workspace_Organization" tokens.txt
```
in "path / workspace_Organization" we can insert:
1) csv file consisting of the following columns:
    - id: contains the user's id;
    - Channel: contains the name of the Channel;
    - Sender: contains the sender of the message;
    - Message: contains the message where the mention is made by entering the @ followed by the name of the Sender (example: @Sender);
    - Time: contains the time of the message.
2) folder containing structured files in SlackArchive format;
3) folder containing structured files in RAW format.
