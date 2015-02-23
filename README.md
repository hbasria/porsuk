# porsuk
Porsuk is a django project to collect informations about Pardus packages from official repos and provide them in a cool interface


## Installation
### 1. virtualenv / virtualenvwrapper
You should already know what is [virtualenv](http://www.virtualenv.org/), preferably [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/) at this stage. So, simply create it for your own project, where `projectname` is the name of your project:

`$ mkvirtualenv --clear porsuk`

### 2. Download
Now, you need the *porsuk* project files in your workspace:

    $ cd /path/to/your/workspace
    $ git clone https://github.com/hbasria/porsuk.git porsuk && cd porsuk

### 3. Requirements
Right there, you will find the *requirements.txt* file that has all the great debugging tools, django helpers and some other cool stuff. To install them, simply type:

`$ pip install -r requirements.txt`

#### Initialize the database
First set the database engine (PostgreSQL, MySQL, etc..) in your settings files; `porsuk/settings/dev.py`. Of course, remember to install necessary database driver for your engine. Then define your credentials as well. Time to finish it up:

`./manage.py migrate`

### Ready? Go!

`./manage.py runserver`