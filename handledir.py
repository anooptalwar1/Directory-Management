import os
import shutil 
import json
import logging
import sys

undolist = []

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
                    filename='diroperation.log',
                    filemode='w')

class dirmanage:

    """ Create User's Directory"""
    def create_user_dir(userid, project=None, user_input=None):
        
        # Create default common users directory if it doesn't exist
        if not os.path.exists("users"):
            os.makedirs("users")
        
        # Create User's home directory
        userdir = os.path.join("users", userid)
        if not os.path.exists(userdir):
            os.makedirs(userdir)
            undolist.append("create " + userdir)
            logging.info(f'{userdir} directory created for {userid}')

        # Create Project directory based on user input
        if project is not None:
            projectdir = os.path.join("users", userid, project)
            if not os.path.exists(projectdir):
                os.makedirs(projectdir)
                undolist.append("create " + projectdir)
                logging.info(f'{projectdir} directory created for {userid}')

        # Create additional directory inside project directory based on user input
        if user_input is not None:
            newdir = os.path.join("users", userid, project, user_input)
            if not os.path.exists(newdir):
                os.makedirs(newdir)
                undolist.append("create " + newdir)
                logging.info(f'{newdir} directory created for {userid}')
        

    """ Delete User's Home Directory"""
    def delete_user_dir(userid):

        # Delete User's home directory
        userdir = os.path.join("users", userid)
        if os.path.exists(userdir):
            shutil.rmtree(userdir, ignore_errors = False)
            undolist.append("delete " + userdir)
            logging.info(f'{userdir} directory tree deleted for {userid}')
            return json.dumps(userdir + " deleted")

    """ Delete User's Project Directory"""
    def delete_user_project_dir(userid, project=None):

        if project is not None:
            # Delete User's Project directory
            userprojectdir = os.path.join("users", userid, project)
            if os.path.exists(userprojectdir):
                shutil.rmtree(userprojectdir, ignore_errors = False)
                undolist.append("delete " + userprojectdir)
                logging.info(f'{userprojectdir} directory tree deleted for {userid}')
                return json.dumps(userprojectdir + " deleted")
        else:
            logging.info(f'{userprojectdir} directory not found for {userid}')

    """ Delete User's Custom Directory"""
    def delete_custom_dir(userid, project=None, user_input=None):

        if project is not None and user_input is not None:
            # Delete User's custom directory
            deldir = os.path.join("users", userid, project, user_input)
            if os.path.exists(deldir):
                shutil.rmtree(deldir, ignore_errors = False)
                undolist.append("delete " + deldir)
                logging.info(f'{deldir} directory tree deleted for {userid}')
                return json.loads(deldir + " deleted")
        else:
            logging.info(f'{user_input} directory not found for {userid}')


    """ Rename Directory"""
    def rename_project_dir(userid, project=None, new_project=None):

        # Rename Project directory
        userdir = os.path.join("users", userid)
        if project is not None and new_project is not None:
            projectdir = os.path.join("users", userid, project)
            new_projectdir = os.path.join("users", userid, new_project)
            if os.path.exists(projectdir):
                os.rename(projectdir , new_projectdir)
                undolist.append("renamed " + projectdir + " " + new_projectdir)
                logging.info(f'{projectdir} directory renamed to {new_projectdir}')
                return json.dumps(projectdir + "renamed to " + new_projectdir)
            else:
                logging.info(f'{projectdir} directory do not exist for {userid}')


    """ Rename Custom Directory"""
    def rename_custom_dir(userid, project=None, user_input=None, new_user_input=None):

        # Rename Project directory
        projectdir = os.path.join("users", userid, project)
        if user_input is not None and new_user_input is not None:
            customdir = os.path.join("users", userid, project, user_input)
            new_customdir = os.path.join("users", userid, project, new_user_input)
            if os.path.exists(customdir):
                os.rename(customdir, new_customdir)
                undolist.append("renamed " + customdir + " " + new_customdir)
                logging.info(f'{customdir} directory renamed to {new_customdir}')
                return json.dumps(customdir + " renamed to " + new_customdir)
        else:
            logging.info(f'{customdir} directory to be renamed not exists')


    """ Move Project Directory"""
    def move_project_dir(userid, project=None, user_input=None):

        # Rename Project directory
        customdir = os.path.join("users", userid, project)
        new_customdir = os.path.join("users", userid, user_input)
        if project is not None and user_input is not None:
            shutil.move(customdir , new_customdir, copy_function = shutil.copytree)
            undolist.append("moved " + customdir + " " + new_customdir)
            logging.info(f'{customdir} directory moved to {new_customdir}')


    """ Move Custom Directory"""
    def move_custom_dir(userid, project=None, user_input=None, new_user_input=None):

        # Rename Project directory
        customdir = os.path.join("users", userid, project, user_input)
        new_customdir = os.path.join("users", userid, project, new_user_input)
        if user_input is not None and new_user_input is not None:
            shutil.move(customdir , new_customdir, copy_function = shutil.copytree)
            undolist.append("moved " + customdir + " " + new_customdir)
            logging.info(f'{customdir} directory moved to {new_customdir}')

    """ List All Directory"""
    def list_custom_dir(userid):
        if userid is not None:    
            # Rename Project directory
            userdir = os.path.join("users", userid)
            all_dir = [ir[0] for ir in os.walk(userdir)]
            logging.info(f'{all_dir} directory listed for {userid}')
            return json.dumps(all_dir)

class undodir:

    """ Undo User's Directory"""
    def undo_dir(userid, project=None, user_input=None):
        if undolist == []:
            return ("undo list is empty")
        else:
            undo_oper = undolist[-1].split()
            
            # Undo Create Operation
            if undolist[-1].split()[0] == "create":
                shutil.rmtree(undo_oper[1], ignore_errors = False)
                logging.info(f'{undolist}')
                return json.dumps("undo " + undolist[-1])
            
            # Undo Delete Operation
            elif undolist[-1].split()[0] == "delete":
                os.makedirs(undo_oper[1])
                logging.info(f'{undolist}')
                return json.dumps("undo " + undolist[-1])

            # Undo Move Operation
            elif undolist[-1].split()[0] == "moved":
                shutil.move(undo_oper[2] , undo_oper[1], copy_function = shutil.copytree)
                logging.info(f'{undolist}')
                return json.dumps("undo " + undolist[-1])

            # Undo Rename Operation
            elif undolist[-1].split()[0] == "renamed":
                os.rename(undo_oper[2] , undo_oper[1])
                logging.info(f'{undolist}')
                return json.dumps("undo " + undolist[-1])