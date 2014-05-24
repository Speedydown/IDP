using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;


namespace VisionEngine.Network
{
    public class NetworkInterface
    {
        private TcpClient  clientSocket = new TcpClient();
        private NetworkStream serverStream;

        public NetworkInterface()
        {

        }

        public void Connect(string Address, int Port, ConnectionForm cform)
        {
            try
            {
                this.clientSocket.Connect(Address, Port);
                this.serverStream = clientSocket.GetStream();
                cform.Invoke(cform.formDelegate, new Object[] {"Connected"});
            }
            catch (ArgumentNullException)
            {
                cform.Invoke(cform.formDelegate, new Object[] {"Hostname not valid"});
            }
            catch (ArgumentOutOfRangeException)
            {
                cform.Invoke(cform.formDelegate, new Object[] {"The port parameter is not between MinPort and MaxPort."});
            }
            catch (SocketException e)
            {
                cform.Invoke(cform.formDelegate, new Object[] {"Socket returned: " + e.ErrorCode});
            }
            catch (ObjectDisposedException)
            {
                cform.Invoke(cform.formDelegate, new Object[] {"Server closed the connection"});
            }
        }

        public void Send(string Data)
        {
            byte[] outStream = System.Text.Encoding.ASCII.GetBytes(Data);
            this.serverStream.Write(outStream, 0, outStream.Length);
            this.serverStream.Flush();

        }

        public string Recv()
        {
            byte[] inStream = new byte[1024];
            
            string Data = string.Empty;
            
            while (!Data.Contains("<EOF>"))
            {
                serverStream.Read(inStream, 0, 1024);
                Data += Encoding.ASCII.GetString(inStream);
                inStream = new byte[1024];
            }

            Data = Data.Replace("\0", "");

            int EOFIndex = Data.IndexOf("<EOF>");
            return Data.Substring(0, EOFIndex);
        }

        public void Disconnect()
        {
            serverStream.Dispose();
        }

    }
}
