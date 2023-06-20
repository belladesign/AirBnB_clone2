#!/usr/bin/python3

"""contains the entry point of the command interpreter"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """The command interpreter"""

    __classes = ["BaseModel",
                 "User",
                 "State",
                 "City",
                 "Place",
                 "Amenity",
                 "Review"
                 ]

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """Quit command to exit the program
        """
        return True

    def emptyline(self):
        """Do not execute"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id"""
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            instance = eval(arg)()
            instance.save()
            print(instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on the
        class name and id
        """
        all_class_objects = storage.all()
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        else:
            given_class = arg_list[0] + "." + arg_list[1]
            for key in all_class_objects.keys():
                if given_class == key:
                    print(all_class_objects[key])
                    return
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        """
        all_class_objects = storage.all()
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg_list()
        if arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        else:
            given_class = arg_list[0] + "." + arg_list[1]
            for key in all_class_objects.keys():
                if key == given_class:
                    del storage.all()[key]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or
        not on the class name"""
        class_list = []
        check = False
        if not arg:
            for key in storage.all().keys():
                class_list.append("{}".format(storage.all()[key]))
        else:
            for key in storage.all().keys():
                class_name = key.split(".")[0]
                print(class_name, arg)
                if arg == class_name:
                    check = True
                    class_list.append("{}".format(storage.all()[key]))
            if check is False:
                print("** class doesn't exist **")
                return
        print(class_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)
        """
        my_classes = storage.all()
        check = False
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if arg_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        name_id = arg_list[0] + "." + arg_list[1]
        if name_id not in list(my_classes.keys()):
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return
        if len(arg_list) < 4:
            print("** value missing **")
            return
        setattr(storage.all()[name_id], arg_list[2], arg_list[3])
        storage.save()

    def default(self, arg):
        """Handles other inputs not captured"""
        my_dict = {"all": self.do_all,
                   "show": self.do_show,
                   "destroy": self.do_destroy,
                   "count": self.do_count,
                   "update": self.do_update
                }
        mo = re.search(r"\.", arg)
        if mo:
            arg_list = [arg[:mo.span()[0]], arg[mo.span()[1]]]
            mo = re.search(r"\((.*?)\)", arg_list[1])
            if mo:
                func = [arg_list[1][:mo.span()[0]], mo.group()[1:-1]]
                if func[0] in my_dict.keys():
                    string = "{} {}".format(arg_list[0], func[1])
                    return my_dict[func[0]](string)
        print("** no instance found **")

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        counter = 0
        for value in storage.all().values():
            if arg == value.__class__.__name__:
                counter += 1
        print(counter)

if __name__ == "__main__":
    HBNBCommand().cmdloop()
