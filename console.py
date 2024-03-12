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
    if type(attrib_value) in (int, float):
        return attrib_value
    else:
        try:
            converted = int(attrib_value)
            return converted
        except ValueError:
            try:
                converted = float(attrib_value)
                return converted
            except ValueError:
                return attrib_value


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
            if line.split()[0] not in classes.keys():
                print("** class doesn't exist **")
                return
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
                    if type(value) is target_class:
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
        # where command is show or destroy
        patn_1 = r'(\w+)\.(\w+)[(]"(.+?)"[)]'
        match_showdestroy = re.match(patn_1, line)

        # Matches MyClass.update(id, attribute_name, attribute_value)
        patn_2 = r'(\w+)\.(\w+)\("([\w+-]+)", "(\w+)", "?((\w+)|\d+\.?\d+)"?\)'
        match_update = re.match(patn_2, line)

        # Partially matches "MyClass.update(id, dictionary)"
        # ---> "MyClass.update(id, {"
        patn_3 = r'^(\w+)\.(\w+)\("(.+?)",\s*\{'
        match_update_using_dict = re.search(patn_3, line)

        # "MyClass.all()" command
        # ---> "all MyClass"
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
        # "MyClass.command()" - command could be show/destroy
        # ---> "show MyClass"
        # ---> "destroy MyClass"
        elif match_showdestroy and match_showdestroy.group(2) != 'update':
            class_name = match_showdestroy.group(1)
            command = match_showdestroy.group(2)
            instance_id = match_showdestroy.group(3)
            return f'{command} {class_name} {instance_id}'
        # MyClass.update(id, attribute_name, attribute_value)
        # ---> "update MyClass id attribute_name attribute_value"
        elif match_update:
            class_name = match_update.group(1)
            command = match_update.group(2)
            instance_id = match_update.group(3)
            att_name = match_update.group(4)
            att_value = match_update.group(5)
            return f'update {class_name} {instance_id} {att_name} {att_value}'
        # MyClass.update(id, attribute_dictionary)
        # ---> "update MyClass id attribute_name attribute_value"
        elif match_update_using_dict:
            line = line.split(".", 1)
            class_name, the_rest = line[0], line[1]
            line = the_rest.split("(", 1)
            command, the_rest = line[0], line[1]
            line = the_rest.split(',', 1)
            inst_id, the_rest = line[0].strip('"'), line[1]
            attrs_dict = eval(the_rest[1:-1])
            for att_name, att_value in attrs_dict.items():
                line = f'{class_name} {inst_id} {att_name} {att_value}'
                self.do_update(line)
            return ""  # To avoid returning None
        else:
            return line

    def emptyline(self):
        pass

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """Ctrl + D exits the program\n"""
        print()
        return True

    def help_precmd(self):
        """
        `precmd` Intercepts and checks command inputs for specific commands
        to either preprocess or implement and execute.

        1. If <line> is of the form "AnyClass.all()", precmd
           changes it to "all AnyClass", which is
           to be executed by do_all() handler

            Usage:
                AnyClass.all()

        2. if <line> is of the form "AnyClass.count(), precmd
           implements counting of the number of occurrences of "AnyClass"
           instances and prints the count

           Usage:
                AnyClass.count()

        3. If <line> is of the form "AnyClass.show('some-uuid')", precmd
           changes it to "show AnyClass some-uuid", which is
           to be executed by do_show() handler

            Usage:
                AnyClass.show('a-uuid')

        4. If <line> is of the form "AnyClass.destroy('some-uuid')", precmd
           changes it to "destroy AnyClass some-uuid", which is
           to be executed by do_destroy() handler

            Usage:
                AnyClass.destroy('uuid')

        5. If <line> is of the form
           "AnyClass.update(uuid, attribute_name, attribute_value)", precmd
           changes it to
           "update AnyClass uuid attribute_name attribute_value",
           which is to be executed by do_update() handler

            Usage:
                AnyClass.update(uuid, attribute_name, attribute_value)

        6. If <line> is of the form
           "AnyClass.update(id, attributes_dictionary)", precmd
           changes it to "update AnyClass uuid attributes_dictionary",
           which is to be executed by do_update() handler one attribute at
           a time

            Usage:
                AnyClass.update(uuid, attributes_dictionary)
        """
        print(getattr(self, "help_precmd").__doc__)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
