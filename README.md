# Technical Test: Python/API Development and DevOps

## Prerequisites

- **Docker** 
- **Git** 
- **Python 3**

##  Installation and Set-up

Open a teminal and navigate to where you want the project repo to live. Then run

```
git clone https://github.com/Taylor-Slade/biokey.git
cd biokey
deploy.sh
```

This will pull the repository down, then cd into it. It will then set up a virtual environment, activate it and 
install the requirements. It will then initialize a database. It will then create a docker image and run the container.
The basic web ui is accessible via ```localhost:5000/users/```

## Unit Testing

- Open a terminal window and run ```pytest``` from the root project directory to run tests locally
- Two separate piplines can be used for complete testing of code/ hotfix testing of code


## Troubleshooting

### **Entrypoint.sh script not running:**

- Check that the line endings in the file are LF. Github will change the line endings to whatever system you are 
using when you pull the files. This can be overwritten with ```git config core.autocrlf false``` for the local 
repo or ```git config --global core.autocrlf false``` for all repos 
- You can also use ```dos2unix``` to fix line endings
