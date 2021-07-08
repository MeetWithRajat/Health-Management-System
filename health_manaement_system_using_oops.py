from datetime import datetime
import sqlite3


class ClientHandle:
    """This class for handling the client"""

    def __init__(self):
        """Initializing the client list and client id from client info [f] and client id no [f]"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute("""CREATE TABLE IF NOT EXISTS client(Id text,
                                                        Name text,
                                                        Age text,
                                                        Height text,
                                                        Weight text,
                                                        Mobile text,
                                                        Address text)""")
        cr.execute("""CREATE TABLE IF NOT EXISTS client_id(Id integer)""")
        conn.commit()

        self.__client_list = dict()

        cr.execute("SELECT * FROM client")
        info = cr.fetchall()
        for item in info:
            self.__client_list[item[0]] = list(item[1:])
        self.__client_list = {key: value for key, value in sorted(self.__client_list.items())}

        cr.execute("SELECT * FROM client_id")
        f = cr.fetchone()
        if f is None:
            self.__client_id = 0
            cr.execute("INSERT INTO client_id VALUES('0')")
            conn.commit()
        else:
            self.__client_id = f[0]
        conn.close()

    def __update_client_input(self, cid):
        """This method for taking input for the client update to the client list"""

        print("\nPress -> 1: Name\t2. Age\t3: Height\t4: Weight\t5: Mobile No\t6: Address")
        update = input("Select what do you want to update: ").lower()
        while (update not in "123456" or len(update) > 1) and update != 'B':
            print("\t\t\tInvalid entered..! Please try again..!\tOR Press 'B' -> BACK")
            update = input("Select what do you want to update: ").upper()
        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        if update == '1':
            name = input("Enter the client name: ")
            cr.execute(f"UPDATE client SET Name = '{name}' WHERE Id = '{cid}'")
            self.__client_list[cid][0] = name
        elif update == '2':
            age = input("Enter the age: ")
            cr.execute(f"UPDATE client SET Age = '{age}' WHERE Id = '{cid}'")
            self.__client_list[cid][1] = age
        elif update == '3':
            height = str(float(input("Enter the height (in inch): "))) + '"'
            cr.execute(f"UPDATE client SET Height = '{height}' WHERE Id = '{cid}'")
            self.__client_list[cid][2] = height
        elif update == '4':
            weight = str(float(input("Enter the weight (in KG): "))) + " KG"
            cr.execute(f"UPDATE client SET Weight = '{weight}' WHERE Id = '{cid}'")
            self.__client_list[cid][3] = weight
        elif update == '5':
            mobile = input("Enter the mobile no: ")
            cr.execute(f"UPDATE client SET Mobile = '{mobile}' WHERE Id = '{cid}'")
            self.__client_list[cid][4] = mobile
        elif update == '6':
            address = input("Enter the address: ")
            cr.execute(f"UPDATE client SET Address = '{address}' WHERE Id = '{cid}'")
            self.__client_list[cid][5] = address
        conn.commit()
        conn.close()
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
        age = input("Enter the age: ")
        height = str(float(input("Enter the height (in inch): "))) + '"'
        weight = str(float(input("Enter the weight (in KG): "))) + " KG"
        mobile = input("Enter the mobile no: ")
        address = input("Enter the address: ")

        self.__client_list[cid] = [name, age, height, weight, mobile, address]

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute(f"""INSERT INTO client VALUES('{cid}',
                                                 '{name}',
                                                 '{age}',
                                                 '{height + '"'}',
                                                 '{weight + " KG"}',
                                                 '{mobile}',
                                                 '{address}')""")
        cr.execute(f"UPDATE client_id SET Id = '{self.__client_id}'")
        conn.commit()
        conn.close()
        print(f"\n\t\tClient added..!  I'd is: {cid}")

    def delete_client(self, cid):
        """This method for remove the selected client from the client list and client info [f] too"""

        print(f"\nClient {cid}, named {self.__client_list[cid][0]} will be deleted..!")
        print("\t\tAre you sure wants to do that..?", end=" ")
        if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
            conn = sqlite3.connect("health_management.db")
            cr = conn.cursor()
            value = self.__client_list[cid]
            print(value)
            cr.execute(f"""INSERT INTO deleted_client VALUES('{cid}',
                                                             '{value[0]}',
                                                             '{value[1]}',
                                                             '{value[2]}',
                                                             '{value[3]}',
                                                             '{value[4]}',
                                                             '{value[5]}')""")

            cr.execute(f"DELETE FROM client WHERE Id = '{cid}'")
            conn.commit()
            conn.close()
            self.__client_list.pop(cid)
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
            print(f"\n\t\tClient info updated..!")
            self.show_client_details(cid)

    def show_client_details(self, cid):
        """This method for show all details of the selected client from the client list"""

        print(f"\nShowing client details:\nClient I'd: {cid}")
        cl = self.__client_list[cid]
        print(f"Name: {cl[0]}\nAge: {cl[1]}\nHeight: {cl[2]}\nWeight: {cl[3]}\nMobile No: {cl[4]}\nAddress: {cl[5]}")

    def show_all_clients(self):
        """This method for show all the clients of the client list"""

        if self.__client_list:
            print("\nShowing all clients:")
            print("______  ______________________  ___  ______  _______  __________  _______________", end="")
            print("_________________________\nI'd\t\tName\t\t\t\t\tAge  Height  Weight   Mobile No   Address")
            print("______  ______________________  ___  ______  _______  __________  _______________", end="")
            print("_________________________")
            for key, val in self.__client_list.items():
                temp = 24 - len(val[0])
                client = val[0] + temp * " " + val[1] + "   " + val[2] + "   " + val[3] + "  " + val[4] + "  " + val[5]
                print(f"{key}\t{client}")
        else:
            print("\n\t\tThe client list is empty..!\n\nAre you wants to add client..?", end=" ")
            if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                self.add_client()

    def recover_client(self, **clients):
        """This method for recover the deleted clients"""

        for key, value in clients.items():
            self.__client_list[key] = value
        self.__client_list = {key: value for key, value in sorted(self.__client_list.items())}


class JobHandle:
    """This class for handling the job"""

    def __init__(self):
        """Initializing the job list"""

        self.__job_list = {'1': "Exercise", '2': "Diet", '3': "Therapy"}
        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute("""CREATE TABLE IF NOT EXISTS exercise(Id text, Time text, Exercise text)""")
        cr.execute("""CREATE TABLE IF NOT EXISTS diet(Id text, Time text, Diet text)""")
        cr.execute("""CREATE TABLE IF NOT EXISTS therapy(Id text, Time text, Therapy text)""")
        conn.commit()
        conn.close()

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

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        add = True
        print()
        while add:
            cr.execute(f"""INSERT INTO {self.__job_list[jid].lower()}
                           VALUES('{cid}',
                                  '{str(datetime.now()).split('.')[0]}',
                                  '{input(f'Enter the {self.__job_list[jid]}: ')}')""")
            print("\t\tWant to add more..?", end=" ")
            add = False if input("Press -> Y: YES\t\t Others: NO\t\tEnter: ").lower() == 'n' else True
        conn.commit()
        conn.close()
        print(f"\n\t\t{self.__job_list[jid]} added..!")

    def retrieve_job(self, cid, jid):
        """This method for retrieve items from the selected job"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute(f"SELECT * FROM {self.__job_list[jid].lower()} WHERE Id = '{cid}'")
        content = cr.fetchall()
        if len(content) != 0:
            print(f"\nShowing {self.__job_list[jid]} list of client {cid}")
            for i in content:
                print(f"[{i[1]}] : {i[2]}")
        else:
            print(f"\n\t\tThe {self.__job_list[jid]} list of client {cid} is empty..!")
        conn.close()

    def update_job(self, cid, jid):
        """This method for update last entered items to the selected job"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute(f"SELECT * FROM {self.__job_list[jid].lower()} WHERE Id = '{cid}'")
        content = cr.fetchall()
        if len(content) != 0:
            print(f"\nOnly last entry can be updated i.e, [{content[-1][1]}] : {content[-1][2]}")
            print("\t\tAre you sure wants to update..?", end=" ")
            if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                cr.execute(f"""UPDATE {self.__job_list[jid].lower()} 
                               SET {self.__job_list[jid]} = '{input(f'Enter the {self.__job_list[jid]}: ')}'
                               WHERE Id = '{cid}' and Time = '{content[-1][1]}'""")
                print(f"\n\t\tLast {self.__job_list[jid].lower()} updated..!")
        else:
            print(f"\n\t\tNothing to update, the {self.__job_list[jid]} list of client {cid} is empty..!")
        conn.commit()
        conn.close()

    def delete_job(self, cid, jid):
        """This method for delete last entered items to the selected job"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute(f"SELECT * FROM {self.__job_list[jid].lower()} WHERE Id = '{cid}'")
        content = cr.fetchall()
        if len(content) != 0:
            print(f"\nOnly last entry can be deleted i.e, [{content[-1][1]}] : {content[-1][2]}")
            print("\t\tAre you sure wants to permanently delete..?", end=" ")
            if input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper() == 'Y':
                cr.execute(f"""DELETE FROM {self.__job_list[jid].lower()}
                               WHERE Id = '{cid}' and Time = '{content[-1][1]}'""")
                print(f"\n\t\tLast {self.__job_list[jid].lower()} deleted..!")
        else:
            print(f"\n\t\tNothing to delete, the {self.__job_list[jid]} list of client {cid} is already empty..!")
        conn.commit()
        conn.close()


class TrashHandle:
    """This class for handling the trash"""

    def __init__(self):
        """Initializing the deleted client list from deleted client info [f]"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        cr.execute("""CREATE TABLE IF NOT EXISTS deleted_client(Id text,
                                                                Name text,
                                                                Age text,
                                                                Height text,
                                                                Weight text,
                                                                Mobile text,
                                                                Address text)""")
        conn.commit()
        self.__deleted_client_list = dict()
        cr.execute("SELECT * FROM deleted_client")
        info = cr.fetchall()
        for item in info:
            self.__deleted_client_list[item[0]] = list(item[1:])
        self.__deleted_client_list = {key: value for key, value in sorted(self.__deleted_client_list.items())}
        conn.close()

    def update_to_list(self):
        """This method for update the deleted client list from the deleted client info [f] when update"""

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        self.__deleted_client_list = dict()
        cr.execute("SELECT * FROM deleted_client")
        info = cr.fetchall()
        for item in info:
            self.__deleted_client_list[item[0]] = list(item[1:])
        self.__deleted_client_list = {key: value for key, value in sorted(self.__deleted_client_list.items())}
        conn.close()

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

        conn = sqlite3.connect("health_management.db")
        cr = conn.cursor()
        value = self.__deleted_client_list[cid]
        cr.execute(f"""INSERT INTO client VALUES('{cid}',
                                                 '{value[0]}',
                                                 '{value[1]}',
                                                 '{value[2]}',
                                                 '{value[3]}',
                                                 '{value[4]}',
                                                 '{value[5]}')""")

        cr.execute(f"DELETE FROM deleted_client WHERE Id = '{cid}'")
        conn.commit()
        conn.close()
        recover_list = {cid: self.__deleted_client_list[cid]}
        self.__deleted_client_list.pop(cid)
        print(f"\n\t\tDeleted client {cid} is recovered successfully..!")
        return recover_list

    def recover_all_deleted_clients(self):
        """This method for recover all the deleted client"""

        if self.__deleted_client_list:
            recover_list = self.__deleted_client_list
            conn = sqlite3.connect("health_management.db")
            cr = conn.cursor()
            for key, value in self.__deleted_client_list.items():
                value = self.__deleted_client_list[key]
                cr.execute(f"""INSERT INTO client VALUES('{key}',
                                                         '{value[0]}',
                                                         '{value[1]}',
                                                         '{value[2]}',
                                                         '{value[3]}',
                                                         '{value[4]}',
                                                         '{value[5]}')""")
                cr.execute(f"DELETE FROM deleted_client WHERE Id = '{key}'")
            conn.commit()
            conn.close()
            self.__deleted_client_list = {}

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
            conn = sqlite3.connect("health_management.db")
            cr = conn.cursor()
            cr.execute(f"DELETE FROM deleted_client WHERE Id = '{cid}'")
            cr.execute(f"DELETE FROM exercise WHERE Id = '{cid}'")
            cr.execute(f"DELETE FROM diet WHERE Id = '{cid}'")
            cr.execute(f"DELETE FROM therapy WHERE Id = '{cid}'")
            conn.commit()
            conn.close()
            print(f"\n\t\tThe clients {cid} are deleted permanently..!")

    def empty_trash(self):
        """This method for delete all clients and information permanently from trash"""

        if self.__deleted_client_list:
            print("\nAll clients and information will be permanently deleted from trash..!")
            print("\t\tAre you sure wants to do that..?", end=" ")
            update = input("Press -> Y: YES\t\t Others: NO AND BACK\t\tEnter: ").upper()
            if update == 'Y':
                conn = sqlite3.connect("health_management.db")
                cr = conn.cursor()
                for cid in self.__deleted_client_list:
                    cr.execute(f"DELETE FROM deleted_client WHERE Id = '{cid}'")
                    cr.execute(f"DELETE FROM exercise WHERE Id = '{cid}'")
                    cr.execute(f"DELETE FROM diet WHERE Id = '{cid}'")
                    cr.execute(f"DELETE FROM therapy WHERE Id = '{cid}'")
                conn.commit()
                conn.close()
                self.__deleted_client_list = {}
                print("\n\t\tAll clients are deleted permanently..! Trash is now empty..!")
        else:
            print("\n\t\tThe trash is already empty..!")

    def show_deleted_client_details(self, cid):
        """This method for show all details of the selected client from the client list"""

        print(f"\nShowing deleted client details:\nClient I'd: {cid}")
        cl = self.__deleted_client_list[cid]
        print(f"Name: {cl[0]}\nAge: {cl[1]}\nHeight: {cl[2]}\nWeight: {cl[3]}\nMobile No: {cl[4]}\nAddress: {cl[5]}")

    def view_all_deleted_clients(self):
        """This method for view all clients present in the trash"""

        if self.__deleted_client_list:
            print("\nShowing all deleted clients information from trash:")
            print("______  ______________________  ___  ______  _______  __________  _______________", end="")
            print("_________________________\nI'd\t\tName\t\t\t\t\tAge  Height  Weight   Mobile No   Address")
            print("______  ______________________  ___  ______  _______  __________  _______________", end="")
            print("_________________________")
            for key, val in self.__deleted_client_list.items():
                temp = 24 - len(val[0])
                client = val[0] + temp * " " + val[1] + "   " + val[2] + "   " + val[3] + "  " + val[4] + "  " + val[5]
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
                            break
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
