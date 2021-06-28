from datetime import datetime
import os
import shutil


class ClientHandle:
    """This class for handling the client"""

    def __init__(self):
        """Initializing the client list and client id from client info [f] and client id no [f]"""

        self.__client_list = dict()

        if os.path.isdir(os.getcwd() + "/files"):
            if os.path.isdir("files/client") is False:
                os.mkdir("files/client")
            if os.path.isdir("files/jobs") is False:
                os.mkdir("files/jobs")
            if os.path.isdir("files/trash") is False:
                os.mkdir("files/trash")
        else:
            os.mkdir("files")
            os.mkdir("files/client")
            os.mkdir("files/jobs")
            os.mkdir("files/trash")

        if os.path.isfile(os.getcwd() + "/files/client/client_info.txt"):
            with open("files/client/client_info.txt") as f:
                info = f.readlines()
                for i in info:
                    item = i.split(" : ")
                    item[-1] = item[-1][:-1]
                    self.__client_list[item[0]] = item[1:]

            if os.path.isfile(os.getcwd() + "/files/client/client_id_no.txt"):
                with open("files/client/client_id_no.txt") as f:
                    self.__client_id = int(f.read())
            elif os.path.isfile(os.getcwd() + "/files/trash/deleted_client_ino.txt"):
                with open("files/trash/deleted_client_ino.txt") as f:
                    content = f.readlines()
                if len(content) != 0:
                    value_dci = int(content[-1][2:6])
                    value_cl = int(info[-1][2:6])
                    self.__client_id = value_dci if value_dci > value_cl else value_cl
                else:
                    self.__client_id = int(info[-1][2:6])
            else:
                self.__client_id = int(info[-1][2:6])
        else:
            self.__client_id = 0

    def __update_info(self):
        """This method for update the client list to the client info [f]"""

        with open("files/client/client_info.txt", "w") as f:
            for key, value in self.__client_list.items():
                f.write(f"{key} : {value[0]} : {value[1]} : {value[2]} : {value[3]} : {value[4]}\n")

    def __update_client_input(self, cid):
        """This method for taking input for the client update to the client list"""

        print("\nPress -> 1: Name\t2: Mobile No\t3: Address\t4: Height\t5: Weight")
        update = input("Select what do you want to update: ").lower()
        while (update not in "12345" or len(update) > 1) and update != 'B':
            print("\t\t\tInvalid entered..! Please try again..!\tOR Press 'B' -> BACK")
            update = input("Select what do you want to update: ").upper()
        if update == '1':
            self.__client_list[cid][0] = input("Enter the client name: ")
        elif update == '2':
            self.__client_list[cid][1] = input("Enter the mobile no: ")
        elif update == '3':
            self.__client_list[cid][2] = input("Enter the address: ")
        elif update == '4':
            self.__client_list[cid][3] = str(float(input("Enter the height (in inch): "))) + '"'
        elif update == '5':
            self.__client_list[cid][4] = str(float(input("Enter the weight (in KG): "))) + " KG"
        return update

    def select_client(self):
        """This method for select the client from the client list"""

        if self.__client_list:
            print("\nPress ->\t", end="")
            for key, value in self.__client_list.items():
                print(f"{key}: {value[0]}\t\t", end="")
            cid = input("\nEnter the client I'd for select: ").upper()
            while cid not in self.__client_list:
                print("\t\t\tWrong I'd entered..! Please try again..!\tOR Press 'B' -> BACK")
                cid = input("Enter the client I'd for select: ").upper()
                if cid == 'B':
                    return None
            print(f"\n\t\tSelected client: {self.__client_list[cid][0]}")
            return cid
        else:
            print("\n\t\tThe client list is empty..!\n\nAre you wants to add client and then select..?", end=" ")
            if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                self.add_client()
                self.select_client()
            else:
                return None

    def add_client(self):
        """This method for add a new client to the client list and client info [f] too"""

        self.__client_id += 1
        if self.__client_id < 10:
            cid = "CL000" + str(self.__client_id)
        elif self.__client_id < 100:
            cid = "CL00" + str(self.__client_id)
        elif self.__client_id < 1000:
            cid = "CL0" + str(self.__client_id)
        else:
            cid = "CL" + str(self.__client_id)

        name = input("\nEnter the client name: ")
        mobile = input("Enter the mobile no: ")
        address = input("Enter the address: ")
        height = float(input("Enter the height (in inch): "))
        weight = float(input("Enter the weight (in KG): "))
        self.__client_list[cid] = [name, mobile, address, str(height) + '"', str(weight) + " KG"]
        self.__update_info()
        with open("files/client/client_id_no.txt", "w") as f:
            f.write(str(self.__client_id))
        print(f"\n\t\tClient added..!  I'd is: {cid}")

    def delete_client(self, cid):
        """This method for remove the selected client from the client list and client info [f] too"""

        print(f"\nClient {cid}, named {self.__client_list[cid][0]} will be deleted..!")
        print("\t\tAre you sure wants to do that..?", end=" ")
        if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
            with open("files/trash/deleted_client_info.txt", "a") as f:
                value = self.__client_list[cid]
                f.write(f"{cid} : {value[0]} : {value[1]} : {value[2]} : {value[3]} : {value[4]}\n")

            exercise = os.getcwd() + f"/files/jobs/{cid}_Exercise.txt"
            diet = os.getcwd() + f"/files/jobs/{cid}_Diet.txt"
            therapy = os.getcwd() + f"/files/jobs/{cid}_Therapy.txt"
            trash_path = os.getcwd() + f"/files/trash"
            if os.path.isfile(exercise):
                shutil.move(exercise, trash_path)
            if os.path.isfile(diet):
                shutil.move(diet, trash_path)
            if os.path.isfile(therapy):
                shutil.move(therapy, trash_path)

            self.__client_list.pop(cid)
            self.__update_info()
            print(f"\n\t\tThe clients {cid} are deleted..!")

    def update_client_info(self, cid):
        """This method for update the selected clients info to the client list and client info [f] too"""

        update = self.__update_client_input(cid)
        if update != 'B':
            more = input("\t\tWant to update more..? Press -> Y: YES\t\t Others: NO\t\tEnter: ").upper()
            while more == 'Y' and update != 'B':
                update = self.__update_client_input(cid)
                if update == 'B':
                    break
                more = input("\t\tWant to update more..? Press -> Y: YES\t\t Others: NO\t\tEnter: ").upper()
            self.__update_info()
            print(f"\n\t\tClient info updated..!")
            self.show_client_details(cid)

    def show_client_details(self, cid):
        """This method for show all details of the selected client from the client list"""

        print(f"\nShowing client details:\nClient I'd: {cid}")
        cl = self.__client_list[cid]
        print(f"Name: {cl[0]}\nMobile No: {cl[1]}\nAddress: {cl[2]}\nHeight: {cl[3]}\nWeight: {cl[4]}")

    def show_all_clients(self):
        """This method for show all the clients of the client list"""

        if self.__client_list:
            print("\nShowing all clients:")
            print("______\t______________________\t__________\t______________________________________\t______\t_______")
            print("I'd\t\tName\t\t\t\t\tMobile No\tAddress\t\t\t\t\t\t\t\t\tHeight\tWeight")
            print("------\t----------------------\t----------\t--------------------------------------\t------\t-------")
            for key, value in self.__client_list.items():
                temp = 24 - len(value[0])
                client = value[0] + temp * " " + value[1] + "\t" + value[2]
                temp = 75 - len(client)
                client += temp * " " + value[3] + "\t" + value[4]
                print(f"{key}\t{client}")
        else:
            print("\n\t\tThe client list is empty..!\n\nAre you wants to add client..?", end=" ")
            if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                self.add_client()

    def recover_client(self, **clients):
        """This method for recover the deleted clients"""

        for key, value in clients.items():
            self.__client_list[key] = value
            exercise = os.getcwd() + f"/files/trash/{key}_Exercise.txt"
            diet = os.getcwd() + f"/files/trash/{key}_Diet.txt"
            therapy = os.getcwd() + f"/files/trash/{key}_Therapy.txt"
            job_path = os.getcwd() + f"/files/jobs"
            if os.path.isfile(exercise):
                shutil.move(exercise, job_path)
            if os.path.isfile(diet):
                shutil.move(diet, job_path)
            if os.path.isfile(therapy):
                shutil.move(therapy, job_path)
        self.__client_list = {key: value for key, value in sorted(self.__client_list.items())}
        self.__update_info()


class JobHandle:
    """This class for handling the job"""

    def __init__(self):
        """Initializing the job list"""

        self.__job_list = {'1': "Exercise", '2': "Diet", '3': "Therapy"}

    def select_job(self):
        """This method for select the job from the job list"""

        print("\nPress ->\t", end="")
        for key, value in self.__job_list.items():
            print(f"{key}: {value}\t\t", end="")
        job_id = input("\nChoose the job: ")
        while job_id not in self.__job_list:
            print("\t\t\tInvalid entered..! Please try again..!\tOR Press 'B' -> BACK")
            job_id = input("\nChoose the job: ")
            if job_id == 'B':
                return None
        print(f"\n\t\tSelected job: {self.__job_list[job_id]}")
        return job_id

    def log_job(self, cid, jid):
        """This method for log item to the selected job"""

        with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt", "a") as f:
            add = True
            print()
            while add:
                f.write(f"[{str(datetime.now()).split('.')[0]}] : {input(f'Enter the {self.__job_list[jid]}: ')}\n")
                print("\t\tWant to add more..?", end=" ")
                add = False if input("Press -> Y: YES\t\t Others: NO\t\tEnter: ").lower() == 'n' else True
        print(f"\n\t\t{self.__job_list[jid]} added..!")

    def retrieve_job(self, cid, jid):
        """This method for retrieve items from the selected job"""

        if os.path.isfile(os.getcwd() + f"/files/jobs/{cid}_{self.__job_list[jid]}.txt"):
            with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt") as f:
                content = f.read()
                if len(content) != 0:
                    print(f"\nShowing {self.__job_list[jid]} list of client {cid}")
                    print(content[:-1])
                else:
                    print(f"\n\t\tThe {self.__job_list[jid]} list of client {cid} is empty..!")
        else:
            print(f"\n\t\tThe {self.__job_list[jid]} list of client {cid} is empty..!")

    def update_job(self, cid, jid):
        """This method for update last entered items to the selected job"""

        if os.path.isfile(os.getcwd() + f"/files/jobs/{cid}_{self.__job_list[jid]}.txt"):
            with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt") as f:
                content = f.read()
            if len(content) != 0:
                flag = content.rindex('[')
                print(f"\nOnly last entry can be updated i.e, {content[flag:-1]}\n\t\tAre you sure wants to update..?",
                      end=" ")
                if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                    with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt", "w") as f:
                        flag = content.rindex(' : ')
                        f.write(f"{content[:flag]} : {input(f'Enter the {self.__job_list[jid]}: ')}\n")
                        print(f"\n\t\tLast {self.__job_list[jid].lower()} updated..!")
            else:
                print(f"\n\t\tNothing to update, the {self.__job_list[jid]} list of client {cid} is empty..!")
        else:
            print(f"\n\t\tNothing to update, the {self.__job_list[jid]} list of client {cid} is empty..!")

    def delete_job(self, cid, jid):
        """This method for delete last entered items to the selected job"""

        if os.path.isfile(os.getcwd() + f"/files/jobs/{cid}_{self.__job_list[jid]}.txt"):
            with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt") as f:
                content = f.read()
            if len(content) != 0:
                flag = content.rindex('[')
                print(f"\nOnly last entry can be deleted i.e, {content[flag:-1]}")
                print("\t\tAre you sure wants to permanently delete..?", end=" ")
                if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                    with open(f"files/jobs/{cid}_{self.__job_list[jid]}.txt", "w") as f:
                        f.write(f"{content[:flag]}")
                        print(f"\n\t\tLast {self.__job_list[jid].lower()} deleted..!")
            else:
                print(f"\n\t\tNothing to delete, the {self.__job_list[jid]} list of client {cid} is already empty..!")
        else:
            print(f"\n\t\tNothing to delete, the {self.__job_list[jid]} list of client {cid} is already empty..!")


class TrashHandle:
    """This class for handling the trash"""

    def __init__(self):
        """Initializing the deleted client list from deleted client info [f]"""

        self.__deleted_client_list = dict()
        self.update_to_list()

    def __update_info(self):
        """This method for update the deleted client list to the deleted client info [f]"""

        with open("files/trash/deleted_client_info.txt", "w") as f:
            for key, value in self.__deleted_client_list.items():
                f.write(f"{key} : {value[0]} : {value[1]} : {value[2]} : {value[3]} : {value[4]}\n")

    def update_to_list(self):
        """This method for update the deleted client list from the deleted client info [f] when update"""

        if os.path.isfile(os.getcwd() + "/files/trash/deleted_client_info.txt"):
            with open("files/trash/deleted_client_info.txt") as f:
                info = f.readlines()
                for i in info:
                    item = i.split(" : ")
                    item[-1] = item[-1][:-1]
                    self.__deleted_client_list[item[0]] = item[1:]

    def select_client_from_trash(self):
        """This method for select the deleted client from the deleted client list"""

        if self.__deleted_client_list:
            for key, value in self.__deleted_client_list.items():
                print(f"{key}: {value[0]}\t\t", end="")
            cid = input("\nEnter the client I'd for select: ").upper()
            while cid not in self.__deleted_client_list:
                print("\t\t\tWrong I'd entered..! Please try again..!\tOR Press 'B' -> BACK")
                cid = input("Enter the client I'd for select: ").upper()
                if cid == 'B':
                    return None
            print(f"\n\t\tSelected client: {self.__deleted_client_list[cid][0]} from trash")
            return cid
        else:
            print("\n\t\tNothing to select, The trash is empty..!")
            return None

    def recover_client_from_trash(self, cid):
        """This method for recover the selected deleted client"""

        recover_list = {cid: self.__deleted_client_list[cid]}
        self.__deleted_client_list.pop(cid)
        self.__update_info()
        print(f"\n\t\tDeleted client {cid} is recovered successfully..!")
        return recover_list

    def recover_all_deleted_clients(self):
        """This method for recover all the deleted client"""

        if self.__deleted_client_list:
            recover_list = self.__deleted_client_list
            self.__deleted_client_list = {}
            self.__update_info()
            print("\n\t\tAll deleted clients are recovered successfully..!")
            return recover_list
        else:
            print("\n\t\tNothing to recover, The trash is empty..!")
            return {}

    def delete_client_from_trash(self, cid):
        """This method for delete the selected client permanently from trash"""

        print(f"\nClient {cid}, named {self.__deleted_client_list[cid][0]} will be permanently deleted..!")
        print("\t\tAre you sure wants to do that..?", end=" ")
        if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
            self.__deleted_client_list.pop(cid)
            self.__update_info()
            if os.path.isfile(os.getcwd() + f"/files/trash/{cid}_Exercise.txt"):
                os.remove(os.getcwd() + f"/files/trash/{cid}_Exercise.txt")
            if os.path.isfile(os.getcwd() + f"/files/trash/{cid}_Diet.txt"):
                os.remove(os.getcwd() + f"/files/trash/{cid}_Diet.txt")
            if os.path.isfile(os.getcwd() + f"/files/trash/{cid}_Therapy.txt"):
                os.remove(os.getcwd() + f"/files/trash/{cid}_Therapy.txt")
            print(f"\n\t\tThe clients {cid} are deleted permanently..!")

    def empty_trash(self):
        """This method for delete all clients and information permanently from trash"""

        if self.__deleted_client_list:
            print("\nAll clients and information will be permanently deleted from trash..!")
            print("\t\tAre you sure wants to do that..?", end=" ")
            update = input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper()
            if update == 'Y':
                trash_path = os.getcwd() + "/files/trash/"
                for f in os.listdir(trash_path):
                    os.remove(os.path.join(trash_path, f))
                self.__deleted_client_list = {}
                print("\n\t\tAll clients are deleted permanently..! Trash is now empty..!")
        else:
            print("\n\t\tThe trash is already empty..!")

    def show_deleted_client_details(self, cid):
        """This method for show all details of the selected client from the client list"""

        print(f"\nShowing deleted client details:\nClient I'd: {cid}")
        cl = self.__deleted_client_list[cid]
        print(f"Name: {cl[0]}\nMobile No: {cl[1]}\nAddress: {cl[2]}\nHeight: {cl[3]}\nWeight: {cl[4]}")

    def view_all_deleted_clients(self):
        """This method for view all clients present in the trash"""

        if self.__deleted_client_list:
            print("\nShowing all deleted clients information from trash:")
            print("______\t______________________\t__________\t______________________________________\t______\t_______")
            print("I'd\t\tName\t\t\t\t\tMobile No\tAddress\t\t\t\t\t\t\t\t\tHeight\tWeight")
            print("------\t----------------------\t----------\t--------------------------------------\t------\t-------")
            for key, value in self.__deleted_client_list.items():
                temp = 24 - len(value[0])
                client = value[0] + temp * " " + value[1] + "\t" + value[2]
                temp = 75 - len(client)
                client += temp * " " + value[3] + "\t" + value[4]
                print(f"{key}\t{client}")
        else:
            print("\n\t\tThe trash is empty..!")


if __name__ == '__main__':
    ch = ClientHandle()
    job = JobHandle()
    trash = TrashHandle()
    print("\n\t\t\t\t\t\t\t\tWelcome To The Health Management System")
    while True:
        print("\n\nPress ->    1: Select Client    2: Add Client    3: Show Clients    4: Go To Trash", end="")
        op = input("    5: Exit    Enter: ")
        if op == '1':
            c_id = ch.select_client()
            while c_id is not None:
                print("\nPress ->    1: Select Job    2: Show Info    3: Update Info    4: Delete Client", end="")
                client_op = input("    5: Back    Enter: ")
                if client_op == '1':
                    j_id = job.select_job()
                    while j_id is not None:
                        print("\nPress ->    1: Log    2: Retrieve    3: Update    4: Delete", end="")
                        job_op = input("    5: Back    Enter: ")
                        if job_op == '1':
                            job.log_job(c_id, j_id)
                        elif job_op == '2':
                            job.retrieve_job(c_id, j_id)
                        elif job_op == '3':
                            job.update_job(c_id, j_id)
                        elif job_op == '4':
                            job.delete_job(c_id, j_id)
                        elif job_op == '5':
                            break
                        else:
                            print("\t\t\tInvalid entered..! Please try again..!")
                elif client_op == '2':
                    ch.show_client_details(c_id)
                elif client_op == '3':
                    ch.update_client_info(c_id)
                elif client_op == '4':
                    ch.delete_client(c_id)
                    trash.update_to_list()
                    break
                elif client_op == '5':
                    break
                else:
                    print("\t\t\tInvalid entered..! Please try again..!")
        elif op == '2':
            ch.add_client()
        elif op == '3':
            ch.show_all_clients()
        elif op == '4':
            print("\n\n\t\tNow you are in trash..! Working with deleted clients..!\n")
            while True:
                print("\nPress ->    1: Select Client    2: Show Clients    3: Recover All Clients", end="")
                trash_op = input("    4: Delete All Clients    5: Back    Enter: ")
                if trash_op == '1':
                    dc_id = trash.select_client_from_trash()
                    while dc_id is not None:
                        print("\nPress ->    1: View Details    2: Recover Client    3: Delete Client", end="")
                        dc_client_op = input("    4: Back    Enter: ")
                        if dc_client_op == '1':
                            trash.show_deleted_client_details(dc_id)
                        elif dc_client_op == '2':
                            rec_list = trash.recover_client_from_trash(dc_id)
                            ch.recover_client(**rec_list)
                            break
                        elif dc_client_op == '3':
                            trash.delete_client_from_trash(dc_id)
                        elif dc_client_op == '4':
                            break
                        else:
                            print("\t\t\tInvalid entered..! Please try again..!")
                elif trash_op == '2':
                    trash.view_all_deleted_clients()
                elif trash_op == '3':
                    rec_list = trash.recover_all_deleted_clients()
                    ch.recover_client(**rec_list)
                elif trash_op == '4':
                    trash.empty_trash()
                elif trash_op == '5':
                    break
                else:
                    print("\t\t\tInvalid entered..! Please try again..!")
        elif op == '5':
            print("\n\n\t\t\t\t\t\t\t\t\tHave a Good Day..!")
            break
        else:
            print("\t\t\tInvalid entered..! Please try again..!")
