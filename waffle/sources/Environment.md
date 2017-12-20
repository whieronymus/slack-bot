*To setup a good working environment*
*1.* You should have a project folder which contains all of your projects. For example `C:\Projects\`
*2.* Make sure you have virtualenv installed, to do this type `pip install virtualenv` in the command line
*3.* You should also have installed a good text editor (e.g. Sublime Text or Atom)
*4.* To start a new project you should follow the following instructions every time:
    *i.* Create a new folder in your projects directory, call it the project name
    *ii.* Navigate into the new folder and type `virtualenv env` in the command line
    *iii.* Type `env\Scripts\activate` to activate your virtual environment
    *iv.* You will now see the command line prefixed with (env), this shows you the virtualenv is activated
    *v.* Install any packages you may need with pip and then type `pip freeze > requirements.txt`
    *vi.* You can now start to create your project.
    *vii.* Make sure you run the project while inside the virtualenv via the command line. Whenever you install a new package with pip, make sure you repeat steps iii to v.
*5.* If you create your project into a git repository, make sure to put `env/` inside your .gitignore file.
