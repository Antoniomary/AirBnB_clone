#!/usr/bin/python3
"""
    A program that serves as the entry point to a command interpreter.
    It does so by defining the HBNNCommand class.
"""
import cmd
from models import storage


class HBNBCommand(cmd.Cmd):
    """A class that inherits from Cmd class"""
    prompt = "(hbnb) "
    all_classes, their_attr_types = storage.classes_and_their_attr_types()

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF (CTRL + D) exits the program
        """
        print()
        return True

    def emptyline(self):
        """Overrides empty line default behaviour when an empty line
           is entered at command line. Now, it will do nothing.
        """
        pass

    def do_create(self, arg):
        """Creates a class instance, saves it to a JSON file and prints the id

        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return

        arg = arg.split()
        if len(arg) > 1 or not (arg[0] in self.all_classes.keys()):
            print("** class doesn't exist **")
        else:
            my_model = self.all_classes[arg[0]]()
            my_model.save()
            print(my_model.id)

    def do_show(self, arg):
        """Prints the string representation of an instance

        Usage: show <class name> <instance id>
        """
        if not arg:
            print("** class name missing **")
            return

        arg = arg.split()
        if not (arg[0] in self.all_classes.keys()):
            print("** class doesn't exist **")
            return
        if len(arg) != 2:
            print("** instance id missing **")
            return
        all_instances = storage.all()
        instance_to_find = arg[0] + '.' + arg[1]
        if instance_to_find in all_instances.keys():
            print(all_instances[instance_to_find])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance and saves the change into a JSON file.

        Usage: destroy <class name> <id>
        """
        if not arg:
            print("** class name missing **")
            return

        arg = arg.split()
        if not (arg[0] in self.all_classes.keys()):
            print("** class doesn't exist **")
            return
        if len(arg) != 2:
            print("** instance id missing **")
            return
        all_instances = storage.all()
        instance_to_delete = arg[0] + '.' + arg[1]
        if instance_to_delete in all_instances.keys():
            del all_instances[instance_to_delete]
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances.

        Usage: all
                   prints the entire instances of the different classes
               all <class name>
                   prints instances of only <class name>
               <class name>.all()
                   also prints instances of only <class name>
        """
        output = "** class doesn't exist **"
        if arg:
            arg = arg.split()
            if len(arg) == 1 and arg[0] in self.all_classes.keys():
                all_instances = storage.all()
                output = []
                for each in all_instances:
                    if each.startswith(arg[0]):
                        output.append(str(all_instances[each]))
        else:
            all_instances = storage.all()
            output = [str(each) for each in all_instances.values()]

        print(output)

    def do_update(self, arg):
        """Updates/adds instance attribute and saves the change to a JSON file

        Usage: update <class name> <id> <attribute name> "<attribute value>"
               <class name>.update(<id>, <attribute name>, <attribute value>)
               <class name>.update(<id>, <dictionary representation>).
        """
        if not arg:
            print("** class name missing **")
            return

        arg = arg.split(' ', 3)
        if arg[0] not in self.all_classes.keys():
            print("** class doesn't exist **")
            return
        else:
            class_name = arg[0]

        arg_len = len(arg)
        if arg_len < 2:
            print("** instance id missing **")
            return
        all_instances = storage.all()
        instance_to_update = arg[0] + '.' + arg[1]
        if instance_to_update not in all_instances.keys():
            print("** no instance found **")
            return

        if arg_len < 3:
            print("** attribute name missing **")
            return
        else:
            attr_name = arg[2]

        if arg_len < 4:
            print("** value missing **")
        else:
            # TODO: add more checks to parse value
            value = arg[3].strip()
            value_len = len(value)
            if value_len > 1 and value.startswith('"'):
                end = value[1:].find('"')
                if end == -1:
                    value = value.split()[0]
                else:
                    value = value[1:end + 1]
            elif len(value.split()) > 1:
                value = value.split()[0]

            if attr_name not in ["id", "created_at", "updated_at"]:
                class_attrs = self.their_attr_types[class_name]
                right_type = str
                if attr_name in class_attrs.keys():
                    right_type = class_attrs[attr_name]
                else:  # the attribute is not in the class attrs
                    if value.isdigit():
                        right_type = int
                    elif value.replace('.', '', 1).isdigit():
                        right_type = float
                try:
                    value = right_type(value)
                except ValueError:
                    pass

                obj = all_instances[instance_to_update]
                obj.__dict__[attr_name] = value
                obj.save()

    def update_alt_dict(self, cls, id, dict):
        """uses the update command as a dotted method.
        It updates using a dictionary.
        """
        try:
            dict = eval(dict)
            for key, value in dict.items():
                line = " ".join([cls, id, str(key), '"' + str(value) + '"'])
                self.do_update(line)
        except Exception:
            print("Error in dictionary")
            pass

    def do_count(self, line):
        """Counts the number of instances of a class

        Usage: <class name>.count()
        """
        cmd.Cmd.default(self, "count " + line)

    def count(self, line):
        """Counts the number of instances of a class

        Usage: <class name>.count()
        """
        if not line:
            print("** class name missing **")
            return
        if line in self.all_classes.keys():
            all_instances = storage.all()
            count = 0
            for key in all_instances:
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """handles some special commands"""
        if line.endswith(".all()"):
            line = line[:-6]
            self.do_all(line)
        elif line.endswith(".count()"):
            line = line[:-8]
            self.count(line)
        else:  # other commands are unknown
            cmd.Cmd.default(self, line)

    def precmd(self, line):
        """checks the command before they are sent for further checks"""
        temp = line.strip()

        if line == "EOF" or temp == "":
            pass
        # avoids the call to count command as count <class name>
        elif temp.split()[0] == "count":
            self.default(temp)
            line = ""
        elif ".show(" in temp and temp[-1] == ')':
            cmd = ("show", temp.find(".show("))
            arg = temp[cmd[1] + len(".show("):-1]
            if arg and arg[0] == '"' and arg[-1] == '"':
                arg = arg[1:-1]
            line = " ".join([cmd[0], temp[:cmd[1]], arg])
        elif ".destroy(" in temp and temp[-1] == ')':
            cmd = ("destroy", temp.find(".destroy("))
            arg = temp[cmd[1] + len(".destroy("):-1]
            if arg and arg[0] == '"' and arg[-1] == '"':
                arg = arg[1:-1]
            line = " ".join([cmd[0], temp[:cmd[1]], arg])
        elif ".update(" in temp and temp[-1] == ')':
            cls = temp[:temp.find(".update(")]
            cmd = ("update", temp.find(".update("))
            args = temp[cmd[1] + len(".update("):-1]
            tmp = args.split(',', 1)
            if len(tmp) == 2:
                id = tmp[0].strip()
                tmp = tmp[1].strip()
                if tmp[0] == '{' and tmp[-1] == '}':
                    if id[0] == '"' and id[-1] == '"':
                        id = id[1:-1]
                    self.update_alt_dict(cls, id, tmp)
                    return ""

            args = args.split(',', 2)
            args_len = len(args)
            id = ""
            name = ""
            value = ""

            for i in range(args_len):
                if 0 <= i < 2 and len(args[i]) > 1:
                    args[i] = args[i].strip()
                    if args[i][0] == '"' and args[i][-1] == '"':
                        args[i] = args[i][1:-1]
                    if i == 0:
                        id = args[i]
                    else:
                        name = args[i]
                else:
                    value = args[i].strip()
                    break
            line = " ".join([cmd[0], cls, id, name, value])

        return line


if __name__ == '__main__':
    HBNBCommand().cmdloop()
