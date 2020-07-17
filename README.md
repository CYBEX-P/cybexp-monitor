# run monitor
```bash
cd cybexp-monitor # move to monitorts root folder
# create the repository where the monitor will push to, it must be named status
git clone git@github.com:CYBEX-P/cybexp-status.git status
source env/bin/activate
python3 monitor.py
```   

important to note that the status folder must be a repository. This repos folder must be named `status` and it must be ready to be pushed i.e. it must have remote origin configured.


