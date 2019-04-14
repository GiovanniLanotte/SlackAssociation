# SlackAssociation
# Setup
Questo progetto utilizza Virtual Environments per l'esecuzione. 
Per configurare l'ambiente eseguire i seguenti step:
- Creare una cartella che ospitera la macchina virtuale:
```
mkdir slackassociation
cd slackassociation
```
- Creare l'ambiente virtuale:
```
python3.6 -m venv v_slack_association
cd v_slack_association
. bin/activate
```
- Aggiungere le librerie
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
- Clone del progetto:
```
git clone 'https://github.com/GiovanniLanotte/SlackAssociation.git'
cd SlackAssociation
```
# Esecuzione
- Creare i file dove contiene tutti i Token, dove ogni riga vengono inseriti i vari Token GitHub

- Lanciare il programma
```
python3.6 main.py organization "path/workspace_Organization" tokens.txt
```
in "path/workspace_Organization" possiamo inserire:
1) file csv costituito dalle seguenti colonne:
    - id: contiene dell'utente
    - team channel: contiene il nome del workspace
    - Channel: contiene il nome del Channel
    - Sender: contiene il mittente del messaggio
    - Message: contiene il messaggio dove la menzione è effettuata inserendo la @ seguito dal nome del Sender (esepio: @Sender)
    - Time: contiene l'orario del messaggio
2) cartella contenente i file strutturati in formato SlackArchive;
3) cartella contenente i file strutturati in formato RAW.
