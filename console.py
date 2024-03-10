#!/usr/bin/python3
"""Defines HBNBCommand class"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


def convert_to_num(attrib_value):
    """Maintains the type of an attribute value"""
    try:
        converted = int(attrib_value)
    except ValueError:
        try:
            converted = float(attrib_value)
        except ValueError:
            converted = attrib_value
    return converted


class HBNBCommand(cmd.Cmd):
    """Represents the AirBnB command interpreter"""

    prompt = "(hbnb) "

    def do_create(self, line):
        """
        Creates a new instance of a class.
        Saves it to a JSON file.
        Displays the id of the instance.

        Usage: create <class_name>
        """

        if line == "":
            print("** class name missing **")
            return
        if line in classes.keys():
            instance = classes[line]()
            storage.new(instance)
            storage.save()
            print(instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        Prints the string representation of an instance
        based on <class_name> and <id>.

        Usage: show <class_name> <id>
        """
        num_toks = len(line.split())

        if num_toks == 0:
            print("** class name missing **")
            return
        elif num_toks == 1:
            if line not in classes.keys():
                print("** class doesn't exist **")
                return
            else:
                print("** instance id missing **")
                return
        else:
            objs_dict = storage.all()
            key = f'{line.split()[0]}.{line.split()[1]}'
            print(objs_dict.get(key, "** no instance found **"))

    def do_destroy(self, line):
        """
        Deletes a stored instance based on <class_name> and <id>

        Usage: destroy <class_name> <id>
        """
        num_toks = len(line.split())

        if num_toks == 0:
            print("** class name missing **")
            return
        elif num_toks == 1:
            if line not in classes.keys():
                print("** class doesn't exist **")
                return
            else:
                print("** instance id missing **")
                return
        else:
            key = f'{line.split()[0]}.{line.split()[1]}'
            if key not in storage.all().keys():
                print("** no instance found **")
                return
            else:
                # delete instance from __objects dict
                del storage.all()[key]
                # save change(s) to file.json
                storage.save()

    def do_all(self, line):
        """
        Prints string representation of all instances
        based on or not based on <class_name>

        Example usage:
            $ all BaseModel
            $ all

         where BaseModel is a <class_name>
        """
        num_toks = len(line.split())
        if num_toks == 0:
            all_instnce_objs = [str(value) for value in storage.all().values()]
            print(all_instnce_objs)
        else:
            class_name = line.split()[0]
            if class_name in classes:
                class_instance_objs = []
                target_class = classes[class_name]
                for value in storage.all().values():
                    if type(value) == target_class:
                        class_instance_objs.append(str(value))
                print(class_instance_objs)
            else:
                print("** class doesn't exist **")

    def do_update(self, line):
        """
        Updates an instance based on the <class_name> and <id>
        by adding or updating attribute.

        Usage: update <class name> <id> <attribute name> "<attribute value>"

        Example:
            $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        num_toks = len(line.split())

        if num_toks == 0:
            print("** class name missing **")
        elif num_toks == 1:
            if line not in classes.keys():
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")
        elif num_toks == 2:
            print("** attribute name missing **")
        elif num_toks == 3:
            print("** value missing **")
        else:
            key = f'{line.split()[0]}.{line.split()[1]}'
            if key not in storage.all().keys():
                print("** no instance found **")
            else:
                attrib_name = line.split()[2]
                attrib_value = convert_to_num(line.split()[3])
                instance = storage.all()[key]
                setattr(instance, attrib_name, attrib_value)
                storage.save()

    def precmd(self, line):
        """
        Intercepts and checks command inputs for specific commands
        to either preprocess or execute.

        Type "help precmd" + Enter for detailed information of the commands
        """
        # This pattern matches "MyClass.command('some-uuid')"
        pattern = r'(\w+)\.(\w+)[(]"(.+?)"[)]'
        match = re.match(pattern, line)

        # "MyClass.all()" command
        if line.endswith(".all()"):
            class_name = line.split('.')[0]
            return f'all {class_name}'
        # "MyClass.count()" command
        elif line.endswith(".count()"):
            class_name = line.split('.')[0]
            count = 0
            for key in storage.all().keys():
                if key.startswith(class_name):
                    count += 1
            print(count)
            count = 0
            return ""  # to avoid returning None
        # "MyClass.command()" line - command could be show/destroy
        elif match:
            class_name = match.group(1)
            command = match.group(2)
            class_id = match.group(3)
            return f'{command} {class_name} {class_id}'
        else:
            return line

    def help_precmd(self):
        """
        `precmd` Intercepts and checks command inputs for specific commands
        to either preprocess or implement and execute.

        1. If <line> is of the form "AnyClass.all()", precmd
           changes it to "all AnyClassName", which is
           to be executed by do_all() handler

            Usage:
                AnyClass.all()  # Translated to "all MyClass"

        2. if <line> is of the form "AnyClass.count(), precmd
           implements counting of the number of occurrences of "AnyClass"
           instances and prints the count

           Usage:
                AnyClass.count()

        3. If <line> is of the form "AnyClass.show('some-uuid')", precmd
           changes it to "show AnyClass some-uuid", which is
           to be executed by do_show() handler

        Usage:
            AnyClass.show('a-uuid')  # Translated to 'show AnyClass a-uuid'
        """
        print(getattr(self, "help_precmd").__doc__)

    def emptyline(self):
        pass

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """Ctrl + D exits the program\n"""
        print()
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
