from st2common.runners.base_action import Action
import paramiko

class VOSSCmd(Action):

    def run(self, ipaddress='192.168.1.1', cmd=''):
        """
        Run a VOSS command on the remote switch

        Args:
            - ipaddress: The IP address of the switch
            - username: login user name
            - password: login password
            - cmd: either a single EXOS command or list of VOSS commands

        Raises:
           - ValueError: On switch reponse being invalid
           - RuntimeError: if switch cannot process the command


        Returns:
            dict: with VOSS CLI results
        """

        username='rwa'
        password='rwa'

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ipaddress,username=username,password=password)

        print 'Successful connection', ipaddress

        remote_connection = ssh_client.invoke_shell()

        print 'Collecting troubeshooting log file of ' + ipaddress

        remote_connection.send(cmd)
        remote_connection.send('\n')

        readoutput = remote_connection.recv(655350)

        saveoutput = open('Log file of ' + ipaddress, 'w')

        print 'Saving to file called Log file of ' + ipaddress + '\n'

        saveoutput.write(readoutput)
        saveoutput.write('\n')
        saveoutput.close

        ssh_client.close()

