# SlackAssociation
# Setup
Questo progetto utilizza Virtual Environments per eseguire il progetto. Esegui gli step successivi per eseguirlo:
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

- Eseguire il programma
```
python3.6 main.py organization "path/workspace_Organization" tokens.csv
```
in "path/workspace_Organization" possiamo inserire:
1) file csv strutturata dalle seguenti colonne:
    - id: dell'utente
    - team channel: nome del workspace
    - Channel: nome del Channel
    - Sender: Il mittente del messaggio
    - Message: messaggio dove la menzione è effettuata trami @Sender
    - Time: orario del messaggio
2) cartella contenente i file strutturati in formato SlackArchive;
3) cartella contenente i file strutturati in formato RAW.
